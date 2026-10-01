import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import { Vector3 } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { createExplorerAnimator } from '../src/player/explorerAnimator.js'
import { createExplorerDynamics, solveLeg, stepSpring } from '../src/player/explorerDynamics.js'

const bytes = await fs.readFile(new URL('../public/models/explorer.glb', import.meta.url))
const asset = await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '')
const make = (ground = () => ({ height: 0, normal: new Vector3(0, 1, 0) })) => {
  const scene = clone(asset.scene), animator = createExplorerAnimator(scene, asset.animations)
  const dynamics = createExplorerDynamics(scene, ground, true)
  return { scene, animator, dynamics, tick(speed = 0, grounded = true, dt = 1 / 60) {
    scene.position.z += speed * dt
    animator.update({ grounded, speed, verticalSpeed: 0 }, dt)
    dynamics.update({ grounded, velocity: { x: 0, y: 0, z: speed }, gait: animator.snapshot() }, dt)
    return dynamics.snapshot()
  }, dispose() { animator.dispose(); dynamics.dispose(); scene.traverse(n => { if (n.isSkinnedMesh) n.skeleton.dispose() }) } }
}

test('leg solver preserves bone lengths at reachable and unreachable targets', () => {
  for (const target of [new Vector3(.1, .15, .2), new Vector3(0, -2, 0), new Vector3(0, .86, 0)]) {
    const hip = new Vector3(0, .86, 0)
    const pose = solveLeg(hip, target, new Vector3(0, 0, 1), .385, .32)
    assert(Math.abs(hip.distanceTo(pose.knee) - .385) < 1e-5)
    assert(Math.abs(pose.knee.distanceTo(pose.ankle) - .32) < 1e-5)
  }
})

test('springs remain bounded through a long frame and settle without residual energy', () => {
  const state = { angle: 0, velocity: 0 }
  for (let i = 0; i < 30; i++) stepSpring(state, i % 2 ? 20 : -20, .1)
  assert(Math.abs(state.angle) <= .5)
  for (let i = 0; i < 600; i++) stepSpring(state, 0, 1 / 60)
  assert(Math.abs(state.angle) < 1e-6 && Math.abs(state.velocity) < 1e-6)
})

test('exported rig plants idle feet on a slope, releases in air and resets safely', () => {
  const rig = make(p => ({ height: p.x * .2, normal: new Vector3(-.2, 1, 0).normalize() }))
  let state
  for (let i = 0; i < 90; i++) state = rig.tick()
  assert.equal(state.contacts, 2)
  assert(state.footError < .01, JSON.stringify(state))
  assert.equal(state.joints, 8)
  state = rig.tick(0, false)
  assert.equal(state.contacts, 0)
  rig.dynamics.reset()
  assert.equal(rig.dynamics.snapshot().springEnergy, 0)
  rig.dispose()
  assert.equal(rig.scene.userData.readDynamics, undefined)
})

test('walk, run, abrupt turns, braking and recovery keep the actual rig finite', () => {
  const rig = make()
  let error = 0
  for (let i = 0; i < 360; i++) {
    if (i === 100) rig.scene.rotation.y = Math.PI / 2
    const state = rig.tick(i < 100 ? 3 : i < 200 ? 5.4 : 0)
    if (i > 20) error = Math.max(error, state.footError)
    rig.scene.traverse(n => { if (n.isBone) assert([...n.position, ...n.quaternion].every(Number.isFinite)) })
    assert(state.deflection <= .65)
  }
  assert(error < .06, `maximum reach correction ${error}`)
  assert(rig.dynamics.snapshot().springEnergy < .01)
  rig.scene.position.z += 20
  assert(rig.tick().footError < .01)
  rig.dispose()
})
