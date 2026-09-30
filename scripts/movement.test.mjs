import test from 'node:test'
import assert from 'node:assert/strict'
import { createMovementInput } from '../src/player/movementInput.js'
import { reachedCheckpoint, WORLD_SPAWNS } from '../src/player/movement.js'

const sample = (input, now, grounded = true) => input.sample({}, now, grounded, {}, { x: 0, y: 0 })

test('releasing one physical key preserves the other binding', () => {
  const input = createMovementInput()
  for (const code of ['KeyW', 'ArrowUp', 'ShiftLeft', 'ShiftRight']) input.key(code, true, 0)
  input.key('KeyW', false, 10)
  input.key('ShiftLeft', false, 10)
  assert.equal(sample(input, 10).forward, true)
  assert.equal(sample(input, 10).run, true)
  input.key('ArrowUp', false, 20)
  input.key('ShiftRight', false, 20)
  assert.equal(sample(input, 20).forward, false)
  assert.equal(sample(input, 20).run, false)
})

test('quick jump tap survives until landing, fires once, expires if too early', () => {
  const input = createMovementInput()
  input.key('Space', true, 0)
  input.key('Space', false, 1)
  assert.equal(sample(input, 50, false).jump, false)
  assert.equal(sample(input, 100).jump, true)
  assert.equal(sample(input, 110).jump, false)
  input.key('Space', true, 200)
  assert.equal(sample(input, 321).jump, false)
})

test('holding jump and keyboard autorepeat never requeue a landing jump', () => {
  const input = createMovementInput()
  input.key('Space', true, 0)
  assert.equal(sample(input, 1).jump, true)
  input.key('Space', true, 500)
  assert.equal(sample(input, 510).jump, false)
  input.key('Space', false, 520)
  input.key('Space', true, 530)
  assert.equal(sample(input, 540).jump, true)
})

test('pause, focus loss or recovery reset clears held movement and queued jump', () => {
  const input = createMovementInput()
  input.key('KeyW', true, 0)
  input.queueJump(0)
  input.reset()
  assert.equal(sample(input, 10).forward, false)
  assert.equal(sample(input, 10).jump, false)
})

test('checkpoints require nearby grounded traversal at the correct elevation', () => {
  const p = { x: -12, y: -6.5, z: -174 }
  assert.deepEqual(reachedCheckpoint(p, true, 0), WORLD_SPAWNS.cavern)
  assert.equal(reachedCheckpoint(p, false, 0), null)
  assert.equal(reachedCheckpoint(p, true, -5), null)
  assert.equal(reachedCheckpoint({ ...p, y: 2 }, true, 0), null)
  assert.equal(reachedCheckpoint({ ...p, x: 0 }, true, 0), null)
})
