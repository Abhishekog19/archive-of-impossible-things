# Current plan — Archive of Impossible Things

Status (revised September 25): complete connected environment scope now covers
REF4/5/6/7/8/10. The September 30 deadline and former future phase dates are superseded.
Accelerated target: October 23, 2026; previous baseline October 25, risk planning
bound November 1. Availability remains one hour per weekday and three hours per
weekend day. The September 23 build-first revision below supersedes older forecasts
and verification cadence; reassess area coverage at the September 27 weekly review.
Phase A (September 12–15) production and bounded route review are complete.
All six areas are connected, with four reserved game locations and comparison
cameras. September 15 closes the forest gap and refines archive framing/root
connections. User visual acceptance remains open; this is a working layout for
asset production, not final art approval. Phase B's technical review is complete;
the September 22 gate was brought forward to September 21. Final art approval is open.
The reusable-kit/browser proof started September 15 and is finalized September 16.
September 17's kit variation was completed early and published September 17 as
version 14 after the usage-limit interruption. September 18's zone export/loading
proof was completed September 17 and published as version 15 on September 18.
September 18's water-only half is finished; September 19 adds the combined cavern
light/fog prototype and initial cost checks. September 20 closes the wider camera,
fallback and sustained-cost review. September 21 completes material-transfer and
repeated-loading review. The kit/prototype gate permits Phase C production.
September 22’s assembled correction patch is complete. September 23’s hub paving
and main ruin silhouette pass was completed early on September 22. September 24
hub vegetation, planted paving, approach stones and contextual corner lighting are
complete as a production pass. September 25 REF5 approach expansion was completed
on September 25 after starting September 24. Next: September 26 REF5 finish and REF6 deep-canopy dressing.
Existing hub layout and corner technical proof remain reusable; final visual
approval is open. Final character movement/physics and games follow environment
completion. Existing movement supports inspection; author collision-ready geometry now.

Scope, dates and acceleration strategy: [connected environment plan](../environment-september-plan.md).
Visual target: [look target](../look-target.md), primary concept `concept/REF4.png`.
Pipeline conventions: [art pipeline](../art-pipeline.md). Its historical MCP status
is outdated: Blender MCP is installed and working; no setup changes are needed.
This milestone takes priority over the older full-game roadmap.

| Step | Completion evidence |
|---|---|
| 1. Whole-world blockout | Hub, forest sections, archive exterior/interior and cavern have clear scale and connected inspection routes. |
| 2. Camera/composition | Matched reference screenshot establishes plaza/path/tree/landmark proportions; gameplay camera reads clearly. |
| 3. Art/detail pass | Terrain/ruins → vegetation → materials → lighting/fog → detail; fix the largest 3–5 visual mismatches per iteration. |
| 4. Optimization/export | Reusable assets and simple colliders export to GLB; textures, draw calls and visible geometry meet existing budgets. |
| 5. R3F loading | Browser loads GLB with correct scale, materials and lighting; representative export is proven early. |
| 6. Integration readiness | Separate collision proxies and usable stairs/slopes/clearances; existing controller aids inspection. Final movement/physics integration follows environment delivery. |
| 7. Browser/mobile testing | Daily affected-area visual/movement check; build/lint when inputs change. Weekly technical batch covers Iris Xe, resources/loading and mobile layout; user-led real-phone controls/thermals remain at the end. |

## Build-first cadence — effective September 23

User direction: spend daily sessions building the complete environment; consolidate
routine technical verification into one weekly session. This supersedes earlier
per-session test requirements and historical next-step dates below.

- Daily loop: build an area → compare the affected reference/player view → briefly
  check the changed walking connection → continue to the next area. Keep routine
  review to about 5–10 minutes per session; address the biggest visual mismatches.
- Before pushing changed runtime/assets, run one production build and lint changed
  JavaScript once. Reuse passing checks until their inputs change. Documentation-only
  changes need a diff/read-through, not a game build, browser run or FPS test.
- No routine daily FPS samples, timed traversal, repeated full-route suites,
  resource/eviction audits, tier matrices, mobile matrices or duplicate deployment
  checks. Queue those for the weekly review. Fix an observed broken load, blocked
  route or crash immediately with a focused check; do not expand it into a broad audit.
- Weekly review: September 27, October 4, 11 and 18, then the final week's review
  on October 23. Reserve 45–60 minutes within existing availability; use the rest
  of the session for building. Run one representative sustained hardware traversal,
  inspect loading/resources/payload and changed transitions, check mobile layout
  and deployment parity, then record actionable fixes. Recheck only failed items.
- Keep Iris Xe/mobile budgets in design decisions. Real-phone controls/thermals
  remain user-led at the end. Final delivery still covers all six reference areas.
- Next production task: September 26 REF5 finish and REF6 deep canopy, broken
  ruins and layered foliage. Next technical review:
  September 27. Sessions still require the user's start; this is not an automation.

Accelerated delivery target: **October 23, 2026**, two calendar days earlier than
the former October 25 target. The revised schedule provides 48 hours from September
22 through October 23 versus the former 54 through October 25: it requires about
six scheduled hours to be recovered through consolidated checks and less duplicate
acceptance work. Those hours are a planning assumption, not measured time saved.
September 25’s production session started on September 24 and completed on
September 25; no full additional day ahead is claimed. The two-day delivery reduction remains a
planning assumption; do not subtract this early session again from the target.
Confirm or revise the target at September 27's weekly review using completed art
coverage. October 25 remains the previous baseline; November 1 is still the risk
planning bound. Do not omit areas or materials/lighting to claim an earlier finish.

## September 25 — REF5 approach expansion completed

- Added a separate editable forest-approach.blend/GLB and reproducible
  npm run blender:forest-approach command. Extended dressed woodland from the
  existing patch at z=-40 to z=-65, following the established curved walking lane.
- Added 100 flagstones, twelve branching trees, 264 clustered ground-cover
  instances, four broken masonry groups and sixteen shoulder outcrops. A thin
  terrain-following moss surface receives the placed canopy/contact lighting.
- Three 2K diffuse atlases separate stone, trunks and ground; shared plant
  prototypes draw in four instance batches. Reduced crown leaf density and
  narrowed trunk/crown proportions after the first visual comparison. Darkened
  undergrowth and removed obsolete road faces from the dressed section so the
  old plain border does not show through; walking collision stays resident.
- Default world remains available. The opt-in art preview replaces nearby coarse
  tree/crown/shoulder proxies, retains the resident floor, and adds simple trunk
  collision. Existing hub and first forest-patch assets are unchanged.
- Compared concept/REF5.png with .artifacts/forest-sep25-reference.jpg and
  forest-sep25-gameplay.jpg. Remaining priorities: the coarse forest beyond this
  section, side-bank/background integration, richer material breakup and a more
  continuous canopy/light rhythm. September 26 owns REF5 finish and REF6 dressing;
  this is a production checkpoint, not final visual acceptance.
- The affected approach route and return pass (eight waypoints, grounded at each,
  no application errors): .artifacts/forest-sep25-connection.json. Changed-file
  lint and production build pass. No FPS or broad regression matrix was run;
  payload, foliage density and loading costs remain for September 27.
- Private-file safety checked through Git metadata only. The user's pre-existing
  hub-blockout.blend change and Blender MCP setup remain untouched.

Next: September 26 production, starting early on September 25. October 23 remains the
provisional delivery target, with no additional completion-date reduction claimed.

## September 24 — hub vegetation and unified lighting completed

- Expanded the hub from three to eight branching trees, retaining established root
  positions and collision proxies. Removed their coarse crowns and foreground
  shrub proxies. Simplified leaf fans before export; no additional runtime shadows.
- Added 136 clustered fern, shrub, grass and broadleaf instances in four batches,
  irregular moss through selected paving joints, and 36 slope-following approach
  slabs joining the old corner to the forest patch.
- Rebuilt the corner's paving and architecture bake in world position with the
  hub sun and canopy shadows. The opt-in art preview uses this contextual version;
  the original corner asset and default blockout path remain available.
