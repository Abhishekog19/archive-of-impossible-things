import test from 'node:test'
import assert from 'node:assert/strict'
import { usesAssembledWorld } from '../src/config/entry.js'

test('plain links and every reference open the assembled world', () => {
  for (const query of ['', 'start=forest', 'patch=1', 'view=reference', 'view=forest',
    'view=canopy', 'view=exterior', 'view=interior', 'view=cavern']) {
    assert(usesAssembledWorld(new URLSearchParams(query)), query)
  }
})

test('explicit study and legacy links keep their original scene', () => {
  for (const scene of ['greyroom', 'kit', 'zones', 'water', 'cavern', 'hub']) {
    assert.equal(usesAssembledWorld(new URLSearchParams(`scene=${scene}&patch=1`)), false)
  }
  assert.equal(usesAssembledWorld(new URLSearchParams('patch=0')), false)
})
