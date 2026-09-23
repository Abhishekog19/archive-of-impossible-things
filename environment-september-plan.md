# Connected environment production plan

Revised September 23, 2026 (Asia/Calcutta): build-first production and weekly
technical verification. Filename retained for existing links.
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
in the delivery candidate. Final character art/animation, movement/physics tuning,
camera polish, game insertion and phone-control redesign follow this milestone.
Use the existing controller or inspection camera during production; author usable
stairs, slopes, clearances and separate collision proxies now to avoid remodeling.

## Expected finish and assumptions

**Accelerated delivery target: October 23, 2026 — two calendar days earlier.**
October 25 is the previous baseline; November 1 remains the risk planning bound.
This September 23 revision consolidates routine technical checks into one weekly
session and removes duplicate final acceptance work. It does not cut any area,
material, vegetation, lighting or environment-delivery requirement.

Availability stays one hour per weekday and three hours per weekend day. The revised
September 22–October 23 window contains 48 scheduled hours, versus the former
54 hours through October 25. Achieving the new target therefore requires roughly
six hours recovered from repeated checks and acceptance overhead. This is an
unmeasured planning allowance, not six hours or two finish days already saved.
Reassess at September 27's weekly review using completed area coverage; if progress
does not support the target, reforecast openly. Hero assets and contextual baking
remain uncertain. No extra hours, unattended work or automatic sessions are assumed.

## Dated plan

| Phase | Dates (2026) | Window | Deliverable and exit check |
|---|---|---:|---|
| A — Whole-world layout | Sep 12–15 | 8 h | Complete; all six areas and connections blocked out. |
| B — Shared kit and risk prototypes | Sep 16–21 (closed early) | 10 h window | Complete technical proofs; final art approval remains open. |
| C — Hub and forest art | Sep 22–28 | 11 h | Finish REF4/5/6 surfaces, vegetation, lighting and transitions; quick affected-area comparisons. Weekly technical batch Sep 27. |
| D — Archive exterior/interior | Sep 29–Oct 5 | 11 h | Complete REF7/8 facade, tree/roots, hall, arches and roof opening; connect forest and descent. Weekly technical batch Oct 4. |
| E — Deep Archive | Oct 6–12 | 11 h | Complete REF10 chamber, shoreline/pool, overhead light and passage. Weekly technical batch Oct 11. |
| F — World consistency and optimization | Oct 13–18 | 10 h | Complete connections, unify material/light scale, tune loading/culling/detail levels and resolve weekly findings. Environment content target Oct 18; weekly technical batch Oct 18. |
| G — Acceptance and contingency | Oct 19–23 | 5 h | Close visual/environment defects. Reuse valid weekly evidence; final week's technical review Oct 23 covers changed paths and delivery readiness. Delivery target Oct 23. |

The phase windows include the weekly review time. October 18 is a content-completion
target, not a finished-delivery promise. Do not omit required areas to recover time.
Final character/physics/game work remains outside this environment milestone.

## Daily building and weekly technical review

Daily: build → quick affected-area reference/player comparison and movement check
→ continue building. Allow about 5–10 minutes for routine daily review. Before a
runtime/assets push, run one production build and lint changed JavaScript once;
reuse results until inputs change. Documentation-only edits need no game tests.

Batch routine FPS, sustained traversal, repeated route/loading/resource checks,
tier/mobile matrices and deployment parity once weekly: **Sep 27, Oct 4, Oct 11,
Oct 18, then Oct 23 for the final week**. Reserve 45–60 minutes within the existing
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
  current availability. Extra workers, purchased assets and extra hours are not assumed.

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
  final controls and final physics acceptance remain later and must be labeled pending.

## Current state and next action

Tooling, hub blockout and corner export/rendering proof exist. September 11's local
one-minute corner test averaged 59.75 FPS; this is not a full-world performance claim.
Historical session evidence is retained in `plans/CURRENT_PLAN.md`.