- Hub export is 11,404,892 bytes with five diffuse atlases (three 2K, two 1K).
  Editable source: art/source/hub-art.blend. Payload/foliage density and broader
  resource costs are queued for September 27, not claimed to pass today.
- Quick REF4/player comparison: .artifacts/hub-sep24-final-reference.jpg and
  hub-sep24-final-gameplay.jpg. Better canopy detail and continuous lit paving;
  remaining major gaps are coarse background forest, bare terrain shoulders and
  simplified foliage lighting. REF5/6 production and the Phase C finish pass own
  these gaps. This completes today's production scope, not final visual approval.
- Production build and changed-JavaScript lint pass. Focused corner-to-forest
  walking connection and return pass; evidence: hub-sep24-connection.json.
  No daily FPS, mobile, sustained traversal or full-world test suite was run.
- Private source remains ignored/untracked (metadata only). The user's existing
  hub-blockout.blend edit and Blender MCP configuration remain untouched.

Next: September 25 REF5 woodland expansion. Target stays October 23; weekly
technical review September 27. Older performance figures below describe older
builds and do not validate today's denser vegetation.

## September 24 — historical first pass, started September 23

The September 22–23 patch/stonework checkpoint is complete and published as
version 18. The September 24 session is now **in progress**, not complete.

- Replaced three established hub tree proxies beside the plaza and old corner
  with fused trunks, branching crowns and layered leaf colours. Preserved root
  positions and resident trunk collision. Their placed shadows now contribute to
  the plaza/ruin bake; no runtime lights or shadow maps were added.
- Added one 1K wood atlas and one merged foliage draw. Hub GLB is now 4,932,840
  bytes with 2K + 1K + 1K atlases. Forest patch is unchanged.
- Compared REF4 with `.artifacts/hub-sep24-first-reference.jpg` and
  `hub-sep24-first-gameplay.jpg`. Remaining priorities: replace the other coarse
  crowns, vary canopy density/shape, grow irregular ground cover through sheltered
  joints and blend the old corner's material scale/light direction with the plaza.
  The smooth connection into the forest also remains undressed.
- Build/lint, all 17 route segments, representative trunk/pillar blocking, sRGB
  transfer, default-world isolation and 390 × 844 layout pass.
  Evidence: `hub-sep24-first-checks.json` and
  `world-art-sep24-first-production.json` in `.artifacts/`.
- A 60-second production regression traversal on Iris Xe/D3D11 averages 60.00 FPS,
  1% low 59.52 FPS, p95 16.7 ms; 1280 × 720, Medium DPR 1.25. All 297 observations
  are visible/grounded; 16 waypoints complete without errors. Evidence:
  `world-art-sep24-first-performance.json`. This is a bounded regression after
  the stone pass's three-minute test, not full-environment or phone acceptance.
- Private-file protection and the user's existing hub source edit remain intact.

Next: finish the remaining September 24 vegetation/material/light work before
starting the September 25 REF5 expansion and throughput review. Starting tomorrow's
work early does not change the October 25 forecast.

## September 22–23 — placed forest patch and hub stone pass

September 22's interrupted first half is finished. September 23's paving/ruin
production is completed on September 22, one calendar day early. This is a
production checkpoint, not final visual approval or an earlier delivery promise.

- Forest: 72 placed slabs follow the existing slope; four trees have fused branch
  junctions, layered leaf values and terrain-grounded roots. A terrain-following
  moss/soil surface and 72 plants receive/cast contextual shadows in a placed 2K
  diffuse bake. Iteration removed black branch collars, extended the interrupted
  paving and changed the evenly spaced plant rows into clusters.
- Hub: 250 chipped flagstones, worn circular inlays and seven weathered column
  silhouettes replace the smooth plaza and matching coarse pillars. Retained the
  26 m footprint, routes, tower, older corner and resident floor/pillar colliders.
  Comparison corrected honeycomb-like cells, regular pillar edges and crisp rings.
- New editable sources and generators: forest patch and hub art. Runtime uses
  unlit sRGB bakes with up to 4x filtering; foliage retains vertex colours. Forest
  GLB: 4,911,392 bytes / one 2K atlas. Hub GLB: 2,339,136 bytes / 2K + 1K atlases.
  Shared context exporter removes only replaced proxies without saving the source
  world. Python caches are ignored. No new real-time lights or shadow maps.
- Review is opt-in: `?patch=1&start=patch` for forest roaming,
  `?patch=1&start=hub` for hub roaming, `?patch=1&view=patch` and
  `?patch=1&view=reference` for comparison. Default world and zone/cavern studies
  retain their existing loading path; new art does not load in the default world.
- REF5/6 comparison: `.artifacts/patch-sep22-reference.jpg`. REF4 comparison:
  `hub-sep23-reference.jpg`; player view: `hub-sep23-gameplay.jpg` in the same
  folder. Largest remaining mismatches: placeholder hub/background crowns, smooth
  undressed approach connections, sparse/regular surface growth, flat broader
  lighting and the visible old-corner transition. September 24 addresses the hub
  portion; REF5/6 expansion remains September 25–29. No similarity score claimed.
- Build/lint pass. All 17 route segments pass with 100% sampled ground contact;
  two trunk approaches and a hub pillar approach remain blocked and grounded.
  Three new baked surfaces retain their expected sRGB maps. Production loading,
  default-world isolation and 390 × 844 no-overflow checks pass.
  Evidence: `hub-sep23-checks.json`, `world-art-sep23-production.json`.
- A 180-second production keyboard traversal on Iris Xe/D3D11 averages 60.00 FPS,
  1% low 59.52 FPS, p95 16.8 ms at 1280 × 720, Medium DPR 1.25. All 898
  observations are visible/grounded; 50 route waypoints complete with no errors.
  Maximum observed: 20 draws / 158,590 triangles. Evidence:
  `world-art-sep23-performance.json`. This validates the local hub/patch route,
  not final full-world density, Vercel parity or phone thermal performance.
- The private source remains ignored/untracked (Git metadata only); the user's
  existing hub-source edit remains unchanged and excluded. Blender MCP setup is
  untouched. No Archive gameplay or final character/phone work was added.

Next session: September 24 hub vegetation/material scale/contextual lighting and
old-corner blending. The dated production sequence is one day ahead; October 25
remains the working finish, with October 25–November 1 planning range and the
September 25 throughput review still required.

## September 22 gate — completed early on September 21

Decision: technical prototypes pass; advance to Phase C with a mandatory visual
correction checkpoint at its start. This closes the planned review, not final art
approval. No new area dressing or runtime change was made during this gate.

| Gate | Evidence and disposition |
|---|---|
| Reusable kit | Six slabs, four masonry forms, arch and broken column, three derived tree forms, two roots and four ground-cover families exist. Sufficient starting kit; hero facade/root/rock assets still belong to their area phases. |
| Export/material transfer | September 21 asset contract and 22 browser batches pass. 2K stone/1K wood atlases retain their bytes, sRGB and filtering. Visual seams and contextual lighting remain art work. |
| Loading/collision readiness | Three eviction cycles, retry, cancellation and resident-floor/gate checks pass. The kit-family strip is a loading proof, not the final six-zone partition. |
| Water/light risk | September 20 four-view/three-tier study passes. Low has no reflection target; Medium/High use bounded targets. Final chamber and shoreline shapes remain Phase E. |
| Local performance | Existing 180-second production tests: streamed strip 59.97 FPS, cavern 60.00 FPS, Iris Xe/D3D11, Medium DPR 1.25, 1280 × 720. These do not approve full-world density, deployment parity or phones. |
| Visual production readiness | Conditional: fix contextual shadows, bark seams/bake orientation and canopy depth in an assembled patch before repeating the kit widely. User visual acceptance remains open. |

Reviewed the unchanged September 15 world screenshots against REF4/5/6/7/8/10,
plus September 21 assembled-kit and September 20 cavern comparisons. These are
existing captured views, not new renders. The review priorities by area are:

