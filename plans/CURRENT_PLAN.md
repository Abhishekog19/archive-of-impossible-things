# Current plan — Archive of Impossible Things

Status (revised September 12): complete connected environment scope now covers
REF4/5/6/7/8/10. The September 30 deadline and former future phase dates are superseded.
Expected finish: October 25, 2026; planning range October 18–November 1, assuming
one hour per weekday and three hours per weekend day. Reforecast September 22.
Phase A (September 12–15) is underway: its first and second layout sessions were
both performed September 12 at the user's request. The second session was brought
forward from September 13. Next: review transitions, boundaries and six-area
composition to close the layout gate. Phase A visual approval remains open.
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
| 7. Browser/mobile testing | Reference-versus-screenshot review, build/lint and measured Iris Xe traversal pass; mobile viewport checks, then user-led real-phone control/thermal verification at the end. |

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
