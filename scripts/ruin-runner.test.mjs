import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import { Vector3 } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { createExplorerAnimator } from '../src/player/explorerAnimator.js'
import { createExplorerDynamics } from '../src/player/explorerDynamics.js'

const bytes = await fs.readFile(new URL('../public/models/ruin-runner.glb', import.meta.url))
const jsonLength = bytes.readUInt32LE(12)
const source = JSON.parse(bytes.subarray(20, 20 + jsonLength).toString())
const document = structuredClone(source)
// Node has no image decoder. Preserve the actual mesh/skin/animation buffers;
// browser review verifies textures. This avoids mocking the skeleton itself.
for (const m of document.materials) {
  delete m.normalTexture; delete m.occlusionTexture; delete m.emissiveTexture
  delete m.pbrMetallicRoughness.baseColorTexture
  delete m.pbrMetallicRoughness.metallicRoughnessTexture
}
delete document.images; delete document.textures
// Repack the JSON chunk so Three can use the embedded BIN without Node fetch.
const json = Buffer.from(JSON.stringify(document))
const padded = Buffer.alloc(Math.ceil(json.length/4)*4,0x20); json.copy(padded)
const bin = bytes.subarray(20 + jsonLength)
const packed = Buffer.alloc(20 + padded.length + bin.length)
bytes.copy(packed,0,0,12); packed.writeUInt32LE(packed.length,8)
packed.writeUInt32LE(padded.length,12); packed.writeUInt32LE(0x4e4f534a,16)
padded.copy(packed,20); bin.copy(packed,20+padded.length)
const asset = await new GLTFLoader().parseAsync(packed.buffer.slice(packed.byteOffset,packed.byteOffset+packed.byteLength), '')

test('replacement carries six clips, fitted secondary joints, textures and normalized weights', () => {
  assert.deepEqual(asset.animations.map(c => c.name).sort(), ['Fall','Idle','Jump','Land','Run','Walk'])
  assert(source.materials.filter(m => m.normalTexture).length >= 4)
  let vertices = 0
  const influenced = new Set()
  asset.scene.traverse(n => {
    if (!n.isSkinnedMesh) return
    const w = n.geometry.attributes.skinWeight, index = n.geometry.attributes.skinIndex
    vertices += w.count
    for (let i = 0; i < w.count; i++) {
      let sum = 0
      for (let j = 0; j < 4; j++) {
        const weight = w.getComponent(i,j); sum += weight
        if (weight > .01) influenced.add(n.skeleton.bones[index.getComponent(i,j)].name)
      }
      assert(Math.abs(sum - 1) < .001)
    }
  })
  assert(vertices > 10000)
  for (const joint of ['Cape','CapeTip','Hem_L','Hem_R','Hair','Rope','Satchel']) assert(influenced.has(joint), joint)
})

test('replacement skin stays finite during locomotion, jump, sharp turn, landing and reset', () => {
  const scene = clone(asset.scene)
  const animator = createExplorerAnimator(scene, asset.animations)
  const dynamics = createExplorerDynamics(scene, p => ({height:p.x*.12, normal:new Vector3(-.12,1,0).normalize()}))
  let maxError = 0
  for (let frame = 0; frame < 480; frame++) {
    const speed = frame < 80 ? 0 : frame < 180 ? 3 : frame < 280 ? 5.4 : 0
    const grounded = frame < 220 || frame > 250
    if (frame === 170) scene.rotation.y = Math.PI/2
    scene.position.z += speed/60
    animator.update({grounded,speed,verticalSpeed:frame<235?3:-3},1/60)
    dynamics.update({grounded,velocity:{x:0,y:0,z:speed},gait:animator.snapshot()},1/60)
    scene.updateMatrixWorld(true)
    if (frame > 20) maxError = Math.max(maxError,dynamics.snapshot().footError)
    scene.traverse(n => {
      if (!n.isSkinnedMesh || frame % 30) return
      n.skeleton.update()
      const count = n.geometry.attributes.position.count
      for (let i=0;i<count;i+=Math.max(1,Math.floor(count/50))) {
        const p = n.getVertexPosition(i,new Vector3())
        assert([...p].every(Number.isFinite))
        assert(p.length() < 3, 'skin escaped the character bounds')
      }
    })
  }
  assert(maxError < .07, `foot reach error ${maxError}`)
  assert.equal(dynamics.snapshot().contacts,2)
  dynamics.reset()
  assert.equal(dynamics.snapshot().springEnergy,0)
  animator.dispose(); dynamics.dispose()
})