| Area/reference | Largest remaining mismatches | Production owner |
|---|---|---|
| Hub / REF4 | Flat plaza/ring surface, placeholder crowns and pillars, missing canopy/contact shadows | Phase C |
| Approach / REF5 | Smooth road ribbon, sparse woodland shoulders, coarse trunk/crown silhouettes | Phase C |
| Deep canopy / REF6 | Blocky overhead masses, weak layered depth, missing dappled light and broken stone detail | Phase C |
| Exterior / REF7 | Box-like facade, angular wrapping roots, absent masonry relief/organic joins | Phase D |
| Interior / REF8 | Uniform arcade/columns, plain floor, missing roof-light/vegetation composition | Phase D |
| Cavern / REF10 | Faceted bowl walls, regular shore/wedges, radial roof light and low surface density | Phase E |

Source evidence: `.artifacts/world-sep15-{reference,forest,canopy,exterior,interior,cavern}.jpg`,
`material-sep21-{ruins,forest}.jpg` and `cavern-sep20-{west,east,shore,low}.jpg`.
Detailed measured checks remain in the September 20/21 entries; no identical tests
were rerun for this documentation-only gate. Private material is ignored/untracked;
the pre-existing hub source stays excluded. Blender setup and live version 17 are unchanged.

Reforecast: retain October 25 as the working finish, with October 25–November 1
as the planning range. The old October 18 optimistic bound is withdrawn: there is
no accepted complete-area art throughput yet to support it. Prototype risk has
fallen, but contextual baking and hero asset production are still unmeasured.
Bring Phase C's start to September 22, giving it 12 scheduled hours through
September 29 and 54 hours remaining through October 25. These are availability
windows, not logged labour or a guarantee. Later phase dates stay unchanged.

Next session (September 22): assemble a connected hub-to-forest sun/shade patch
in the actual world; correct bark seams and baked-light orientation, add grounded
canopy/contact shadows and layered foliage values; export and compare fixed and
player views. Preserve the approved layout and existing hub-source edit. Expand
only after that patch meets its visual checkpoint. See the dated Phase C sessions
in `environment-september-plan.md`. This review is one calendar day early; it does
not establish a one-day earlier environment delivery.

## September 21 — assembled material transfer and loading risk review

- Reviewed REF2 stone and REF5 forest against the assembled zone views at
  1280 × 720 (`.artifacts/material-sep21-{ruins,forest}.jpg`). This session is
  technical/visual review, not new world dressing or final material approval.
- Added `npm run verify:zone-assets`: checks manifest sizes/nodes, embedded atlas
  identity against the source kit, UV0, foliage colours and the current runtime's
  material contract. Both packages pass; in-memory stale-size and changed-atlas
  negative checks are rejected. No source assets are rewritten.
- Browser audit verifies 22 instance batches: unlit baked materials, sRGB 2K
  stone/1K wood atlases, 4x filtering, correct vertex colours and fog support.
  The transfer is intact; flat lighting is not evidence of missing texture maps.
  Evidence: `.artifacts/material-sep21.json`.
- Three in-place eviction/reload cycles return to 16 geometries / 2 textures in
  ruins, 14 / 2 in forest, and 26 / 3 in overlap. Failed fetch keeps the gate solid;
  Retry and cancellation/re-entry recover without errors or resource growth.
  Evidence: `.artifacts/zones-sep21-checks.json` (rerun of existing lifecycle test).
- A 180-second production keyboard traversal on Iris Xe/D3D11 in GPU-backed
  headless Chromium averages 59.97 FPS, 1% low 56.47 FPS, p95 16.7 ms. Medium,
  DPR 1.25, 1280 × 720; nine endpoint arrivals, 864 visible/grounded observations,
  no application errors. Each endpoint returns to the same resource baseline.
  Observed maximum: 26 draws / 114,824 triangles. Evidence:
  `.artifacts/zones-sep21-performance.json`. This proves the prototype strip,
  not final dressing density, full-world transitions, Vercel parity or phone thermals.
- Production 390 × 844 layout has no overflow and loads grounded. Build/lint and
  export checks pass. Private source stays ignored/untracked by metadata only;
  the pre-existing hub-source edit is unchanged and excluded from commits.

Priorities for September 22's gate: (1) contextual ground/contact/canopy shadows,
(2) bark atlas seams and directional-bake orientation, (3) foliage value/depth and
background enclosure. Current unlit preview highlights rotate with reused assets;
prove an assembled sun/shade patch before repeating final art. These are explicit
art-production blockers, not a claim that today fixed them. Pipeline notes describe
the export check and baking decision. World art/runtime are unchanged today.

Next: review the kit/prototype gate and reforecast September 22 before Phase C
hub/forest dressing. October 25 remains the provisional finish; no schedule lead
is claimed from a completed review day. The playable preview remains version 17.

## September 20 — cavern angles, Low fallback and sustained cost

- Compared REF10 with four fixed views: original, west, east and low shoreline.
  Use `?scene=cavern&view=cavern`, `cavern-west`, `cavern-east` or `cavern-shore`.
  Evidence: `.artifacts/cavern-sep20-{low,west,east,shore}.jpg`.
- Water now follows scene fog at every tier. Low retains a soft analytical
  opening-light reflection without a render target; it does not reflect scenery
  or the character. Medium/High retain their bounded planar reflection targets.
- All 12 camera/tier combinations pass without application/shader errors. Three
  in-place quality cycles return to stable resource counts. Fixed main view:
  Low 3 draws / 512 triangles / 3 geometries / 1 texture; Medium/High 6 draws /
  1,090 triangles / 4 geometries / 2 textures, including reflection rendering.
  Shore travel/return, fall recovery and the upper gate pass.
- Production spawn/tier switching, 390 × 844 layout and default-world isolation
  pass. Build/lint pass. Evidence: `.artifacts/cavern-sep20-{checks,production}.json`.
- A 180-second production traversal in GPU-backed headless Chromium on actual
  Iris Xe/D3D11 averages 60.00 FPS; 1% low 58.99 FPS, p95 frame time 16.8 ms.
  At 1280 × 720, Medium DPR 1.25, all 917 observations remain visible/grounded;
  64 shoreline waypoints complete with no application errors. Evidence:
  `.artifacts/cavern-sep20-performance.json`. A first run stalled at its return
  waypoint and is excluded; the final route checks for stalls throughout.
  This is local prototype evidence, not whole-world, Vercel or phone acceptance.
- Largest remaining REF10 gaps are coarse wall facets, a regular rounded bank,
  angular shoreline wedges and roof-light spokes/limited atlas density. These
  need Phase E geometry and contextual art; this prototype is not visual approval.
- Private material remains ignored/untracked by metadata checks only. The user's
  pre-existing hub-source edit is unchanged and excluded. Blender setup is untouched.

Next: September 21 assembled material/lighting transfer and repeated-loading risk
review. Phase B's September 22 gate and October 25 forecast remain unchanged;
this closes the scheduled day and does not establish a full-project schedule lead.

## September 18–19 — water half completed, light prototype verified

- Published the pending zone-loading checkpoint (version 15). Finished the
  requested water-only half, then resumed on September 19 at the user's request.
  Water work was committed/pushed separately as `436230e`.
- `?scene=water` preserves the old cavern for comparison. It reuses the Blender
  GLB pool outline with calm ripples, angle-dependent tint and a 384/512px planar
  reflection on Medium/High. Low has no reflection target. Nested reflection
  draws are included in the HUD; owned targets/materials/geometry are disposed.
- `npm run blender:cavern` extracts the existing cavern into its own editable
  study and bakes colour/direct/indirect illumination through the opening, at
  40 CPU samples. One 1024px atlas; GLB 226,036 bytes; source 1,023,422 bytes.
  The world/hub source assets and Blender MCP setup remain unchanged.
- `?scene=cavern` loads only this study GLB, with unlit baked stone, cool fog,
  opening light and a soft transparent shaft. Low omits the shaft/reflection.
  It retains inspection movement, closes the extracted passage's upper end and
  returns falls to the cavern entrance. No swimming, final physics or gameplay.
