# Current plan — Archive of Impossible Things

Status: Phase 1 in progress; September 7 terrain/composition session complete.
Final layout review is September 8.
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

Next session (September 8): final Phase 1 layout review. Compare reference and
gameplay views with the user, settle plaza/approach scale, and address any route
readability issues. Main remaining visual mismatches belong to later art work:
untextured paving, crude foliage masses, plain tower silhouette, uniform surface
lighting, and missing canopy shadows. Phase 2 starts with one representative
finished corner to prove stone, vegetation, materials and lighting in-browser.

Keep material/bake proof for Phase 2. Real-phone UX and thermal testing remain
deferred to the end. No Archive gameplay or game insertion has been built.
