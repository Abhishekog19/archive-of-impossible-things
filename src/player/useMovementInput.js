import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useButtonStore, useJoystickStore } from 'ecctrl/input'
import { useGameStore } from '../store'
import { isUiTarget, resetTouchInput } from './inputState'
import { createMovementInput, KEY_MAP } from './movementInput'

const NO_JOYSTICK = { x: 0, y: 0 }
const STOP = { forward: false, backward: false, leftward: false, rightward: false,
  jump: false, run: false, joystick: NO_JOYSTICK }

export default function useMovementInput(controllerRef, active) {
  const input = useRef(null)
  const frame = useRef({ ...STOP })
  if (input.current === null) input.current = createMovementInput()

  useEffect(() => {
    const state = input.current
    const reset = () => {
      state.reset()
      resetTouchInput()
      controllerRef.current?.setMovement(STOP)
    }
    const onKey = (down) => (e) => {
      if (!KEY_MAP[e.code]) return
      if (down && e.repeat) return
      const game = useGameStore.getState()
      if (down && (!active || game.settingsOpen || game.worldLoading || isUiTarget(e.target))) return
      if (down && e.code === 'Space' && e.target instanceof Element && e.target.closest('button')) return
      if (!isUiTarget(e.target)) e.preventDefault()
      state.key(e.code, down, performance.now())
    }
    const onDown = onKey(true)
    const onUp = onKey(false)
    reset()
    window.addEventListener('keydown', onDown)
    window.addEventListener('keyup', onUp)
    window.addEventListener('blur', reset)
    document.addEventListener('visibilitychange', reset)
    const unsubscribe = useGameStore.subscribe((s, previous) => {
      if (s.settingsOpen !== previous.settingsOpen || s.worldLoading !== previous.worldLoading ||
          s.recoveryCount !== previous.recoveryCount) reset()
    })
    const unsubscribeJump = useButtonStore.subscribe(
      (s) => !!s.buttons.jump,
      (pressed) => { if (pressed && active) state.queueJump(performance.now()) },
    )
    return () => {
      reset()
      window.removeEventListener('keydown', onDown)
      window.removeEventListener('keyup', onUp)
      window.removeEventListener('blur', reset)
      document.removeEventListener('visibilitychange', reset)
      unsubscribe()
      unsubscribeJump()
    }
  }, [controllerRef, active])

  // Feed input before ecctrl's frame callback, avoiding a frame of stale movement.
  useFrame(() => {
    const c = controllerRef.current
    if (!c) return
    const s = useGameStore.getState()
    if (!active || s.settingsOpen || s.worldLoading || (document.hidden && !s.physicsForced)) {
      input.current.reset()
      c.setMovement(STOP)
      return
    }
    c.setMovement(input.current.sample(frame.current, performance.now(),
      c.isOnGround && !c.jumpActive,
      useButtonStore.getState().buttons,
      useJoystickStore.getState().joysticks.move ?? NO_JOYSTICK))
  }, -1)
}
