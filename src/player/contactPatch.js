// Build a small receiver patch, clipping entire triangles at ledges/steps.
// The caller supplies real ground ray hits; no new world collider is created.
export function updateContactPatch(geometry, origin, sample, feetOffset) {
  const positions = geometry.attributes.position
  const uv = geometry.attributes.uv
  const heights = []
  const radius = .7
  const centre = sample(origin.x, origin.z)
  if (!centre || centre.normal.y < .65) { geometry.setDrawRange(0, 0); return 0 }
  const gap = Math.max(0, origin.y - feetOffset - centre.height)
  const opacity = .42 * Math.max(0, 1 - gap / 1.6)
  const spread = radius + Math.min(gap, 1) * .18
  for (let i = 0; i < positions.count; i++) {
    const x = origin.x + (uv.getX(i) - .5) * spread * 2
    const z = origin.z + (uv.getY(i) - .5) * spread * 2
    const hit = sample(x, z)
    heights.push(hit && hit.normal.y > .65 ? hit.height : null)
    positions.setXYZ(i, x, (hit?.height ?? centre.height) + .055, z)
  }
  const indices = []
  for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) {
    const a = y * 5 + x, b = a + 1, c = a + 5, d = c + 1
    for (const tri of [[a, c, b], [b, c, d]]) {
      const h = tri.map(i => heights[i])
      if (h.every(v => v !== null) && Math.max(...h) - Math.min(...h) < .32) indices.push(...tri)
    }
  }
  geometry.setIndex(indices)
  geometry.setDrawRange(0, indices.length)
  positions.needsUpdate = true
  geometry.computeBoundingSphere()
  return opacity
}
