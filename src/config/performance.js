// October 14 working target: preserve the environment while aiming for 50–55 FPS.
// This is a rendering budget, not a frame-rate cap.
export const PERFORMANCE = { minimumFps: 50, recoveryFps: 55 }

export const FRAME_PROBE = { graceSeconds: 5, windowSeconds: 5, cooldownSeconds: 8 }

export function createFrameProbe() {
  return { clock: 0, sampleSeconds: 0, weightedFps: 0, holdUntil: FRAME_PROBE.graceSeconds }
}

// Returns true once per sustained undershoot. Pauses/loading do not count as
// slow rendering; a single long frame cannot satisfy the evidence window.
export function sampleFrameBudget(probe, delta, fps, paused = false) {
  probe.clock += Math.min(Math.max(delta, 0), .25)
  if (paused) {
    probe.sampleSeconds = 0
    probe.weightedFps = 0
    probe.holdUntil = probe.clock + FRAME_PROBE.graceSeconds
    return false
  }
  if (probe.clock < probe.holdUntil || fps <= 0) return false
  // Average a full window. Resetting evidence on one healthy quarter-second
  // reading lets alternating 30/60 FPS frames evade adaptation indefinitely.
  const step = Math.min(delta, .25)
  probe.sampleSeconds += step
  probe.weightedFps += fps * step
  if (probe.sampleSeconds < FRAME_PROBE.windowSeconds) return false
  const averageFps = probe.weightedFps / probe.sampleSeconds
  probe.sampleSeconds = 0
  probe.weightedFps = 0
  if (averageFps >= PERFORMANCE.minimumFps) return false
  probe.holdUntil = probe.clock + FRAME_PROBE.cooldownSeconds
  return true
}

export function budgetAction(dpr, floor, pinned, tier) {
  if (dpr > floor + .001) return 'resolution'
  return !pinned && tier !== 'low' ? 'tier' : null
}

export function summarizeFrameTimes(times) {
  const sorted = [...times].sort((a, b) => a - b)
  const percentile = p => sorted[Math.max(0, Math.ceil(sorted.length * p) - 1)] || 0
  return {
    p95FrameMs: Number(percentile(.95).toFixed(2)),
    p99FrameMs: Number(percentile(.99).toFixed(2)),
    framesOver50ms: times.filter(ms => ms > 50).length,
    framesOver100ms: times.filter(ms => ms > 100).length,
  }
}
