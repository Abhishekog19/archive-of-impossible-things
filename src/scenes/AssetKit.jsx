import { useEffect, useLayoutEffect, useMemo, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { CuboidCollider, RigidBody } from '@react-three/rapier'
import { DoubleSide, Matrix4, Quaternion, Vector3 } from 'three'

// Prototype placements only. Zone art will replace this isolated assembly proof.
const placements = {}
function put(name, x, y, z, scale = 1) {
  ;(placements[name] ??= []).push({ position: [x, y, z], scale })
}
for (let row = 0; row < 12; row++) {
  for (let col = 0; col < 4; col++) {
    put(`Slab_${1 + (row * 3 + col) % 6}`, (col - 1.5) * 1.12 + (row % 2) * 0.15,
      -0.08, 4.5 - row * 1.12)
  }
}
for (let row = 0; row < 4; row++) {
  for (let i = 0; i < 7 - row; i++) {
    put(`Masonry_${row === 0 ? 1 : 2 + i % 2}`, -3.7, row * 0.5, 1 - i * 1.02 - row * 0.22)
  }
}
put('Arch_Ruin', 0, 0, -10)
put('Column_Broken', 3.8, 0, -3)
put('Column_Broken', -4.2, 0, -12)
for (const [x, z, scale] of [[6, -6, 1.1], [-6, -9, 1.3], [7, -16, 1.4]]) {
  put('Tree_Broadleaf', x, 0, z, scale)
  put('Tree_Leaves', x, 0, z, scale)
}
put('Root_1', -3.2, 0, -5)
put('Root_2', 4, 0, -6)
for (let i = 0; i < 24; i++) {
  const side = i % 2 ? -1 : 1
  put('Fern', side * (2.8 + 0.7 * Math.sin(i * 2.1)), 0, 3 - i * 0.65, 0.65 + (i % 4) * 0.12)
}

function Batch({ node, transforms }) {
  const ref = useRef(null)
  useLayoutEffect(() => {
    const m = new Matrix4(), q = new Quaternion()
    transforms.forEach(({ position, scale }, i) => {
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

export default function AssetKit({ reference = false }) {
  const { nodes, materials } = useGLTF('/models/archive-kit.glb')
  const camera = useThree((s) => s.camera)
  const gl = useThree((s) => s.gl)
  useLayoutEffect(() => {
    for (const material of Object.values(materials)) {
      if (!material.map) continue
      material.map.anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
      material.map.needsUpdate = true
    }
  }, [materials, gl])
  const batches = useMemo(() => Object.entries(placements), [])
  useEffect(() => {
    if (!reference) return
    camera.position.set(10, 7, 12)
    camera.lookAt(0, 2, -5)
    camera.updateProjectionMatrix()
  }, [camera, reference])
  return (
    <>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.03, -6]}>
        <planeGeometry args={[38, 42]} />
        <meshBasicMaterial color="#4a5340" />
      </mesh>
      <RigidBody type="fixed" colliders={false}>
        <CuboidCollider args={[19, 0.2, 21]} position={[0, -0.17, -6]} />
      </RigidBody>
      {batches.map(([name, transforms]) => (
        <group key={name}>
          <Batch node={nodes[name]} transforms={transforms} />
          {nodes[`Collider_${name}`] && transforms.map(({ position, scale }, i) => (
            <RigidBody key={i} type="fixed" colliders="trimesh" includeInvisible position={position} scale={scale}>
              <mesh geometry={nodes[`Collider_${name}`].geometry} visible={false} />
            </RigidBody>
          ))}
        </group>
      ))}
    </>
  )
}
