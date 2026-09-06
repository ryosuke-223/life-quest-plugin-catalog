#!/usr/bin/env python3
"""Validate catalog manifests using the same contract as the iOS app."""

import json
import math
import re
import sys
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
VISUALIZATION_TYPES = {
    "progressSummary",
    "achievementCards",
    "groupProgress",
    "statusMap",
    "statusGrid",
    "nextAchievements",
    "itemList",
}


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


def validate_location(path: Path, item: dict) -> None:
    item_id = item["id"]
    has_latitude = "latitude" in item and item["latitude"] is not None
    has_longitude = "longitude" in item and item["longitude"] is not None
    if has_latitude != has_longitude:
        fail(path, f"incomplete location for {item_id}")

    radius = item.get("radiusMeters")
    if not has_latitude:
        if radius is not None:
            fail(path, f"radiusMeters without coordinates for {item_id}")
        return

    latitude = item["latitude"]
    longitude = item["longitude"]
    if not is_number(latitude) or not is_number(longitude) or not math.isfinite(float(latitude)) or not math.isfinite(float(longitude)):
        fail(path, f"invalid coordinates for {item_id}")
    if not -90 <= float(latitude) <= 90 or not -180 <= float(longitude) <= 180:
        fail(path, f"coordinates out of range for {item_id}")
    if radius is not None and (not is_number(radius) or not math.isfinite(float(radius)) or not 0 < float(radius) <= 100_000):
        fail(path, f"invalid radiusMeters for {item_id}")


def validate_automation(path: Path, item: dict) -> None:
    automation = item.get("automation")
    if automation is None:
        return
    if not isinstance(automation, dict):
        fail(path, f"invalid automation for {item['id']}")

    automation_type = automation.get("type")
    if automation_type == "photoLocation":
        if item.get("latitude") is None or item.get("longitude") is None:
            fail(path, f"photoLocation needs coordinates for {item['id']}")
    elif automation_type == "healthKitAnnualStepCount":
        minimum = automation.get("minimum")
        if not is_integer(minimum) or not 0 < minimum <= 1_000_000_000:
            fail(path, f"invalid HealthKit threshold for {item['id']}")
        if any(item.get(key) is not None for key in ("latitude", "longitude", "radiusMeters")):
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
    has_coordinates = any(item.get("latitude") is not None and item.get("longitude") is not None for item in items)
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
        validate_location(path, item)
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
