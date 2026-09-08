# Current plan — Archive of Impossible Things

Status: Phase 1 production/checks complete. Phase 2 first session completed early
on September 8 at the user's request; material/lighting benchmark ready for review.
Target: September 30, 2026; about one hour daily plus
longer weekend sessions. Recheck remaining capacity when production begins.

Scope and dated time caps: [September plan](../environment-september-plan.md).
Visual target: [look target](../look-target.md), primary concept `concept/REF4.png`.
Pipeline conventions: [art pipeline](../art-pipeline.md). Its historical MCP status
is outdated: Blender MCP is installed and working; no setup changes are needed.
This milestone takes priority over the older full-game roadmap.

| Step | Completion evidence |
|---|---|
| 1. Hub blockout | Plaza, three path mouths, tower and short canopy approach have readable scale and traversable routes. |
| 2. Camera/composition | Matched reference screenshot establishes plaza/path/tree/landmark proportions; gameplay camera reads clearly. |
| 3. Art/detail pass | Terrain/ruins → vegetation → materials → lighting/fog → detail; fix the largest 3–5 visual mismatches per iteration. |
| 4. Optimization/export | Reusable assets and simple colliders export to GLB; textures, draw calls and visible geometry meet existing budgets. |
| 5. R3F loading | Browser loads GLB with correct scale, materials and lighting; representative export is proven early. |
| 6. Rapier + ecctrl roaming | Existing character moves across all intended routes; grounding, slopes, stairs and camera collision work. |
| 7. Browser/mobile testing | Reference-versus-screenshot review, build/lint and measured Iris Xe traversal pass; mobile viewport checks, then user-led real-phone control/thermal verification at the end. |

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

Next work: finish the Phase 2 visual proof before kit production. Improve masonry
breaks/moss placement, layered canopy volume, warm/cool contrast and dappled shadows;
review JPEG/UV softness at player distance. The rectangular sample edge is temporary
and will be blended into the dressed hub during composition. Prove reusable
vegetation instancing separately; this static merged benchmark does not prove it.
Phase 2 retains its three-session cap (originally September 9–11); the first session
was brought forward, not added to capacity. Final visual quality is not approved,
and the approximate 80% reference target has not been reached.

Real-phone UX and thermal testing remain
deferred to the end. No Archive gameplay or game insertion has been built.
