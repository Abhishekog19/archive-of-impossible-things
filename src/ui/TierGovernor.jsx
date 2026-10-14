import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { TIERS } from '../config/look'
import { PROBE, effectiveDpr } from '../config/tiers'
import { createFrameProbe, sampleFrameBudget, budgetAction } from '../config/performance'
import { useGameStore } from '../store'
import { perf } from './perf'

/**
 * Enforces the tier policy at runtime. Lives inside the Canvas because it owns
 * the camera's far plane; the DPR itself flows through React (App computes it
 * from tier + dprDrop and passes it to <Canvas dpr>), so there is exactly one
 * authority for resolution and no fight between a prop and an imperative call.
 *
 * The rules it implements are numbered in config/tiers.js. In short: after a
 * grace period, sustained FPS below 50 sheds resolution, then reduces effects
 * if automatic quality is already at the DPR floor. Every action has a cooldown; hidden-tab
 * frames are discarded -- the visibility pause makes their deltas meaningless.
 */
export default function TierGovernor({ farOverride }) {
  const tier = useGameStore((s) => s.tier)
  const tierOverride = useGameStore((s) => s.tierOverride)
  const demoteTier = useGameStore((s) => s.demoteTier)
  const shedDpr = useGameStore((s) => s.shedDpr)

  const probe = useRef(createFrameProbe())
  const skipFrame = useRef(false)

  useEffect(() => {
    const reset = () => {
      probe.current = createFrameProbe()
      skipFrame.current = true
    }
    reset()
    document.addEventListener('visibilitychange', reset)
    const unsubscribe = useGameStore.subscribe((state, previous) => {
      if (state.settingsOpen !== previous.settingsOpen || state.worldLoading !== previous.worldLoading) reset()
    })
    return () => { document.removeEventListener('visibilitychange', reset); unsubscribe() }
  }, [tier, tierOverride])

  useFrame((state, delta) => {

    // The far plane is a tier value (matched to where fog reaches ~95% opacity,
    // look-target section 5), so it moves with the tier. R3F only applies the
    // camera prop on mount; afterwards the projection is ours to maintain --
    // and per-frame mutation belongs here, not in an effect. The camera comes
    // from the frame state rather than useThree so nothing returned by a hook
    // is written to (react-hooks/immutability).
    const far = farOverride ?? TIERS[tier].far
    if (state.camera.far !== far) {
      state.camera.far = far
      state.camera.updateProjectionMatrix()
    }

    // A hidden tab pauses physics and rAF; whatever perf.fps says around that
    // boundary is about the pause, not the device.
    const game = useGameStore.getState()
    const paused = document.hidden || game.settingsOpen || game.worldLoading || game.physicsForced || skipFrame.current
    skipFrame.current = false
    if (!sampleFrameBudget(probe.current, delta, perf.fps, paused)) return
    const action = budgetAction(effectiveDpr(tier, game.dprDrop), PROBE.dprFloor, tierOverride, tier)
    if (action === 'resolution') shedDpr()
    else if (action === 'tier') demoteTier()
  })

  return null
}
