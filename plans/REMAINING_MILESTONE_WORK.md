# Remaining environment milestone work — October 14, 2026

Latest rendering pass: **59.31 FPS** over a corrected 60-second local check,
with 65 peak rendering submissions. The user's target is now **50–55 FPS**.
Earlier traversal FPS figures below used a faulty extra-render steering helper
and are not normal-play rates. Sustained, geometry/resource, phone and deployment
acceptance remain open; the count is still six groups. See
[the rendering review](RENDER_COST_PASS_2026-10-14.md).

The five original audit implementation phases have been delivered. Their remaining
art and acceptance gaps are grouped below; these are work groups, not new numbered
audit phases or a promise that one iteration will close each group.

| Work group | Remaining scope |
| --- | --- |
| Hub | REF4 woodland depth, terrain shoulders, branch/crown connections; retain remaining paving and masonry differences for final comparison. |
| Forest and canopy | REF5/REF6 broad bank forms, canopy density, background depth and light composition. |
| Archive and hall | REF7/REF8 soft stone shading, repeated courses, facade/root hierarchy and window/descent landscape depth. |
| Cavern | REF10 dome and wall massing, angular joins, repeated surfaces and shore segmentation. |
| Character | Approved Ruin Runner likeness, face/hair, garment silhouette and wear, plus final deformation/animation acceptance. |
| Performance | Sustain the new 50–55 FPS target, visible geometry budgets, startup transfer and resource stability; use corrected measurements to select fixes. |
| Final acceptance | Whole-world reference/player comparisons, connected roaming, production/deployment parity and actual phone evidence. |

Seven work groups were open at the start of October 13. The focused hub depth pass
is now implemented and checked; its remaining visual differences are carried into
the final acceptance group. **Six further production/verification batches are
planned**, in this order: performance, forest/canopy, archive/hall, cavern,
character, and final acceptance. This is a planning count, not a guarantee that
six iterations will resolve every gap. The character is implemented and animated
but its final likeness is unapproved. No Archive gameplay is included.

The October 13 local weekly review is recorded separately: 28.51 average FPS fails
the performance gate. Optimization therefore takes priority over further art
expansion. The next routine review is October 20. Desktop browser results do not
establish actual-phone behavior or deployment parity.

October 14 handoff: the focused loading pass is implemented. The final targeted
October 13 run averaged 38.84 FPS with no sampled area-loading pauses; draw and
triangle budgets and the 60 FPS goal still fail. Entry shader/texture preparation,
earlier portal loading and a decoder worker are in place. See
[the loading review](LOADING_PERFORMANCE_PASS_2026-10-14.md). The count remains
six open work groups, with performance still first; cold-start transfer, resource
stability, real-phone and live Vercel evidence remain outstanding.