- REF10 comparisons: `.artifacts/cavern-sep19-{reference,gameplay}.jpg`, plus
  `water-sep18-half-{reference,gameplay}.jpg`. Two lighting iterations reduced
  overall brightness, noisy mottling and weak separation around the shaft.
  Coarse triangular walls, flat/regular shore, roof light spokes and limited
  pool framing remain the largest visual gaps; this is not final art approval.
- Three Low/High/Medium cycles return to the same resource counts. Fixed study:
  Low 3 draws / 512 triangles / 3 geometries / 1 texture; Medium/High 6 draws /
  1,090 triangles / 4 geometries / 2 textures, including the reflection pass.
  The atlas is sRGB, unlit and filtered up to 4x. Shore walk/return, entrance
  recovery and the closed upper passage pass. No application/shader errors.
- Production spawn, tier changes, 390 × 844 layout and default-world isolation
  pass. The default does not fetch the study GLB or either cavern shader chunk.
  Build/lint pass. Evidence: `.artifacts/cavern-sep19-{checks,production}.json`.
- A brief visible production sample at 1280 × 720, Medium DPR 1.25, holds about
  60 FPS after settling; 9 draws / 1,726 triangles / 6 geometries / 3 textures.
  `cavern-sep19-live.json` contains 15 HUD observations, not a three-minute
  traversal or real-phone thermal acceptance. Headless FPS is excluded.
- Private material remains ignored/untracked by Git metadata only. User's
  modified `hub-blockout.blend` remains excluded, with its original hash intact.

September 19's implementation session is complete. September 20 remains the
broader angle/fallback/sustained-cost review within the existing two-day prototype
window. Phase B is not complete; the September 22 review and October 25 forecast
are unchanged. Separate pushed groups: water `436230e`, Blender/export `310b4f8`,
runtime `73e407e`, followed by the documentation checkpoint containing this record.

## September 17 — zone-loading proof brought forward from September 18

- Finished the pending kit publication in three separately pushed commits:
  ba0fb52 (art), f154a40 (preview), 1746c00 (documentation); version 14 is live.
  The earlier automatic approval failure was a usage-limit interruption, now cleared.
- Added `npm run blender:zones`: reads the editable kit without modifying it and
  exports independent ruins (824,268 bytes) and forest (2,051,460 bytes) GLBs with
  a package manifest. These are kit-family packages used in two test sections,
  not final exports of the six-area world.
- Added `?scene=zones`: existing inspection movement crosses a resident floor.
  Ruins/forest preload at 28/29 m from their centres and unload beyond 40/39 m;
  separate thresholds prevent repeated loading near one boundary. Each mount owns
  its parsed geometry/materials/textures; eviction disposes them and closes decoded
  image bitmaps. Pending fetches abort, and late completed parses are discarded.
- Loading or failed sections retain solid entry gates. A fixed screen overlay
  reports readiness and offers Retry. A review caught the original 3D-anchored
  overlay disappearing behind the camera; the final overlay remains screen-fixed.
  Shared `KitBatch` preserves the earlier preview's instancing behaviour.
- Three in-place round trips return to 16 geometries / 2 textures in ruins and
  14 / 2 in forest; overlap reaches 26 / 3. Simulated HTTP failure blocks the
  character at the gate, Retry recovers, and cancellation/re-entry returns to the
  same baseline. No application errors. Evidence: `.artifacts/zones-sep17-checks.json`.
- A production keyboard walk from z=6 to below -50 and back passes with all 72
  sampled positions grounded. Resource counts return to 16 / 2. The default world
  requests neither zone packages nor the asset preview. Headless FPS is excluded
  from hardware performance claims. Evidence: `zones-sep17-production.json`.
- Initial production resources: 2,010,279 encoded bytes / 4,338,997 decoded bytes,
  excluding the HTML document and HTTP headers; only the ruins GLB is fetched at
  spawn. Forest loads on approach. This is a prototype payload measurement, not
  proof that the complete world meets the 8 MB initial-load budget.
- Brief live production ruins sample: 60 FPS, Medium DPR 1.25, 1280 × 720;
  16 draws / 5,836 triangles. Forest test view renders about 109K triangles;
  sustained forest/Iris Xe and phone performance remain unaccepted. Build/lint pass.
  At 390 × 844, the production prototype loads grounded without horizontal
  overflow or application errors (`.artifacts/zones-sep17-mobile.json`).
- Compared REF2 stone and REF5/6 forest direction with fixed views at
  `.artifacts/zones-sep17-{ruins,forest}.jpg`. The forest camera was lowered and
  centred to keep the route readable. Flat ground, sparse background enclosure,
  simplified leaf light and bark atlas seams remain art limitations; this loading
  proof does not replace Phase C dressing. Reference views keep both zones loaded.
- Existing world art and controller behaviour are preserved. User hub-source hash
  remains unchanged; private material is ignored/untracked by metadata-only checks.
  Blender MCP setup was untouched. New work is grouped as exports, runtime and docs.

Next session: the September 19–20 cavern water/overhead-light prototype, using REF10
and an early browser cost check. The September 18 checkpoint is complete one day
early; this does not move the full-phase finish or October 25 forecast. Reforecast
September 22 after the remaining material/light risks are reviewed.

## September 17 work — completed early on September 16

- Completed both halves: three derived tree silhouettes, four ground-cover
  families (fern, grass tuft, broadleaf clump, low shrub), four masonry variants,
  softer damp-stone islands and mixed broken caps. Plants use opaque vertex-colour
  geometry, yaw/scale variation and six sheltered clusters; the path stays clear.
- Replaced the old vertically stretched moss stripes on masonry, column and arch
  with varied noise islands and a gentle damp-height falloff. The first comparison
  exposed a repeating sawtooth cap row; the final arrangement mixes the cap forms.
- Compared REF2 stone and REF5/6 undergrowth/tree direction with the fixed and
  gameplay views: `.artifacts/kit-sep17-{reference,gameplay}.jpg`. Repetition is
  reduced. The sparse test floor, simplified canopy shading/branch structure and
  absence of contextual ground shadows remain prototype limitations, not art approval.
- Source: 5,853,402 bytes; GLB: 2,875,388 bytes. Seventeen stone/wood prototypes
  plus seven foliage meshes retain two 2K/1K atlases. No new runtime effects.
  Three tree shapes increase wood atlas occupancy; check close-range density when
  placing them in zones. The main world still does not fetch the preview kit.
- Build/lint pass. Eight outward/return checkpoints, wall blocking, arch passage
  and both new trunk approaches pass with 100% sampled route grounding. Three
  production kit/world reload cycles have stable counts and no application errors.
  These are bounded checks; full-page reloads do not prove in-place zone disposal.
  Evidence: `.artifacts/kit-sep17-{checks,loading}.json`.
- Brief production desktop sample: 60 FPS, Medium DPR 1.25, 1280 × 720; 27 draws,
  51,284 triangles, 27 geometries / 3 textures. The 390 × 844 viewport loads grounded
  without overflow. Evidence: `.artifacts/kit-sep17-{production,mobile}.json`.
  Neither these samples nor headless checks establish sustained whole-world or
  real-phone acceptance; the Vercel report remains unresolved.
- Both halves are grouped for separate art, runtime and documentation commits.
  Private material remains ignored/untracked (metadata only); the user's existing
  hub-source hash is unchanged and excluded. Blender MCP setup is unchanged.

This completes the September 17 checkpoint one calendar day early. Next session:
the September 18 zone export/loading proof, including payload and resource costs.
Later phase dates and the October 25 forecast remain unchanged until reforecast.

## September 17 work — historical first-half checkpoint, superseded above

- Stopped at the requested halfway boundary: tree silhouettes only. Added tall
  narrow and low leaning variants alongside the broadleaf original. Deterministic
  nonlinear shape changes keep wood, leaves and trunk proxies aligned, with roots
  anchored at the origin. These are derived forms, not three independently authored
  species. Ground-cover expansion and moss/masonry refinement remain untouched.
