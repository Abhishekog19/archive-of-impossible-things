# Connected environment production plan

Revised September 28, 2026 (Asia/Calcutta): numbered production days; target two to
three production packages per working day. Filename retained for existing links.
This replaces the September 30 hub-only scope and future phase dates. Completed
production evidence remains in `plans/CURRENT_PLAN.md`.

## Required outcome

One complete connected environment covering all six references:

| Reference | Required area |
|---|---|
| REF4 | Central crossroads hub, ruined plaza and tower landmark |
| REF5 | Forest approach with paving, tall trees and woodland shoulders |
| REF6 | Deeper enclosed canopy, ruins and sunlight shafts |
| REF7 | Archive exterior with authored facade, giant tree and wrapping roots |
| REF8 | Enterable archive hall with arches, columns, broken roof and vegetation |
| REF10 | Deep Archive cavern with rock walls, pool, shoreline and overhead opening |

Proposed route: hub → forest approach → deeper canopy → archive exterior → interior
→ descending connection → cavern, with return connections. Set scale and branches
during blockout. Background vistas can use simplified geometry; intended accessible
spaces must be authored. Reserve four candidate game locations without building games.

Completion includes models, textures/materials, vegetation, water appearance,
lighting/fog, connecting spaces, GLB exports, R3F loading, optimization and visual
review of every area. No placeholder surfaces or deferred environment-art passes
in the delivery candidate. Character art/animation, third-person movement, Rapier/
ecctrl physics, camera polish and desktop roaming acceptance are INCLUDED before
handoff. Only game insertion and phone-control redesign/testing remain afterward.
Use the existing controller during environment production; author usable stairs,
slopes, clearances and separate collision proxies now to avoid remodeling.

## Production-day schedule and throughput

A production day (PD) is a deliverable package, not a calendar date or a fixed-hour
unit. Target **2–3 PD packages per active working day**, completing dependencies
in order. The prior 3-hour weekday / 9-hour weekend assumptions and October 4
calendar promise are superseded. Do not multiply the old schedule by three again
or claim a package complete simply because its time allowance has elapsed.

There are 11 packages including the current former-September-27 package. After
PD06 implementation, five full packages plus PD05/06 visual reviews remain:
a planning range of **2–3 further active working days**
at 2–3 packages per day. Allow 1–2 additional working days if hero art, animation,
baking or technical fixes overrun. This is a throughput goal, not measured speed.
Sessions begin on the user's request; no unattended work or automation is implied.

| Production day | Work and completion checkpoint |
|---|---|
| PD01 — former Sep 27 | Hub/forest backdrop and material/light closure pass; one scheduled weekly technical review; first REF7 facade and hero tree/root production. Completed production/review checkpoint; final visual acceptance remains PD11. |
| PD02 — complete Sep 27 | REF7 damaged silhouette, courtyard paving/rubble, facade moss/ivy, tree/root refinement and placed lighting. Shared REF7/8 surface helpers begun; hall art follows in PD03. Build, reference/player comparison and walking connection pass. |
| PD03 — complete Sep 27 | REF8 hall arcades, fluted columns, broken roof, planted paving, ivy and rear windows/portal. Exterior–hall–reserved space–descent connection, build/lint and reference/player review pass. |
| PD04 — complete | REF10 chamber, fractured walls, shoreline, overhead opening and descent built; final build/lint and full shore-loop connection pass. Final shoreline comparison closed using the user's screenshot; automated browser access remains restricted. Structural checkpoint only; materials/light and final art acceptance remain ahead. |
| PD05 — built, visual review pending | Metre-scaled 1024px stone colour/normal/roughness, wet shoreline layering and connected reflective water. Build/lint and unchanged collision check pass. Explicit local-preview authorization is required after automatic approval rejection; prove sharpness, shader correctness and water/shore appearance before closing. |
| PD06 — built, visual review pending | Authored oculus, bounded overhead lighting, soft shaft, connected descent fog/ambient transition and aligned opening reflection. Build/lint, transition check and unchanged collision check pass; combined PD05/06 reference/player review still awaits local-browser permission. |
| PD07 | Finish all connections and six-area material/light consistency; loading/culling, GLB/texture/geometry optimization. Resolve recorded visual and weekly technical findings. |
| PD08 | Replace capsule presentation with a coherent stylized character, rig and idle/walk/run/jump/land animation states; Blender/GLB/R3F pipeline. Use an authored simple explorer or suitably licensed rig, with provenance retained. |
| PD09 | Finish desktop movement and Rapier/ecctrl physics: acceleration/deceleration, turn response, grounded jumps, steps/slopes, collisions, fall recovery and pause/resume. Verify all six areas and four future game locations are reachable. |
| PD10 | Character/animation polish, foot placement and grounding, camera smoothing/collision/occlusion, near-wall character visibility, input/settings clarity and transitions. No phone-control redesign or gameplay. |
| PD11 | Final six-reference review, complete desktop roam, character/physics/camera acceptance, scalable graphics/mobile layout and release. Reuse weekly evidence if unchanged; recheck affected failures. Only game insertion and phone controls remain. |

