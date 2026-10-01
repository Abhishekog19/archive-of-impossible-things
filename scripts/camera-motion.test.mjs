import test from 'node:test'
import assert from 'node:assert/strict'
import RAPIER from '@dimforge/rapier3d-compat'
import { avatarOpacity, cameraClearance, cameraLensRadius, recoverCameraDistance } from '../src/player/cameraMotion.js'

await RAPIER.init()
test('camera pulls in immediately and returns smoothly independent of frame rate', () => {
  assert.equal(recoverCameraDistance(4, 0.3, 1 / 60), 0.3)
  assert.equal(recoverCameraDistance(0.3, 4, 0, true), 4)
  const simulate = hz => {
    let distance = 0.3
    for (let i = 0; i < hz; i++) distance = recoverCameraDistance(distance, 4, 1 / hz)
    return distance
  }
  assert(Math.abs(simulate(30) - simulate(144)) < 1e-10)
  assert(recoverCameraDistance(0.3, 4, 1 / 60) < 0.8)
})

test('near-camera fade is bounded and larger viewports reserve lens corners', () => {
  assert.equal(avatarOpacity(0.1), 0)
  assert.equal(avatarOpacity(4), 1)
  assert(avatarOpacity(0.8) > 0 && avatarOpacity(0.8) < 1)
  assert(cameraLensRadius(0.1, 50, 2.4) > cameraLensRadius(0.1, 50, 1))
})

test('Rapier sweep protects a lens corner even when the centre ray misses', () => {
  const world = new RAPIER.World({ x: 0, y: 0, z: 0 })
  const wall = world.createRigidBody(RAPIER.RigidBodyDesc.fixed().setTranslation(0.25, 1, 2))
  world.createCollider(RAPIER.ColliderDesc.cuboid(0.1, 1, 0.1), wall)
  const player = world.createRigidBody(RAPIER.RigidBodyDesc.fixed().setTranslation(0, 1, 0))
  world.createCollider(RAPIER.ColliderDesc.ball(0.35), player)
  world.createCollider(RAPIER.ColliderDesc.cuboid(1, 1, 0.1).setTranslation(0, 1, 0.8).setSensor(true))
  world.step()
  const origin = { x: 0, y: 1, z: 0 }, direction = { x: 0, y: 0, z: 1 }
  const flags = RAPIER.QueryFilterFlags.EXCLUDE_SENSORS
  assert.equal(world.castRay(new RAPIER.Ray(origin, direction), 4, true, flags, undefined, undefined, player), null)
  const shape = new RAPIER.Ball(cameraLensRadius(0.1, 50, 2.4))
  const allowed = cameraClearance(world, RAPIER, shape, origin, direction, 4, player)
  assert(allowed > 1 && allowed < 2)
  assert.equal(world.intersectionWithShape({ ...origin, z: allowed }, { x: 0, y: 0, z: 0, w: 1 },
    shape, flags, undefined, undefined, player), null)
  world.free()
})