- Rebuilt the editable kit, GLB and manifest; preview displays one of each form.
  GLB is 2,880,112 bytes, up from 1,718,472. Still two 2K/1K atlases; increased
  wood atlas occupancy needs close-range review during later material refinement.
- REF5 comparison: taller trunk/raised crown and leaning spread reduce identical
  silhouette repetition. Preview framing and gameplay captures are saved as
  `.artifacts/kit-sep17-half-{reference,gameplay}.jpg`. Crown layering, leaf-scale
  consistency and natural branching remain review points before whole-world use.
- Build/lint pass. Eight route checkpoints, wall/arch checks and both new trunk
  approaches pass with grounding; no application errors. Default world still does
  not request the kit. Evidence: `.artifacts/kit-sep17-half-checks.json`.
- Brief live development sample: 60 FPS, Low/saved DPR 1.00, 1280 × 720; 23 draws,
  48,434 triangles, 23 geometries / 3 textures. This is not sustained performance
  acceptance or directly comparable to the earlier Medium production sample.
  Evidence: `.artifacts/kit-sep17-half-live.json`.
- No commit, push or deployment for this half-session. Public version 13 remains
  unchanged. User hub-source edit is preserved; private material remains ignored
  and untracked by metadata-only checks. Stop here as requested.

Remaining half: ground-cover families and less repetitive moss/masonry patterns,
then combined visual review. Dates/October 25 forecast are unchanged; this early
partial session does not establish a full day ahead.

## September 16 — Phase B first kit and browser proof

- Finished the September 15 carryover: six slabs, three masonry variants, broken
  column, arch, one tree silhouette and two roots, plus leaf and fern meshes.
  The three displayed trees reuse one silhouette; vegetation expansion remains.
- Added editable `art/source/archive-kit.blend` (5,329,807 bytes), runtime GLB
  (1,718,472 bytes), dimensions manifest and `npm run blender:kit`. Shared 2K stone
  and 1K wood preview atlases; opaque vertex-coloured foliage; separate colliders.
- Added lazy-loaded `?scene=kit` inspection and `?scene=kit&view=kit` fixed camera.
  Repeated assets are instanced. Default world navigation does not fetch this GLB.
  Directional diffuse preview bakes need contextual zone rebaking before delivery.
- Compared REF2 stone, REF5/6 vegetation and REF7/8 architecture direction with
  `.artifacts/kit-sep16-reference.jpg`. Initial iteration corrected column scale,
  slab/arch export and excessive upper-wall moss. Biggest remaining gaps: repeated
  tree crowns, regular arch/block silhouettes, patterned moss and contextual
  ground/lighting. The flat preview floor is a test surface, not finished world art.
- Build/lint pass. September 15 development physics checks pass eight outward/return
  checkpoints with 100% sampled grounding, wall blocking and arch passage;
  evidence: `.artifacts/kit-sep15-checks.json`. Production omits the development
  stepping hook intentionally; today's loading checks inspect the rendered UI.
- Production spot check: 60 FPS, Medium DPR 1.25, 1280 × 720; 19 draws, 48,434
  triangles, 19 geometries / 3 textures. Grounded, no application errors. At
  390 × 844 it loads grounded without overflow. These are brief desktop/viewport
  observations, not sustained whole-world or real-phone performance acceptance.
- Three production kit → world navigations pass with stable kit resource counts,
  no errors and no kit request on the default route. Full-page navigation does not
  prove in-place zone disposal. Headless FPS is excluded from performance claims.
  Evidence: `.artifacts/kit-sep16-{production,mobile,loading}.json`.
- Private material remains ignored/untracked by metadata-only checks. The user's
  hub-source hash is unchanged and excluded from commits. Blender MCP setup,
  phone controls, existing world art and Archive gameplay are unchanged.

Schedule: Phase B began September 15, one calendar day early; its first checkpoint
is finalized September 16, on schedule. No completed-day lead or earlier finish
is established. Next: tree/ground-cover variation, zone export/loading and cavern
water/light proofs. Phase B ends September 22; expected environment finish remains
October 25, subject to the September 22 review.

## September 15 — Phase A layout review

- Yesterday's pending publication is confirmed live. Today's export restores
  eastern forest coverage without blocking the courtyard comparison camera.
  The archive view is more frontal; roots now begin within the bent hero trunk,
  follow the facade and extend into the ground instead of ending above it.
- Compared all six reference views at 1280 × 720. Evidence:
  `.artifacts/world-sep15-{reference,forest,canopy,exterior,interior,cavern}.jpg`.
  The REF5 gap is closed; REF6 retains a sky opening toward the courtyard. The
  archive entrance/root hierarchy is clearer, but its framing remains tighter
  than REF7. Future dressing must preserve the entrance and clear walking lane.

| Area | Layout review | Art work still required |
|---|---|---|
| REF4 hub | Crossroads, plaza and landmark remain readable. | Replace broad ground/tree proxies; unify the detailed corner with the hub. |
| REF5/6 forest | Connected winding route, shoulders and clearing remain usable. | Authored branches/leaf clusters, irregular paving, ground cover and canopy light. |
| REF7 exterior | Entrance, taller central facade and wrapping roots read together. | Broken masonry, broader tree integration, finer roots and less cropped framing. |
| REF8 hall | Open aisle/arcades lead into the descent. | Vary arch/column damage; add vegetation, roof breakup and light hierarchy. |
| REF10 cavern | Shore, pool and overhead opening form a connected destination. | Less bowl-like rock planes, water/reflection treatment and overhead light. |

- Final GLB: 4,341,104 bytes. Build/lint pass. All 24 outward and 24 return route
  checkpoints pass with 100% sampled grounding, including remote game clearings;
  eight boundary approaches pass, with no application errors. Evidence:
  `.artifacts/world-routes-sep15.json` and clearing/descent gameplay captures.
  Camera distance is still 4 m in the passage and 0.37 m close to its wall; final
  camera polish and real-phone input/thermal acceptance remain deferred.
- Production archive spot check: 60 FPS at Medium DPR 1.25, 1280 × 720;
  12 draws / 44,719 triangles / 12 geometries / 1 texture. Grounded, no
  application errors (`.artifacts/world-sep15-production.json`). This stationary
  observation and fixed-step route screenshots are not sustained performance
  acceptance; the reported Vercel difference remains unresolved.
- Private material is ignored/untracked by metadata-only checks. The user's
  hub-source hash is unchanged and excluded from commits. No Blender setup,
  gameplay, controller or new runtime-effect changes.

Next session: Phase B's first reusable stone/masonry and tree/root modules, with
one exported browser proof before broad placement. Zone-loading and cavern
water/light prototypes belong to Phase B. Keep the September 22 reforecast and
October 25 working finish; do not treat the layout review as an 80% art match.

## September 14 — Phase A silhouette refinement

- Added layered background woodland and bent foreground trunks for REF5/6.
  Continuous tapered meshes replace overlapping capped segments, removing visible
  joints in trunks and roots. Kept the forest clearing and route clear.
- Raised the archive's central facade above its wings, bent the hero trunk,
  layered its crown and added an upper wrapping root for REF7. Moved the exterior
  comparison camera into a clear courtyard sightline; shifted background trees
  after the first comparison exposed foliage occlusion.
- Reviewed six 1280 × 720 browser comparisons against REF4/5/6/7/8/10:
  `.artifacts/world-sep14-{reference,forest,canopy,exterior,interior,cavern}.jpg`.
  Forest enclosure is fuller, but an eastern canopy gap remains near the courtyard.
  The archive is taller; framing is still tighter/more oblique than REF7 and its
  root transitions and masonry remain coarse. Hub, hall and cavern composition
  are retained. These are blockout improvements, not final art acceptance.
- GLB: 4,335,920 bytes (174,220 bytes above September 13). Build/lint pass.
  Final regression passes all 24 outward and 24 return checkpoints with 100%
  sampled grounding, plus eight boundary approaches; no application errors.
  Evidence: `.artifacts/world-routes-sep14.json`. Gameplay captures of the clearing
  and descent remain readable. The passage camera still pulls from 4 m to 0.37 m
  beside a wall; final camera tuning remains deferred. The earlier concurrent
  build/test screenshot timeout is excluded; the completed final run passes.
