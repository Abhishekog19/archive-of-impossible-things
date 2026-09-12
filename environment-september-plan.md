# Connected environment production plan

Revised September 12, 2026 (Asia/Calcutta). Filename retained for existing links.
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

**Expected finish: October 25, 2026. Planning range: October 18–November 1.**
September 30 is no longer a deadline. This is an initial estimate, not a quality
guarantee. Reforecast after September 22 using actual asset-production throughput.
The hub and technical corner proof are reusable, but do not prove finished quality
across the expanded world. Architecture/root composition, cavern water/light and
whole-world performance are the largest uncertainties.

Existing availability: one hour per weekday and three hours per weekend day.
September 12–October 25 provides 30 weekday hours + 42 weekend hours = 72 shared
production/review hours. The early/late bounds provide approximately 61–83 hours.
These are working windows, not pure artist-labor or agent-runtime estimates.
Assume reviews within about one day, no major direction restart, and explicitly
started sessions; no unattended work or extra daily availability is assumed.

## Dated plan

| Phase | Dates (2026) | Window | Deliverable and exit check |
|---|---|---:|---|
| A — Whole-world layout | Sep 12–15 | 8 h | Block out every area and connection; establish four future game locations and six reference cameras; inspect the complete route in-browser. |
| B — Shared kit and risk prototypes | Sep 16–22 | 11 h | Stone/masonry/arch/tree/root/vegetation kit; prove repeated assets, zone exports/loading and a small cavern water/light prototype. Review material direction and reforecast. |
| C — Hub and forest art | Sep 23–29 | 11 h | Apply art across REF4/5/6; replace placeholders, finish vegetation/lighting and review transitions. |
| D — Archive exterior/interior | Sep 30–Oct 6 | 11 h | Complete REF7/8 facade, tree/root composition, hall, arches and roof opening; connect forest and cavern descent; compare in-browser. |
| E — Deep Archive | Oct 7–13 | 11 h | Complete REF10 rock chamber, shoreline/pool, overhead light and passage; verify visual result and Iris Xe cost. |
| F — World consistency and optimization | Oct 14–20 | 11 h | Finish all connections; unify lighting/material scale; tune loading, culling and detail levels; resolve worst visual/performance gaps. Environment content complete by Oct 20. |
| G — Acceptance and contingency | Oct 21–25 | 9 h | Six reference comparisons, repeated zone entry, sustained performance, deployment verification and environment fixes; delivery candidate Oct 25. |

October 18 is possible only with limited rework and early gate completion. Do not
compress verification or silently remove required areas to hit a date. If a phase
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
cavern shape/framing were refined. Next: transitions, boundaries and six-area
composition review to close Phase A. Keep the remaining review windows rather
than inferring final quality from the existence of all areas. Detailed evidence is
in `plans/CURRENT_PLAN.md`; October forecast is unchanged. Preserve the pre-existing
user edit to `art/source/hub-blockout.blend`; the world generator writes separate
world-blockout assets and does not overwrite that file. Blender setup is untouched.
