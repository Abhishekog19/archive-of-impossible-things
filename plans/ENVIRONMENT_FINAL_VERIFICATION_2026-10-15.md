# Environment handoff verification — October 15, 2026

The current environment and third-person roaming build is locally verified for
handoff. The user's final-verification request closes this implementation pass;
it does not establish that the remaining concept, hardware or deployment gates
have passed. No gameplay or further art expansion was added.

## Fix found during verification

The first sustained traversal exposed one additional GPU geometry on each repeat
visit to the cavern. Streamed areas deliberately disable automatic disposal of
their GLB resources, which also prevented automatic cleanup of the generated
light shaft and opening material. `CavernLight` now explicitly owns and disposes
its generated geometry and materials, while leaving the supplied opening geometry
to its existing owner. Commit: `85bcfdc`.

After the fix, matched repeat visits return to the same resource counts: cavern
45 geometries / 86 textures, hub return 57 / 98, and the loaded forest corridor
79 / 134. Before the fix these geometry counts rose by one per lap. This verifies
the observed leak over the tested route; it is not a GPU-byte measurement or a
long thermal soak. No GLB, collider or Blender source changed.

## Final local sustained measurement

Corrected live runner, visible Codex desktop browser, Medium, 1280 × 720. The
route covers hub → forest → canopy → archive → hall → cavern banks → hub,
repeated for three minutes. Normal animation and render frame counts match.

| Metric | Result |
| --- | --- |
| Duration / waypoints | 180 seconds / 55; more than two complete 26-waypoint loops |
| Average FPS | **58.64**, passes the user's 50–55 FPS working target |
| Render / animation frames | 10,555 / 10,555 |
| Hidden frames | 0 |
| p95 / p99 frame time | 16.9 / 33.2 ms |
| Frames over 50 / 100 ms | 30 / 9 |
| Lowest one-second sample | 36.61 FPS |
| Samples below 50 / below 30 | 9 / 0 of 177 samples |
| Samples reporting area loading | 0 |
| Peak rendering submissions | 66; below the 150 budget |
| Peak visible triangles | 720,944; above the 300,000 budget |
| DPR | 1.0 → 0.875; effects stayed Medium |

This establishes local sustained average performance, not a minimum of 50 FPS
on every frame. Brief stalls remain. The governor reduced pixel cost once during
the run. The earlier 60-second result was 59.31 FPS at DPR 1.0; this longer run
also exercises area eviction and re-entry. Neither is an Iris Xe/phone certification
or a cold network measurement. Older live traversal figures recorded before the
October 14 steering correction are invalid as normal-play FPS comparisons.

## Functional and production checks

- 20 connected-world checkpoints pass, including every reserved location and
  cavern recovery after an out-of-bounds fall.
- 17 shoreline sectors pass around the complete pool.
- 12 return-to-hub checkpoints pass through the ascent, hall, forest and arrival.
- Four cavern-return checks pass, including a 1.03 m uphill jump.
- Eight contact-shading checks pass across all six areas, jump fade and landing.
- All 44 automated tests pass after the fix. Changed-file ESLint, `git diff
  --check` and the production build pass. Existing Rapier test initialization
  emits a deprecation warning, without test failures.
- Production `/` enters the assembled world. Settings fit at 390 × 844, Low and
  Medium switching work, and returning to play works. Desktop-width preview and
  all six saved reference cameras render. Captured browser error logs are empty.
- Actual touch controls, phone GPU performance, thermals and Vercel delivery are
  not established by desktop viewport testing.

## Reference comparison and acceptance limits

Production screenshots were compared side by side with REF4, REF5, REF6, REF7,
REF8 and REF10. The natural-ruins/forest direction and connected route are present.
The current render still differs materially from the approved concepts:

| Area | Remaining visual differences |
| --- | --- |
| Hub / REF4 | Sparse distant woodland and exposed horizon; smaller tower presence; regular plaza paving and simpler ruined path branches. |
| Forest and canopy / REF5–6 | More open crowns, broad bank planes and a shorter-looking corridor; weaker background depth and sunlight composition. |
| Archive / REF7 | Simpler facade silhouette and root hierarchy, repeated soft stone courses, limited surrounding landscape depth. |
| Hall / REF8 | Repeated dark masonry, simpler open roof/window context and a darker, shorter-looking descent. |
| Cavern / REF10 | Broad dome, angular wall joins, repeated rock texture and segmented shore forms; less dramatic opening/light composition. |

These comparisons do not establish the approximately 80% visual target. Final
character likeness remains unapproved; this pass reuses the existing character
and passing deformation/motion tests. The current version is the handoff baseline,
not a claim that these differences were corrected or waived.

The visible-triangle budget and startup-transfer target also remain unmet. The
last unchanged-asset inventory counted 18,871,164 bytes of startup GLBs alone,
above the 8 MB goal; this is not measured HTTP transfer or GPU memory. Live Vercel
checks need a deployed URL, and physical-device acceptance needs a real phone.
No additional art batch is started by this verification pass. The routine review
date remains October 20 if work resumes.

## Evidence and handoff

Local evidence is in `.artifacts/final-environment-oct15/` (ignored by Git):

- `sustained-180s.json`: initial run that exposed resource growth.
- `sustained-fixed-180s.json`, `sustained-fixed-result.png`: final corrected run.
- `connected-route.txt`, `shoreline.txt`, `return-to-hub.txt`,
  `cavern-ascent.txt`, `contact-check.txt`: 61 passing checkpoints.
- `production-hub.png`, `production-narrow-settings.png`,
  `production-narrow-low.png`: production checks.
- `REF4-current.png` through `REF8-current.png`, `REF10-current.png`, and
  `comparison-4-5.png`, `comparison-6-7.png`, `comparison-8-10.png`: final visuals.

Deployment setup remains in [the Vercel notes](VERCEL_DEPLOYMENT.md). The existing
uncommitted `art/source/hub-blockout.blend` edit is preserved and excluded from
commits. The protected personal-source file was checked through Git metadata only:
ignored and untracked.
