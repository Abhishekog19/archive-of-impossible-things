import { useEffect, useLayoutEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { CuboidCollider, RigidBody } from '@react-three/rapier'
import KitBatch from './KitBatch'

// Prototype placements only. Zone art will replace this isolated assembly proof.
const placements = {}
function put(name, x, y, z, scale = 1, yaw = 0) {
  ;(placements[name] ??= []).push({ position: [x, y, z], scale, yaw })
}
for (let row = 0; row < 12; row++) {
  for (let col = 0; col < 4; col++) {
    put(`Slab_${1 + (row * 3 + col) % 6}`, (col - 1.5) * 1.12 + (row % 2) * 0.15,
      -0.08, 4.5 - row * 1.12)
  }
}
for (let row = 0; row < 4; row++) {
  for (let i = 0; i < 7 - row; i++) {
    const variant = row === 3 ? [4, 2, 3, 1][i] : [1, 3, 2, 4, 2, 1, 3][(i + row * 2) % 7]
    put(`Masonry_${variant}`, -3.7 + Math.sin(i * 2.4 + row) * 0.045,
      row * 0.5, 1 - i * 1.02 - row * 0.22)
  }
}
put('Arch_Ruin', 0, 0, -10)
put('Column_Broken', 3.8, 0, -3)
put('Column_Broken', -4.2, 0, -12)
for (const [name, leaves, x, z, scale] of [
  ['Tree_Leaning', 'Tree_Leaning_Leaves', 6, -6, 1.1],
  ['Tree_Tall', 'Tree_Tall_Leaves', -6, -9, 1.1],
  ['Tree_Broadleaf', 'Tree_Leaves', 7, -16, 1.4],
]) {
  put(name, x, 0, z, scale)
  put(leaves, x, 0, z, scale)
}
put('Root_1', -3.2, 0, -5)
put('Root_2', 4, 0, -6)
for (let i = 0; i < 24; i++) {
  const side = i % 2 ? -1 : 1
  put('Fern', side * (2.8 + 0.7 * Math.sin(i * 2.1)), 0, 3 - i * 0.65,
    0.65 + (i % 4) * 0.12, i * 2.399)
}
// Group plants at sheltered edges rather than filling the walking lane evenly.
for (const [cluster, x, z] of [[0, -3.1, 1], [1, -3.0, -4.3], [2, 3.5, -2.8],
  [3, 4.3, -6.3], [4, -5.3, -9.2], [5, 3.4, -10.5]]) {
  for (let i = 0; i < 7; i++) {
    const angle = i * 2.399 + cluster, radius = 0.2 + (i % 3) * 0.22
    const name = ['Broadleaf_Clump', 'Grass_Tuft', 'Low_Shrub'][(i + cluster) % 3]
    put(name, x + Math.cos(angle) * radius, 0, z + Math.sin(angle) * radius,
      0.7 + (i % 4) * 0.15, angle)
  }
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
          <KitBatch node={nodes[name]} transforms={transforms} />
          {nodes[`Collider_${name}`] && transforms.map(({ position, scale, yaw }, i) => (
            <RigidBody key={i} type="fixed" colliders="trimesh" includeInvisible position={position} rotation={[0, yaw, 0]} scale={scale}>
              <mesh geometry={nodes[`Collider_${name}`].geometry} visible={false} />
            </RigidBody>
          ))}
        </group>
      ))}
    </>
  )
}
