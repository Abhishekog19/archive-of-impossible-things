import { DoubleSide, MeshBasicMaterial } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

// Each mounted zone owns its parse. No useGLTF/global cache retains evicted data.
export function disposeZone(scene) {
  const geometry = new Set(), materials = new Set(), textures = new Set()
  scene.traverse((node) => {
    if (node.geometry) geometry.add(node.geometry)
    for (const material of [node.material].flat().filter(Boolean)) {
      materials.add(material)
      for (const value of Object.values(material)) if (value?.isTexture) textures.add(value)
    }
  })
  geometry.forEach((value) => value.dispose())
  materials.forEach((value) => value.dispose())
  textures.forEach((value) => { value.dispose(); value.source?.data?.close?.() })
}

export async function loadZone(url, signal, anisotropy) {
  const response = await fetch(url, { signal })
  if (!response.ok) throw new Error(`Zone request failed (${response.status})`)
  const bytes = await response.arrayBuffer()
  signal.throwIfAborted()
  const gltf = await new GLTFLoader().parseAsync(bytes, '/models/zones/')
  if (signal.aborted) { disposeZone(gltf.scene); signal.throwIfAborted() }
  const nodes = {}, converted = new Map()
  gltf.scene.traverse((node) => {
    nodes[node.name] = node
    if (!node.isMesh) return
    const original = node.material
    if (!converted.has(original)) {
      if (original.map) {
        original.map.anisotropy = anisotropy
        original.map.needsUpdate = true
      }
      converted.set(original, new MeshBasicMaterial({
        map: original.map, vertexColors: !!node.geometry.attributes.color, side: DoubleSide,
      }))
    }
    node.material = converted.get(original)
  })
  converted.forEach((_, original) => original.dispose())
  return { scene: gltf.scene, nodes, bytes: bytes.byteLength }
}
