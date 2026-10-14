# Loading and performance pass — October 14, 2026

The loading implementation and targeted measurements were completed October 13;
the final production review and handoff continued October 14 after an automatic
approval-review usage limit interrupted browser access. Performance acceptance
remains open.

## Changes

- The entry screen now covers the initial scene load and reports actual download,
  decode, texture and shader preparation stages. It waits for the hub and first
  connector area at normal spawn; it has a retry action for failed areas.
- A shared Meshopt worker moves geometry decompression off the render thread,
  with a synchronous fallback when workers cannot be created.
- GPU preparation is serialized, with texture initialization spread across
  frames and shader compilation using the real scene's lighting/fog. Streamed
  areas become ready after preparation. Aborted owners retain their materials
  until compilation settles, then release their resources.
- Hall/cavern preparation starts at camera Z -12, before their portal becomes
  required at -37. Collision remains resident and loading gates still protect
  cold entries. Eviction remains enabled; the whole world is not pinned in GPU
  memory.
- Static instance markers are removed from the render hierarchy after their
  transforms reach the instance buffer. Streamed static world matrices no longer
  update every frame. Stone/bark detail work is skipped beyond its existing fade.
- Vercel has explicit static Vite build settings. See
  [deployment notes](VERCEL_DEPLOYMENT.md). No live deployment was performed.

## Verification and measurements

All 39 automated tests, changed-JavaScript lint and the production build pass.
Tests cover preparation order, deduplicated uploads, cancellation during/behind
compilation, failure recovery, entry/portal requirements, instance transforms
and resource disposal. No GLBs or collision data changed. Hub before/after,
forest portal and cavern views retain their composition/materials; inspected
development browser error logs are empty.

The October 14 connected-route check passes all 20 rows, including cavern
recovery; maximum destination error is 0.67 m. Production entry, 390 × 844 Settings,
Low quality switching and restoring Automatic pass. A temporary local proxy
delayed resident/hub/connector model responses by 4/5/12 seconds: the entry
screen stays visible, advances to 1 of 2 areas ready, and clears after completion.
This caught and corrected a screen-positioning bug in the camera-anchored HTML
overlay. The shared screen overlay also disables world-anchor hiding when the
camera faces away from the origin. Final affected-file lint/build pass after
that UI-only correction; the steady traversal measurement below is reused.
Retrieved production error logs are empty. The temporary delay proxy is stopped.

The final local development traversal used Medium, 1280 × 720, DPR 1.25:

| Measurement | Earlier October 13 review | Final targeted run |
| --- | ---: | ---: |
| Duration | 180.03 s | 180.01 s |
| Average FPS | 28.51 | 38.84 |
| Waypoints | 67 | 87 |
| Hidden frames | 0 | 0 |
| Samples reporting area loading | 3 | 0 |
| Approximately one-second samples below 30 FPS | 97 / 174 | 5 / 176 |
| Lowest sampled FPS | 11.84 | 24.61 |
| Peak sampled draw calls | 309 | 289 |
| Peak sampled triangles | 799,919 | 778,742 |

These are local runs with matching review settings, not a controlled hardware
benchmark or a guarantee for first visits. An intermediate run averaged 39.52 FPS
but recorded a severe 0.87 FPS sample on its first connector pass. A focused
preparation trace did not reproduce that multi-second hitch; decode stages took
hundreds of milliseconds. The final run followed the worker and entry-gate
changes and did not reproduce it, but browser/driver caches also differ. Do not
claim that cold-start stalls have been eliminated.

Final resource samples range from 226–440 geometries and 52–68 textures. Repeated
cavern visits still reach approximately 292–293 geometries after the first pass.
Resident geometry uploaded when first seen on the return journey may contribute;
this is a hypothesis, not proof that resource stability has been accepted.

Evidence is local and ignored under `.artifacts/loading-performance-oct13/`,
including `final-performance.json`, `final-traversal-result.png`, the earlier
trial, preparation trace and affected-view screenshots.

## Remaining performance work

1. Reduce visible geometry and draw calls, especially forest/return views. The
   60 FPS goal, fewer-than-150-call budget and approximately 300K-triangle budget
   remain unmet. Avoid whole-area visibility cutoffs that reopen portal holes.
2. Verify a genuinely cold production/deployed visit and comparable repeated
   resource cycles. A loader cannot remove the cost of drawing every frame.
3. Measure startup transfer over the wire. The resident, hub and connector GLBs
   alone total 18,871,164 file bytes; preparation does not solve the 8 MB target.
   This file-size total is not a browser transfer measurement.
4. Complete live Vercel parity and actual-phone controls/thermals when available.
   The next routine weekly review remains October 20.

Six work groups remain open, including the unfinished performance acceptance
work. This completes a focused loading pass, not the entire performance group.
The protected hub-blockout source edit and private-source exclusion are preserved.
