// Derive streaming packages from reproducible Blender exports; never rewrite originals.
import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { Document, NodeIO, Logger } from '@gltf-transform/core'
import { ALL_EXTENSIONS, EXTMeshoptCompression } from '@gltf-transform/extensions'
import { compactPrimitive, copyToDocument, dedup, prune, quantize, reorder, simplifyPrimitive, textureCompress, unpartition, weld } from '@gltf-transform/functions'
import { MeshoptEncoder, MeshoptDecoder, MeshoptSimplifier } from 'meshoptimizer'
import sharp from 'sharp'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const output = path.join(root, 'public/models/placed')
await fs.mkdir(output, { recursive: true })
await Promise.all([MeshoptEncoder.ready, MeshoptDecoder.ready, MeshoptSimplifier.ready])
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
  'meshopt.encoder': MeshoptEncoder, 'meshopt.decoder': MeshoptDecoder,
})
const sources = new Map()
async function replaceExport(target, bytes) {
  // Avoid replacing identical cloud-backed files, which may be held by sync.
  try {
    if ((await fs.readFile(target)).equals(Buffer.from(bytes))) return
  } catch (error) {
    if (error.code !== 'ENOENT') throw error
  }
  const temporary = target + '.next'
  await fs.writeFile(temporary, bytes)
  try {
    await fs.rename(temporary, target)
  } catch (error) {
    // Cloud-backed Windows files may require CopyFile rather than rename.
    if (process.platform !== 'win32' || error.code !== 'EPERM') throw error
    await fs.copyFile(temporary, target)
    await fs.unlink(temporary)
  }
}
async function source(name) {
  if (!sources.has(name)) sources.set(name, await io.read(path.join(root, 'public/models', `${name}.glb`)))
  return sources.get(name)
}
function document() { return new Document().setLogger(new Logger(Logger.Verbosity.ERROR)) }
function copy(target, from, nodes, offset) {
  for (const ext of from.getRoot().listExtensionsUsed()) target.createExtension(ext.constructor).setRequired(ext.isRequired())
  const map = copyToDocument(target, from, nodes)
  const scene = target.getRoot().listScenes()[0] || target.createScene('Scene')
  for (const node of nodes) {
    const copied = map.get(node)
    if (offset) copied.setTranslation(copied.getTranslation().map((v, i) => v + offset[i]))
    scene.addChild(copied)
  }
}
const collider = (node) => /Collision/.test(node.getName())
const triangles = (doc) => doc.getRoot().listMeshes().reduce((sum, mesh) => sum + mesh.listPrimitives()
  .reduce((n, p) => n + (p.getIndices()?.getCount() || p.getAttribute('POSITION').getCount()) / 3, 0), 0)

function splitCells(doc) {
  const scene = doc.getRoot().listScenes()[0]
  for (const node of [...scene.listChildren()]) {
    if (!node.getMesh() || collider(node) || /Prototype|Cavern|Pool/.test(node.getName())) continue
    const primitives = node.getMesh().listPrimitives()
    if (primitives.length !== 1) continue
    const original = primitives[0], positions = original.getAttribute('POSITION'), indices = original.getIndices()
    if (!indices || indices.getCount() < 1800) continue
    const cells = new Map(), point = []
    for (let i = 0; i < indices.getCount(); i += 3) {
      const tri = [indices.getScalar(i), indices.getScalar(i + 1), indices.getScalar(i + 2)]
      let x = 0, z = 0
      for (const index of tri) { positions.getElement(index, point); x += point[0] / 3; z += point[2] / 3 }
      const key = `${Math.floor(x / 24)}_${Math.floor(z / 24)}`
      if (!cells.has(key)) cells.set(key, [])
      cells.get(key).push(...tri)
    }
    if (cells.size < 2) continue
    for (const [key, list] of cells) {
      const primitive = original.clone().setIndices(doc.createAccessor().setType('SCALAR')
        .setArray(new Uint32Array(list)).setBuffer(indices.getBuffer()))
      compactPrimitive(primitive)
      const mesh = doc.createMesh().addPrimitive(primitive)
      scene.addChild(doc.createNode(`${node.getName()}_Cell_${key}`).setMesh(mesh).setMatrix(node.getMatrix()))
    }
    node.dispose()
  }
}

async function write(doc, id, simplify = true) {
  const before = triangles(doc)
  await doc.transform(weld())
  if (simplify) for (const node of doc.getRoot().listNodes()) {
    if (!node.getMesh() || collider(node)) continue
    const name = node.getName()
    // Position-limited simplification, with UV seams and silhouette borders intact.
    const terrain = /Terrain_bank/.test(name)
    const wood = /Wood|Trees/.test(name)
    if (!terrain && !wood) continue
    for (const primitive of node.getMesh().listPrimitives()) simplifyPrimitive(primitive, {
      simplifier: MeshoptSimplifier, ratio: terrain ? .18 : .45,
      error: terrain ? .0006 : .001, lockBorder: true,
    })
  }
  splitCells(doc)
  // Keep position precision and node transforms; only compact normals/colours.
  await doc.transform(quantize({ pattern: /^(NORMAL|COLOR)/, quantizeNormal: 10, quantizeColor: 8, cleanup: false }))
  // Keep texture resolution. WebP changes transfer size, not GPU texture memory.
  await doc.transform(textureCompress({ encoder: sharp, targetFormat: 'webp', quality: 92,
    slots: /baseColorTexture/, effort: 60 }), dedup(),
  prune({ keepLeaves: true, keepAttributes: true }), unpartition(), reorder({ encoder: MeshoptEncoder }))
  // Lossless geometry encoding: deliberately omit quantize(), since collider
  // coordinates and the existing world-space mesh contract must stay exact.
  doc.createExtension(EXTMeshoptCompression).setRequired(true)
    .setEncoderOptions({ method: EXTMeshoptCompression.EncoderMethod.QUANTIZE })
  const bytes = await io.writeBinary(doc)
  await replaceExport(path.join(output, `${id}.glb`), bytes)
  const entry = { url: `/models/placed/${id}.glb`, bytes: bytes.length,
    trianglesBefore: before, triangles: triangles(doc) }
  console.log(id, JSON.stringify(entry))
  return entry
}

