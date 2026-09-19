# World Heritage Precision Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve photo GPS matching at remote mountain checkpoints while preserving small default areas and adding property polygons only when the boundary data can be redistributed under confirmed terms.

**Architecture:** Keep the existing iOS polygon and multipolygon resolver and catalog validator unchanged. Set an explicit 300m circle on the nine remote natural-heritage summit checkpoints selected for additional GPS tolerance; retain 200m for all other checkpoints. Update the heritage source notes to record why the exception is narrow and why current official boundary datasets are not bundled.

**Tech Stack:** JSON plugin manifest, generated JSON catalog, Python `unittest`, catalog validation and generation scripts.

## Global Constraints

- A heritage parent item is achieved once when a photo GPS coordinate matches any one of its eligible checkpoints.
- The default checkpoint radius remains 200m.
- Only these nine named summit checkpoints use 300m: Yakushima `asset-002`–`asset-004`, Ogasawara `asset-001`–`asset-002`, and Amami/Okinawa `asset-001`–`asset-004`.
- Do not enlarge island checkpoints to represent an entire island or registered property.
- Do not enlarge sea-adjacent circles in a way that could trigger while passing by boat without visiting a public component.
- Do not add boundary polygons from datasets unless the geometry's source and redistribution rights are confirmed for catalog bundling.
- Okinoshima remains display-only and is not a GPS checkpoint; the four public Munakata checkpoints remain eligible.
- Preserve existing unrelated user changes in the dirty catalog checkout.

---

### Task 1: Encode and verify the narrow radius exception and boundary-data policy

**Files:**
- Modify: `scripts/test_validate_catalog.py`
- Modify: `plugins/japan-world-heritage.json`
- Modify: `catalog.json` (regenerate only with `scripts/build_catalog.py`)
- Modify: `WORLD_HERITAGE_COORDINATE_RESEARCH.md`
- Modify: `WORLD_HERITAGE_DATA_SOURCES.md`

**Interfaces:**
- Consumes: `items[].locations[]`, each location's `id` and `radiusMeters`. Source details are kept in the accompanying research notes and PR, not in the manifest.
- Produces: Explicit 300m radii for the nine selected summits, a 200m default for all remaining World Heritage checkpoints, and documented polygon-data constraints.

- [ ] **Step 1: Change the regression test first**

Update `WorldHeritageDataTests.test_island_radius_and_okinoshima_display_rules_are_preserved` so it asserts:

```python
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
```

Keep the existing Okinoshima assertions in the same test.

- [ ] **Step 2: Run the focused test and confirm the expected failure**

Run: `python3 -m unittest scripts.test_validate_catalog.WorldHeritageDataTests -v`

Expected: FAIL on the first selected checkpoint because its manifest radius is still 200m.

- [ ] **Step 3: Update the plugin manifest**

In `plugins/japan-world-heritage.json`, increment `version` from `3` to `4`, change the summary to say a photo inside any checkpoint's configured range achieves one heritage item, and change only the nine checkpoint radii listed above from `200` to `300`.

- [ ] **Step 4: Update research and source notes**

In `WORLD_HERITAGE_COORDINATE_RESEARCH.md`, state that 200m remains the default and list the nine 300m summit exceptions, explaining that they add a modest margin around isolated mountain checkpoints rather than covering island/property areas. State that circles remain approximations, not official property boundaries.

In `WORLD_HERITAGE_DATA_SOURCES.md`, record that MLIT A34 World Cultural Heritage data and A28 World Natural Heritage data are marked non-commercial and their terms restrict redistribution of copies, so neither is bundled. Note that the app and catalog validator already support Polygon/MultiPolygon, and boundary geometries can be added later only from a source with confirmed redistribution terms.

- [ ] **Step 5: Rebuild and verify**

Run:

```bash
python3 scripts/build_catalog.py
python3 -m unittest scripts.test_validate_catalog -v
python3 scripts/validate_catalog.py
git diff --check
```

Expected: all catalog tests pass, catalog validation succeeds, the manifest and generated catalog agree, the selected checkpoints alone have 300m radii, and Okinoshima is still not a checkpoint.