September 12's first Phase A production session has connected rough versions of all
six areas, reserved four game locations and established provisional comparison views.
The sampled outward/return route passes; this is not final layout/art approval.
The next layout session was also completed September 12, brought forward from
September 13: forest bends, archive proportions/root silhouette, hall scale and
cavern shape/framing were refined. September 13's session added continuous terrain
banks, the enclosed descent, courtyard transition and archive join fixes; checked
side routes/boundaries and compared all six areas. September 14 refines forest
background enclosure, continuous bent trunks, the taller archive facade and hero
tree/root masses. September 15 completes the production layout review, restoring
forest coverage, refining archive framing and grounding the wrapping roots.
Six comparisons and bounded outward/return/boundary checks are recorded; user
visual acceptance remains open. Phase B began September 15, one calendar day early.
Its first reusable-kit/browser proof is finalized September 16, on the planned
start date. The September 22 technical review was subsequently completed September
21, one calendar day early. Phase C started September 22 with explicit art corrections.
The September 23 cadence revision above now governs future dates. Completed B sessions are below.
Do not infer final art quality from the existence of all areas. Detailed evidence is
in `plans/CURRENT_PLAN.md`; October 23 is now the accelerated delivery target. Preserve the pre-existing
user edit to `art/source/hub-blockout.blend`; the world generator writes separate
world-blockout assets and does not overwrite that file. Blender setup is untouched.

## Phase B session record — closed September 21

| Date | Target |
|---|---|
| Sep 16 | Finish the first reusable kit, instanced browser preview, collision/loading checks and grouped publication. |
| Sep 17 | Completed early Sep 16: three tree forms, four ground-cover families, varied masonry/moss and combined browser checks. |
| Sep 18 | Completed early Sep 17: separate ruins/forest packages, distance loading/eviction, retry/cancellation and transfer/resource checks. |
| Sep 19–20 | Complete: water, baked overhead light and fog/shaft prototype; four camera comparisons, all-tier fog, Low opening cue and sustained local Iris Xe cost review. Detailed evidence and limits in CURRENT_PLAN. |
| Sep 21 | Complete: atlas/material transfer audit, reusable export check, repeated loading/recovery and three-minute Iris Xe strip traversal (59.97 FPS average). Art blockers recorded for the gate. |
| Sep 22 | Completed early Sep 21: six-reference review, technical pass with visual conditions, and reforecast. Final art approval stays open. |

The completed review advanced Phase C's start. Future phases now follow the
September 23 revision above. Sessions require the user's explicit start.

## Phase C sessions — September 22–28 (11 h window)

September 23 status: correction patch and September 23 hub paving/main ruin
silhouettes are complete; final art approval stays open. September 24 started
early on September 23 with three hub trees and their contextual shadows; the
remaining vegetation/material/light work is still open.
September 24 is partly done, not a completed day saved. The accelerated delivery
target is October 23, pending the September 27 review. Existing measured evidence
and remaining visual mismatches are in plans/CURRENT_PLAN.md.

| Date | Window | Work and exit check |
|---|---:|---|
| Sep 22 | 1 h | Completed Sep 22, including the interrupted second half: connected sun/shade patch, fused bark joins, placed bake orientation, canopy/contact shadows and foliage depth. Fixed/player comparisons and route checks pass; final art approval remains open. |
| Sep 23 | 1 h | Completed early Sep 22: patch correction checkpoint, hub paving and main ruin silhouettes with preserved layout. Comparison, export, traversal and local hardware checks pass. |
| Sep 24 | 1 h | In progress, started early Sep 23: three tree replacements and their shadows are integrated. Finish hub vegetation, material scale and contextual lighting; remove the seam between the old corner and surrounding art. |
| Sep 25 | 1 h | Build REF5 path edges, trunks/crowns, woodland shoulders and ground cover; make a quick visual/route check, then continue building. |
| Sep 26 | 3 h | Complete REF5 and dress REF6: enclosed canopy, broken ruins, layered foliage and readable light. Maintain the continuous inspection route. |
| Sep 27 | 3 h | Build hub/forest bakes and transitions for about 2 h. Use the weekly 45–60 minute technical batch for changed-area performance/loading/mobile checks and a coverage-based reforecast. |
| Sep 28 | 1 h | Finish the largest REF4/5/6 visual gaps and remaining art. No placeholder surfaces in the Phase C candidate; reuse Sep 27 technical results. |
| Sep 29 | 1 h | Begin Phase D archive exterior structure. The former standalone technical review is folded into Sep 27. |

Patch checkpoint: bark joins should hold up at player distance; warm sun/cool shade
and grounded canopy/contact shadows should read coherently across adjacent assets;
foliage should have layered values without obscuring the route. Review fixed and
moving views in-browser against REF4/5/6. No similarity percentage is inferred.
Use contextual static bakes plus reusable foliage/props as described in
`art-pipeline.md`. Keep simple colliders and the existing inspection controller;
final movement, phone-control redesign and games remain after the environment.
