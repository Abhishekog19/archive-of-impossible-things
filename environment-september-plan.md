# Connected environment production plan

Revised September 23, 2026 (Asia/Calcutta), including the finished correction patch
and September 23 hub stonework completed early. Filename retained for existing links.
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

**Expected finish: October 25, 2026. Planning range: October 25–November 1.**
September 22's reforecast was completed September 21. September 30 is no longer a
deadline. The technical kit, loading and cavern proofs reduce implementation risk,
but no complete area has accepted final art yet. There is insufficient area-art
throughput evidence to retain October 18 as an optimistic bound. October 25 stays
the working estimate, conditional on the first assembled material/light patch and
Phase C area progress. Recheck September 25; do not invent an art-completion rate
from prototype count, frame rate or early review sessions. Hero architecture/roots,
contextual baking, cavern art and whole-world performance remain uncertainties.

Existing availability: one hour per weekday and three hours per weekend day.
The original September 12–October 25 window provides 72 shared production/review
hours. With the September 22 review completed early, September 22–October 25 now
provides 54 remaining scheduled hours; extending through November 1 adds 11 hours.
These are working windows, not pure artist-labor or agent-runtime estimates.
Assume reviews within about one day, no major direction restart, and explicitly
started sessions; no unattended work or extra daily availability is assumed.

## Dated plan

| Phase | Dates (2026) | Window | Deliverable and exit check |
|---|---|---:|---|
| A — Whole-world layout | Sep 12–15 | 8 h | Block out every area and connection; establish four future game locations and six reference cameras; inspect the complete route in-browser. |
| B — Shared kit and risk prototypes | Sep 16–21 (closed early) | 10 h window | Technical proofs and September 22 review complete. Advance with a material/light correction checkpoint; final art is not approved. |
| C — Hub and forest art | Sep 22–29 | 12 h | First prove an assembled sun/shade patch; then apply art across REF4/5/6, replace placeholders, finish vegetation/lighting and review transitions. |
| D — Archive exterior/interior | Sep 30–Oct 6 | 11 h | Complete REF7/8 facade, tree/root composition, hall, arches and roof opening; connect forest and cavern descent; compare in-browser. |
| E — Deep Archive | Oct 7–13 | 11 h | Complete REF10 rock chamber, shoreline/pool, overhead light and passage; verify visual result and Iris Xe cost. |
| F — World consistency and optimization | Oct 14–20 | 11 h | Finish all connections; unify lighting/material scale; tune loading, culling and detail levels; resolve worst visual/performance gaps. Environment content complete by Oct 20. |
| G — Acceptance and contingency | Oct 21–25 | 9 h | Six reference comparisons, repeated zone entry, sustained performance, deployment verification and environment fixes; delivery candidate Oct 25. |

October 18 is no longer a supported forecast. Do not compress verification or
silently remove required areas to hit a date. If a phase
exceeds its window, explicitly reforecast, using November 1 as a planning bound,
not a guaranteed latest date. Character/physics/game work is not included above.

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
- Target 60 FPS on Iris Xe at DPR 1.25. Measure actual frames for at least three
  minutes across representative areas/transitions. Under 150 draw calls (preferably
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
21, one calendar day early. Phase C starts September 22 with explicit art corrections;
this does not bring the full environment finish forward. Completed B sessions are below.
Do not infer final art quality from the existence of all areas. Detailed evidence is
in `plans/CURRENT_PLAN.md`; October 25 remains the working finish. Preserve the pre-existing
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

The completed review advances only Phase C's start. Later phases retain their dates;
October 25 is still the working finish. Sessions require the user's explicit start.

## Phase C sessions — September 22–29 (12 h window)

September 23 status: correction patch and September 23 hub paving/main ruin
silhouettes are complete; final art approval stays open. September 24 started
early on September 23 with three hub trees and their contextual shadows; the
remaining vegetation/material/light work is still open.
The dated work is one calendar day ahead, while the October 25 forecast and
September 25 throughput review remain unchanged. Measured evidence and remaining
visual mismatches are in plans/CURRENT_PLAN.md.

| Date | Window | Work and exit check |
|---|---:|---|
| Sep 22 | 1 h | Completed Sep 22, including the interrupted second half: connected sun/shade patch, fused bark joins, placed bake orientation, canopy/contact shadows and foliage depth. Fixed/player comparisons and route checks pass; final art approval remains open. |
| Sep 23 | 1 h | Completed early Sep 22: patch correction checkpoint, hub paving and main ruin silhouettes with preserved layout. Comparison, export, traversal and local hardware checks pass. |
| Sep 24 | 1 h | In progress, started early Sep 23: three tree replacements and their shadows are integrated. Finish hub vegetation, material scale and contextual lighting; remove the seam between the old corner and surrounding art. |
| Sep 25 | 1 h | Build the REF5 forest approach pass: path edges, trunks/crowns, woodland shoulders and ground cover. Review achieved area coverage and revise dates if the remaining window is insufficient. |
| Sep 26 | 3 h | Complete REF5 and dress REF6: enclosed canopy, broken ruins, layered foliage and readable light. Maintain the continuous inspection route. |
| Sep 27 | 3 h | Finish hub/forest contextual bakes, transitions and local corrections; export/cull/instance using measured budgets. |
| Sep 28 | 1 h | Compare REF4/5/6 at fixed and player views; fix the largest remaining 3–5 mismatches. No placeholder surfaces in the Phase C candidate. |
| Sep 29 | 1 h | Sustained traversal/resource and layout checks; capture the three comparisons and record visual acceptance/remaining gaps before Phase D. |

Patch checkpoint: bark joins should hold up at player distance; warm sun/cool shade
and grounded canopy/contact shadows should read coherently across adjacent assets;
foliage should have layered values without obscuring the route. Review fixed and
moving views in-browser against REF4/5/6. No similarity percentage is inferred.
Use contextual static bakes plus reusable foliage/props as described in
`art-pipeline.md`. Keep simple colliders and the existing inspection controller;
final movement, phone-control redesign and games remain after the environment.
