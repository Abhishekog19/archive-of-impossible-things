import test from 'node:test'
import assert from 'node:assert/strict'
import { PlaneGeometry } from 'three'
import { updateContactPatch } from '../src/player/contactPatch.js'

const ground = height => ({ height, normal: { x: 0, y: 1, z: 0 } })
test('contact receiver follows a slope and fades through a jump', () => {
  const geometry = new PlaneGeometry(1, 1, 4, 4)
  const sample = x => ground(x * .25)
  const standing = updateContactPatch(geometry, { x: 0, y: 1.05, z: 0 }, sample, 1.05)
  const p = geometry.attributes.position
  for (let i = 0; i < p.count; i++) assert(Math.abs(p.getY(i) - p.getX(i) * .25 - .055) < 1e-6)
  assert.equal(geometry.drawRange.count, 96)
  const airborne = updateContactPatch(geometry, { x: 0, y: 2, z: 0 }, sample, 1.05)
  assert(airborne > 0 && airborne < standing)
  assert.equal(updateContactPatch(geometry, { x: 0, y: 3, z: 0 }, sample, 1.05), 0)
  geometry.dispose()
})
test('contact triangles never bridge a ledge or missing ground', () => {
  for (const sample of [x => ground(x > .2 ? -1 : 0), x => x > .2 ? null : ground(0)]) {
    const geometry = new PlaneGeometry(1, 1, 4, 4)
    updateContactPatch(geometry, { x: 0, y: 1.05, z: 0 }, sample, 1.05)
    const indices = geometry.index, p = geometry.attributes.position
    assert(indices.count < 96)
    for (let i = 0; i < indices.count; i += 3) {
      const heights = [0, 1, 2].map(j => p.getY(indices.getX(i + j)))
      assert(Math.max(...heights) - Math.min(...heights) < .32)
    }
    assert.equal(updateContactPatch(geometry, { x: 0, y: 1.05, z: 0 }, () => null, 1.05), 0)
    assert.equal(geometry.drawRange.count, 0)
    geometry.dispose()
  }
})
