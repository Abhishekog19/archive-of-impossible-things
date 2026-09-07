# September environment plan — Archive of Impossible Things

Created September 5, 2026. Target delivery: September 30, 2026, Asia/Calcutta.

## Status and authority

**Phase 0: Blender setup complete. Phase 1: IN PROGRESS (September 6).**
The user authorized scheduled production on September 6 and 7. Both daily
sessions completed; see `plans/CURRENT_PLAN.md` for evidence and remaining layout
work. Later phases do not start automatically from these dates.

This plan changes the immediate execution order of build-roadmap.md. That roadmap
continues to describe the eventual three-archive game and portfolio reveal; this
document owns the September environment milestone. Existing M2 phone controls work
according to user feedback, but portrait play feels crowded. Phone redesign and
full-environment phone validation are deferred by user instruction.

## September 30 deliverable

A polished, desktop-playable **central crossroads hub inspired by concept/REF4.png**,
with a third-person character, reliable collision/camera behaviour, and a short
canopy approach. The player enters the website and freely explores the authored
area. Fun movement and curiosity remain the objective; there is no archive game,
exposition, or portfolio reveal in this milestone.

Committed content:

- One circular limestone plaza, ruined columns/walls, uneven terrain and a distant
  tower landmark. Provisional plaza diameter: 24–30 m; settle scale in Phase 1.
- Three visibly different path mouths: one open, one overgrown, one interrupted
  by a gap. The blocked branches communicate the future world; they are not
  secretly complete playable levels.
- One 30–50 m canopy approach or exploration spur, with a safe return route.
- Dense-looking forest framing, selected roots, moss, ferns and rubble clusters.
- Existing character/controller integrated into the environment, coherent visual
  presentation, contact grounding and idle/walk/run/jump behaviour.
- Baked static lighting, controlled materials and atmosphere, a minimal settings
  interface and optional performance HUD.
- Browser verification, comparison screenshots and a documented build handoff.

Stretch only after all acceptance gates pass: a small water detail or one distant
archive facade. **Three archive interiors, the full connecting road network, the
Deep Archive, progression and final character customization are outside September.**
The wider roamable world remains the next expansion after this benchmark.

## Time budget and working agreement

User availability: about one hour daily plus longer weekend sessions. Schedule
assumption: **1 hour per weekday and 3 hours per weekend day**, September 6–30:
18 weekday hours + 21 weekend hours = **39 hours**. An optional fourth weekend hour
is contingency, not capacity already promised to another feature.

These are shared working/review windows, not a claim that every asset can be
authored manually in 39 hours. Scripts and agent-assisted production run within
explicitly started sessions; unattended work between sessions is not assumed.
No time estimate guarantees reference quality. At the Phase 2 gate we must decide
whether the kit and lighting pipeline support this deadline at the desired quality.

Weekday rhythm: 10 minutes inspect the last result, 40 minutes for one bounded
change, 10 minutes record evidence and the next action. Weekend rhythm: 30 minutes
review, 2 hours production/iteration, 30 minutes export and browser verification.

Log actual time per phase. A missed gate consumes its allocated time; it does not
silently move every later date. Cut the listed scope or explicitly revise the target.

## Phases and fixed gates

| Phase | Dates | Session cap | Deliverable | Exit gate |
|---|---|---:|---|---|
| 0 — Tooling | Sep 5 | Setup only | Blender runner, empty metric template, disposable render/export test | Background Python, CPU render and GLB round-trip pass |
| 1 — Layout and scale | Sep 6–8 | 5 h | Hub/path blockout in Blender and browser; landmarks/tree masses; reference and gameplay cameras | Walk every intended route; plaza/paths/tower read like REF4; no detailed assets yet |
| 2 — Material and lighting proof | Sep 9–11 | 3 h | One representative finished corner: paving, wall, tree/root, foliage; UV/bake/export/browser proof | Browser appearance is recognizably related to the reference; no missing maps; capture actual draw/triangle/FPS costs |
| 3 — Reusable asset kit | Sep 12–16 | 9 h | Small coherent stone/terrain/vegetation kit, shared textures, export conventions, simple colliders | Variants survive export and repeat without obvious uniformity; no sprawling asset library |
| 4 — Hub composition | Sep 17–21 | 9 h | Dressed hub, three branch mouths, tower framing and canopy approach | Whole committed area is traversable; scenery reads from gameplay viewpoints, not just the reference camera |
| 5 — Traversal and atmosphere | Sep 22–25 | 4 h | Camera/stair fixes, character grounding, coherent light/shade, restrained wind/fog; optional basic ambience | No falls through surfaces, persistent clipping, stuck movement or missing return route |
| 6 — Acceptance and delivery candidate | Sep 26–28 | 7 h | Performance pass, visual comparison, release candidate and reproducible handoff | Desktop acceptance below passes; no new content after Sep 28 |
| 7 — Contingency | Sep 29–30 | 2 h | Fix blockers and finalize the environment build | Final verification; honest remaining-issues list; deliver Sep 30 |