- Production forest spot check: 60 FPS, 12 draws, 44,671 triangles, 16 geometries /
  3 textures, Medium DPR 1.25 at 1280 × 720; grounded and no application errors.
  Evidence: `.artifacts/world-sep14-production.json`. This brief stationary check
  does not replace sustained traversal or resolve the reported Vercel slowdown.
  Fixed-step regression screenshots do not measure live performance.
- At 390 × 844, the production archive spawn is grounded with no horizontal
  overflow or application errors (`.artifacts/world-sep14-mobile.json`). This is
  a desktop viewport smoke check, not a real-phone control/thermal test.
- Private material remains ignored/untracked by Git metadata checks only. The
  pre-existing hub-source hash is unchanged and excluded from commits. Blender
  MCP setup was untouched. No gameplay or new runtime effects/textures added.

Next: September 15 layout review, including the eastern canopy gap and archive
framing/root transitions, before shared-kit production. Surface detail, dressed
vegetation, water and lighting remain in the dated art phases. October 25 remains
the working forecast; reforecast September 22. Real-phone acceptance stays pending.

## September 13 — Phase A transitions and boundaries

- Added continuous irregular terrain banks from the forest into the archive sides,
  with matching collision proxies. Preserved the west clearing; moved nearby
  decorative shoulder masses outside its camera orbit after a gameplay capture
  exposed an occlusion. The forest road widens into the courtyard continuously.
- Replaced separated descent rocks with a connected side/roof shell and walkable
  shoulders. Retained the 33 m descent and 5 m paving; the central roof clearance
  is at least 6.2 m. The entry overlaps the archive arch crown to remove a daylight
  seam. Set roof remnants behind the facade to remove a detached-looking lip.
- Reviewed REF4/5/6/7/8/10 against six browser reference views at 1280 × 720;
  evidence: `.artifacts/world-sep13-{reference,forest,canopy,exterior,interior,cavern}.jpg`.
  Gameplay captures: `world-sep13-descent.png` and `world-sep13-clearing.png`.
  Diagnostic files are local, ignored artifacts.
- Composition review: hub split and landmark are retained (REF4); forest path
  hierarchy is clear but side/background canopy remains sparse (REF5/6); archive
  entrance reads, but facade/tree/root masses still need authored silhouettes
  (REF7); hall aisle and descent are connected but arcades remain uniform (REF8);
  cave opening, pool and bank read together, but the shell remains bowl-like and
  needs varied rock planes and atmosphere (REF10). These are blockout comparisons,
  not an 80% match or final art acceptance.
- Final GLB: 4,161,700 bytes; build and lint pass. All 24 outward and 24 return
  checkpoints pass with 100% sampled grounding, including the three remote game
  clearings. Eight boundary approaches pass: both forest banks, courtyard sides,
  passage sides and cavern outer walls. The passage camera is 4 m in the open and
  pulls to 0.37 m beside a wall; that close pull-in still needs the deferred camera
  polish. These are bounded checks, not exhaustive jump/camera/physics acceptance.
  Evidence: `.artifacts/world-routes-sep13.json`, no application errors.
- The isolated physics regression suppresses redundant render submissions during
  fixed stepping. Its screenshot FPS values are not live performance measurements.
  Visual comparison uses the normal browser renderer separately. No new runtime
  effects, textures, controller changes or gameplay. Private material remains
  ignored/untracked (Git metadata only); the user's hub-source hash is unchanged
  and that file stays outside commits. Blender MCP setup was untouched.
- Production forest HUD spot check: 60 FPS, 12 draws, 42,547 triangles, 16
  geometries / 3 textures, Medium at DPR 1.25 and 1280 × 720. Grounded; no
  application errors. This is a brief stationary observation, not a sustained
  performance claim or a resolution of the Vercel report. Evidence:
  `.artifacts/world-sep13-production.json`.
- The production cavern spawn loads grounded at 390 × 844 without horizontal
  overflow or application errors (`world-sep13-mobile.json`). This is a desktop
  viewport smoke check; real-phone input and thermal verification remain pending.

Remaining Phase A review: forest side silhouettes and archive massing before kit
production; final layout approval is open. Keep September 14–15 for that review.
Phase B remains September 16–22 and October 25 remains the working finish forecast.
Detailed surfaces, canopy dressing, water/light and sustained whole-world/real-phone
acceptance remain later gates; do not infer final quality from route checks.

## September 12 — Phase A second session, brought forward

- Added a gentle S-bend to the forest extension and staggered tree positions while
  retaining the 5.6 m route width and forest game clearing. REF5/6 comparison now
  has changing foreground/midground overlap instead of a straight avenue.
- Replaced the uniform archive frontage with stepped wings and a narrower central
  crown. Bent the root proxies around the facade; reduced hall arch openings from
  18 m to 12 m. Relocated the hall's future-game anchor to [-23,1.65,-123] so it
  remains clear of the revised column line. The earlier anchor below is historical.
- Broke up cavern wall planes and shoreline radius, lowered/moved the roof opening
  to include it with the shore in the comparison frame, and added grounded rock
  masses. The entrance now cuts the lower wall only. These are shape changes;
  water, final lighting and surface detail remain later art work.
- Compared `.artifacts/world-sep12b-{forest,exterior,interior,cavern}.png` with
  REF5/7/8/10 and the first session's captures. The second visual iteration fixes
  floating rock silhouettes and an unintended roof slit. No final-quality or
  numerical similarity claim; roots and masonry are still coarse proxies.
- Verification: build/lint pass; final world GLB is 4,138,036 bytes. All 24 outward
  and 24 return checkpoints pass with 100% sampled grounding; evidence is
  `.artifacts/world-routes-sep12b.json`. These are bounded route checks, not final
  movement/physics acceptance. Browser navigation has zero application errors and
  the two existing dependency warnings. User hub-source edit and Blender setup
  remain untouched. Private source material is ignored/untracked, checked by Git
  metadata only. New detailed textures/effects were not added.

One early session does not automatically move all later dates. Remaining Phase A
  work: terrain margins/descent enclosure, boundary and side-route review, and all
  six composition views before kit production. Use recovered time for that gate;
  Phase B remains Sep 16–22 unless the gate is actually completed earlier. October
  25 remains the working forecast, to be re-estimated at the kit/prototype gate.

## September 12 — Phase A first session

- Added a separate editable `art/source/world-blockout.blend` and
  `public/models/world-blockout.glb` (4,101,244 bytes). Rebuild with
  `npm run blender:world`. The hub generator can now supply its editable scene
  in memory, avoiding an intermediate export; the user's hub source is never loaded
  or overwritten. Its pre-existing edit remains unchanged and outside our commits.
- Connected hub → existing approach → deeper canopy → archive courtyard/facade
  → open hall → descent → cavern shore. The forest road is about 5.6 m wide,
  the hall about 30 × 28 m, and the cavern about 50 m across. These are provisional
  layout dimensions. The 33 m descent drops 9.15 m (about 15.5 degrees); reduce or
  reshape it during layout review if needed, before final physics work.
- Reserved four empty future-game anchors in Blender/GLB, at browser coordinates:
  hub [5,0,5], forest [-23,1.65,-68], hall [-19,1.65,-127], cavern [-33,-7.5,-195].
  No game mechanics or game interfaces were added.
- Six provisional comparison cameras: `?view=reference`, `forest`, `canopy`,
  `exterior`, `interior`, `cavern` (each latter value uses `?view=`). Inspection
  spawns use `?start=forest|canopy|exterior|interior|cavern`; `?start=corner` remains.
  Default loads the connected world. `?scene=hub` retains the earlier hub export;
  the greyroom test course is retained.
- Iterations fixed overlapping forest/courtyard ground, opened the north boundary,
  adjusted cavern camera/wall radii, corrected cavern material colour export and
  closed the visible shoreline gap. Water is an opaque study surface, not a final
  water effect; all new areas remain untextured blockouts with temporary lighting.
