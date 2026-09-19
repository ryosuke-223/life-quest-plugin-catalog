# Castle Plugin Completion Plan

**Goal:** Bring the castle collection closer to its stated grounds-based visit rule and make its map, attribution, source record, tests, and mockup agree.

**Architecture:** Keep the existing schema-version-1 plugin shape backward compatible. Use source-traceable OpenStreetMap castle or named castle-park polygons only where the mapped area contains the Wikidata representative coordinate and represents more than a keep footprint; retain the documented 250 m circle where no suitable public area exists. Show circle and polygon ranges with matching visit-status colors, and display attribution text from optional plugin metadata. Park boundaries are documented as community-mapped proxies rather than official moat or cultural-property boundaries.

**Tech Stack:** Swift, SwiftUI, MapKit, XCTest/Swift Testing, Python catalog validator, GeoJSON.

## Global Constraints

- Do not add per-location `sourceURL` fields.
- Do not invent or hand-trace castle boundaries without a traceable source.
- Keep estimated photo matches and existing visit-count semantics unchanged.
- Keep old manifests valid when the optional attribution field is absent.
- Mark OSM-derived geometry and its ODbL license separately from Wikidata CC0 coordinates.

## Tasks

### Task 1: Regressions for range display and polygon edges

**Files:**
- Modify: `../life-quest/LifeQuest/LifeQuestTests/LifeQuestDomainTests.swift`
- Test: `xcodebuild test -project ../life-quest/LifeQuest/LifeQuest.xcodeproj -scheme LifeQuest -destination 'platform=iOS Simulator,name=iPhone 17' -derivedDataPath /private/tmp/life-quest-castle-derived`

- [x] Add a geometry test whose only observation lies exactly on an inner-ring edge and assert it remains unvisited.
- [x] Add a map-data test asserting a checkpoint pin uses its parent castle name and the configured effective radius.
- [x] Add a progress percentage test asserting 8 of 27 displays as 30 after rounding.
- [x] Run the tests before implementation and confirm the new behavior fails.

### Task 2: Correct map geometry and attribution

**Files:**
- Modify: `../life-quest/LifeQuest/LifeQuest/PluginModels.swift`
- Modify: `../life-quest/LifeQuest/LifeQuest/MapBoundaries.swift`
- Modify: `../life-quest/LifeQuest/LifeQuest/ContentView.swift`
- Modify: `../life-quest/LifeQuest/LifeQuestTests/LifeQuestDomainTests.swift`

- [x] Exclude the boundary of GeoJSON interior rings, matching the documented hole rule.
- [x] Carry each checkpoint's effective radius, parent title, and plugin symbol into map data.
- [x] Draw status-colored `MKCircle` overlays for circular ranges and keep polygon overlays for area ranges.
- [x] Replace the hard-coded airplane glyph with the plugin's icon and show the castle name in the callout.
- [x] Show optional map attribution beneath the map and link OpenStreetMap credit to its copyright page.
- [x] Round the whole-progress percentage to the nearest integer.
- [x] Run the focused tests and the full app test/build command available in this environment.

### Task 3: Add traceable boundary data and source notes

**Files:**
- Modify: `plugins/japan-castle-collection.json`
- Modify: `CASTLE_PLUGIN_DATA_SOURCES.md`
- Modify: `../life-quest/LifeQuest/LifeQuest/PluginModels.swift`
- Modify: `../life-quest/LifeQuest/LifeQuestTests/LifeQuestDomainTests.swift`
- Modify: `README.md`

- [x] Add optional `mapAttribution` metadata, decoding as absent for older manifests and validating bounded non-empty text when present.
- [x] Add source-traceable OSM park/castle geometry for the 19 candidates that represent mapped precincts; preserve 250 m circles for the eight without suitable grounds polygons.
- [x] Record every castle's Wikidata QID and every adopted OSM way/relation ID in the data-source note, with separate CC0 and ODbL terms.
- [x] Explain that mapped park boundaries are non-official proxies and that the eight fallback circles remain approximate.
- [x] Keep the manifest free of `sourceURL` fields and validate all catalog manifests and validator tests.

### Task 4: Align the mockup with runtime

**Files:**
- Modify: `mockups/meijo-plugin-mockup.svg`

- [x] Match map status colors, castle marker glyph, map-range legend, and the displayed rounded percentage to the app.
- [x] Label the artwork clearly as an above-the-fold concept and identify the achievement-card and castle-list sections below it.
- [x] Parse the SVG; a raster preview is unavailable in this sandbox (`sips` cannot render SVG and `qlmanage` cannot initialize).

## Verification

- Run `python3 scripts/validate_catalog.py` and `python3 -m unittest scripts.test_validate_catalog` in this repository.
- Run the LifeQuest XCTest target using the simulator destination above; if the simulator runtime is unavailable, run `xcodebuild build-for-testing` with the generic iOS Simulator destination and report that execution of tests was blocked.
- Confirm all 27 manifest entries remain present, no location contains `sourceURL`, and the 19 geometry entries contain their representative point.

**Environment note:** Xcode test execution and simulator build were attempted, but Xcode reported `No available simulator runtimes for platform iphonesimulator`. The platform-independent Swift domain files typecheck and a standalone resolver check confirms a photo on a polygon hole edge stays unvisited. The full UIKit/SwiftUI typecheck could not run because its Xcode macro plugins are also blocked by this sandbox.
