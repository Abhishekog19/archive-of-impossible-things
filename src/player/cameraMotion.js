import { CAMERA } from '../config/look.js'

export const CAMERA_RETURN_RATE = 7
export const CAMERA_FADE_NEAR = 0.45
export const CAMERA_FADE_FAR = 1.15

export const dampFactor = (rate, dt) => 1 - Math.exp(-rate * Math.min(Math.max(dt, 0), 0.1))

/** Pull in immediately for safety; ease out only while the path remains clear. */
export function recoverCameraDistance(previous, allowed, dt, snap = false) {
  return snap || allowed < previous ? allowed
    : previous + (allowed - previous) * dampFactor(CAMERA_RETURN_RATE, dt)
}

export function avatarOpacity(distance) {
  const t = Math.max(0, Math.min(1, (distance - CAMERA_FADE_NEAR) / (CAMERA_FADE_FAR - CAMERA_FADE_NEAR)))
  return t * t * (3 - 2 * t)
}

// A sphere enclosing the near plane also protects its corners at wide aspects.
export function cameraLensRadius(near, fov, aspect) {
  const halfHeight = near * Math.tan(fov * Math.PI / 360)
  return Math.hypot(near, halfHeight, halfHeight * aspect) + 0.03
}

const IDENTITY = { x: 0, y: 0, z: 0, w: 1 }
export function cameraClearance(world, rapier, shape, origin, direction, length, body) {
  const hit = world.castShape(origin, IDENTITY, direction, shape, 0, length, true,
    rapier.QueryFilterFlags.EXCLUDE_SENSORS, undefined, undefined, body)
  return hit ? Math.max(0, hit.time_of_impact - CAMERA.collisionMargin) : length
}
