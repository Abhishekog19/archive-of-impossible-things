# Weekly local technical review — October 13, 2026

The local review is recorded after the hub depth pass. The performance gate fails;
the next batch should address rendering/loading cost before adding more scenery.

## Results

- All 36 automated tests and the production build pass. No JavaScript changed.
- Ten hub/arrival/overlook controller checkpoints pass, maximum error 0.31 m.
- The live controller traverses 67 waypoints in 180.03 seconds, with zero hidden
  frames, on Medium at 1280 × 720 and DPR 1.25. Average FPS is **28.51**. This
  fails the review's 30 FPS floor and the project's 60 FPS goal.
- The 174 approximately one-second samples range from 11.84 to 35.44 FPS;
  97 samples fall below 30. Three samples report area loading. The lowest samples
  recur near the forest portal region at Z approximately -43 to -44.
- Render counts range from 34–309 calls and 149,420–799,919 triangles. Peaks
  exceed the working budgets of fewer than 150 calls and about 300K triangles.
  The largest sampled triangle count occurs on the return/turn at the hub.
- Resource counts range from 243–439 geometries and 52–68 textures. Counts drop
  as areas unload, but comparable cavern visits retain 243, then 292, then 293
  geometries. This run does not establish long-term resource stability.
- The production preview loads the hub. Settings fits at 390 × 844; Low quality
  switching and restoring Medium work. Retrieved development and production
  browser error samples are empty.

This is a local development-browser traversal, not a production hardware benchmark
or real-phone result. The October 6 run averaged 38.96 FPS, but multiple art batches
and host conditions differ; this is not a controlled attribution of the drop to
the hub change alone. Do not describe the current build as performance-accepted.

## Follow-up order

1. Profile the forest portal loading region and return-view visibility. Reduce
   simultaneously rendered scenery while retaining the required portal sightline.
2. Investigate retained geometry across repeated area loads; distinguish expected
   caches from resources that should be disposed.
3. Measure actual initial-to-inspectable transfer and production runtime cost.
   The 8 MB startup target remains unproven; total derived world assets are
   36,652,652 bytes and must not be confused with startup transfer.
4. Compare the intended deployed URL when supplied. No deployment URL was found
   in the repository plans, and none was supplied during this review. Actual-phone
   controls/thermals and deployment parity remain pending.

Next routine weekly review: October 20. Targeted measurements needed to validate
performance fixes may run sooner. Local ignored evidence, including all 174
samples, is under `.artifacts/hub-depth-oct13/`.
