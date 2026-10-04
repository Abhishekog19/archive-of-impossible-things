# World audit correction phases

Tracks production against [the October 3 audit](WORLD_AUDIT_2026-10-03.md).
An implemented correction is not whole-world visual acceptance.

## Phase 1 — visible structure and connections — in progress

### First batch: archive hall and portal continuity, October 3

- **I02, main arch separation: corrected in the inspected REF8 view.** Closed
  radial joints, added recessed continuous arch cores, and extended nave/portal
  piers to meet their springlines. Rebuilt and baked the editable hall source and
  exported the runtime GLB/package.
- **I01, light seams: partial.** Added recessed sidewall and lower rear-wall
  masonry cores plus buried entrance footings. The inspected entrance footing
  no longer shows the bright ground slit. Small upper masonry seams, the opposite
  entrance return, and additional oblique views still need acceptance checks.
- **E06, missing portal destination: loading correction implemented.** Courtyard
  and hall sightlines now require the hall and cavern packages before the loading
  gate releases. The exterior player view shows the hall/descent consistently.
  Overall portal appearance remains tied to I05.
- **I05/V01, descent: partial structural study only.** Lifted the visible upper
  vault and added four connected rock seams. The unchanged ramp remains walkable,
  but the REF8 view still reads as a grey portal surface with a bright far opening;
  the reverse view retains straight floor/wall joins. Do not close these issues.

Verification:

- Compared REF8 with matching 1280 × 720 before/after reference captures, plus
  courtyard player, entrance-side and reverse passage views.
- Actual ecctrl/Rapier cavern return check: three destinations passed (0.10–0.21 m
  final errors); uphill jump passed with 0.99 m rise and airborne state.
- Resident package is byte-for-byte identical before/after (SHA-256
  `2ce0c8af2e12d495bc230b52eeaf2fa34951b1abbd4f380fc6192c5d3965273a`).
- Six placed-world tests pass, including a new cold-entry portal dependency test;
  changed JavaScript lint and production build pass. Retrieved reverse-view
  console sample contains no error entries.
- Temporary inspection cameras were restored byte-for-byte. Existing modified
  `hub-blockout.blend` was preserved. Private file checked by Git metadata only:
  ignored and untracked. This batch was subsequently committed and pushed in
  the separate groups recorded below.

Local evidence in `.artifacts/world-audit-oct03/`:
`hall-phase1-before.png`, `hall-phase1-after.png`, `exterior-phase1-after.png`,
`entrance-seam-phase1-after.png`, `descent-phase1-after.png`, and
`phase1-cavern-return.txt`. Generator, package, test and build logs are in
`.artifacts/blender/audit-*.log`. Ignored evidence is local to this checkout.

Largest remaining differences in the inspected hall: padded/repetitive stone
profiles, shallow portal depth cues, pale blank window surroundings, and flat
plant silhouettes. Keep material and foliage acceptance open.

### Next structural batches

1. H01/H02/F01: hub perimeter blockouts, reverse arrival composition, connector
   bank ends. Compare REF4/REF5 plus player-height reverse/side views.
2. C01/E01/E02: tree/ruin intersection, connected facade roots, forest/courtyard
   ground transition. Compare REF6/REF7 plus affected route checks.
3. Finish I01/I05/V01 and E06 appearance: seal remaining joins, author a legible
   descent threshold and natural rock-to-floor transitions. Keep existing routes.

## Phase 2 — representative materials — study implemented, acceptance open

The user requested advancing to this phase and pushing systematically on October
3. Phase 1's remaining items above stay open; moving ahead does not close them.

The forest connector now provides the representative stone/bark/ground study for
F03/F04/X02 and static root/plant contact under X01:

- Metre-scaled limestone variation and two-scale irregular moss, directional bark,
  soil/moss variation, and short-distance contact/relief are baked in Blender.
- Stone, wood and ground export as distinct meshes sharing the original 2048px
  atlas. This fixes the prior merged `ForestPatch_Baked` mesh's inability to receive
  family-specific runtime detail. The legacy patch component also uses the new
  mesh contract.
- Only this patch receives the new close-range mineral pores and broken bark
  fissures. Detail fades with distance and uses derivatives for antialiasing;
  no additional texture or render pass was introduced. Roughness/relief here are
  baked appearance, not a new realtime PBR material or character-contact fix.
- Added repeatable `view=material-stone` and `view=material-bark` cameras, plus
  the development-only “Check forest connector” route button.

Comparison: the 1280 × 720 connector before/after and close views were compared
with REF5. Stone is cooler, bark direction clearer, and root contact/soil more
distinct. Close surfaces still have soft broad colour, roots retain local dark
seams, and paving has thin/open edge joins. Adjacent blockouts, background depth
and polygonal plants remain. Do not propagate or declare full visual acceptance
until the remaining geometry and material response are reviewed together.

