// Portal sightlines can see the pool before entering the reflection range.
export function cavernWaterView(camera, pool, shoreline) {
  if (!shoreline) return { visible: true, reflect: true }
  const distanceSq = (camera.x - pool.x) ** 2 + (camera.y - pool.y) ** 2 + (camera.z - pool.z) ** 2
  const visible = camera.z < -85 && camera.y < 12 && distanceSq < 125 ** 2
  return { visible, reflect: visible && camera.z < -145 && distanceSq < 60 ** 2 }
}
