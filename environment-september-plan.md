# Connected environment production plan

Revised September 26, 2026 (Asia/Calcutta): three-times availability, build-first
production and weekly technical verification. Filename retained for existing links.
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

**Working delivery target: October 4, 2026; contingency October 5–6.**
This supersedes the October 23 forecast. It moves the planned finish 19 calendar
days earlier; that is a forecast, not measured days saved or a quality guarantee.
All six reference areas and the environment-delivery requirements above remain.

The user increased work hours to three times the previous baseline. Planning now
assumes **3 hours per weekday and 9 hours per weekend day**, including production,
review and export time. Sessions still require the user's start; no automation or
unattended production is implied. If the intended availability is 3 hours every
day instead, this forecast must be revised.

After September 26's forest session, the previous plan allocates 41 remaining
hours: Phase C finish 4, archive D 11, cavern E 11, consistency/optimization F 10,
and acceptance G 5. September 27–October 4 provides 42 hours over eight production
dates. These are inherited planning allowances, not measured effort estimates.
Hero tree/root work, materials, contextual bakes and unresolved performance issues
can exceed them; increased hours do not automatically triple production speed.
Reassess after September 27's coverage/technical review and September 29's archive
checkpoint. October 5–6 provides up to six additional contingency hours, not a
promise that every possible defect fits that window.

## Remaining dated plan

| Date (2026) | Hours | Work and exit checkpoint |
|---|---:|---|
| Sep 27, Sunday | 9 | Close Phase C hub/forest art: outer backdrop, material/light transitions and biggest REF4/5/6 gaps (4 h, including weekly technical review). Begin REF7 facade and hero tree/root production (5 h). |
| Sep 28, Monday | 3 | Continue REF7 exterior: authored stonework, wrapping roots, vegetation and placed materials/light; begin shared REF8 architecture. |
| Sep 29, Tuesday | 3 | Finish REF8 hall arches, columns, broken roof, floor and vegetation; join forest, exterior and descent. Close Phase D with REF7/8 browser comparisons. |
| Sep 30, Wednesday | 3 | Build REF10 cavern rock walls, shoreline, overhead opening and descending passage using the proven cavern prototype. |
| Oct 1, Thursday | 3 | Cavern pool/water appearance, rock materials and shoreline surface art. |
| Oct 2, Friday | 3 | Cavern overhead light, reflections, fog and shoreline detail; compare REF10 at reference and player heights. |
| Oct 3, Saturday | 9 | Close cavern art and passage (2 h); unify all six areas' materials/light and connections, then loading/culling, texture and geometry budgets (7 h). |
| Oct 4, Sunday | 9 | Finish world optimization/export/integration (3 h); six-reference acceptance, weekly technical review, targeted fixes and release (5 h); 1 h reserve. |
| Oct 5–6, contingency only | Up to 3/day | Use only for unresolved hero-art, baking, loading or acceptance defects. Reforecast if more work remains; do not silently drop scope. |

Phases A/B are complete; Phase C production through September 26 is complete,
with final hub/forest art closure still due September 27. Phase D uses 11 hours
September 27–29; E uses 11 hours September 30–October 3; F uses 10 hours October
3–4; G uses 5 hours October 4. The plan keeps technical review inside those windows.
Environment content should be complete October 3; final delivery depends on the
October 4 acceptance gate. Character/physics polish and game insertion follow.

## Daily building and weekly technical review

Daily: build → quick affected-area reference/player comparison and movement check
→ continue building. Allow about 5–10 minutes for routine daily review. Before a
runtime/assets push, run one production build and lint changed JavaScript once;
reuse results until inputs change. Documentation-only edits need no game tests.

Batch routine FPS, sustained traversal, repeated route/loading/resource checks,
tier/mobile matrices and deployment parity once weekly: **Sep 27 and Oct 4** (continue weekly only if delivery slips). Reserve 45–60 minutes within the existing
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
  final controls and final physics acceptance remain later and must be labeled pending.

## Current state and next action

September 26 forest finishing is complete: widened planted banks, additional tree
layers, broken masonry, irregular paving moss, clearing paving and the canopy path
extended to z=-96. The focused forest/clearing/return connection and production
build pass. The export-name collision found in browser review is fixed. Detailed
counts, evidence and limits are in plans/CURRENT_PLAN.md.

This is not final visual approval. REF6 still exposes coarse outer background
crowns/terrain and an undressed archive facade; ambient depth, foliage lighting
and material consistency need the Phase C close and later world pass. September 27
closes hub/forest gaps and begins archive production. All six areas have connected
blockouts, but REF7/8/10 still need their full art passes. Weekly resource/performance
acceptance remains pending; older FPS results do not validate the new dense assets.

Preserve the user's pre-existing art/source/hub-blockout.blend modification and
Blender MCP setup. The private source file remains excluded from Git, verified
through metadata only. Historical production records remain in CURRENT_PLAN.md;
older dates there are superseded by the schedule above.