Validation: six placed-world checks pass (including the shared-atlas/new-node
contract); changed JavaScript lint and final production build pass. The actual
connector route passes at its middle, far end and return (0.10, 0.08, 0.30 m
destination errors). Retrieved browser error samples are empty. Resident collision
retains the SHA-256 above. Source geometry remains 81,506 triangles; the existing
wood simplifier now recognizes its separate family and derives 69,612 runtime
triangles. Package size is 1,722,608 bytes. These are asset counts, not FPS results.

Local evidence: `.artifacts/material-study-oct03/01-connector-before.png`,
`02-connector-after.png`, `03-bark-close.png`, `04-stone-close.png`, and
`connector-route.txt`. Logs: `.artifacts/blender/phase2-*.log`.

Next: resolve the recorded structural joins and root attachments before material
propagation, then continue terrain/vegetation and lighting acceptance.

## Phase 3 — terrain, roots and vegetation — connector batch implemented

October 3, at the user's request to continue to the next phase:

- Replaced eight connector wall blockouts with baked stone courses on their
  original footprints, with embedded rubble and low plants at their bases.
- Fitted the four patch trees' low root vertices to the sloping terrain. Removed
  the covered khaki road skin beneath the existing earth/paving replacement.
- Folded fern, broadleaf and shrub faces, reduced oversized ground plants and
  added shoulder/base clusters: 128 ground-cover instances in the patch.
- Added repeatable `connector-side` and `connector-reverse` comparison cameras.

Compared the matching 1280 × 720 before/after and side/reverse captures with REF5.
The local wall blockouts and exposed road border are replaced, with denser low
planting. **Phase 3 acceptance remains open:** the outer banks still have broad
bare facets, crowns repeat and flatten, background depth is weak, and root/paving
joins retain dark seams. Column ivy remains flat. This batch does not finish
bank reshaping, canopy production or facade root attachments elsewhere.

Validation: actual ecctrl/Rapier connector middle, far end and return pass with
0.02, 0.20 and 0.17 m destination errors. Six placed-world tests and the production
build pass. Resident visuals changed, but its 21,189 collision triangles match
the pre-audit baseline after world transforms (canonical coordinates rounded to
five decimals; SHA-256 `f999ff671c6c896c8768b12f0a50222a6032d5b7f24b9eceff6c6c64d9c1e123`).
The existing source-boundary collision test also passes. Patch runtime geometry
is 77,276 triangles and 1,970,876 bytes, still using the shared 2K atlas. These are
asset counts, not FPS results; broad performance checks stay in the weekly batch.

Local evidence: `.artifacts/phase3-connector-oct03/01-before.png`, `02-after.png`,
`03-side.png`, `04-reverse.png`, `connector-route.txt`, and `collision.json`.
Generator/package/test/build logs: `.artifacts/blender/phase3-*.log`.

Next Phase 3 batch: connector bank silhouettes and ends, root/paving seams, then
crown variation and depth before treating lighting as the remaining difference.

## Phase 4 — lighting and water — production complete

### October 4 completion pass

The user requested finishing the phase rather than another partial study.
Lighting, water and contact production is complete. Runtime work is pushed in
`50661ce`, with index-buffer reuse corrected in `54ecfb5`. Asset and documentation
groups are recorded below. This closes the Phase 4 implementation scope; overall
reference acceptance and earlier phases' geometry corrections remain open.

- **Outdoor contrast/depth:** continuous world-space colour grading retains the
  original baked light, cools woodland shade and sheltered hall sides, and warms
  three canopy openings. The same field affects instanced plants and the player.
  Hub/courtyard/hall fog now spans 32–145 m; forest fog blends to 22–115 m with a
  greener background. Fog and background remain the same colour.
- **Canopy light:** two bounded, soft shafts align with the ground light field.
  They disappear on Low, with fog disabled, and beyond their short draw range.
- **Player contact:** one 32-triangle receiver follows the collision terrain and
  visible paving height, clips at ledges/steps and fades during jumps. It reuses
  its index buffer. No shadow map, screen-space pass or texture is introduced.
- **Static prop contact:** 0.32 m contact occlusion is baked into the
  existing forest approach, canopy, archive exterior and hall atlases. The hub
  and connector retain their existing baked contact. No atlas resolution increase.
- **Cavern/water:** retained the earlier sharper reflections, quieter ripples,
  wet-shore response and focused skylight; repositioned the existing fill as
  pool bounce so the near shore is readable. Reflection resolutions remain
  384/512, with no reflection target on Low.

Runtime validation: eight focused tests and changed-file lint pass, including
shader-hook composition, resource disposal, contact slope/ledge/jump behaviour
and index-buffer reuse. The connected route passes all 19 checkpoints plus fall
recovery. Six-area contact checks pass; jump opacity falls from 0.42 to 0.16 and
returns to 0.42 on landing. Low contact rendering was inspected and the original
Medium preference restored. Final eight tests and production build pass after
asset preparation and the buffer fix; the final browser error sample is empty.

Final asset validation: all eight runtime packages retain the baseline canonical
world-space triangle fingerprints (coordinates rounded to four decimals),
including collision. The selective release-finishing pass preserves existing
forest/canopy/exterior detail after rebaking. Reproduce it after the base bakes
with `node scripts/blender/run.cjs release-finish --assets forest-approach,forest-canopy,archive-exterior`,
then `npm run prepare:world`. Total derived package size is 27,402,540 bytes,
down from 27,897,820; atlas sizes and triangle counts are unchanged. These are
asset measurements, not hardware/FPS results.

