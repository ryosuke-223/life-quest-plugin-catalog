#!/usr/bin/env python3
"""Generate the curated airport achievement manifests from OurAirports CSV data."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins"
RADIUS_METERS = 1500

JAPAN_AIRPORTS = [
    ("CTS", "新千歳空港", "hokkaido"),
    ("WKJ", "稚内空港", "hokkaido"),
    ("KUH", "釧路空港", "hokkaido"),
    ("HKD", "函館空港", "hokkaido"),
    ("AKJ", "旭川空港", "hokkaido"),
    ("OBO", "帯広空港", "hokkaido"),
    ("SDJ", "仙台空港", "tohoku"),
    ("AXT", "秋田空港", "tohoku"),
    ("GAJ", "山形空港", "tohoku"),
    ("HND", "東京国際空港（羽田）", "kanto"),
    ("NRT", "成田国際空港", "kanto"),
    ("NGO", "中部国際空港（セントレア）", "chubu"),
    ("KIJ", "新潟空港", "chubu"),
    ("KIX", "関西国際空港", "kansai"),
    ("ITM", "大阪国際空港（伊丹）", "kansai"),
    ("HIJ", "広島空港", "chugoku"),
    ("UBJ", "山口宇部空港", "chugoku"),
    ("TAK", "高松空港", "shikoku"),
    ("MYJ", "松山空港", "shikoku"),
    ("KCZ", "高知龍馬空港", "shikoku"),
    ("FUK", "福岡空港", "kyushu"),
    ("KKJ", "北九州空港", "kyushu"),
    ("NGS", "長崎空港", "kyushu"),
    ("KMJ", "阿蘇くまもと空港", "kyushu"),
    ("OIT", "大分空港", "kyushu"),
    ("KMI", "宮崎空港", "kyushu"),
    ("KOJ", "鹿児島空港", "kyushu"),
    ("OKA", "那覇空港", "okinawa"),
]

WORLD_AIRPORTS = {
    "east-asia": "ICN PEK PKX PVG CAN SZX HKG TPE MFM UBN".split(),
    "southeast-asia": "MNL CEB SIN BKK KUL CGK DPS SGN HAN KTI RGN".split(),
    "south-asia": "DAC DEL BOM BLR MAA CMB KTM MLE".split(),
    "middle-east": "DXB AUH DOH JED RUH IST TLV AMM CAI BAH KWI MCT".split(),
    "europe": "LHR CDG AMS FRA MUC MAD BCN FCO MXP ZRH VIE BRU CPH ARN OSL HEL DUB LIS ATH WAW PRG BUD MAN".split(),
    "north-america": "ATL LAX ORD DFW DEN JFK EWR SFO SEA MIA YYZ YVR IAH LAS MEX".split(),
    "latin-america": "GRU EZE SCL LIM BOG PTY UIO".split(),
    "oceania": "SYD MEL BNE PER AKL CHC".split(),
    "africa": "JNB CPT CMN ADD NBO LOS ACC MRU".split(),
}

JAPAN_GROUP_TITLES = {
    "hokkaido": "北海道",
    "tohoku": "東北",
    "kanto": "関東",
    "chubu": "中部",
    "kansai": "関西",
    "chugoku": "中国",
    "shikoku": "四国",
    "kyushu": "九州",
    "okinawa": "沖縄",
}

WORLD_GROUP_TITLES = {
    "east-asia": "東アジア",
    "southeast-asia": "東南アジア",
    "south-asia": "南アジア",
    "middle-east": "中東",
    "europe": "ヨーロッパ",
    "north-america": "北米",
    "latin-america": "中南米",
    "oceania": "オセアニア",
    "africa": "アフリカ",
}


def load_airports(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return {
            row["iata_code"]: row
            for row in rows
            if row.get("iata_code") and row.get("latitude_deg") and row.get("longitude_deg")
        }


def location_item(code: str, title: str, group_id: str, row: dict[str, str]) -> dict:
    return {
        "id": f"airport-{code.lower()}",
        "title": f"{title}（{code}）",
        "groupID": group_id,
        "latitude": round(float(row["latitude_deg"]), 6),
        "longitude": round(float(row["longitude_deg"]), 6),
        "radiusMeters": RADIUS_METERS,
        "automation": {"type": "photoLocation"},
    }


def world_item(code: str, group_id: str, row: dict[str, str]) -> dict:
    airport_name = row["name"]
    municipality = row.get("municipality") or row.get("iso_country") or ""
    return {
        "id": f"airport-{code.lower()}",
        "title": f"{airport_name}（{code}）",
        "detail": municipality,
        "groupID": group_id,
        "latitude": round(float(row["latitude_deg"]), 6),
        "longitude": round(float(row["longitude_deg"]), 6),
        "radiusMeters": RADIUS_METERS,
        "automation": {"type": "photoLocation"},
    }


def achievement(item_id: str, title: str, detail: str, condition: dict) -> dict:
    return {"id": item_id, "title": title, "detail": detail, "condition": condition}


def make_plugin(
    plugin_id: str,
    title: str,
    summary: str,
    items: list[dict],
    groups: list[dict],
    achievements: list[dict],
    visualizations: list[dict],
    version: int = 1,
) -> dict:
    return {
        "schemaVersion": 1,
        "id": plugin_id,
        "version": version,
        "title": title,
        "summary": summary,
        "iconSystemName": "airplane.departure",
        "items": items,
        "groups": groups,
        "achievements": achievements,
        "visualizations": visualizations,
    }


def build_japan(airports: dict[str, dict[str, str]]) -> dict:
    items = [location_item(code, title, group_id, airports[code]) for code, title, group_id in JAPAN_AIRPORTS]
    groups = [{"id": key, "title": title} for key, title in JAPAN_GROUP_TITLES.items()]
    achievements = [
        achievement("domestic-first", "最初の空港", "1空港を訪れる", {"type": "itemCount", "minimum": 1}),
        achievement("domestic-five", "空港めぐり5空港", "5空港を訪れる", {"type": "itemCount", "minimum": 5}),
        achievement("domestic-ten", "空港めぐり10空港", "10空港を訪れる", {"type": "itemCount", "minimum": 10}),
        achievement("domestic-twenty", "全国空港ハンター", "20空港を訪れる", {"type": "itemCount", "minimum": 20}),
        achievement("domestic-complete", "拠点空港コンプリート", "28空港をすべて訪れる", {"type": "completionRate", "minimum": 1}),
    ]
    achievements.extend(
        achievement(f"region-{group_id}", f"{title}空港制覇", f"{title}の対象空港をすべて訪れる", {"type": "groupComplete", "groupID": group_id})
        for group_id, title in JAPAN_GROUP_TITLES.items()
    )
    visualizations = [
        {"type": "progressSummary"},
        {
            "type": "metricCards",
            "metrics": ["visitedCount", "completionRate", "remainingCount", "unlockedAchievements"],
        },
        {"type": "lineChart", "metric": "visitedCount", "aggregation": "cumulativeCount"},
        {"type": "barChart", "metric": "visitedCount", "aggregation": "annualVisitedItemCount"},
        {"type": "groupProgress"},
        {"type": "itemList", "sort": "group"},
    ]
    plugin = make_plugin("japan-airports", "日本の拠点空港めぐり", "国土交通省の拠点空港28空港。写真位置から訪問を自動判定します。", items, groups, achievements, visualizations, version=3)
    plugin["showsPeriodSelector"] = False
    return plugin


def build_world(airports: dict[str, dict[str, str]]) -> dict:
    items = [world_item(code, group_id, airports[code]) for group_id, codes in WORLD_AIRPORTS.items() for code in codes]
    groups = [{"id": key, "title": title} for key, title in WORLD_GROUP_TITLES.items()]
    count = len(items)
    achievements = [
        achievement("world-first", "最初の海外空港", "海外の空港を1つ訪れる", {"type": "itemCount", "minimum": 1}),
        achievement("world-five", "海外空港5選", "海外の空港を5つ訪れる", {"type": "itemCount", "minimum": 5}),
        achievement("world-ten", "空港トラベラー", "海外の空港を10個訪れる", {"type": "itemCount", "minimum": 10}),
        achievement("world-quarter", "世界空港25%", "対象空港の25%を訪れる", {"type": "completionRate", "minimum": 0.25}),
        achievement("world-half", "世界空港ハーフ", "対象空港の半分を訪れる", {"type": "completionRate", "minimum": 0.5}),
        achievement("world-complete", "世界主要空港コンプリート", f"対象空港{count}空港をすべて訪れる", {"type": "completionRate", "minimum": 1}),
    ]
    achievements.extend(
        achievement(f"region-{group_id}", f"{title}空港制覇", f"{title}の対象空港をすべて訪れる", {"type": "groupComplete", "groupID": group_id})
        for group_id, title in WORLD_GROUP_TITLES.items()
    )
    visualizations = [
        {"type": "progressSummary"},
        {
            "type": "metricCards",
            "metrics": ["visitedCount", "completionRate", "remainingCount", "unlockedAchievements"],
        },
        {"type": "lineChart", "metric": "visitedCount", "aggregation": "cumulativeCount"},
        {"type": "pieChart", "breakdown": "status"},
        {"type": "groupProgress"},
        {"type": "itemList", "sort": "group"},
    ]
    return make_plugin("world-major-airports", "世界の主要空港めぐり", "世界の主要国際空港100空港。写真位置から訪問を自動判定します。", items, groups, achievements, visualizations, version=3)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate_airport_plugins.py /path/to/airports.csv")
    airports = load_airports(Path(sys.argv[1]))
    required = {code for code, _, _ in JAPAN_AIRPORTS} | {code for codes in WORLD_AIRPORTS.values() for code in codes}
    missing = sorted(required - airports.keys())
    if missing:
        raise ValueError(f"missing IATA codes in source: {', '.join(missing)}")
    for plugin in (build_japan(airports), build_world(airports)):
        output = PLUGIN_DIR / f"{plugin['id']}.json"
        output.write_text(json.dumps(plugin, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output} ({len(plugin['items'])} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
