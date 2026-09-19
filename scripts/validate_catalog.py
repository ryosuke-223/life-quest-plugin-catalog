#!/usr/bin/env python3
"""Validate catalog manifests using the same contract as the iOS app."""

import json
import math
import re
import sys
from urllib.parse import urlsplit
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins"
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MAX_ITEMS = 500
MAX_GROUPS = 200
MAX_ACHIEVEMENTS = 100
MAX_ID_BYTES = 128
MAX_PLUGIN_TITLE_BYTES = 200
MAX_SUMMARY_BYTES = 500
MAX_ITEM_TITLE_BYTES = 300
MAX_ITEM_DETAIL_BYTES = 500
MAX_GROUP_TITLE_BYTES = 200
MAX_ACHIEVEMENT_TITLE_BYTES = 200
MAX_ACHIEVEMENT_DETAIL_BYTES = 500
MAX_VISUALIZATIONS = 12
MAX_LOCATIONS = 2_000
MAX_POLYGON_COORDINATES = 50_000
MAX_SOURCE_URL_BYTES = 2_048
MAX_MAP_ATTRIBUTION_BYTES = 300
MAX_MAP_MARKER_SVG_BYTES = 20_000
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
SVG_TAG = re.compile(r"</?(?:svg|g|path)(?:\s[^>]*)?/?>", re.IGNORECASE)
SVG_PATH = re.compile(r"<path\b[^>]*\bd\s*=\s*([\"'])(.*?)\1[^>]*>", re.IGNORECASE | re.DOTALL)
SVG_VIEWBOX = re.compile(r"\bviewBox\s*=\s*([\"'])\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s*\1", re.IGNORECASE)
SVG_PATH_COMMANDS = re.compile(r"^[MmLlHhVvCcQqZz0-9+\-.,eE\s]+$")
VISUALIZATION_TYPES = {
    "progressSummary",
    "achievementCards",
    "groupProgress",
    "statusMap",
    "statusGrid",
    "nextAchievements",
    "itemList",
    "metricCards",
    "lineChart",
    "barChart",
    "pieChart",
    "areaChart",
    "heatmap",
}
CHART_METRICS = {"visitedCount", "completionRate", "remainingCount", "unlockedAchievements", "totalAchievements"}
CHART_AGGREGATIONS = {"cumulativeCount", "annualCount", "annualVisitedItemCount", "completionRate"}
BREAKDOWNS = {"status", "group"}
HEATMAP_DIMENSIONS = {"yearByGroup", "yearByStatus"}


