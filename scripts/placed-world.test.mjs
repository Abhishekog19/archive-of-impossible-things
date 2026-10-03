import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { NodeIO } from '@gltf-transform/core'
import { ALL_EXTENSIONS } from '@gltf-transform/extensions'
import { MeshoptDecoder } from 'meshoptimizer'
import { BoxGeometry, Group, Matrix4, Mesh, MeshBasicMaterial, Object3D, Texture, Vector3 } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { loadPlaced, disposePlaced } from '../src/scenes/placedResource.js'
import { desiredAreas, requiredAreas } from '../src/config/placed-streaming.js'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const manifest = JSON.parse(await fs.readFile(path.join(root, 'src/config/placed-world.json')))
await MeshoptDecoder.ready
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder })
const read = name => io.read(path.join(root, 'public/models', `${name}.glb`))

test('entry loads only its area; hysteresis retains then evicts old areas', () => {
  assert.deepEqual(desiredAreas(6, manifest.zones, [], true), ['hub'])
  assert.deepEqual(desiredAreas(-195, manifest.zones, [], true), ['cavern'])
  const aroundHub = desiredAreas(-30, manifest.zones, ['hub'])
  assert(aroundHub.includes('hub') && aroundHub.includes('approach'))
  assert(!desiredAreas(-195, manifest.zones, aroundHub).includes('hub'))
  for (const z of [30, 6, -20, -55, -80, -105, -135, -170, -220]) {
    const needed = requiredAreas(z, manifest.zones)
    assert(needed.length > 0)
    for (const area of needed) assert(manifest.zones.includes(area))
  }
})

test('archive portal sightlines require hall and descent on cold entry', () => {
  for (const z of [-87, -98, -114, -135, -144]) {
    const ids = requiredAreas(z, manifest.zones).map(area => area.id)
    assert(ids.includes('hall'), `hall missing from portal view at ${z}`)
    assert(ids.includes('cavern'), `descent missing from portal view at ${z}`)
    assert.equal(new Set(ids).size, ids.length)
  }
  assert(!requiredAreas(-67, manifest.zones).some(area => area.id === 'cavern'))
  assert(!requiredAreas(6, manifest.zones).some(area => area.id === 'hall'))
})

function collisionTriangles(doc, offset = [0, 0, 0]) {
  const triangles = [], point = new Vector3(), matrix = new Matrix4(), xyz = []
  for (const node of doc.getRoot().listNodes().filter(n => /Collision/.test(n.getName()))) {
    matrix.fromArray(node.getWorldMatrix())
    for (const p of node.getMesh().listPrimitives()) {
      const positions = p.getAttribute('POSITION'), indices = p.getIndices()
      const count = indices?.getCount() || positions.getCount()
      for (let i = 0; i < count; i += 3) {
        const triangle = []
        for (let j = 0; j < 3; j++) {
          positions.getElement(indices ? indices.getScalar(i + j) : i + j, xyz)
          point.fromArray(xyz).applyMatrix4(matrix)
          triangle.push(point.toArray().map((v, k) => (v + offset[k]).toFixed(5)).join(','))
        }
        triangles.push(triangle.sort().join(';'))
      }
    }
  }
  return triangles
}

test('resident collision exactly preserves all authored source boundaries', async () => {
  const expected = []
  for (const name of ['world-art-context', 'hub-corner', 'forest-patch', 'forest-approach', 'forest-canopy', 'cavern-structure']) {
    expected.push(...collisionTriangles(await read(name), name === 'hub-corner' ? [-8, 0, -9] : undefined))
  }
  const actual = collisionTriangles(await read('placed/resident'))
  const hash = list => createHash('sha256').update(list.sort().join('|')).digest('hex')
  assert.equal(actual.length, expected.length)
  assert.equal(hash(actual), hash(expected))
})

test('all compressed packages decode, match manifest and retain required nodes', async () => {
  for (const area of [manifest.resident, ...manifest.zones]) {
    const file = path.join(root, 'public', area.url)
    assert.equal((await fs.stat(file)).size, area.bytes)
    const doc = await io.read(file)
    assert(doc.getRoot().listMeshes().length > 0)
    if (area.id) assert.equal(doc.getRoot().listNodes().filter(n => /Collision/.test(n.getName())).length, 0)
    if (area.id === 'cavern') {
      for (const name of ['CavernStructure_Rock', 'Cavern_Oculus']) assert(doc.getRoot().listNodes().some(n => n.getName() === name))
    }
    const sourceName = { hub: 'hub-art', approach: 'forest-approach', canopy: 'forest-canopy' }[area.id]
    if (sourceName) {
      const source = await read(sourceName)
      const markers = d => d.getRoot().listNodes().filter(n => /^(HubPlant_|ApproachPlant_)/.test(n.getName())).map(n => n.getName()).sort()
      assert.deepEqual(markers(doc), markers(source))
    }
  }
})

test('streamed resource preserves marker transforms and releases owned GPU resources', async t => {
  const scene = new Group()
  const template = new Mesh(new BoxGeometry(), new MeshBasicMaterial())
  template.name = 'FernPrototype'; scene.add(template)
  const marker = new Object3D(); marker.name = 'GroundFern_001'; marker.position.set(-8, 2, -9); scene.add(marker)
  const stone = new Mesh(new BoxGeometry(), new MeshBasicMaterial({ map: new Texture() }))
  stone.name = 'ArchiveHall_Walls_Cell_0_0'; scene.add(stone)
  let textureDisposed = false, geometryDisposed = false, instanceDisposed = false
  stone.material.map.addEventListener('dispose', () => { textureDisposed = true })
  stone.geometry.addEventListener('dispose', () => { geometryDisposed = true })
  t.mock.method(globalThis, 'fetch', async () => ({ ok: true, arrayBuffer: async () => new ArrayBuffer(0) }))
  t.mock.method(GLTFLoader.prototype, 'parseAsync', async () => ({ scene }))
  const resource = await loadPlaced('/test.glb', new AbortController().signal, 4, new Texture())
  const instances = scene.children.find(n => n.isInstancedMesh)
  const matrix = new Matrix4(); instances.getMatrixAt(0, matrix)
  assert.deepEqual(new Vector3().setFromMatrixPosition(matrix).toArray(), [-8, 2, -9])
  assert.equal(template.visible, false)
  assert.equal(stone.material.customProgramCacheKey(), 'world-stone-detail-v1')
  instances.addEventListener('dispose', () => { instanceDisposed = true })
  disposePlaced(resource.scene)
  assert(textureDisposed && geometryDisposed && instanceDisposed)
})

test('failed/aborted requests never deliver a live scene', async t => {
  t.mock.method(globalThis, 'fetch', async () => ({ ok: false, status: 503 }))
  await assert.rejects(loadPlaced('/failed.glb', new AbortController().signal, 1, null), /503/)
  const scene = new Group(), mesh = new Mesh(new BoxGeometry(), new MeshBasicMaterial())
  scene.add(mesh)
  let disposed = false; mesh.geometry.addEventListener('dispose', () => { disposed = true })
  const controller = new AbortController()
  t.mock.method(globalThis, 'fetch', async () => ({ ok: true, arrayBuffer: async () => new ArrayBuffer(0) }))
  t.mock.method(GLTFLoader.prototype, 'parseAsync', async () => { controller.abort(); return { scene } })
  await assert.rejects(loadPlaced('/aborted.glb', controller.signal, 1, null), { name: 'AbortError' })
  assert(disposed)
})
