import { BatchedMesh, Matrix4 } from 'three'

// Keep each authored cell's own bounds, material and transform, but submit cells
// sharing a material together. Three retains per-cell frustum culling and sorts
// opaque cells front to back. No distance cutoffs or geometry simplification.
export function batchStaticMeshes(root) {
  root.updateMatrixWorld(true)
  const inverse = new Matrix4().copy(root.matrixWorld).invert()
  const groups = new Map()
  root.traverse(node => {
    if (!node.isMesh || node.isInstancedMesh || node.isBatchedMesh || !node.visible ||
      node.children.length || node.isSkinnedMesh || Array.isArray(node.material) ||
      node.material.transparent || node.geometry.groups.length ||
      Object.keys(node.geometry.morphAttributes).length || node.matrixWorld.determinant() <= 0) return
    // Hidden ancestors must not accidentally become visible in the root batch.
    for (let parent = node.parent; parent && parent !== root; parent = parent.parent) if (!parent.visible) return
    const geometry = node.geometry
    const layout = Object.entries(geometry.attributes).sort(([a], [b]) => a.localeCompare(b))
      .map(([name, attribute]) => `${name}:${attribute.itemSize}:${attribute.normalized}`).join('|')
    const key = `${node.material.uuid}:${node.layers.mask}:${!!geometry.index}:${layout}`
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(node)
  })
  const batches = []
  for (const meshes of groups.values()) {
    if (meshes.length < 2) continue
    const geometries = [...new Set(meshes.map(mesh => mesh.geometry))]
    const batch = new BatchedMesh(meshes.length,
      geometries.reduce((sum, g) => sum + g.attributes.position.count, 0),
      geometries.reduce((sum, g) => sum + (g.index?.count || 0), 0), meshes[0].material)
    batch.name = `StaticBatch_${meshes[0].name}`
    batch.layers.mask = meshes[0].layers.mask
    const ids = new Map(geometries.map(g => [g, batch.addGeometry(g)]))
    for (const mesh of meshes) {
      const id = batch.addInstance(ids.get(mesh.geometry))
      batch.setMatrixAt(id, new Matrix4().multiplyMatrices(inverse, mesh.matrixWorld))
      // Retain original resources for the existing owner's disposal path.
      mesh.visible = false
      mesh.userData.batchedSurface = true
    }
    batch.computeBoundingSphere()
    root.add(batch)
    batches.push(batch)
  }
  return batches
}

export function disposeStaticBatches(root) {
  const batches = []
  root.traverse(node => { if (node.isBatchedMesh) batches.push(node) })
  for (const batch of batches) {
    batch.removeFromParent()
    batch.dispose()
  }
}