- Build/lint pass. Final controller smoke check reached all 22 outward and 22
  return checkpoints with 100% sampled grounding, including forest/hall clearings
  and cavern shelf. This proves the sampled route, not exhaustive boundaries,
  camera collision or final movement/physics acceptance. The pool is not walkable;
  entering it falls into the existing recovery behavior until later integration.
- Six short, stationary production-build frame samples (three seconds per location)
  ranged 57.71–60.35 FPS, Medium/DPR 1.25 at 1536 × 864. Sampled draws ranged 6–16,
  with at most 65,035 triangles. These are smoke observations, not sustained
  whole-world or phone acceptance. Archive loads grounded at 390 × 844 without
  horizontal overflow. Production navigation reports zero application errors;
  the two existing dependency warnings remain. Vercel parity is still unresolved.
- Comparison evidence: `.artifacts/world-sep12-{reference,forest,canopy,exterior,
  interior,cavern}.png`; route evidence `.artifacts/world-routes-sep12.json`.
  Use REF4/5/6/7/8/10 respectively. No similarity percentage or visual approval claimed.
- Largest remaining layout mismatches: overly straight forest route and even tree
  spacing; box-like archive facade and straight root proxies; oversized/uniform
  hall arcades; cavern still reads as a bowl, and the comparison framing does not
  yet capture both overhead opening and shore as in REF10. Address in remaining
  Phase A sessions, before fine detail. Terrain margins/descent enclosure also
  need composition review. World loading remains one coarse GLB; zone loading is
  scheduled for Phase B. No final atmosphere, optimized detailed world or finished
  environment is claimed. October forecast is unchanged.

The entries below are historical evidence; superseded dates/scope are not active instructions.

## September 6 evidence

- Editable source: `art/source/hub-blockout.blend`; deterministic generator:
  `scripts/blender/hub_blockout.py`; rebuild with `npm run blender:blockout`.
  Generated source is reproducible; save manual edits under a different filename.
- GLB: `public/models/hub-blockout.glb`, approximately 1.10 MB. Default browser
  scene is the hub; `?view=reference` uses the composition camera and `?scene=greyroom`
  retains the existing test course. Blender MCP configuration was untouched.
- Implemented 26 m plaza, three path mouths, 30 m canopy strip, tower and forest
  proxies. Reference comparison corrected excessive fog, sparse central green mass,
  overlapping surfaces, branch orientation, and tower framing.
- Browser screenshots: `.artifacts/hub-blockout-reference.png` and
  `.artifacts/hub-blockout-gameplay.png`. Reference view: 8 draw calls / 12,164
  triangles; gameplay: 10 calls / 12,488 triangles. Brief live sample near 60 FPS
  at DPR 1.25; this is not the required sustained Iris Xe/phone acceptance test.
- Build and lint passed. Browser reports zero application errors. Deterministic
  controller checks: plaza walk, 20 m canopy walk, return segment, blocked overgrown
  mouth and fall recovery passed. These checks do not establish complete route acceptance.

## September 7 changes

- Replaced detached ground plates with continuous terrain and a cut ravine.
  The arrival descends gently into the plaza; the canopy route climbs at 5.5%.
- Added irregular crown volumes, branch silhouettes, midground trees, and woodland
  shoulders. Reduced distant mesh complexity while retaining near silhouettes.
- Preserved the hub layout the user liked; reduced the oversized concentric motif,
  adjusted reference framing, and replaced uniform pillars with broken courses and walls.
- Connected road ribbons and collision surfaces; added boulder boundaries. Fixed
  a transient null-body error in fall recovery during scene loading.
- The `.blend` now preserves separate editable objects; only the runtime export
  is merged. Rebuilding still replaces the generated source: save manual edits
  under a separate filename.

September 7 verification:
- Build and lint pass. Final browser navigation has no application errors; two
  existing Three.js/Rapier dependency deprecation warnings remain.
- All 15 waypoint segments passed: arrival → hub → rising canopy route → return,
  plus right spur and return. Final stepped run sampled 100% ground contact;
  synthetic stepping verifies movement, not FPS. Overgrown mouth and fall recovery pass.
- Additional checks stopped at the right barrier, canopy end, arrival boundary,
  and west boulder boundary. Exhaustive jumping and camera-edge cases are still
  part of later traversal acceptance.
