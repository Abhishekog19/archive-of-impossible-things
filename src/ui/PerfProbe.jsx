import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { perf } from './perf'

/**
 * Reads `renderer.info` once a frame. Lives inside the Canvas because that is
 * the only place with a renderer.
 *
 * build-roadmap.md puts the dev HUD in M1 rather than later for a specific
 * reason: a draw-call regression found the session it happens is a five-minute
 * fix, and the same regression found at M13 is an archaeology project. So the
 * numbers are on screen from the first milestone, next to the budgets they have
 * to stay under.
 *
 * FPS is averaged over a rolling window rather than taken from a single delta.
 * An instantaneous 1/delta reading jitters by 10+ fps between frames, which is
 * exactly wrong for the judgement being made here — "does this hold 30" is a
 * question about the sustained rate, and a jittering number invites tuning
 * against noise.
 */
export default function PerfProbe() {
  const gl = useThree((s) => s.gl)
  const window_ = useRef({ frames: 0, elapsed: 0 })

  useFrame((_, delta) => {
    const w = window_.current
    w.frames += 1
    w.elapsed += delta

    if (w.elapsed >= 0.25) {
      perf.fps = w.frames / w.elapsed
      perf.frameMs = (w.elapsed / w.frames) * 1000
      w.frames = 0
      w.elapsed = 0
    }

    // `info.render` is reset by three.js each frame, so this is the cost of the
    // frame just drawn. `info.memory` is cumulative and is what will expose the
    // dispose() leaks M8 is about.
    perf.calls = gl.info.render.calls
    perf.triangles = gl.info.render.triangles
    perf.geometries = gl.info.memory.geometries
    perf.textures = gl.info.memory.textures
    perf.programs = gl.info.programs?.length ?? 0
    perf.dpr = gl.getPixelRatio()
  })

  return null
}
