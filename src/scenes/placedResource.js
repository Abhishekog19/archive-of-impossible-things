import { DoubleSide, InstancedMesh, MeshBasicMaterial } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js'
import { disposeZone } from './zoneResource.js'
import { addBarkDetail, addStoneDetail } from './stoneDetail.js'

export async function loadPlaced(url, signal, anisotropy, detail, cavern = false) {
  const response = await fetch(url, { signal })
  if (!response.ok) throw new Error(`Area request failed (${response.status})`)
  const data = await response.arrayBuffer()
  signal.throwIfAborted()
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
    if (cavern || /Collision/.test(node.name)) return
    const original = node.material
    const stone = /Paving|Stone|Ruins|Courtyard|Arcades|Floor|Walls|Limestone|Tower|Perimeter|ForestPatch_Ground/.test(node.name)
    const bark = /Trees|Wood/.test(node.name)
    const study = node.name.startsWith('ForestPatch_')
    const key = original.uuid + (stone ? '-stone' : bark ? '-bark' : '') + (study ? '-study' : '')
    if (!converted.has(key)) {
      const material = new MeshBasicMaterial({ map: original.map, color: original.color,
        vertexColors: !original.map && !!node.geometry.attributes.color, side: original.map ? original.side : DoubleSide })
      if (stone && detail) addStoneDetail(material, detail, study)
      else if (bark && detail) addBarkDetail(material, detail, study)
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
    }
  }
  return { ...gltf, nodes }
}

export function disposePlaced(scene) {
  scene.traverse(node => { if (node.isInstancedMesh) node.dispose() })
  disposeZone(scene)
}