Suggested working-day batches after closing PD05/06 review: PD07–08; PD09–10; PD11.
Merge adjacent batches toward three working days only if preceding gates pass. Keep checkpoints visible rather
than forcing an unfinished package into the next package's completion claim.

## Daily building and weekly technical review

Daily: build → quick affected-area reference/player comparison and movement check
→ continue building. Allow about 5–10 minutes for routine daily review. Before a
runtime/assets push, run one production build and lint changed JavaScript once;
reuse results until inputs change. Documentation-only edits need no game tests.

Batch routine FPS, sustained traversal, repeated route/loading/resource checks,
tier/mobile matrices and deployment parity once weekly: **once per seven calendar days**, independent of how many PD packages are completed.
PD01 completed the former September 27 review on September 26; next routine
batch October 3 if the project is still active. PD11 reuses valid evidence and checks changed risks. Reserve 45–60 minutes within the existing
session, not an additional test day. Recheck failures only. Fix an observed crash,
failed load or blocked route immediately with a targeted check. Do not turn that
into another broad technical audit. The detailed operating rule is in
`plans/CURRENT_PLAN.md`; prior daily test records are historical evidence.

## Speed-up strategy

- Assemble the full rough world before detailed art, revealing spatial problems early.
- Share one limestone/ruin library across hub, forest and archive. REF5/6 share
  vegetation; REF7/8 share architecture. Give the cavern a small rock/water family.
- Start with 4–6 slab variants, 3–4 masonry variants, 2–3 arch/column modules,
  three tree silhouettes and 3–4 ground-cover families. Expand for visible need only.
- Script scattering, controlled variation, baking and export; hand-direct hero
  compositions, roots, route readability and meaningful vegetation placement.
- Review complete area passes and fix the biggest 3–5 mismatches per iteration.
  Avoid repeatedly polishing a tiny corner while required areas remain unbuilt.
- Prove water/light transfer and zone loading early. Batch visual decisions within
  the increased availability above. Extra workers and purchased assets are not assumed.

## Acceptance and performance

- Stylized natural ruins/forest; no neon, futuristic machinery or photoreal drift.
  Each area uses its own reference, with REF4 governing the hub. Judge the roughly
  80% aspiration through concrete comparisons, never an invented numerical score.
- Fixed reference views plus multiple player-height views per area must show
  convincing silhouettes, material scale, foliage masses, light and depth.
- Blender → GLB → R3F; editable source retained. Bake/recreate unsupported effects,
  separate decorative meshes from simple collision proxies, and verify browser output.
- Use shared assets, instancing, zone loading/culling and detail levels. Most textures
  near 1K, selective 2K; avoid one low-resolution atlas across the entire world.
- Target 60 FPS on Iris Xe at DPR 1.25. During the weekly technical batch, measure
  actual frames for at least three minutes across representative areas/transitions. Under 150 draw calls (preferably
  under 100) and about 300K visible triangles per view remain working budgets.
- Aim for initial-to-inspectable transfer within the existing 8 MB target using
  staged loading. Measure actual payload; total world download is a separate metric.
  Do not claim the existing build already meets the load budget.
- Build/lint and browser checks pass; no application errors or growing resource
  counts after repeated zone transitions. Verify intended deployment build/settings
  parity; the user's Vercel slowdown remains unresolved.
- Browser/mobile layout and scalable graphics are included. Real-phone thermals,
  and phone controls remain later and must be labeled pending. Desktop character,
  movement, physics and camera acceptance must pass before this milestone closes.

## Current state and next action

PD01–PD04 are complete as production checkpoints. PD01 covered hub/forest
backdrop, terrain colour/depth, first REF7 art and the weekly technical review.
PD02 finished the exterior stonework, planted courtyard, ivy, roots and placed
lighting. Its production build, reference/player comparison and ten-waypoint
courtyard-to-hall connection pass. PD03 adds the REF8 hall arcades, broken roof,
planted floor and rear portal/windows; its build/lint, reference/player comparison
and 13-waypoint hall/descent route pass. PD04 adds cavern structure and matching
wall/passage collision; the 21-waypoint shore/descent route passes, and the user's
screenshot closes the final shoreline comparison. No routine FPS review was repeated.
Counts, comparison evidence and review limitations are in plans/CURRENT_PLAN.md.

PD05 materials/water and PD06 overhead light/fog are implemented September 28;
their focused browser visual checkpoints remain pending explicit local-preview
authorization. Five full packages plus those reviews remain.
Next: close the combined cavern comparison, then PD07 six-area consistency/optimization.
PD07 must close remaining hub boundaries/landmark/foliage and material/light gaps,
reduce the sampled ~566K triangle peak and replace eager ~53.5 MB GLB loading
with staged placed-art loading. The sampled 59.05 average FPS is not final
performance acceptance: low-percentile spikes and transfer/geometry budgets remain
open. Vercel build parity is unverified because the public URL redirects to login.
PD11 requires final six-reference and roaming acceptance, with no art placeholders.

Character art/animation, movement/physics and camera polish are included in PD08–11.
Only game insertion and phone controls follow handoff. Preserve the user's existing
hub-blockout.blend edit, private-file exclusion and Blender MCP setup. Older records
in CURRENT_PLAN.md retain historical dates/scope and do not override this PD plan.
