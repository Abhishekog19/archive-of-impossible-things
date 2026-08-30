/**
 * A frame's worth of measurements, shared between the probe inside the Canvas
 * and the HUD outside it.
 *
 * A plain mutable object rather than store state, deliberately. These numbers
 * change every frame and are read ~5 times a second; routing them through
 * zustand would push 60 renders a second through React to update text nobody can
 * read that fast. The probe writes here, the HUD samples on a timer.
 */
export const perf = {
  fps: 0,
  frameMs: 0,
  calls: 0,
  triangles: 0,
  geometries: 0,
  textures: 0,
  programs: 0,
  dpr: 0,
}