def fail(path: Path, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_string(path: Path, value: object, field: str, maximum_bytes: int, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        fail(path, f"{field} must be a string")
    if nonempty and not value.strip():
        fail(path, f"{field} must not be empty")
    if len(value.encode("utf-8")) > maximum_bytes:
        fail(path, f"{field} is too long")
    return value


def require_identifier(path: Path, value: object, field: str) -> str:
    if not isinstance(value, str) or value != value.strip() or len(value.encode("utf-8")) > MAX_ID_BYTES or not IDENTIFIER.fullmatch(value):
        fail(path, f"invalid {field}")
    return value


def validate_svg(path: Path, value: object, field: str) -> str:
    svg = require_string(path, value, field, MAX_MAP_MARKER_SVG_BYTES)
    normalized = svg.strip()
    if not normalized.lower().startswith("<svg") or not re.search(r"</svg>\s*$", normalized, re.IGNORECASE):
        fail(path, f"{field} must be a static SVG")
    lower = normalized.lower()
    forbidden = ("<script", "<!doctype", "<![cdata", "href=", "xlink:", "url(", "style=", "transform=", "clip-path=", "mask=", " on", "<image", "<use", "<foreignobject", "<filter", "<lineargradient", "<radialgradient")
    if any(value in lower for value in forbidden):
        fail(path, f"{field} contains unsupported SVG content")
    view_box = SVG_VIEWBOX.search(normalized)
    if view_box is None:
        fail(path, f"{field} needs a positive viewBox")
    try:
        width = float(view_box.group(4))
        height = float(view_box.group(5))
    except (TypeError, ValueError):
        fail(path, f"{field} needs a positive viewBox")
    if not math.isfinite(width) or not math.isfinite(height) or width <= 0 or height <= 0:
        fail(path, f"{field} needs a positive viewBox")
    if not SVG_TAG.search(normalized):
        fail(path, f"{field} must use only svg, g, and path tags")
    stripped = SVG_TAG.sub("", normalized)
    if stripped.strip():
        fail(path, f"{field} contains unsupported SVG tags or text")
    matches = list(SVG_PATH.finditer(normalized))
    if not matches:
        fail(path, f"{field} needs at least one path")
    for match in matches:
        path_data = match.group(2)
        if len(path_data.encode("utf-8")) > MAX_MAP_MARKER_SVG_BYTES // 2 or not SVG_PATH_COMMANDS.fullmatch(path_data) or not re.search(r"[MmLlHhVvCcQqZz]", path_data):
            fail(path, f"{field} contains unsupported path commands")
    return svg


def validate_status_colors(path: Path, value: object, field: str) -> None:
    if not isinstance(value, dict):
        fail(path, f"{field} must be an object")
    for status in ("unvisited", "estimated", "confirmed"):
        if status not in value or not isinstance(value[status], str) or not HEX_COLOR.fullmatch(value[status]):
            fail(path, f"{field}.{status} must be a hex color")


def validate_map_style(path: Path, plugin: dict) -> None:
    style = plugin.get("mapStyle")
    if style is None:
        return
    if not isinstance(style, dict):
        fail(path, "mapStyle must be an object")
    if "markerSVG" in style and style["markerSVG"] is not None:
        validate_svg(path, style["markerSVG"], "mapStyle.markerSVG")
    for field in ("markerColors", "areaFillColors", "areaStrokeColors"):
        if field in style and style[field] is not None:
            validate_status_colors(path, style[field], f"mapStyle.{field}")


def validate_coordinate(path: Path, item_id: str, location: dict, location_id: str, required: bool = True) -> None:
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    if ("latitude" in location and latitude is not None) != ("longitude" in location and longitude is not None):
        fail(path, f"incomplete location for {location_id}")
    if latitude is None or longitude is None:
        if required:
            fail(path, f"photoLocation needs coordinates for {item_id}")
        return
    if not is_number(latitude) or not is_number(longitude) or not math.isfinite(float(latitude)) or not math.isfinite(float(longitude)):
        fail(path, f"invalid coordinates for {location_id}")
    if not -90 <= float(latitude) <= 90 or not -180 <= float(longitude) <= 180:
        fail(path, f"coordinates out of range for {location_id}")

    radius = location.get("radiusMeters")
    if radius is not None and (not is_number(radius) or not math.isfinite(float(radius)) or not 0 < float(radius) <= 100_000):
        fail(path, f"invalid radiusMeters for {location_id}")


def validate_geometry(path: Path, location: dict, location_id: str) -> int:
    geometry = location.get("geometry")
    if not isinstance(geometry, dict):
        fail(path, f"geometry must be an object for {location_id}")

    geometry_type = geometry.get("type")
    if not isinstance(geometry_type, str) or geometry_type not in {"Polygon", "MultiPolygon"}:
        fail(path, f"unsupported geometry type for {location_id}")
    if location.get("radiusMeters") is not None:
        fail(path, f"cannot combine polygon geometry and radiusMeters for {location_id}")
    validate_coordinate(path, location_id, location, location_id, required=False)

    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or not coordinates:
        label = "at least one polygon" if geometry_type == "MultiPolygon" else "at least one ring"
        fail(path, f"{geometry_type} must contain {label} for {location_id}")
    polygons = coordinates if geometry_type == "MultiPolygon" else [coordinates]
    coordinate_count = 0
    for polygon in polygons:
        if not isinstance(polygon, list) or not polygon:
            fail(path, f"polygon must contain at least one ring for {location_id}")
        for ring in polygon:
            if not isinstance(ring, list) or len(ring) < 4:
                fail(path, f"polygon ring must contain at least four positions for {location_id}")
            coordinate_count += len(ring)
            if coordinate_count > MAX_POLYGON_COORDINATES:
                fail(path, f"polygon coordinate count exceeds {MAX_POLYGON_COORDINATES}")
            if ring[0] != ring[-1]:
                fail(path, f"polygon ring must be a closed ring for {location_id}")

            normalized_ring = []
            for position in ring:
                if (not isinstance(position, list) or len(position) != 2
                        or not all(is_number(value) and math.isfinite(float(value)) for value in position)):
                    fail(path, f"polygon positions must be two-dimensional for {location_id}")
                longitude, latitude = map(float, position)
                if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
                    fail(path, f"polygon coordinate out of range for {location_id}")
                normalized_ring.append((longitude, latitude))
            if abs(ring_area(normalized_ring)) <= 1e-12:
                fail(path, f"polygon ring must enclose an area for {location_id}")

    return coordinate_count


def ring_area(ring: list[tuple[float, float]]) -> float:
    origin = ring[0][0]
    unwrapped = [
        (origin + ((longitude - origin + 180) % 360) - 180, latitude)
        for longitude, latitude in ring
    ]
    return sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(unwrapped, unwrapped[1:])
    ) / 2


def validate_location(path: Path, item: dict) -> tuple[int, int]:
    item_id = item["id"]
    if "locations" in item:
        locations = item["locations"]
        if any(key in item for key in ("latitude", "longitude", "radiusMeters")):
            fail(path, f"cannot mix top-level coordinates and locations for {item_id}")
        if not isinstance(locations, list) or not locations:
            fail(path, f"locations must not be empty for {item_id}")

        location_ids = set()
        polygon_coordinate_count = 0
        for location in locations:
            if not isinstance(location, dict):
                fail(path, f"location must be an object for {item_id}")
            location_id = require_identifier(path, location.get("id"), f"{item_id}.location id")
            if location_id in location_ids:
                fail(path, f"duplicate location id {location_id} for {item_id}")
            location_ids.add(location_id)
            require_string(path, location.get("title"), f"{location_id}.title", MAX_ITEM_TITLE_BYTES)
            if "sourceURL" in location:
                source_url = require_string(path, location.get("sourceURL"), f"{location_id}.sourceURL", MAX_SOURCE_URL_BYTES)
                parsed_source_url = urlsplit(source_url)
                if parsed_source_url.scheme != "https" or not parsed_source_url.hostname or parsed_source_url.username or parsed_source_url.password:
                    fail(path, f"invalid HTTPS sourceURL for {location_id}")
            if location.get("geometry") is not None:
                polygon_coordinate_count += validate_geometry(path, location, location_id)
            else:
                validate_coordinate(path, item_id, location, location_id)
            if polygon_coordinate_count > MAX_POLYGON_COORDINATES:
                fail(path, f"polygon coordinate count exceeds {MAX_POLYGON_COORDINATES}")
        return len(locations), polygon_coordinate_count

    has_latitude = "latitude" in item and item["latitude"] is not None
    has_longitude = "longitude" in item and item["longitude"] is not None
    if has_latitude != has_longitude:
        fail(path, f"incomplete location for {item_id}")
    if not has_latitude:
        if item.get("radiusMeters") is not None:
            fail(path, f"radiusMeters without coordinates for {item_id}")
        return 0, 0

    validate_coordinate(path, item_id, item, item_id)
    return 1, 0


def validate_automation(path: Path, item: dict) -> None:
    automation = item.get("automation")
    if automation is None:
        return
    if not isinstance(automation, dict):
        fail(path, f"invalid automation for {item['id']}")

    automation_type = automation.get("type")
    if automation_type == "photoLocation":
        if not item.get("locations") and (item.get("latitude") is None or item.get("longitude") is None):
            fail(path, f"photoLocation needs coordinates for {item['id']}")
    elif automation_type == "healthKitAnnualStepCount":
        minimum = automation.get("minimum")
        if not is_integer(minimum) or not 0 < minimum <= 1_000_000_000:
            fail(path, f"invalid HealthKit threshold for {item['id']}")
        if "locations" in item or any(item.get(key) is not None for key in ("latitude", "longitude", "radiusMeters")):
            fail(path, f"HealthKit item cannot have coordinates for {item['id']}")
    else:
        fail(path, f"unknown automation type for {item['id']}")


def validate_visualizations(path: Path, plugin: dict, items: list[dict], groups: list[dict]) -> None:
    visualizations = plugin.get("visualizations")
    if visualizations is None:
        return
    if not isinstance(visualizations, list) or len(visualizations) > MAX_VISUALIZATIONS:
        fail(path, "visualizations count is outside limits")

    seen = set()
    has_coordinates = any(
        (item.get("latitude") is not None and item.get("longitude") is not None)
        or bool(item.get("locations"))
        for item in items
    )
    for visualization in visualizations:
        if not isinstance(visualization, dict):
            fail(path, "visualization must be an object")
        visualization_type = visualization.get("type")
        if visualization_type not in VISUALIZATION_TYPES:
            fail(path, f"unknown visualization type {visualization_type}")
        if visualization_type in seen:
            fail(path, f"duplicate visualization type {visualization_type}")
        seen.add(visualization_type)

        if visualization_type == "groupProgress" and not groups:
            fail(path, "groupProgress needs groups")
        if visualization_type == "statusMap" and not has_coordinates:
            fail(path, "statusMap needs coordinates")
        if visualization_type == "statusGrid":
            columns = visualization.get("columns", 3)
            if not is_integer(columns) or not 2 <= columns <= 6:
                fail(path, "statusGrid.columns must be between 2 and 6")
        if visualization_type == "nextAchievements":
            limit = visualization.get("limit", 3)
            if not is_integer(limit) or not 1 <= limit <= 10:
                fail(path, "nextAchievements.limit must be between 1 and 10")
        if visualization_type == "itemList" and visualization.get("sort", "status") not in {"status", "title", "group"}:
            fail(path, "itemList.sort is invalid")
        if visualization_type == "metricCards":
            metrics = visualization.get("metrics", ["visitedCount", "completionRate"])
            if (not isinstance(metrics, list) or not metrics or len(metrics) > 6
                    or len(set(metrics)) != len(metrics) or not all(metric in CHART_METRICS for metric in metrics)):
                fail(path, "metricCards.metrics is invalid")
        if visualization_type in {"lineChart", "barChart", "areaChart"}:
            if visualization.get("metric", "visitedCount") not in CHART_METRICS:
                fail(path, f"{visualization_type}.metric is invalid")
            if visualization.get("aggregation", "cumulativeCount") not in CHART_AGGREGATIONS:
                fail(path, f"{visualization_type}.aggregation is invalid")
        if visualization_type == "pieChart" and visualization.get("breakdown", "status") not in BREAKDOWNS:
            fail(path, "pieChart.breakdown is invalid")
        if visualization_type == "heatmap" and visualization.get("dimension", "yearByGroup") not in HEATMAP_DIMENSIONS:
            fail(path, "heatmap.dimension is invalid")


def validate_plugin(path: Path, plugin: object) -> None:
    if not isinstance(plugin, dict):
        fail(path, "plugin must be an object")

    required = ("schemaVersion", "id", "version", "title", "summary", "iconSystemName", "items", "groups", "achievements")
    for key in required:
        if key not in plugin:
            fail(path, f"missing {key}")

    if plugin["schemaVersion"] != 1 or not is_integer(plugin["version"]) or plugin["version"] <= 0:
        fail(path, "invalid schemaVersion or version")
    plugin_id = require_identifier(path, plugin["id"], "plugin id")
    require_string(path, plugin["title"], "title", MAX_PLUGIN_TITLE_BYTES)
    require_string(path, plugin["summary"], "summary", MAX_SUMMARY_BYTES)
    require_string(path, plugin["iconSystemName"], "iconSystemName", 100)
    if "mapAttribution" in plugin:
        require_string(path, plugin["mapAttribution"], "mapAttribution", MAX_MAP_ATTRIBUTION_BYTES)
    if "showsPeriodSelector" in plugin and not isinstance(plugin["showsPeriodSelector"], bool):
        fail(path, "showsPeriodSelector must be a boolean")
    validate_map_style(path, plugin)

    items = plugin["items"]
    groups = plugin["groups"]
    achievements = plugin["achievements"]
    if not isinstance(items, list) or not items or len(items) > MAX_ITEMS:
        fail(path, "items count is outside limits")
    if not isinstance(groups, list) or len(groups) > MAX_GROUPS:
        fail(path, "groups count is outside limits")
    if not isinstance(achievements, list) or len(achievements) > MAX_ACHIEVEMENTS:
        fail(path, "achievements count is outside limits")

    all_ids = set()
    item_ids = set()
    total_locations = 0
    total_polygon_coordinates = 0
    for item in items:
        if not isinstance(item, dict):
            fail(path, "item must be an object")
        item_id = require_identifier(path, item.get("id"), "item id")
        if item_id in item_ids:
            fail(path, f"duplicate item id {item_id}")
        item_ids.add(item_id)
        all_ids.add(item_id)
        require_string(path, item.get("title"), f"{item_id}.title", MAX_ITEM_TITLE_BYTES)
        if item.get("detail") is not None:
            require_string(path, item["detail"], f"{item_id}.detail", MAX_ITEM_DETAIL_BYTES, nonempty=False)
        location_count, polygon_coordinate_count = validate_location(path, item)
        total_locations += location_count
        total_polygon_coordinates += polygon_coordinate_count
        if total_locations > MAX_LOCATIONS:
            fail(path, f"locations count exceeds {MAX_LOCATIONS}")
        if total_polygon_coordinates > MAX_POLYGON_COORDINATES:
            fail(path, f"polygon coordinate count exceeds {MAX_POLYGON_COORDINATES}")
        validate_automation(path, item)

    group_ids = set()
    for group in groups:
        if not isinstance(group, dict):
            fail(path, "group must be an object")
        group_id = require_identifier(path, group.get("id"), "group id")
        if group_id in group_ids:
            fail(path, f"duplicate group id {group_id}")
        if group_id in all_ids:
            fail(path, f"duplicate ID across plugin sections {group_id}")
        group_ids.add(group_id)
        all_ids.add(group_id)
        require_string(path, group.get("title"), f"{group_id}.title", MAX_GROUP_TITLE_BYTES)
        if "mapMarkerSymbolName" in group:
            require_string(path,
                           group["mapMarkerSymbolName"],
                           f"{group_id}.mapMarkerSymbolName",
                           MAX_GROUP_TITLE_BYTES)
        if "mapMarkerSVG" in group and group["mapMarkerSVG"] is not None:
            validate_svg(path, group["mapMarkerSVG"], f"{group_id}.mapMarkerSVG")

    for item in items:
        group_id = item.get("groupID")
        if group_id is not None and (not isinstance(group_id, str) or group_id not in group_ids):
            fail(path, f"missing group {group_id} for {item['id']}")

    achievement_ids = set()
    for achievement in achievements:
        if not isinstance(achievement, dict):
            fail(path, "achievement must be an object")
        achievement_id = require_identifier(path, achievement.get("id"), "achievement id")
        if achievement_id in achievement_ids:
            fail(path, f"duplicate achievement id {achievement_id}")
        if achievement_id in all_ids:
            fail(path, f"duplicate ID across plugin sections {achievement_id}")
        achievement_ids.add(achievement_id)
        all_ids.add(achievement_id)
        require_string(path, achievement.get("title"), f"{achievement_id}.title", MAX_ACHIEVEMENT_TITLE_BYTES)
        require_string(path, achievement.get("detail"), f"{achievement_id}.detail", MAX_ACHIEVEMENT_DETAIL_BYTES, nonempty=False)

        condition = achievement.get("condition")
        if not isinstance(condition, dict):
            fail(path, f"missing condition for {achievement_id}")
        condition_type = condition.get("type")
        if condition_type == "itemCount":
            minimum = condition.get("minimum")
            if not is_integer(minimum) or not 0 < minimum <= len(item_ids):
                fail(path, f"invalid itemCount for {achievement_id}")
        elif condition_type == "groupComplete":
            group_id = condition.get("groupID")
            if not isinstance(group_id, str) or group_id not in group_ids or not any(item.get("groupID") == group_id for item in items):
                fail(path, f"invalid groupComplete for {achievement_id}")
        elif condition_type == "specificItems":
            item_ids_for_condition = condition.get("itemIDs")
            if (not isinstance(item_ids_for_condition, list)
                    or not item_ids_for_condition
                    or not all(isinstance(item_id, str) for item_id in item_ids_for_condition)
                    or len(set(item_ids_for_condition)) != len(item_ids_for_condition)
                    or not all(item_id in item_ids for item_id in item_ids_for_condition)):
                fail(path, f"invalid specificItems for {achievement_id}")
        elif condition_type == "completionRate":
            minimum = condition.get("minimum")
            if not is_number(minimum) or not 0 < float(minimum) <= 1:
                fail(path, f"invalid completionRate for {achievement_id}")
        else:
            fail(path, f"unknown condition for {achievement_id}")

    validate_visualizations(path, plugin, items, groups)

    # Keep this local variable intentional: it makes duplicate plugin IDs easy to
    # diagnose if this function is later reused by a multi-file validator.
    if not plugin_id:
        fail(path, "empty plugin id")


def main() -> int:
    paths = sorted(PLUGIN_DIR.glob("*.json"))
    if not paths:
        raise ValueError("no plugin manifests found")
    ids = set()
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            plugin = json.load(handle)
        validate_plugin(path, plugin)
        plugin_id = plugin["id"]
        if plugin_id in ids:
            fail(path, f"duplicate plugin id {plugin_id}")
        ids.add(plugin_id)
    print(f"validated {len(paths)} plugin manifests")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
