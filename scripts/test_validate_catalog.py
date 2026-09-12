import copy
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

    def test_rejects_non_boolean_period_selector(self):
        with self.assertRaisesRegex(ValueError, "showsPeriodSelector must be a boolean"):
            validate_plugin(Path("test.json"), manifest(shows_period_selector="false"))

    def test_rejects_unknown_chart_aggregation(self):
        invalid = copy.deepcopy(manifest(aggregation="unknown"))
        with self.assertRaisesRegex(ValueError, "barChart.aggregation is invalid"):
            validate_plugin(Path("test.json"), invalid)

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


if __name__ == "__main__":
    unittest.main()