Dates assume Phase 1 begins September 6. If production starts later, reduce scope
at the start; do not compress verification or pretend the lost days still exist.

## Visual production rules

Primary composition: REF4. Stone/water surfaces: REF1, REF2, REF11. Root and masonry
relationships: REF3 and REF7. Canopy depth and dapple: REF5 and REF6. REF8/REF9 inform
material consistency, not extra rooms. REF10 is reserved for later expansion.
REF's neon and photoreal panels are anti-goals. Similarity percentages in the context
snapshot are aspirations; acceptance uses concrete comparisons, not a fabricated score.

Build silhouette first, edge/joint detail second, fine texture last. Use geometry
for features that change silhouette or create meaningful depth; bake or texture
small cracks, grain and colour breakup. Give moss ecological placement (joints,
shaded bases, water-adjacent areas), not uniform green noise. Keep walkable collision
smoother than decorative paving.

Start with 4–6 slab variants, 3–4 masonry variants, 2–3 arch/column pieces, 3 tree
silhouettes and 3–4 ground-cover families. These are caps for the first kit, not a
requirement to make every possible combination. Recolour and simplify licensed
source vegetation if it meets the look; verify each asset's actual licence.

Blender authors editable assets, UVs, placement and static light bakes. R3F handles
loading, camera, animation, fog, wind/water effects and interaction. Do not assume
Blender nodes, fog, lights or collection instances export unchanged to glTF.
Prove actual browser instancing and lightmap binding during Phase 2. MeshBasicMaterial
does not use normal-map lighting; bake relief appearance or explicitly choose another
material. Keep static baked architecture separate from reusable instanced vegetation.

Retain a reference camera for image comparison and a gameplay camera for traversal.
Judge primary silhouettes, route visibility, tree masses, warm/cool separation,
material scale and distant haze. Do not force the elevated concept viewpoint into
third-person controls. The distant tower may need a simplified backdrop treatment
separate from the nearby fog/culling setup; prove its visibility without loading a
playable distant landscape.

## Deadline protection

- Sep 8: if the hub does not read correctly, simplify route lengths and terrain.
  Do not add detail to hide a composition problem.
- Sep 11: if baking/UV transfer consumes the cap, compare a simpler full-colour
  bake or vertex-colour treatment in-browser. Accept a fallback only if its visual
  result is good enough; otherwise explicitly revise scope/date before mass production.
- Sep 16: if the kit is late, reduce asset families and reuse good variants. Preserve
  important silhouettes and material consistency.
- Sep 21: freeze the hub footprint. Cut the approach toward 30 m and remove stretch
  water/facade work before reducing dressing quality around the main plaza.
- Sep 25: remove optional effects if needed. Keep collision, stable camera and
  character grounding. Fix traversability before polish.
- Sep 28: content freeze. Sep 29–30 are only for blockers and delivery.

## Desktop acceptance

- Enter from the website and roam the entire committed area with the character.
- All accessible routes have working collision and a safe return; the blocked
  branches are intentional. No persistent camera embedding or unintended soft-locks.
- Compare REF4 and the reference camera capture, then review at least four gameplay
  angles. Plaza, paths, tower and tree masses remain readable. No neon or photoreal
  material drift; moss, stone and foliage scales agree.
- Target 60 FPS on the actual Iris Xe at baseline DPR 1.25. Log a three-minute
  desktop traversal with representative views; a stepped/synthetic FPS is not evidence.
- Fewer than 150 draw calls, preferably fewer than 100; approximately 300K visible
  triangles maximum. Keep total costs visible during production, not only at Phase 6.
- Standard textures around 1K, selective 2K hero textures; choose atlas count and
  texel density from the benchmark. No giant 1K atlas stretched over the whole world.
- Prefer no realtime shadows; keep postprocessing minimal. Target initial-to-playable
  transfer at or below the existing 8 MB budget. Measure the actual delivered assets.
- Build/lint pass, no application errors, and no growing geometry/texture counts
  over repeated mount/unmount or scene entry/exit checks where applicable.
- Phone UX and real-phone thermal acceptance remain pending; desktop completion
  must not be described as full-device completion.

## Actuals log

| Phase | Actual working/review time | Result |
|---|---|---|
| 0 | Not timed; do not invent hours | Blender 5.2.1 LTS setup verified |
| 1 | September 6–7 sessions not time-tracked | Blockout plus terrain/forest/ruin composition and connected route checks complete; September 8 layout gate remains open |
| 2–7 | Not started | Await completion of preceding gates |
