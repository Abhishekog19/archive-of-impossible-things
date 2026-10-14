import { DoubleSide, InstancedMesh, MeshBasicMaterial } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js'
import { disposeZone } from './zoneResource.js'
import { addBarkDetail, addStoneDetail } from './stoneDetail.js'
import { addOutdoorLighting } from './outdoorLighting.js'
import { shorelineLayer } from './cavernMaterial.js'
import { batchStaticMeshes, disposeStaticBatches } from './staticBatches.js'

// GLTFLoader uses decodeGltfBufferAsync, but without a worker that API still
// decompresses on the render thread. One shared worker bounds CPU/memory use.
if (typeof Worker !== 'undefined' && MeshoptDecoder.supported) {
  // This decoder API is not a React hook despite its upstream name.
  const configureWorkers = MeshoptDecoder.useWorkers
  try { configureWorkers(1) }
  catch { configureWorkers(0) } // Retain loading on browsers/CSPs without workers.
}

export async function loadPlaced(url, signal, anisotropy, detail, cavern = false, onStage = () => {}, batching = true) {
  onStage('download')
  const response = await fetch(url, { signal })
  if (!response.ok) throw new Error(`Area request failed (${response.status})`)
  const data = await response.arrayBuffer()
  signal.throwIfAborted()
  onStage('decode')
  const gltf = await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(data, '/models/placed/')
  if (signal.aborted) { disposeZone(gltf.scene); signal.throwIfAborted() }
  gltf.scene.updateMatrixWorld(true)
  const nodes = {}, converted = new Map()
  gltf.scene.traverse((node) => {
    nodes[node.name] = node
    if (!node.isMesh) return
    if (/Collision|Prototype|Pool_study/.test(node.name)) node.visible = false
    for (const texture of Object.values(node.material).filter(v => v?.isTexture)) {
      texture.anisotropy = anisotropy; texture.needsUpdate = true
    }
    if (cavern) {
      if (node.name === 'CavernStructure_Rock') {
        node.material.side = DoubleSide
        node.material.normalScale.set(.22, .22)
        node.material.onBeforeCompile = shorelineLayer
        node.material.customProgramCacheKey = () => 'cavern-wet-stone-v3-enclosed-fog'
      }
      return
    }
    if (/Collision/.test(node.name)) return
    const original = node.material
    const stone = /Paving|Stone|Ruins|Courtyard|Arcades|Floor|Walls|Limestone|Tower|Perimeter|ForestPatch_Ground/.test(node.name)
    const bark = /Trees|Wood/.test(node.name)
    const study = stone || bark
    const key = original.uuid + (stone ? '-stone' : bark ? '-bark' : '') + (study ? '-study' : '')
    if (!converted.has(key)) {
      const material = new MeshBasicMaterial({ map: original.map, color: original.color,
        vertexColors: !original.map && !!node.geometry.attributes.color, side: original.map ? original.side : DoubleSide })
      if (stone && detail) addStoneDetail(material, detail, study)
      else if (bark && detail) addBarkDetail(material, detail, study)
      addOutdoorLighting(material)
      converted.set(key, { original, material })
    }
    node.material = converted.get(key).material
  })
  new Set([...converted.values()].map(v => v.original)).forEach(m => m.dispose())
  const families = ['Fern', 'Low_Shrub', 'Grass_Tuft', 'Broadleaf_Clump']
  for (const [prototype, marker] of [['HubPlantPrototype_', 'HubPlant_'], ['ApproachPlantPrototype_', 'ApproachPlant_'], ['FernPrototype', 'GroundFern_']]) {
    for (const family of prototype === 'FernPrototype' ? [''] : families) {
      const template = nodes[prototype + family]
      const placements = Object.values(nodes).filter(n => n.name.startsWith(marker + (family ? family + '_' : '')))
      if (!template || !placements.length) continue
      const instances = new InstancedMesh(template.geometry, template.material, placements.length)
      instances.name = prototype + family + '_Instances'
      placements.forEach((node, i) => instances.setMatrixAt(i, node.matrixWorld))
      instances.instanceMatrix.needsUpdate = true
      instances.computeBoundingSphere()
      gltf.scene.add(instances)
      // Markers are authoring data, not runtime objects. Their world transforms
      // are now in the instance buffer; avoid walking them on every render.
      placements.forEach(node => node.removeFromParent())
    }
  }
  if (!cavern && batching) batchStaticMeshes(gltf.scene)
  gltf.scene.updateMatrixWorld(true)
  gltf.scene.traverse(node => { node.matrixAutoUpdate = false; node.matrixWorldAutoUpdate = false })
  return { ...gltf, nodes }
}

export function disposePlaced(scene) {
  disposeStaticBatches(scene)
  scene.traverse(node => { if (node.isInstancedMesh) node.dispose() })
  disposeZone(scene)
}
