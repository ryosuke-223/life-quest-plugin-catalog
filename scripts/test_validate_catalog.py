import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_airport_plugins import JAPAN_AIRPORTS, WORLD_AIRPORTS, build_japan, build_world
from validate_catalog import validate_plugin


def manifest(aggregation="annualVisitedItemCount", shows_period_selector=False):
    return {
        "schemaVersion": 1,
        "id": "test-plugin",
        "version": 1,
        "title": "テスト",
        "summary": "テスト",
        "iconSystemName": "star",
        "items": [{"id": "a", "title": "項目A"}],
        "groups": [],
        "achievements": [],
        "showsPeriodSelector": shows_period_selector,
        "visualizations": [
            {"type": "barChart", "metric": "visitedCount", "aggregation": aggregation}
        ],
    }


def airport_rows():
    codes = {code for code, _, _ in JAPAN_AIRPORTS}
    codes.update(code for group_codes in WORLD_AIRPORTS.values() for code in group_codes)
    return {
        code: {
            "name": f"Airport {code}",
            "latitude_deg": "35.0",
            "longitude_deg": "139.0",
            "municipality": "City",
            "iso_country": "JP",
        }
        for code in codes
    }


class ValidateCatalogTests(unittest.TestCase):
    def test_accepts_annual_visited_item_count_and_hidden_period_selector(self):
        validate_plugin(Path("test.json"), manifest())

    def test_accepts_optional_map_attribution(self):
        plugin = manifest()
        plugin["mapAttribution"] = "© OpenStreetMap contributors · ODbL 1.0"

        validate_plugin(Path("test.json"), plugin)

    def test_accepts_optional_group_map_marker_symbol_name(self):
        plugin = manifest()
        plugin["groups"] = [{
            "id": "cultural",
            "title": "文化遺産",
            "mapMarkerSymbolName": "building.columns.fill",
        }]

        validate_plugin(Path("test.json"), plugin)

    def test_rejects_invalid_group_map_marker_symbol_name(self):
        for value in ("", "   ", 42, "x" * 201):
            with self.subTest(value=value):
                plugin = manifest()
                plugin["groups"] = [{
                    "id": "cultural",
                    "title": "文化遺産",
                    "mapMarkerSymbolName": value,
                }]
                with self.assertRaisesRegex(ValueError, "cultural.mapMarkerSymbolName"):
                    validate_plugin(Path("test.json"), plugin)

    def test_rejects_invalid_map_attribution(self):
        for value in ("", "   ", 42, ["OpenStreetMap"], "x" * 301):
            with self.subTest(value=value):
                plugin = manifest()
                plugin["mapAttribution"] = value
                with self.assertRaisesRegex(ValueError, "mapAttribution"):
                    validate_plugin(Path("test.json"), plugin)

    def test_rejects_non_boolean_period_selector(self):
        with self.assertRaisesRegex(ValueError, "showsPeriodSelector must be a boolean"):
            validate_plugin(Path("test.json"), manifest(shows_period_selector="false"))

    def test_rejects_unknown_chart_aggregation(self):
        invalid = copy.deepcopy(manifest(aggregation="unknown"))
        with self.assertRaisesRegex(ValueError, "barChart.aggregation is invalid"):
            validate_plugin(Path("test.json"), invalid)

    def test_accepts_photo_location_checkpoints_and_status_map(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "heritage",
            "title": "世界遺産",
            "automation": {"type": "photoLocation"},
            "locations": [{
                "id": "main-site",
                "title": "主な構成資産",
                "latitude": 35.0,
                "longitude": 139.0,
                "radiusMeters": 200,
            }],
        }]
        plugin["visualizations"] = [{"type": "statusMap", "cluster": True}]

        validate_plugin(Path("test.json"), plugin)

    def test_accepts_polygon_and_multipolygon_visit_areas(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "castle",
            "title": "城郭",
            "automation": {"type": "photoLocation"},
            "locations": [
                {
                    "id": "main-keep",
                    "title": "本丸",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[139.0, 35.0], [139.01, 35.0], [139.01, 35.01], [139.0, 35.01], [139.0, 35.0]]],
                    },
                },
                {
                    "id": "outer-grounds",
                    "title": "城郭一帯",
                    "latitude": 35.0,
                    "longitude": 139.0,
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [[[139.0, 35.0], [139.01, 35.0], [139.01, 35.01], [139.0, 35.01], [139.0, 35.0]]],
                            [[[139.1, 35.1], [139.11, 35.1], [139.11, 35.11], [139.1, 35.11], [139.1, 35.1]]],
                        ],
                    },
                },
            ],
        }]

        validate_plugin(Path("test.json"), plugin)

    def test_accepts_null_geometry_as_an_omitted_optional_field(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "castle",
            "title": "城郭",
            "locations": [{
                "id": "gate",
                "title": "門",
                "latitude": 35.0,
                "longitude": 139.0,
                "geometry": None,
            }],
        }]

        validate_plugin(Path("test.json"), plugin)

    def test_rejects_malformed_or_conflicting_polygon_visit_areas(self):
        valid_ring = [[139.0, 35.0], [139.01, 35.0], [139.01, 35.01], [139.0, 35.01], [139.0, 35.0]]
        cases = [
            ({"type": "Polygon", "coordinates": [[valid_ring[0], *valid_ring[1:-1]]]}, "closed ring"),
            ({"type": "Polygon", "coordinates": [[[139.0, 35.0], [139.01, 35.0], [139.0, 35.0]]]}, "at least four positions"),
            ({"type": "Polygon", "coordinates": [[[139.0, 35.0, 1], *valid_ring[1:-1], [139.0, 35.0, 1]]]}, "must be two-dimensional"),
            ({"type": "Polygon", "coordinates": [[[139.0, 35.0], [139.01, 35.0], [139.0, 35.0], [139.0, 35.0]]]}, "must enclose an area"),
            ({"type": "Polygon", "coordinates": [[[181.0, 35.0], [182.0, 35.0], [182.0, 36.0], [181.0, 36.0], [181.0, 35.0]]]}, "coordinate out of range"),
            ({"type": "MultiPolygon", "coordinates": []}, "at least one polygon"),
            ({"type": "Point", "coordinates": [139.0, 35.0]}, "unsupported geometry type"),
            ({"type": [], "coordinates": []}, "unsupported geometry type"),
        ]
        for geometry, message in cases:
            with self.subTest(message=message):
                plugin = manifest()
                plugin["items"] = [{
                    "id": "castle",
                    "title": "城郭",
                    "automation": {"type": "photoLocation"},
                    "locations": [{"id": "grounds", "title": "城内", "geometry": geometry}],
                }]
                with self.assertRaisesRegex(ValueError, message):
                    validate_plugin(Path("test.json"), plugin)

        plugin = manifest()
        plugin["items"] = [{
            "id": "castle",
            "title": "城郭",
            "locations": [{
                "id": "grounds",
                "title": "城内",
                "latitude": 35.0,
                "longitude": 139.0,
                "radiusMeters": 200,
                "geometry": {"type": "Polygon", "coordinates": [valid_ring]},
            }],
        }]
        with self.assertRaisesRegex(ValueError, "cannot combine polygon geometry and radiusMeters"):
            validate_plugin(Path("test.json"), plugin)

    def test_rejects_polygon_coordinate_counts_over_the_plugin_limit(self):
        corner_a = [139.0, 35.0]
        ring = []
        for _ in range(12_501):
            ring.extend([corner_a, [140.0, 35.0], [140.0, 36.0], [139.0, 36.0]])
        ring.append(corner_a)
        plugin = manifest()
        plugin["items"] = [{
            "id": "castle",
            "title": "城郭",
            "automation": {"type": "photoLocation"},
            "locations": [{"id": "grounds", "title": "城内", "geometry": {"type": "Polygon", "coordinates": [ring]}}],
        }]

        with self.assertRaisesRegex(ValueError, "polygon coordinate count exceeds 50000"):
            validate_plugin(Path("test.json"), plugin)

    def test_rejects_malformed_checkpoint_records(self):
        cases = [
            ([{"id": "site", "title": "構成資産", "latitude": 35.0, "sourceURL": "https://www.wikidata.org/wiki/Q123"}], "incomplete location for site"),
            ([{"id": "site", "title": "構成資産", "latitude": 35.0, "longitude": 139.0, "radiusMeters": 0, "sourceURL": "https://www.wikidata.org/wiki/Q123"}], "invalid radiusMeters for site"),
            ([{"id": "site", "title": "構成資産", "latitude": 35.0, "longitude": 139.0, "sourceURL": "https://www.wikidata.org/wiki/Q123"},
              {"id": "site", "title": "重複", "latitude": 35.1, "longitude": 139.1, "sourceURL": "https://www.wikidata.org/wiki/Q124"}], "duplicate location id site"),
            ([], "locations must not be empty for heritage"),
        ]
        for locations, message in cases:
            with self.subTest(message=message):
                plugin = manifest()
                plugin["items"] = [{"id": "heritage", "title": "遺産", "locations": locations}]
                with self.assertRaisesRegex(ValueError, message):
                    validate_plugin(Path("test.json"), plugin)

    def test_rejects_mixed_legacy_coordinates_and_checkpoints(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "heritage",
            "title": "遺産",
            "latitude": 35.0,
            "longitude": 139.0,
            "locations": [{"id": "site", "title": "構成資産", "latitude": 35.0, "longitude": 139.0, "sourceURL": "https://www.wikidata.org/wiki/Q123"}],
        }]
        with self.assertRaisesRegex(ValueError, "cannot mix top-level coordinates and locations for heritage"):
            validate_plugin(Path("test.json"), plugin)

        plugin["items"][0]["latitude"] = None
        plugin["items"][0]["longitude"] = None
        with self.assertRaisesRegex(ValueError, "cannot mix top-level coordinates and locations for heritage"):
            validate_plugin(Path("test.json"), plugin)

    def test_rejects_locations_on_healthkit_items(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "steps",
            "title": "年間歩数",
            "automation": {"type": "healthKitAnnualStepCount", "minimum": 1_000_000},
            "locations": [{
                "id": "site",
                "title": "地点",
                "latitude": 35.0,
                "longitude": 139.0,
                "sourceURL": "https://www.wikidata.org/wiki/Q123",
            }],
        }]
        with self.assertRaisesRegex(ValueError, "HealthKit item cannot have coordinates for steps"):
            validate_plugin(Path("test.json"), plugin)

    def test_accepts_null_legacy_coordinate_fields_on_healthkit_items(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "steps",
            "title": "年間歩数",
            "automation": {"type": "healthKitAnnualStepCount", "minimum": 1_000_000},
            "latitude": None,
            "longitude": None,
            "radiusMeters": None,
        }]
        validate_plugin(Path("test.json"), plugin)

    def test_rejects_photo_location_without_coordinates_or_checkpoints(self):
        plugin = manifest()
        plugin["items"] = [{"id": "heritage", "title": "遺産", "automation": {"type": "photoLocation"}}]
        with self.assertRaisesRegex(ValueError, "photoLocation needs coordinates for heritage"):
            validate_plugin(Path("test.json"), plugin)

    def test_rejects_invalid_source_url_when_provided(self):
        invalid_urls = ["not-a-url", "http://example.org/site", "https:///missing-host"]
        for source_url in invalid_urls:
            with self.subTest(source_url=source_url):
                plugin = manifest()
                location = {"id": "site", "title": "構成資産", "latitude": 35.0, "longitude": 139.0}
                location["sourceURL"] = source_url
                plugin["items"] = [{"id": "heritage", "title": "遺産", "locations": [location]}]
                with self.assertRaisesRegex(ValueError, "sourceURL"):
                    validate_plugin(Path("test.json"), plugin)

    def test_rejects_more_than_2000_location_checkpoints(self):
        plugin = manifest()
        plugin["items"] = [{
            "id": "heritage",
            "title": "遺産",
            "automation": {"type": "photoLocation"},
            "locations": [
                {
                    "id": f"site-{index}",
                    "title": "構成資産",
                    "latitude": 35.0,
                    "longitude": 139.0,
                    "sourceURL": f"https://www.wikidata.org/wiki/Q{index + 1}",
                }
                for index in range(2001)
            ],
        }]
        with self.assertRaisesRegex(ValueError, "locations count exceeds 2000"):
            validate_plugin(Path("test.json"), plugin)

    def test_airport_generators_declare_year_charts_and_compact_item_details(self):
        rows = airport_rows()
        japan = build_japan(rows)
        world = build_world(rows)

        self.assertIs(japan["showsPeriodSelector"], False)
        self.assertIn({"type": "lineChart", "metric": "visitedCount", "aggregation": "cumulativeCount"}, japan["visualizations"])
        self.assertIn({"type": "barChart", "metric": "visitedCount", "aggregation": "annualVisitedItemCount"}, japan["visualizations"])
        self.assertNotIn("pieChart", {visualization["type"] for visualization in japan["visualizations"]})
        self.assertTrue(all("detail" not in item for item in japan["items"]))
        self.assertTrue(all(item["detail"] == "City" for item in world["items"]))
        self.assertNotIn("showsPeriodSelector", world)
        validate_plugin(Path("japan.json"), japan)
        validate_plugin(Path("world.json"), world)


