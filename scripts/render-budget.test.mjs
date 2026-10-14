import test from 'node:test'
import assert from 'node:assert/strict'
import { BoxGeometry, Group, Matrix4, Mesh, MeshBasicMaterial, Vector3 } from 'three'
import { batchStaticMeshes, disposeStaticBatches } from '../src/scenes/staticBatches.js'
import { budgetAction, createFrameProbe, sampleFrameBudget, summarizeFrameTimes } from '../src/config/performance.js'

test('frame budget ignores pauses and isolated stalls, then acts with cooldown', () => {
  const probe = createFrameProbe()
  const sample = (seconds, fps, paused = false) => {
    let actions = 0
    for (let i = 0; i < seconds * 60; i++) if (sampleFrameBudget(probe, 1 / 60, fps, paused)) actions++
    return actions
  }
  assert.equal(sample(12, 10, true), 0)
  assert.equal(sampleFrameBudget(probe, 20, 1), false, 'one stall must not reduce quality')
  assert.equal(sample(4, 20), 0, 'pause recovery needs a grace period')
  assert.equal(sample(7, 40), 1)
  assert.equal(sample(7, 40), 0, 'cooldown must hold')
  assert.equal(sample(8, 60), 0, 'healthy windows must not reduce quality')
})

test('alternating fast and slow readings cannot hide a sustained undershoot', () => {
  const probe = createFrameProbe()
  for (let i = 0; i < 301; i++) sampleFrameBudget(probe, 1 / 60, 60)
  let actions = 0
  for (let i = 0; i < 330; i++) {
    const fps = Math.floor(i / 15) % 2 ? 60 : 30
    if (sampleFrameBudget(probe, 1 / 60, fps)) actions++
  }
  assert.equal(actions, 1, 'a 45 FPS window must act even with healthy spikes')
})

test('resolution falls before effects and pinned tiers never demote', () => {
  assert.equal(budgetAction(1, .75, null, 'medium'), 'resolution')
  assert.equal(budgetAction(.75, .75, null, 'medium'), 'tier')
  assert.equal(budgetAction(.75, .75, 'high', 'high'), null)
  assert.equal(budgetAction(.75, .75, null, 'low'), null)
  assert.deepEqual(summarizeFrameTimes([10, 20, 30, 60, 120]), {
    p95FrameMs: 120, p99FrameMs: 120, framesOver50ms: 2, framesOver100ms: 1,
  })
})

test('static batching preserves cell geometry, transforms, bounds and original receivers', () => {
  const root = new Group(), parent = new Group(), material = new MeshBasicMaterial()
  root.position.set(10, 0, -20); parent.position.set(1, 2, 3); root.add(parent)
  const geometry = new BoxGeometry(); geometry.clearGroups()
  const a = new Mesh(geometry, material), b = new Mesh(geometry, material)
  a.position.set(-5, 3, -10); b.position.set(7, 0, 11)
  parent.add(a, b); root.updateMatrixWorld(true)
  const expected = [a, b].map(mesh => mesh.matrixWorld.clone())
  const [batch] = batchStaticMeshes(root)
  assert(batch?.isBatchedMesh)
  assert.equal(batch.instanceCount, 2)
  assert.equal(batch.perObjectFrustumCulled, true)
  assert.equal(batch.material, material)
  root.updateMatrixWorld(true)
  for (let i = 0; i < 2; i++) {
    const matrix = new Matrix4()
    batch.getMatrixAt(i, matrix); matrix.premultiply(batch.matrixWorld)
    assert.deepEqual(matrix.elements, expected[i].elements)
    const sphere = batch.boundingSphere.clone().applyMatrix4(batch.matrixWorld)
    assert(sphere.containsPoint(new Vector3().setFromMatrixPosition(matrix)))
  }
  assert(!a.visible && a.userData.batchedSurface && !b.visible && b.userData.batchedSurface)
  let disposed = 0
  batch.geometry.addEventListener('dispose', () => disposed++)
  disposeStaticBatches(root)
  assert.equal(batch.parent, null)
  assert.equal(disposed, 1)
  assert.equal(a.geometry, geometry, 'cached original geometry remains owned by the scene')
  geometry.dispose(); material.dispose()
})

test('batching does not expose hidden parents or merge incompatible materials', () => {
  const root = new Group(), hidden = new Group()
  hidden.visible = false; root.add(hidden)
  const geometry = new BoxGeometry(); geometry.clearGroups()
  const material = new MeshBasicMaterial()
  const a = new Mesh(geometry, material), b = new Mesh(geometry, material)
  hidden.add(a, b)
  root.add(new Mesh(geometry, material), new Mesh(geometry, new MeshBasicMaterial()))
  assert.equal(batchStaticMeshes(root).length, 0)
  geometry.dispose(); material.dispose()
})
