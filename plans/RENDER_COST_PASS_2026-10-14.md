# Rendering cost pass — October 14, 2026

The working target is now **50–55 FPS**, as requested. This is a target rather
than a cap. The corrected local 60-second traversal averaged **59.31 FPS** on
Medium at 1280 × 720 / DPR 1.0. This meets the short-check target, not sustained
device or deployment acceptance.

## Changes

- Static cells sharing a material use Three.js multi-draw batching. Individual
  cell bounds, front-to-back sorting, transforms, authored geometry and materials
  remain intact. Browsers without `WEBGL_multi_draw` keep ordinary meshes.
- Stone, bark and outdoor grading account for each batched transform. Contact
  shadows raycast the original small cells, ignoring detached streamed areas.
  Batched buffers/textures are released when their owner is evicted.
- Medium starts at DPR 1.0 instead of 1.25: 36% fewer pixels at equal viewport
  size. Five-second average FPS below 50 reduces resolution by 0.125 to a floor
  of 0.75, with an eight-second cooldown. Automatic effects demotion follows only
  at that floor and retains the reduced resolution. Manual quality pins effects.
  Loading, settings, hidden pages and manual stepping reset/hold the probe.
- The review UI offers a focused 60-second check and records p95/p99 frame times,
  long frames, and render-frame versus animation-frame counts.

## Measurement correction

The old live traversal called `turnTo` each animation frame. Its `turn` helper
also forced two manual frames, switching the render clock into and out of manual
mode. This rendered extra frames and corrupted the governor's time evidence.
`turn` now steps only when the test is already in manual mode. The live runner
requires render and animation counts to agree within two frames.

Consequently the older 28.51 / 38.84 FPS reviews, this pass's initial 28.88 FPS
baseline, and intermediate 40.12 / 36.29 FPS short checks **are not normal-play
FPS measurements**. Do not claim a percentage FPS gain from those figures to
the corrected result. Their saved traces remain useful for diagnosing the test.
Two attempted long runs were interrupted by preview session loss and are not
accepted measurements. A complete corrected sustained run remains pending.

## Recorded result

| Metric | Corrected 60-second check |
| --- | --- |
| Average FPS | 59.31 |
| p95 / p99 frame time | 16.8 / 17.0 ms |
| Render / animation frames | 3,559 / 3,559 |
| Hidden frames | 0 |
| Waypoints reached | 18; hub through cavern and part of the return |
| Lowest one-second sample | 47.26 FPS |
| Samples below 50 / below 30 | 1 / 0 |
| Frames over 50 / 100 ms | 2 / 1 |
| Samples reporting area loading | 0 |
| Peak submissions / triangles | 65 / 717,375 |
| Resolution | DPR 1.0 throughout; no shedding needed |

The submission count is below the 150 budget in this sample. Triangle count still
exceeds 300,000. Do not describe the remaining long frame as eliminated. This
was a warm local check after contact tests, not a cold download measurement.

## Verification and next work

All 44 tests, changed-JavaScript lint and the production build pass. The eight
contact-shading checkpoints pass across all areas, jumping and landing. The
production entry and Low/Medium quality switching also pass. The
forest before/after comparison retains composition and material placement, with
slightly softer fine edges at lower DPR. No GLB, collision or Blender source was
changed by this pass. Existing art gaps remain unchanged.

Production hub versus the prior screenshot also retains the same geometry and
composition. REF4 still has deeper layered woodland, a stronger tower silhouette,
more organic paving and richer ruined path forms than the current scene; this
optimization pass does not close those visual gaps. Production browser errors: none.

Evidence is under `.artifacts/render-cost-oct14/`: `corrected-live-60s.json`,
`corrected-live-result.png`, `contact-check.txt`, and forest comparisons.

Next: corrected sustained traversal/resource stability, visible foliage geometry
reduction where the remaining cost warrants it, startup transfer and real-phone /
live Vercel verification. The routine broad review remains October 20. Performance
is still one of six open milestone work groups.