- Final GLB: 5,932,608 bytes (down from today's first 8,535,420-byte export).
  Reference view: 8 draw calls, 45,660 rendered triangles, approximately 60 FPS
  during a short live sample at DPR 1.25. No sustained hardware/phone claim.
- Reviewed REF4 against `.artifacts/hub-sep07-reference.png`, plus four gameplay
  views: `hub-sep07-arrival.png`, `hub-sep07-hub.png`, `hub-sep07-canopy.png`, and
  `hub-sep07-ravine.png` in `.artifacts/`. Route evidence is in
  `.artifacts/hub-routes-sep07.json` (local diagnostics).
- Composition is improved but not visually approved as final. In particular,
  boulder boundaries still look repetitive, and the broken-spur obstruction
  limits the ravine view at player height; include these in September 8 review.

## September 8 — Phase 1 layout gate

- Kept the 26 m plaza, 30 m canopy strip, camera framing and tower placement from
  the layout the user liked. Cleared understory back from the path mouths.
- Replaced the repeated boundary-boulder row with continuous, irregular stepped
  rock profiles; visible ridge geometry also supplies collision.
- Extended the right spur to an overlook, lowered its parapet, moved the far bridge
  fragment across the gap, and prevented road shoulders from filling the ravine.
- Compared REF4 against `.artifacts/hub-sep08-reference.png` and reviewed hub,
  canopy, ravine and west gameplay screenshots with the same filename prefix.
  The route split and gap read more clearly. Boundary shapes are still coarse;
  the canopy end remains a placeholder rock block. Neither is final art.
- All 17 waypoint segments passed, including both return routes. Sampled grounding:
  99.6% arrival/canopy, 100% right spur. Overgrown mouth, four boundary approaches
  and fall recovery passed. Plaza jump rose 1.60 m and landed; camera pulled to
  1.83 m beside the canopy-end obstruction and returned to 4 m in the open.
  This is a bounded smoke check, not exhaustive jump/boundary/camera acceptance.
- GLB: 5,815,328 bytes. Reference view: 8 draw calls / 44,772 rendered triangles,
  brief live sample about 60 FPS at DPR 1.25. No sustained Iris Xe or phone claim.
- Build and lint passed; reference/gameplay navigation produced no application
  errors. Blender saved the editable source and exported successfully despite
  its nonblocking thumbnail-write warning. Route evidence:
  `.artifacts/hub-routes-sep08.json`. Private file remains ignored and untracked;
  content was not accessed. Blender MCP setup was untouched.

## Phase 2 first session — brought forward to September 8

- Added an 8 × 9 m benchmark at the left-path junction: chipped paving with seam
  depth, bevelled broken masonry, a branching tree with buttress roots, leaf sprays,
  ground foliage and fallen stone. Replaced one matching blockout column; preserved
  deterministic forest placement and cleared overlapping coarse shrubs.
- `npm run blender:corner` creates `art/source/hub-corner.blend` and
  `public/models/hub-corner.glb`. The source packs the atlas and retains hidden
  editable authoring objects; unhide them to edit, and save manual work separately.
- Proved full-colour DIFFUSE bake (colour + direct + indirect light, 24 CPU samples),
  UV0, embedded 1024px JPEG and sRGB loading through GLB. `HubCorner` uses an unlit
  material so runtime lighting does not illuminate the baked result twice.
  Fine foliage uses opaque geometry and vertex tinting in a second draw call;
  its shadows are baked into the static surfaces. No realtime shadows added.
- Iteration fixed shrub overlap, leaf atlas artifacts, excessive stone mottling
  and export size. Corner GLB dropped from 3,564,488 to 1,333,884 bytes. Removed
  unused UVs from the untextured blockout export: now 4,444,632 bytes.
- Final corner browser view: 10 draw calls / 56,104 triangles, approximately
  60 FPS in a short live sample at actual DPR 1.25. A previous CPU-busy sample
  triggered adaptive DPR reduction; this is not sustained Iris Xe acceptance.
- All 17 hub segments passed with 100% sampled ground contact. Dedicated corner
  walk covered about 8 m and returned grounded; blocked paths and recovery pass.
  Build/lint pass and final browser navigation has zero application errors.
- Compared `.artifacts/corner-final.png`, `corner-gameplay.png` and
  `hub-phase2-reference.png` against REF4 and surface/forest reference direction.
  Source/export report: `.artifacts/blender/corner-report.json`.
- Review links: `?start=corner` starts beside the benchmark; `?view=corner` is its
  static camera; `?view=reference` shows the whole hub. The default remains roaming.

## September 9 — Phase 2 second session, advanced one day

- Reworked the same corner: variable fractured slabs, narrower joints, sharper
  wall courses and a broken column crown; curved roots, branched leaf clusters,
  sheltered moss patches and 24 fern instances along the shoulders.
- Split the bake into 2048px paving and 1024px architecture atlases. Removed buried
  slab undersides from the bake/export. Grain and directional bark relief are
  baked into colour; no runtime normal maps or realtime shadows were added.
- Warmer sun, cooler sky fill and a new sun direction produce visible canopy
  shadows across the paving. Two 40-sample CPU bakes export through UV0/sRGB.
  Final corner GLB: 2,001,884 bytes; editable packed source: 5,718,856 bytes.
- Browser confirms 24 ferns in one InstancedMesh. Gameplay: 14 draw calls,
  59,318 triangles, 3 textures; static corner: 12 calls / 58,994 triangles.
  A 15-second live sample held 59.8–60.2 FPS on Iris Xe, Medium, actual DPR 1.25,
  at a 1536 × 674 CSS viewport. Earlier loading/busy samples were lower. This
  does not replace the three-minute traversal/thermal acceptance test.
- All 17 hub waypoint segments passed with 100% sampled ground contact.
  Corner walk covered 11.7 m and returned; jump rose 1.60 m and landed.
  Camera pulled to 0.41 m beside the wall and returned to 4 m in open space.
  Blocked routes, four boundary approaches and fall recovery passed. These are
  bounded smoke checks, not exhaustive collision/camera acceptance.
- Build/lint pass; browser reports no application errors (two existing dependency
  warnings). Blender's thumbnail-write warning did not prevent save/export.
- At a 390 × 844 mobile viewport the scene loads, the character is grounded and
  there is no horizontal overflow. Real-phone controls/thermals remain pending.
- Compared REF4 with `.artifacts/hub-sep09-reference.png`, and REF2/REF6 surface
  direction with `corner-sep09-final.png` and `corner-sep09-gameplay.png` in the
  same folder. Route evidence: `.artifacts/hub-routes-sep09.json`.

## September 10 — Phase 2 final production/proof session

- Replaced spear-shaped sprays with rounded overlapping leaves, shaded lower
  layers and an uneven upper crown. Broke the upper wall silhouette, baked moss
  into lower stone faces and added shallow fragments around the sample perimeter.
  Two browser iterations corrected the first pass's flat umbrella silhouette and
  moss patches that no longer followed the eroded wall tops.
- Retained 2K/1K atlases and 24 ferns in one instance batch. Corner GLB is
  1,904,484 bytes; packed editable Blender source is 5,943,158 bytes. Smooth leaf
  normals and shared per-leaf colours reduce duplicate exported vertices.
- Browser filtering is capped at the supported value up to 4x, with a 1x fallback.
  Both maps load as sRGB. Gameplay at the corner: 14 draws / 65,226 triangles;
  static camera: 12 draws / 64,902 triangles. No realtime shadows or extra atlases.
- A completed 180-second production-build keyboard traversal through the corner
  averaged 60.06 FPS from actual animation-frame timestamps on Iris Xe. All 177
  one-second observations were visible, grounded and at DPR 1.25 (Medium); viewport
  1536 × 730 CSS pixels. Counts stayed at 14 draws / 14 geometries / 3 textures.
  This is a corner performance proof, not full-world/phone thermal acceptance.
  The earlier interrupted development-server run is excluded from this result.
- Build and lint pass. All 17 route segments and the corner walk pass with 100%
  sampled grounding. Corner jump rises 1.58 m and lands; camera pulls to 0.39 m by
  the wall and returns to 4 m in open space. Four boundary approaches, the blocked
  path and fall recovery pass. These remain bounded collision checks.
- Production navigation has zero application errors; two existing dependency
  warnings remain. A 390 × 844 viewport loads without horizontal overflow. Real
  phone input and thermal checks stay deferred. Blender MCP setup was untouched;
  the private source file remains ignored and untracked, checked by metadata only.
- Evidence: `.artifacts/corner-sep10-final.png`, `corner-sep10-gameplay.png`,
  `hub-sep10-reference.png`, `hub-routes-sep10.json` and
  `corner-sep10-live-performance.json`. Compare REF4 for hub composition and
  REF2/REF6 for stone surfaces, vegetation masses and lighting.

## September 11 — recovered review/contingency session

- Replaced long paving rows with interlocking irregular cells, narrow joints and
  chipped outlines. Moss follows selected joints and has more distinct vertical
  growth at masonry bases. Removed exposed corners from selected wall/column
  courses while retaining simple collision. Two bake/browser iterations corrected
  the first pass's overly clean stone edges. No new runtime effects or atlas slots.
- Final corner GLB: 2,115,576 bytes; packed source: 5,894,001 bytes. Retained
  2K/1K sRGB atlases, up to 4x filtering, and 24 ferns in one instance batch.
  Gameplay: 14 draw calls / 67,858 triangles / 14 geometries / 3 textures.
- A 60-second production-build keyboard traversal averaged 59.75 FPS on Iris Xe,
  Medium, DPR 1.25, 1536 × 864 CSS pixels. The 59 one-second observations ranged
  from 52.18 to 61.41 FPS; all were visible, grounded and at the same DPR/counts.
  This is a local corner regression sample following September 10's three-minute
  proof, not full-world or real-phone performance acceptance.
- Build/lint pass. All 17 route segments passed with 100% sampled ground contact;
  corner walk/return, blocked route, four boundary approaches and fall recovery
  passed. Jump rose 1.60 m and landed; camera pulled to 0.49 m by the wall and
  returned to 4 m in open space. These remain bounded smoke checks.
- Production browser navigation has zero application errors and the two existing
  dependency warnings. The 390 × 844 viewport loads grounded without horizontal
  overflow; real-phone controls/thermals remain deferred. Blender saved/exported
  successfully despite its nonblocking thumbnail-write warning.
- Compared REF4 and REF2 surface direction with `.artifacts/corner-sep11-final.png`,
  `corner-sep11-gameplay.png` and `hub-sep11-reference.png`. Local diagnostics:
  `hub-routes-sep11.json` and `corner-sep11-live-performance.json` in `.artifacts/`.
- Preserved the pre-existing uncommitted `art/source/hub-blockout.blend` change;
  it is excluded from today's commits. Private material remains ignored and
  untracked, verified using Git metadata only. Blender MCP setup was untouched.

Historical next-step proposal, superseded September 12: the former hub-only plan
put reusable-kit production next. The expanded plan now begins with whole-world
layout, then shared-kit production and technical risk prototypes.

The corner is not final-quality approval or an 80% similarity claim. Largest
remaining visual gaps: paving faces still have simplified relief, moss boundaries
need more organic breakup, leaf lighting is simplified, and the lit corner meets
an undressed hub. Hub/forest dressing is now Phase C; do not multiply unresolved
material/foliage choices across the world before review.

Deployment performance issue: the user reports 60 FPS on ChatGPT Sites versus
15–30 FPS on the supplied Vercel deployment. That Vercel URL redirected automated
inspection to login; build/settings/device parity and root cause remain unverified.
Today's local result does not resolve that report.

Real-phone UX and thermal testing remain
deferred to the end. No Archive gameplay or game insertion has been built.
