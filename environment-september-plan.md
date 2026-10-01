# Connected environment production plan

Revised October 1, 2026 (Asia/Calcutta): numbered production days; target two to
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

There are 11 packages including the former-September-27 package. PD08 was reopened
after the user rejected its character, then parked September 30 to finish PD09.
PD09 and PD10 functional movement/presentation are implemented and checked on the
temporary gameplay explorer. PD08 redesign and PD11 acceptance remain,
together with recorded environment corrections. The previous
1–2 active-day forecast is withdrawn; re-estimate after the model and one-panel
secondary-motion proof in plans/CHARACTER_REDESIGN.md. Throughput is a goal, not
permission to skip visual acceptance.
Sessions begin on the user's request; no unattended work or automation is implied.

| Production day | Work and completion checkpoint |
|---|---|
| PD01 — former Sep 27 | Hub/forest backdrop and material/light closure pass; one scheduled weekly technical review; first REF7 facade and hero tree/root production. Completed production/review checkpoint; final visual acceptance remains PD11. |
| PD02 — complete Sep 27 | REF7 damaged silhouette, courtyard paving/rubble, facade moss/ivy, tree/root refinement and placed lighting. Shared REF7/8 surface helpers begun; hall art follows in PD03. Build, reference/player comparison and walking connection pass. |
| PD03 — complete Sep 27 | REF8 hall arcades, fluted columns, broken roof, planted paving, ivy and rear windows/portal. Exterior–hall–reserved space–descent connection, build/lint and reference/player review pass. |
| PD04 — complete | REF10 chamber, fractured walls, shoreline, overhead opening and descent built; final build/lint and full shore-loop connection pass. Final shoreline comparison closed using the user's screenshot; automated browser access remains restricted. Structural checkpoint only; materials/light and final art acceptance remain ahead. |
| PD05 — built, initial review recorded | Metre-scaled 1024px stone colour/normal/roughness, wet shoreline layering and connected reflective water. Build/lint and unchanged collision check pass. PD07's authorized reference/player review confirms rendering; excessive stone grain corrected. Final material acceptance remains open. |
| PD06 — built, initial review recorded | Authored oculus, bounded overhead lighting, soft shaft, connected descent fog/ambient transition and aligned opening reflection. Build/lint and pure transition check pass. PD07 reviews reference/player appearance; physical descent/return comparison remains open. |
| PD07 — implemented and initially reviewed | Shared outdoor stone detail, articulated landmark/perimeter ruins and smoother cavern shell; seven streamed visual packages, resident collision/backdrop, mesh cells and optimized GLBs/textures. Build/lint and five focused tests pass. Six-area screenshots reviewed; three immediate visual corrections made. Recorded art gaps, connected transition checks and technical budgets remain open. |
| PD08 — parked Sep 30, unapproved | Replace rejected prototype with approved Image 3 Ruin Runner design: face/hair, natural proportions, layered tunic, asymmetric shoulder cloth, side satchel, rope ties and wraps. Compare front/side/back before detailed skinning and animation. Existing passing export tests do not establish design acceptance. |
| PD09 — implemented and checked Sep 30 | Hold-to-run and buffered jump input, acceleration/braking/turn response, shape grounding, gentler falls, capsule CCD, area recovery and shared pause state. Focused controls, uneven road/ramps/stairs, six-area/four-location connected walk, cavern return and recovery pass. Build/lint and five focused tests pass. Final animation, art and user feel approval remain. |
| PD10 — functional production complete Oct 1 | Camera clearance/fade, gait transitions, ground-sampled leg placement, slope-aligned boots, turn/landing polish and eight spring-driven cape/scarf/hem/hair/rope/satchel bones are implemented and checked on the temporary explorer. One skin/material, 25 bones. Final art and fitting to the replacement rig remain PD08/PD11 acceptance work. No phone-control redesign or gameplay. |
| PD11 | Final six-reference review, complete desktop roam, character/physics/camera acceptance, scalable graphics/mobile layout and release. Reuse weekly evidence if unchanged; recheck affected failures. Only game insertion and phone controls remain. |

Current direction (October 1): PD08 is parked; PD09 and PD10 functional production
are implemented and checked using the existing gameplay explorer, now extended
with secondary-motion bones. PD10 completion does not approve this temporary art.
Final replacement rig fitting and clothing appearance require the PD08 design proof;
PD11 remains the final acceptance gate and cannot approve a placeholder character.
Combine the remaining batches only if preceding gates pass. Keep checkpoints visible rather
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

PD05 materials/water, PD06 overhead light/fog and PD07 consistency/staged loading
are implemented September 28. Explicit local-preview permission was received and
six fixed reference views plus cavern player-height were reviewed. The original
PD08 explorer and six clips were implemented September 29, then rejected by the
user for character quality and locomotion. PD08 is reopened around the selected
Image 3 Ruin Runner turnaround; see plans/CHARACTER_REDESIGN.md. A separate neutral
study and local reference/GLB comparison page now exist. Face/hair, draped clothing,
wraps and material wear still need visual correction before skinning. Improved
locomotion and a reactive cloth-panel proof follow. PD08 redesign, PD09–PD11 and
recorded art/transition corrections remain.
PD07 replaces eager placed-art loading with seven visual packages and resident
collision, adds shared stone detail and landmark/boundary geometry, and smooths the
cavern crown. Corrected missing distant crowns, whole-area visibility cutoffs and
overstrong cavern grain after browser comparison. Lighter distant crowns and 24 m
cells complete the export pass. Derived world GLBs total 24.23 MB; startup hub
assets including the explorer/detail tile are 7.47 MB, excluding engine/runtime
and later prefetch. The complete 8 MB target is not yet proven. Counts are calculated file sizes, not browser
transfer measurements. The earlier ~566K triangle peak, 59.05 average FPS and
~53.5 MB transfer sample predate the latest area art and are historical evidence.
Visible geometry, low-percentile spikes and complete initial-load budgets remain
open until measured in the weekly batch. Vercel build parity is still unverified.
PD11 requires final six-reference and roaming acceptance, with no art placeholders.

Character art/animation, movement/physics and camera polish are included in PD08–11.
Only game insertion and phone controls follow handoff. Preserve the user's existing
hub-blockout.blend edit, private-file exclusion and Blender MCP setup. Older records
in CURRENT_PLAN.md retain historical dates/scope and do not override this PD plan.
