// Export contract for the current baked, opaque KitBatch pipeline.
// This checks transfer integrity, not artistic quality or complete glTF validity.
const fs = require('node:fs')
const path = require('node:path')
const assert = require('node:assert/strict')
const { createHash } = require('node:crypto')
const root = path.resolve(__dirname, '..')
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'src/config/zone-packages.json')))

function readGlb(file) {
  const bytes = fs.readFileSync(file)
  assert.equal(bytes.toString('ascii', 0, 4), 'glTF', file)
  assert.equal(bytes.readUInt32LE(4), 2, file)
  assert.equal(bytes.readUInt32LE(8), bytes.length, file)
  assert.equal(bytes.readUInt32LE(16), 0x4e4f534a, file)
  const end = 20 + bytes.readUInt32LE(12)
  const json = JSON.parse(bytes.toString('utf8', 20, end))
  assert.equal(bytes.readUInt32LE(end + 4), 0x004e4942, file)
  const bin = bytes.subarray(end + 8)
  assert.equal(bin.length, bytes.readUInt32LE(end), file)
  const images = (json.images || []).map((image) => {
    assert.equal(image.uri, undefined, 'Atlas must be embedded')
    const view = json.bufferViews[image.bufferView]
    assert.equal(view.buffer, 0)
    const offset = view.byteOffset || 0
    assert(offset + view.byteLength <= bin.length, 'Atlas outside buffer')
    return createHash('sha256').update(bin.subarray(offset, offset + view.byteLength)).digest('hex')
  })
  return { json, images, bytes: bytes.length }
}

const kit = readGlb(path.join(root, 'public/models/archive-kit.glb'))
for (const [id, entry] of Object.entries(manifest.packages)) {
  assert(/^\/models\/zones\/[a-z-]+\.glb$/.test(entry.url), 'Unexpected package path')
  const zone = readGlb(path.join(root, 'public', entry.url.slice(1)))
  assert.equal(zone.bytes, entry.bytes, `${id}: stale size manifest`)
  assert.deepEqual(zone.json.nodes.map((node) => node.name).sort(), [...entry.nodes].sort(), `${id}: node manifest`)
  assert(zone.images.every((hash) => kit.images.includes(hash)), `${id}: atlas changed during split export`)
  let textured = 0, coloured = 0, colliders = 0
  for (const node of zone.json.nodes) {
    assert(Number.isInteger(node.mesh), `${node.name}: expected mesh`)
    if (node.name.startsWith('Collider_')) { colliders++; continue }
    for (const primitive of zone.json.meshes[node.mesh].primitives) {
      const material = zone.json.materials[primitive.material]
      assert(material, `${node.name}: missing material`)
      assert.equal(material.alphaMode || 'OPAQUE', 'OPAQUE', `${node.name}: transparency unsupported by KitBatch`)
      assert.equal(material.normalTexture, undefined, `${node.name}: runtime would drop normal map`)
      assert.equal(material.emissiveTexture, undefined, `${node.name}: runtime would drop emissive map`)
      const pbr = material.pbrMetallicRoughness || {}
      assert.deepEqual(pbr.baseColorFactor || [1, 1, 1, 1], [1, 1, 1, 1], `${node.name}: runtime would drop tint`)
      const texture = pbr.baseColorTexture
      if (texture) {
        assert.equal(texture.texCoord || 0, 0, `${node.name}: UV0 required`)
        assert.equal(texture.extensions, undefined, `${node.name}: texture transform needs runtime support`)
        assert(Number.isInteger(primitive.attributes.TEXCOORD_0), `${node.name}: missing UV0`)
        assert(zone.images[zone.json.textures[texture.index]?.source], `${node.name}: missing atlas`)
        textured++
      } else {
        assert(Number.isInteger(primitive.attributes.COLOR_0), `${node.name}: missing foliage colours`)
        coloured++
      }
    }
  }
  console.log(`${id}: ${zone.bytes} bytes; ${textured} textured, ${coloured} vertex-coloured meshes; ${colliders} separate colliders; atlas bytes match kit`)
}