Visual comparison: matching 1280 × 720 forest, canopy, exterior and hall views
were checked against the saved pre-bake captures and REF5/6/7/8. Contact is
slightly stronger at bases and joins without broadly crushing the lit stone.
The runtime pass separates cool shaded areas from warm openings; REF10 cavern
and shore/player comparisons retain clearer reflected silhouettes and a readable
near shore. The contact rebake is a subtle grounding correction. Broad bare
banks, flat/repeated foliage, detached facade roots, the grey descent threshold
and regular cavern rock/shore geometry remain visible differences to resolve in
the earlier production scopes and Phase 5 comparisons. No similarity score or
whole-world acceptance is claimed.

Local evidence: `.artifacts/phase4-completion-oct04/` contains reference/player
captures, `contact-check.txt`, `connected-route.txt`, bake/test/build logs and
geometry fingerprints. Final asset captures are `forest-after.png`,
`canopy-after.png`, `exterior-after.png` and `hall-after.png`; runtime evidence
includes `hub-after.png`, `cavern-after.png`, `cavern-shore-after.png`,
`contact-canopy.png` and `low-contact.png`. These ignored files are local to this
checkout. The original modified hub Blender file remains unchanged by this work.

### First cavern study (historical)

October 4: advanced at the user's request. Earlier phases' remaining geometry,
material and vegetation corrections stay open.

- V06: reduced broad fill, concentrated the skylight and its shaft, and moved
  the fog transition farther away. Retained enough hemisphere light for the
  near shore after checking the first darker iteration at player height.
- V05: reduced water distortion and removed the extra five-tap blur. The existing
  bilinear-filtered 384/512 reflection targets and one reflection pass are retained;
  low quality still uses the existing analytic opening fallback without a target.
- V03/V04 contact study: narrowed and softened wet-stone darkening and adjusted
  shallow-water colour. No shoreline geometry or collision edits. The regular
  kerb silhouette and dark plate edges remain unresolved.
- Added `view=cavern-shore` for repeatable player-height water inspection.

Compared REF10 against matching 1280 × 720 medium-quality before/after captures,
plus shore and player views. Reflected silhouettes are clearer and the far shore
is more strongly focused under the opening. Repeated wedge forms, noisy surfaces,
the regular shoreline and near-shore darkness remain larger mismatches. V05/V06
were improved studies at this point; the completion pass above subsequently
implemented outdoor canopy lighting and cross-world character/prop contact.

Validation: changed-file ESLint and final production build pass. Actual cavern
ascent, archive return and slope approach pass (0.28, 0.24, 0.25 m errors); uphill
jump rises 1.07 m with airborne state. Low-quality fallback was visually checked,
then the original medium preference restored. This is not a hardware/FPS audit.
No GLB/source/collision package changed; the existing hub Blender edit was excluded.

Local evidence: `.artifacts/phase4-cavern-oct04/01-before.png`, `02-after.png`,
`03-shore.png`, `04-low-fallback.png`, `05-player.png`, `cavern-return.txt`, and
`build.log`. Images show the final study except the explicitly labelled baseline.
The evidence directory is ignored and local to this checkout.

## Phase 5 — focused comparison and acceptance — pending

Compare the largest 3–5 remaining mismatches per iteration. Keep character
acceptance separate. Hardware, sustained performance, deployment and mobile
regression remain in the weekly batch, not per-art-change checks.

## Push groups — approved GitHub origin/main

1. `498b965` — portal destination loading and regression check; pushed separately.
2. `35dfc22` — hall/descent generators, editable sources and exports; pushed separately.
3. `051202a` — representative connector material study, assets and review controls;
   pushed separately.
4. `c8dfe44` — close-view pore distribution and subpixel filtering correction;
   separate push after visual comparison and rebuilt production bundle.
5. `e4108ae` — audit register, phase tracker and current-plan update; pushed separately.
6. `5a30495` — Phase 3 connector generator, editable source, exports and comparison
   cameras; pushed separately.
7. `ee88193` — Phase 3 evidence and remaining-work documentation; pushed separately.
8. `2715072` — Phase 4 cavern lighting/water runtime changes and shore review
   camera; pushed separately.
9. `72b3fc9` — first Phase 4 evidence notes; pushed separately.
10. `50661ce` — regional light, canopy shafts, player contact and review checks;
    pushed separately.
11. `54ecfb5` — reuse the player contact index buffer and verify reuse;
    pushed separately.
12. `61360ac` — forest/archive contact bakes, editable sources, derived packages
    and selective finishing workflow; pushed separately.
13. Phase 4 completion evidence, look target and current-plan update;
    separate documentation push after the verified runtime and asset groups.

The pre-existing modified `art/source/hub-blockout.blend` is excluded from these
commits. Private source material remains ignored/untracked and was not read.
