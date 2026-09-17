import { useLayoutEffect, useRef } from 'react'
import { DoubleSide, Matrix4, Quaternion, Vector3 } from 'three'

export default function KitBatch({ node, transforms }) {
  const ref = useRef(null)
  useLayoutEffect(() => {
    const m = new Matrix4(), q = new Quaternion()
    transforms.forEach(({ position, scale, yaw }, i) => {
      q.setFromAxisAngle(new Vector3(0, 1, 0), yaw)
      m.compose(new Vector3(...position), q, new Vector3(scale, scale, scale))
      ref.current.setMatrixAt(i, m)
    })
    ref.current.instanceMatrix.needsUpdate = true
    ref.current.computeBoundingSphere()
    const instance = ref.current
    return () => { instance.material.dispose(); instance.dispose() }
  }, [transforms])
  return (
    <instancedMesh ref={ref} name={`KitInstances_${node.name}`} args={[node.geometry, undefined, transforms.length]} dispose={null}>
      <meshBasicMaterial map={node.material.map} vertexColors={!!node.geometry.attributes.color} side={DoubleSide} />
    </instancedMesh>
  )
}

