import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useButtonStore, useJoystickStore } from 'ecctrl/input'
import { useGameStore } from '../store'
import { isUiTarget, resetTouchInput } from './inputState'

/**
 * The input layer. This exists because ecctrl 2.x has none.
 *
 * Worth stating plainly, because the docs imply otherwise: ecctrl 2.0.1's
 * README Quick Start wraps `<Ecctrl>` in drei's `<KeyboardControls>`, but the
 * built component imports nothing keyboard-related and contains no key
 * handling — `useKeyboardControls` appears nowhere in its bundle. The 1.x
 * behaviour, where the controller read the keyboard and the camera itself, is
 * gone. In 2.x the *only* way movement enters the controller is the imperative
 * `setMovement()` handle. So this hook is not a convenience wrapper; without it
 * the character cannot move.
 *
 * That is also why it's shaped the way it is. M2 has to add a touch joystick and
 * virtual buttons, and ecctrl's `MovementInput` already accepts a `joystick`
 * field alongside the booleans. So this hook composes one frame of input from
 * however many sources exist and pushes it in a single call — meaning M2 adds a
 * source here rather than a second code path, and both inputs stay live
 * simultaneously, which is what Part C of the plan requires (touchscreen laptops
 * are real).
 */

const KEY_MAP = {
  KeyW: 'forward',
  ArrowUp: 'forward',
  KeyS: 'backward',
  ArrowDown: 'backward',
  KeyA: 'leftward',
  ArrowLeft: 'leftward',
  KeyD: 'rightward',
  ArrowRight: 'rightward',
  Space: 'jump',
  ShiftLeft: 'run',
  ShiftRight: 'run',
}
const NO_JOYSTICK = { x: 0, y: 0 }

export default function useMovementInput(controllerRef) {
  // Held keys, by action name. A ref because this changes on every keypress and
  // must never cause a React render — input at 60 Hz through useState would
  // re-render the whole tree on each footstep.
  const held = useRef({
    forward: false,
    backward: false,
    leftward: false,
    rightward: false,
    jump: false,
    run: false,
  })

  // The object handed to setMovement, reused rather than rebuilt each frame.
  // A ref, not useMemo: it is mutated every frame, and react-hooks' immutability
  // rule correctly rejects mutating a value produced during render.
  const frame = useRef({
    forward: false,
    backward: false,
    leftward: false,
    rightward: false,
    jump: false,
    run: false,
  })

  useEffect(() => {
    const onKey = (down) => (e) => {
      const action = KEY_MAP[e.code]
      if (!action) return
      if (down && (isUiTarget(e.target) || useGameStore.getState().settingsOpen)) return
      if (down && e.code === 'Space' && e.target instanceof Element && e.target.closest('button')) return
      // Space scrolls the page and arrow keys scroll it too. Harmless on a
      // locked-overflow body, but it also steals the key from a focused element,
      // which shows up later as "movement stops after clicking a button".
      e.preventDefault()
      held.current[action] = down
    }
    const onDown = onKey(true)
    const onUp = onKey(false)

    // Keys held while the tab loses focus never fire keyup, so the character
    // walks forever into a wall until you come back and tap W again.
    const onBlur = () => {
      for (const k of Object.keys(held.current)) held.current[k] = false
      resetTouchInput()
    }

    window.addEventListener('keydown', onDown)
    window.addEventListener('keyup', onUp)
    window.addEventListener('blur', onBlur)
    document.addEventListener('visibilitychange', onBlur)
    const unsubscribe = useGameStore.subscribe((state, previous) => {
      if (state.settingsOpen !== previous.settingsOpen) onBlur()
    })
    return () => {
      window.removeEventListener('keydown', onDown)
      window.removeEventListener('keyup', onUp)
      window.removeEventListener('blur', onBlur)
      document.removeEventListener('visibilitychange', onBlur)
      unsubscribe()
    }
  }, [])

  useFrame(() => {
    const controller = controllerRef.current
    if (!controller) return

    const k = held.current
    const f = frame.current
    f.forward = k.forward
    f.backward = k.backward
    f.leftward = k.leftward
    f.rightward = k.rightward
    const buttons = useButtonStore.getState().buttons
    f.jump = k.jump || !!buttons.jump
    f.run = k.run || !!buttons.run
    f.joystick = useJoystickStore.getState().joysticks.move ?? NO_JOYSTICK

    if (document.hidden || useGameStore.getState().settingsOpen) {
      f.forward = f.backward = f.leftward = f.rightward = f.jump = f.run = false
      f.joystick = NO_JOYSTICK
    }

    controller.setMovement(f)
  })

  return held
}