const resident = document()
const context = await source('world-art-context')
copy(resident, context, context.getRoot().listScenes()[0].listChildren())
const finish = await source('world-finish')
copy(resident, finish, finish.getRoot().listScenes()[0].listChildren())
const boundaries = await source('hub-boundaries')
copy(resident, boundaries, boundaries.getRoot().listScenes()[0].listChildren())
// Distant crowns must remain behind streamed foregrounds, otherwise resident
// background trunks become bare poles when the neighbouring zone is absent.
const backdrop = await source('woodland-backdrop')
copy(resident, backdrop, backdrop.getRoot().listScenes()[0].listChildren())
for (const name of ['hub-corner', 'forest-patch', 'forest-approach', 'forest-canopy', 'archive-exterior', 'cavern-structure']) {
  const doc = await source(name)
  copy(resident, doc, doc.getRoot().listNodes().filter(collider), name === 'hub-corner' ? [-8, 0, -9] : undefined)
}
// Only physics positions/indices are needed on collider meshes.
for (const node of resident.getRoot().listNodes().filter(collider)) for (const p of node.getMesh().listPrimitives()) {
  p.setMaterial(null)
  for (const semantic of p.listSemantics()) if (semantic !== 'POSITION') p.setAttribute(semantic, null)
}
const manifest = { resident: await write(resident, 'resident'), zones: [] }
// Share one small stone detail tile across all outdoor baked stone surfaces.
const stone = await source('cavern-structure')
const tile = stone.getRoot().listTextures().find(t => /colour 1024/.test(t.getName()))
if (!tile) throw new Error('Cavern stone detail tile missing')
await fs.mkdir(path.join(root, 'public/textures'), { recursive: true })
await sharp(tile.getImage()).webp({ quality: 92 }).toFile(path.join(root, 'public/textures/stone-grain.webp'))
const definitions = [
  { id: 'hub', files: ['hub-art'], minZ: -23, maxZ: 35, load: 38, keep: 72, draw: 58 },
  { id: 'patch', files: ['forest-patch'], minZ: -42, maxZ: -18, load: 38, keep: 68, draw: 32 },
  { id: 'approach', files: ['forest-approach'], minZ: -68, maxZ: -38, load: 38, keep: 68, draw: 32 },
  { id: 'canopy', files: ['forest-canopy'], minZ: -100, maxZ: -63, load: 38, keep: 68, draw: 32 },
  { id: 'exterior', files: ['archive-exterior'], minZ: -131, maxZ: -92, load: 55, keep: 82, draw: 62 },
  { id: 'hall', files: ['archive-hall'], minZ: -144, maxZ: -113, load: 32, keep: 58, draw: 35 },
  { id: 'cavern', files: ['cavern-structure'], minZ: -225, maxZ: -141, load: 32, keep: 58, draw: 35 },
]
for (const zone of definitions) {
  const doc = document()
  for (const name of zone.files) {
    const from = await source(name)
    copy(doc, from, from.getRoot().listScenes()[0].listChildren().filter(n => !collider(n)))
  }
  if (zone.id === 'hub') {
    const corner = await source('hub-corner')
    copy(doc, corner, corner.getRoot().listScenes()[0].listChildren().filter(n => /Foliage|Fern/.test(n.getName())), [-8, 0, -9])
  }
  if (['approach', 'canopy'].includes(zone.id)) {
    // The old baked moss floor climbs across the bank in large triangles.
    // Remove only that overlapping outer skin where the boundary export owns
    // the new rock face; retain the source atlas, route floor and all physics.
    const ground = doc.getRoot().listNodes().find(n => n.getName() === (zone.id === 'approach' ? 'ForestApproach_Ground' : 'ForestCanopy_Ground'))
    for (const p of ground.getMesh().listPrimitives()) {
      const positions = p.getAttribute('POSITION'), indices = p.getIndices(), retained = []
      for (let i = 0; i < indices.getCount(); i += 3) {
        const triangle = [0, 1, 2].map(j => indices.getScalar(i + j))
        const points = triangle.map(index => positions.getElement(index, []))
        const covered = points.some(v => v[1] > 2.4) &&
          (points.every(v => v[0] > 4) || points.every(v => v[0] < -28))
        if (!covered) retained.push(...triangle)
      }
      p.setIndices(doc.createAccessor().setType('SCALAR').setArray(new Uint32Array(retained)).setBuffer(indices.getBuffer()))
    }
  }
  manifest.zones.push({ ...zone, ...await write(doc, zone.id) })
}
await replaceExport(path.join(root, 'src/config/placed-world.json'), JSON.stringify(manifest, null, 2) + '\n')
console.log('Total derived bytes:', manifest.resident.bytes + manifest.zones.reduce((sum, z) => sum + z.bytes, 0))
