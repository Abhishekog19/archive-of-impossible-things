// ecctrl 2.0.1 uses impulse coefficients, not durations, for acc/decDeltaTime.
export const MOVEMENT = {
  maxWalkVel: 3, maxRunVel: 5.4,
  enableToggleRun: false,
  accDeltaTime: 0.16, decDeltaTime: 0.24,
  rejectVelFactor: 0.65, moveImpulsePointOffset: 0,
  autoBalanceSpringOnY: 0.1, autoBalanceDampingOnY: 0.012,
  jumpVel: 4.5, jumpDuration: 0.07,
  airDragFactor: 0.08, fallingGravityScale: 1.8, fallingMaxVel: 16,
  groundDetection: 'shapeCast', slopeMaxAngle: Math.PI / 4,
  rayHitForgiveness: 0.16,
  ccd: true,
}

export const SPAWN = [0, 2, 6]
export const CORNER_SPAWN = [-8, 2, -4]
export const WORLD_SPAWNS = {
  hub: SPAWN, patch: [-12, 2.5, -20],
  forest: [-12, 3.5, -43], canopy: [-12, 3.5, -67],
  exterior: [-12, 3.5, -98], interior: [-12, 3.5, -116],
  cavern: [-12, -5.5, -174],
}

/** Only activate authored area spawns after reaching their ground level. */
export function reachedCheckpoint(position, grounded, verticalSpeed) {
  if (!grounded || Math.abs(verticalSpeed) > 0.5) return null
  return Object.values(WORLD_SPAWNS).find(([x, y, z]) =>
    Math.hypot(position.x - x, position.z - z) < 4 &&
    Math.abs(position.y - y) < 3) ?? null
}
