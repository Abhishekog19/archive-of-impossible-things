import test from 'node:test'
import assert from 'node:assert/strict'
import { cavernWaterView } from '../src/config/cavern-water-view.js'

const pool = { x: -12, y: -7.6, z: -195 }
test('archive and hall portals retain water without a reflection render', () => {
  for (const [x, y, z] of [[-12, 8, -87], [-14, 4.5, -116], [-12, 3.4, -136]]) {
    assert.deepEqual(cavernWaterView({ x, y, z }, pool, true), { visible: true, reflect: false })
  }
})
test('reflection resumes inside the cavern while unrelated outdoor views omit water', () => {
  assert.deepEqual(cavernWaterView({ x: -27, y: -5.9, z: -181 }, pool, true), { visible: true, reflect: true })
  for (const camera of [{ x: 0, y: 3, z: 6 }, { x: -12, y: 4, z: -67 }, { x: -12, y: 30, z: -195 }]) {
    assert.deepEqual(cavernWaterView(camera, pool, true), { visible: false, reflect: false })
  }
})
