# World Heritage Visit Rules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep island properties on verified 200m checkpoint circles and show inaccessible Okinoshima as informational text without allowing it to trigger or count toward the Munakata heritage achievement.

**Architecture:** Keep the catalog schema and app resolver unchanged. Store the public, visitable checkpoints in each heritage item's existing `locations` array; use the visible item `detail` field for the inaccessible Okinoshima notice, with no coordinates for that component. Rebuild `catalog.json` from the plugin source manifest.

**Tech Stack:** JSON catalog manifests, Python `unittest`, catalog validation and generation scripts.

## Global Constraints

- A heritage parent item is achieved once when a photo GPS coordinate is within 200 meters of any one of its eligible checkpoints.
- Do not add island-wide circles or expand island checkpoint radii to cover whole islands.
- Do not give Okinoshima itself a GPS checkpoint because general access is prohibited.
- Keep the Munakata parent heritage eligible through its publicly visitable component checkpoints; do not mark the whole parent pre-achieved or exclude it from totals.
- Show Okinoshima's non-counting status in the Munakata item's visible detail text.
- Preserve the existing user's uncommitted catalog work and update only the world-heritage files needed here.

---

### Task 1: Encode and verify the island and Okinoshima visit rules

**Files:**
- Modify: `scripts/test_validate_catalog.py`
- Modify: `plugins/japan-world-heritage.json`
- Modify: `catalog.json` (regenerate only with `scripts/build_catalog.py`)
- Modify: `README.md`
- Modify: `WORLD_HERITAGE_COORDINATE_RESEARCH.md`
- Modify: `WORLD_HERITAGE_DATA_SOURCES.md`

**Interfaces:**
- Consumes: Existing manifest fields `items[].detail`, `items[].locations[]`, and `locations[].radiusMeters`.
- Produces: No app-model or schema change; catalog source and generated catalog both state the agreed visit rules.

- [x] **Step 1: Add the rule regression test first**

Add a `WorldHeritageDataTests` class to `scripts/test_validate_catalog.py`. Its test must load `plugins/japan-world-heritage.json`, find the items whose IDs are `ogasawara-islands` and `amami-okinawa`, and assert every location has `radiusMeters == 200`. Find the item whose ID is `okinotsushima-munakata`, assert its detail contains `沖ノ島本島`, `判定対象外`, and `表示のみ`, assert no location title is `沖ノ島本島`, and assert the public `宗像大社沖津宮遙拝所` checkpoint remains present.

- [x] **Step 2: Run the new test and confirm the expected failure**

Run: `python3 -m unittest scripts.test_validate_catalog.WorldHeritageDataTests -v`

Expected: FAIL because the manifest does not yet label Okinoshima display-only and the test requires that user-approved behavior.

- [x] **Step 3: Update the manifest and explanatory text**

In `plugins/japan-world-heritage.json`, increment the plugin `version` from `2` to `3`, make its summary state that one of the listed checkpoints within 200m achieves one heritage item, and update only the Munakata item's `detail` to explain that Okinoshima itself is inaccessible, shown for information only, and does not participate in GPS judging; keep its four existing public checkpoints and all island checkpoint radii at 200m.

In `README.md`, state that island-wide circles are not used and that natural island properties use selected public checkpoints rather than full-area coverage. In `WORLD_HERITAGE_COORDINATE_RESEARCH.md` and `WORLD_HERITAGE_DATA_SOURCES.md`, document that all Ogasawara and Amami-region checkpoints retain the standard 200m radius, no whole-island radius is used, and Okinoshima is a displayed, non-counting notice while public Munakata components can still achieve the parent item.

- [x] **Step 4: Rebuild and run focused plus full catalog checks**

Run: `python3 scripts/build_catalog.py`

Run: `python3 -m unittest scripts.test_validate_catalog -v`

Run: `python3 scripts/validate_catalog.py`

Expected: all unit tests pass, and validation prints `validated` with the catalog manifest count.

- [x] **Step 5: Verify the final diff and per-heritage conditions**

Run `git diff --check` and inspect `git diff -- scripts/test_validate_catalog.py plugins/japan-world-heritage.json catalog.json README.md WORLD_HERITAGE_COORDINATE_RESEARCH.md WORLD_HERITAGE_DATA_SOURCES.md`. Confirm only the intended rules and generated catalog data changed, all 27 parent items still have one or more GPS checkpoints, and the four public Munakata checkpoints remain capable of achieving its parent item.
