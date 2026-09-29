import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import { AnimationMixer, Box3, Vector3 } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { EXPLORER_CLIPS, advanceAnimation, animationRate, initialAnimation } from '../src/player/explorerAnimation.js'

const bytes = await fs.readFile(new URL('../public/models/explorer.glb', import.meta.url))
const asset = await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '')
const sample = (grounded, speed = 0, verticalSpeed = 0) => ({ grounded, speed, verticalSpeed })

test('locomotion handles short ground misses, a jump/fall/land, then returns to idle', () => {
  let state = initialAnimation()
  state = advanceAnimation(state, sample(false), .04)
  assert.equal(state.name, 'Idle')
  state = advanceAnimation(state, sample(true), .016)
  assert.equal(state.name, 'Idle')
  state = advanceAnimation(state, sample(false, 2, 3), .08)
  assert.equal(state.name, 'Jump')
  state = advanceAnimation(state, sample(false, 2, -1), .08)
  assert.equal(state.name, 'Fall')
  state = advanceAnimation(state, sample(true), .016)
  assert.equal(state.name, 'Land')
  for (let n=0;n<20;n++) state=advanceAnimation(state,sample(true),.016)
  assert.equal(state.name, 'Idle')
})

test('speed thresholds have run hysteresis and cadence stays bounded', () => {
  let state=advanceAnimation(initialAnimation(),sample(true,3),.016)
  assert.equal(state.name,'Walk')
  state=advanceAnimation(state,sample(true,5),.016)
  assert.equal(state.name,'Run')
  assert.equal(advanceAnimation(state,sample(true,4),.016).name,'Run')
  assert.equal(advanceAnimation(state,sample(true,3.5),.016).name,'Walk')
  assert.equal(animationRate('Walk',100),2.25)
  assert.equal(animationRate('Land',100),1)
})

test('export supplies six named clips, one material/skin, normalized weights and metre scale', () => {
  assert.deepEqual(asset.animations.map(a=>a.name).sort(),[...EXPLORER_CLIPS].sort())
  const meshes=[];asset.scene.traverse(n=>{if(n.isMesh)meshes.push(n)})
  assert.equal(meshes.length,1)
  const mesh=meshes[0]
  assert(mesh.isSkinnedMesh)
  assert.equal(mesh.skeleton.bones.length,17)
  assert(!Array.isArray(mesh.material))
  const weights=mesh.geometry.attributes.skinWeight
  for(let i=0;i<weights.count;i++) assert(Math.abs(weights.getX(i)+weights.getY(i)+weights.getZ(i)+weights.getW(i)-1)<.001)
  asset.scene.updateMatrixWorld(true)
  const bounds=new Box3().setFromObject(asset.scene),size=bounds.getSize(new Vector3())
  assert(Math.abs(bounds.min.y)<.015)
  assert(Math.abs(size.y-1.7)<.015)
  assert(size.x<.75 && size.z<.6)
  assert(bytes.length<750_000)
})

test('all exported clips deform an independent skeleton without root travel or invalid vertices', () => {
  const scene=clone(asset.scene),mixer=new AnimationMixer(scene)
  let mesh;scene.traverse(n=>{if(n.isSkinnedMesh)mesh=n})
  assert.notEqual(mesh.skeleton.bones[0],asset.scene.getObjectByName('Explorer').skeleton.bones[0])
  const vertex=new Vector3(),bounds=new Box3()
  for(const clip of asset.animations){
    const action=mixer.clipAction(clip).play()
    for(const t of [.15,.5,.85]){
      mixer.setTime(clip.duration*t);scene.updateMatrixWorld(true);mesh.skeleton.update();bounds.makeEmpty()
      for(let i=0;i<mesh.geometry.attributes.position.count;i++){
        mesh.getVertexPosition(i,vertex).applyMatrix4(mesh.matrixWorld)
        assert(vertex.toArray().every(Number.isFinite),clip.name)
        bounds.expandByPoint(vertex)
      }
      assert(bounds.min.y>-.16 && bounds.max.y<1.9,clip.name+' vertical bounds')
      assert(Math.abs(bounds.getCenter(vertex).z)<.35,clip.name+' must stay in place')
    }
    action.stop()
  }
  mixer.stopAllAction();mixer.uncacheRoot(scene);mesh.skeleton.dispose()
})
