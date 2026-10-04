# 日本の博物館・美術館めぐり Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Life Questの既存JSON契約に適合する、全国の代表的な博物館・美術館を写真位置で記録できるプラグインを追加する。

**Architecture:** 個別マニフェスト `plugins/japan-museums-art.json` に地域別の28館、`photoLocation` 自動判定、実績、固定可視化、プラグイン所有の地図スタイルを定義する。座標・名称・選定根拠は `MUSEUM_ART_PLUGIN_DATA_SOURCES.md` に分離し、`catalog.json` は既存ビルドスクリプトで再生成する。

**Tech Stack:** JSON manifest、Python `unittest`、既存の `validate_catalog.py` / `build_catalog.py`、WikidataのCC0座標と各館公式案内。

## Global Constraints

- プラグインはSwift、JavaScript、外部API、任意クエリを実行しない。
- 位置自動判定は固定アダプタの `photoLocation` のみを使う。
- 判定円は施設境界を保証しないため、誤判定時はLife Questの手動修正を使える説明を資料に含める。
- マニフェストの座標に出典URLを埋め込まず、出典と確認日を資料に記録する。
- `mapStyle` は静的SVGと未訪問・推定・確認済みの色をすべて指定する。
- 既存プラグインのID・項目ID・グループID・実績IDと衝突させない。

---

### Task 1: Manifest contract test

**Files:**
- Modify: `scripts/test_validate_catalog.py`

**Interfaces:**
- Consumes: `plugins/japan-museums-art.json`
- Produces: A regression test that checks the plugin has 28 unique location-backed items, eight regional groups, photo-location automation, the expected achievement types, and all required visualizations.

- [x] **Step 1: Write the failing test**

Add `test_japan_museums_art_manifest_shape` to `ValidateCatalogTests`. Load the manifest, assert its ID, item/group counts, unique IDs, all items' `automation.type`, coordinate presence through `locations`, regional group IDs, `specificItems` and `groupComplete` achievements, and `validate_plugin` acceptance.

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_validate_catalog.ValidateCatalogTests.test_japan_museums_art_manifest_shape -v`
Expected: FAIL because `plugins/japan-museums-art.json` does not exist yet.

- [x] **Step 3: Keep implementation pending**

Do not add the manifest until the expected missing-file failure is observed.

### Task 2: Museum and art museum manifest

**Files:**
- Create: `plugins/japan-museums-art.json`

**Interfaces:**
- Consumes: Existing manifest contract and the item list documented in `MUSEUM_ART_PLUGIN_DATA_SOURCES.md`.
- Produces: A valid plugin with 28 items, eight regional groups, 14 achievements, 10 fixed visualization blocks, and a museum-shaped static marker.

- [x] **Step 1: Add the 28 items**

Use the exact IDs, Japanese titles, region group IDs, Wikidata-derived coordinates, and 300m radius described in the source document. Every item uses `automation: {"type": "photoLocation"}` and one `locations` entry titled `館の代表地点`.

- [x] **Step 2: Add achievements and visualizations**

Add item-count thresholds 1/5/10/20, one art-circuit `specificItems` achievement, each regional `groupComplete` achievement, and a completion-rate achievement. Configure progress summary, metric cards, status map, group progress, cumulative line chart, annual visited-item bar chart, status pie chart, achievement cards, next achievements, and grouped item list.

- [x] **Step 3: Add the static map style**

Use only `svg` and `path` tags with a museum-building silhouette; provide all three status color maps and `mapAttribution` only when a third-party geometry source is used. This plugin uses point coordinates only, so no OSM attribution is required.

### Task 3: Sources and catalog integration

**Files:**
- Create: `MUSEUM_ART_PLUGIN_DATA_SOURCES.md`
- Modify: `README.md`
- Modify: `catalog.json`

**Interfaces:**
- Consumes: The manifest's item IDs, coordinates, and selection rules.
- Produces: Reproducible source notes, README directory coverage, and a catalog generated from all plugin manifests.

- [x] **Step 1: Document sources**

Record the 2026-09-27 verification date, the 28-item scope, Wikidata item IDs and P625 coordinates, CC0 licensing, official museum pages used to confirm identity/category, 300m radius rationale, and the GPS false-positive/manual-correction limitation.

- [x] **Step 2: Register the source document**

Add `MUSEUM_ART_PLUGIN_DATA_SOURCES.md` to the README directory listing and plugin notes.

- [x] **Step 3: Rebuild the catalog**

Run `python3 scripts/build_catalog.py` so `catalog.json` includes the new manifest sorted by plugin ID.

### Task 4: Verification

**Files:**
- Test: `scripts/test_validate_catalog.py`
- Validate: `plugins/japan-museums-art.json`, `catalog.json`

- [x] **Step 1: Run focused test**

Run: `python3 -m unittest scripts.test_validate_catalog.ValidateCatalogTests.test_japan_museums_art_manifest_shape -v`
Expected: PASS.

- [x] **Step 2: Run full validation and tests**

Run: `python3 scripts/validate_catalog.py` and `python3 -m unittest discover -s scripts -p 'test_*.py' -v`.
Expected: all manifests validate and all tests pass.

- [x] **Step 3: Check generated diff**

Run: `git diff --check` and inspect `git diff --stat` plus the new catalog entry.
Expected: no whitespace errors and only the planned plugin, source notes, test, README, plan, and generated catalog changes.

- [x] **Step 4: Commit**

Run:
```bash
git add docs/superpowers/plans/2026-09-27-japan-museum-art-plugin.md plugins/japan-museums-art.json MUSEUM_ART_PLUGIN_DATA_SOURCES.md scripts/test_validate_catalog.py README.md catalog.json
git commit -m "feat: add Japan museum and art museum plugin"
```