class WorldHeritageDataTests(unittest.TestCase):
    def test_world_heritage_manifest_declares_all_time_dashboard_and_marker_symbols(self):
        manifest_path = Path(__file__).resolve().parents[1] / "plugins" / "japan-world-heritage.json"
        plugin = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(plugin["version"], 5)
        self.assertIs(plugin["showsPeriodSelector"], False)
        self.assertEqual(
            {group["id"]: group["mapMarkerSymbolName"] for group in plugin["groups"]},
            {"cultural": "building.columns.fill", "natural": "mountain.2.fill"},
        )
        self.assertEqual(plugin["visualizations"], [
            {"type": "progressSummary"},
            {"type": "metricCards", "metrics": [
                "visitedCount", "completionRate", "remainingCount", "unlockedAchievements"]},
            {"type": "lineChart", "metric": "visitedCount", "aggregation": "cumulativeCount"},
            {"type": "barChart", "metric": "visitedCount", "aggregation": "annualVisitedItemCount"},
            {"type": "groupProgress"},
            {"type": "achievementCards"},
            {"type": "nextAchievements", "limit": 3},
            {"type": "statusMap", "cluster": True},
            {"type": "itemList", "sort": "title"},
        ])

    def test_remote_summit_radius_exceptions_and_okinoshima_display_rules(self):
        manifest_path = Path(__file__).resolve().parents[1] / "plugins" / "japan-world-heritage.json"
        plugin = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(plugin["items"]), 27)
        locations = [location for item in plugin["items"] for location in item["locations"]]
        self.assertEqual(len(locations), 251)
        self.assertTrue(all(location.get("sourceURL", "").startswith("https://") for location in locations))
        self.assertNotIn("沖ノ鳥島", json.dumps(plugin, ensure_ascii=False))
        radii = [location["radiusMeters"] for location in locations]
        self.assertEqual(radii.count(200), 242)
        self.assertEqual(radii.count(300), 9)

        wider_checkpoints = {
            "yakushima": {"asset-002", "asset-003", "asset-004"},
            "ogasawara-islands": {"asset-001", "asset-002"},
            "amami-okinawa": {"asset-001", "asset-002", "asset-003", "asset-004"},
        }
        for heritage_id, checkpoint_ids in wider_checkpoints.items():
            item = next(item for item in plugin["items"] if item["id"] == heritage_id)
            for location in item["locations"]:
                expected_radius = 300 if location["id"] in checkpoint_ids else 200
                self.assertEqual(location["radiusMeters"], expected_radius, (heritage_id, location["id"]))

        munakata = next(item for item in plugin["items"] if item["id"] == "okinotsushima-munakata")

        self.assertIn("沖ノ島本島", munakata["detail"])
        self.assertIn("判定対象外", munakata["detail"])
        self.assertIn("表示のみ", munakata["detail"])
        checkpoint_titles = {location["title"] for location in munakata["locations"]}
        self.assertEqual(len(munakata["locations"]), 4)
        self.assertEqual(checkpoint_titles, {
            "宗像大社中津宮",
            "宗像大社辺津宮",
            "新原・奴山古墳群",
            "宗像大社沖津宮遙拝所",
        })
        self.assertNotIn("沖ノ島本島", checkpoint_titles)


