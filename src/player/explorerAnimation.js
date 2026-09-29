export const EXPLORER_CLIPS = ['Idle', 'Walk', 'Run', 'Jump', 'Fall', 'Land']

export function initialAnimation() {
  return { name: 'Idle', airTime: 0, landTime: 0 }
}

// Brief missed ground rays on uneven paving should not flicker into a fall pose.
export function advanceAnimation(previous, { grounded, speed, verticalSpeed }, delta) {
  const dt = Math.min(Math.max(delta, 0), .1)
  if (!grounded) {
    const airTime = previous.airTime + dt
    const name = verticalSpeed > .35 ? 'Jump' : airTime > .09 ? 'Fall' : previous.name
    return { name, airTime, landTime: 0 }
  }
  const landTime = previous.airTime > .1 ? .26 : Math.max(0, previous.landTime - dt)
  if (landTime > (speed > .2 ? .14 : 0)) return { name: 'Land', airTime: 0, landTime }
  const runThreshold = previous.name === 'Run' ? 3.8 : 4.2
  return { name: speed > runThreshold ? 'Run' : speed > .18 ? 'Walk' : 'Idle', airTime: 0, landTime }
}

export function animationRate(name, speed) {
  return name === 'Walk' ? Math.max(.55, Math.min(2.25, speed / 1.4))
    : name === 'Run' ? Math.max(.75, Math.min(1.7, speed / 3.6)) : 1
}
