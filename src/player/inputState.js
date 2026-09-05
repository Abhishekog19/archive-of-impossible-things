import { useButtonStore, useJoystickStore } from 'ecctrl/input'

export function resetTouchInput() {
  useJoystickStore.getState().resetJoystick('move')
  useButtonStore.getState().resetAllButtons()
}

export function isUiTarget(target) {
  return target instanceof Element && !!target.closest('button, select, input, textarea, dialog, [contenteditable="true"]')
}
