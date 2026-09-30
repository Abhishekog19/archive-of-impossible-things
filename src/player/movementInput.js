export const KEY_MAP = {
  KeyW: 'forward', ArrowUp: 'forward', KeyS: 'backward', ArrowDown: 'backward',
  KeyA: 'leftward', ArrowLeft: 'leftward', KeyD: 'rightward', ArrowRight: 'rightward',
  Space: 'jump', ShiftLeft: 'run', ShiftRight: 'run',
}

/** Physical keys stay independent; a jump is a press, never keyboard autorepeat. */
export function createMovementInput() {
  const keys = new Set()
  let jumpUntil = -Infinity
  return {
    key(code, down, now) {
      if (!KEY_MAP[code]) return
      if (down) {
        if (code === 'Space' && !keys.has(code)) jumpUntil = now + 120
        keys.add(code)
      } else keys.delete(code)
    },
    queueJump(now) { jumpUntil = now + 120 },
    reset() { keys.clear(); jumpUntil = -Infinity },
    sample(out, now, canJump, buttons, joystick) {
      out.forward = keys.has('KeyW') || keys.has('ArrowUp')
      out.backward = keys.has('KeyS') || keys.has('ArrowDown')
      out.leftward = keys.has('KeyA') || keys.has('ArrowLeft')
      out.rightward = keys.has('KeyD') || keys.has('ArrowRight')
      out.run = keys.has('ShiftLeft') || keys.has('ShiftRight') || !!buttons.run
      out.jump = canJump && now <= jumpUntil
      if (out.jump) jumpUntil = -Infinity
      out.joystick = joystick
      return out
    },
  }
}
