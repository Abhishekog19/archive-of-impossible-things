import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { TIERS } from '../config/look'
import { PROBE } from '../config/tiers'
import { useGameStore } from '../store'
import { perf } from './perf'

/**
 * Enforces the tier policy at runtime. Lives inside the Canvas because it owns
 * the camera's far plane; the DPR itself flows through React (App computes it
 * from tier + dprDrop and passes it to <Canvas dpr>), so there is exactly one
 * authority for resolution and no fight between a prop and an imperative call.
 *
 * The rules it implements are numbered in config/tiers.js. In short: after a
 * grace period, fps continuously below the tier's floor for WINDOW seconds
 * demotes one tier (rule 2/3); on Low, or under a user override, it sheds DPR
 * instead (rules 4/5). Every action is followed by a cooldown, and hidden-tab
 * frames are discarded -- the visibility pause makes their deltas meaningless.
 */
export default function TierGovernor() {
  const tier = useGameStore((s) => s.tier)
  const tierOverride = useGameStore((s) => s.tierOverride)
  const demoteTier = useGameStore((s) => s.demoteTier)
  const shedDpr = useGameStore((s) => s.shedDpr)

  const clock = useRef(0)
  const badTime = useRef(0)
  const holdUntil = useRef(PROBE.graceSeconds)
  const skipFrame = useRef(false)

  useEffect(() => {
    const reset = () => {
      badTime.current = 0
      holdUntil.current = clock.current + PROBE.graceSeconds
      skipFrame.current = true
    }
    reset()
    document.addEventListener('visibilitychange', reset)
    const unsubscribe = useGameStore.subscribe((state, previous) => {
      if (state.settingsOpen !== previous.settingsOpen) reset()
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
    const far = TIERS[tier].far
    if (state.camera.far !== far) {
      state.camera.far = far
      state.camera.updateProjectionMatrix()
    }

    // A hidden tab pauses physics and rAF; whatever perf.fps says around that
    // boundary is about the pause, not the device.
    if (document.hidden || useGameStore.getState().settingsOpen || skipFrame.current) {
      badTime.current = 0
      skipFrame.current = false
      return
    }
    clock.current += delta
    if (clock.current < holdUntil.current) return

    const fps = perf.fps
    if (fps <= 0) return // probe not warmed up yet

    const floor = PROBE.demoteBelow[tier]
    if (fps < floor) {
      badTime.current += delta
    } else if (fps > floor + PROBE.recoverMargin) {
      // Healthy by a clear margin: the dip ended. Readings inside the band
      // neither charge nor reset, so hovering at the floor still accumulates.
      badTime.current = 0
    }

    if (badTime.current < PROBE.windowSeconds) return

    // Sustained undershoot -- act once, then hold judgement while the scene
    // settles at its new cost.
    badTime.current = 0
    holdUntil.current = clock.current + PROBE.cooldownSeconds

    if (tierOverride || tier === 'low') {
      shedDpr() // rules 4 and 5: nothing coarser left to cut, or tier pinned
    } else {
      demoteTier()
    }
  })

  return null
}
