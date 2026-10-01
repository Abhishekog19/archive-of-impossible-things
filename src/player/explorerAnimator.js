import { AnimationMixer, LoopOnce, LoopRepeat } from 'three'
import { advanceAnimation, animationRate, EXPLORER_CLIPS, gaitTransitionTime, initialAnimation } from './explorerAnimation.js'
import { dampFactor } from './cameraMotion.js'

/** Presentation only: never changes the capsule or the controller's velocity. */
export function createExplorerAnimator(scene, clips, diagnostics = false) {
  const mixer = new AnimationMixer(scene)
  const actions = Object.fromEntries(clips.map(clip => {
    const action = mixer.clipAction(clip)
    const once = clip.name === 'Jump' || clip.name === 'Land'
    action.setLoop(once ? LoopOnce : LoopRepeat, once ? 1 : Infinity)
    action.clampWhenFinished = once
    return [clip.name, action]
  }))
  let motion = initialAnimation(), current = null, cadenceSpeed = 0
  const reset = () => {
    mixer.stopAllAction()
    motion = initialAnimation()
    cadenceSpeed = 0
    current = actions.Idle
    current?.reset().setEffectiveWeight(1).play()
    mixer.update(0)
  }
  reset()
  const animator = {
    reset,
    update(input, delta, preview) {
      const dt = Math.min(Math.max(delta, 0), 0.1)
      motion = advanceAnimation(motion, input, dt)
      cadenceSpeed += (input.speed - cadenceSpeed) * dampFactor(14, dt)
      const name = EXPLORER_CLIPS.includes(preview) ? preview : motion.name
      const next = actions[name]
      if (!next) return
      if (current !== next) {
        const phase = current ? gaitTransitionTime(current.getClip().name, current.time,
          current.getClip().duration, name, next.getClip().duration) : 0
        const fade = name === 'Jump' ? 0.08 : name === 'Land' ? 0.1 : 0.18
        current?.fadeOut(fade)
        next.reset().setEffectiveWeight(1).fadeIn(fade).play()
        next.time = phase
        current = next
      }
      // Both sides of a gait crossfade advance at the same normalized cycle rate.
      const rate = preview ? 1 : animationRate(name, cadenceSpeed)
      next.setEffectiveTimeScale(rate)
      if (name === 'Walk' || name === 'Run') {
        const other = actions[name === 'Walk' ? 'Run' : 'Walk']
        if (other?.isRunning()) other.setEffectiveTimeScale(rate * other.getClip().duration / next.getClip().duration)
      }
      mixer.update(dt)
    },
    snapshot: () => ({ name: current?.getClip().name, time: current?.time ?? 0,
      phase: current ? (current.time / current.getClip().duration) % 1 : 0,
      rate: current?.getEffectiveTimeScale() ?? 0, cadenceSpeed }),
    dispose() {
      mixer.stopAllAction(); mixer.uncacheRoot(scene)
      if (diagnostics) delete scene.userData.readMotion
    },
  }
  if (diagnostics) scene.userData.readMotion = animator.snapshot
  return animator
}
