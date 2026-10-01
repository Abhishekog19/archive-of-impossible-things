export const EXPLORER_CLIPS = ['Idle', 'Walk', 'Run', 'Jump', 'Fall', 'Land']

export function initialAnimation() {
  return { name: 'Idle', airTime: 0, landTime: 0, fallSpeed: 0, hasGrounded: false }
}

// Brief missed ground rays on uneven paving should not flicker into a fall pose.
export function advanceAnimation(previous, { grounded, speed, verticalSpeed }, delta) {
  const dt = Math.min(Math.max(delta, 0), .1)
  if (!grounded) {
    const airTime = previous.airTime + dt
    const name = verticalSpeed > .35 && airTime > .035 ? 'Jump' : airTime > .09 ? 'Fall' : previous.name
    return { name, airTime, landTime: 0, fallSpeed: Math.min(previous.fallSpeed, verticalSpeed), hasGrounded: previous.hasGrounded }
  }
  const landTime = previous.hasGrounded && previous.airTime > .1 && previous.fallSpeed < -1.5
    ? .26 : Math.max(0, previous.landTime - dt)
  const groundedState = { airTime: 0, landTime, fallSpeed: 0, hasGrounded: true }
  if (landTime > (speed > .2 ? .14 : 0)) return { ...groundedState, name: 'Land' }
  const runThreshold = previous.name === 'Run' ? 3.8 : 4.2
  const walkThreshold = previous.name === 'Walk' ? .12 : .22
  return { ...groundedState, name: speed > runThreshold ? 'Run' : speed > walkThreshold ? 'Walk' : 'Idle' }
}

export function animationRate(name, speed) {
  return name === 'Walk' ? Math.max(0, Math.min(2.25, speed / 1.4))
    : name === 'Run' ? Math.max(.75, Math.min(2.25, speed / (1.8 / .7))) : 1
}

/** Preserve the planted/swing leg when crossing between gait clips. */
export function gaitTransitionTime(previousName, previousTime, previousDuration, nextName, nextDuration) {
  return ['Walk', 'Run'].includes(previousName) && ['Walk', 'Run'].includes(nextName)
    ? (previousTime / previousDuration % 1) * nextDuration : 0
}