class CastlePluginDataTests(unittest.TestCase):
    @staticmethod
    def polygon_contains(longitude, latitude, geometry):
        def ring_contains(ring):
            inside = False
            for start, end in zip(ring, ring[1:]):
                x1, y1 = start
                x2, y2 = end
                if (y1 > latitude) != (y2 > latitude):
                    crossing = x1 + (x2 - x1) * (latitude - y1) / (y2 - y1)
                    if crossing >= longitude:
                        inside = not inside
            return inside

        polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        return any(ring_contains(polygon[0]) and not any(ring_contains(hole) for hole in polygon[1:])
                   for polygon in polygons)

    def test_uses_traced_polygons_with_documented_circle_fallbacks_and_no_source_urls(self):
        manifest_path = Path(__file__).resolve().parents[1] / "plugins" / "japan-castle-collection.json"
        plugin = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(plugin["items"]), 27)
        self.assertEqual(plugin["mapAttribution"], "© OpenStreetMap contributors · ODbL 1.0")

        polygons = []
        circle_fallbacks = []
        for item in plugin["items"]:
            location = item["locations"][0]
            self.assertNotIn("sourceURL", location)
            if "geometry" in location:
                polygons.append(item["id"])
                self.assertIn("latitude", location)
                self.assertIn("longitude", location)
                self.assertIn(location["geometry"]["type"], {"Polygon", "MultiPolygon"})
                self.assertTrue(self.polygon_contains(location["longitude"], location["latitude"], location["geometry"]),
                                item["id"])
            else:
                circle_fallbacks.append(item["id"])
                self.assertEqual(location["radiusMeters"], 250)

        self.assertEqual(len(polygons), 19)
        self.assertEqual(len(circle_fallbacks), 8)


if __name__ == "__main__":
    unittest.main()
