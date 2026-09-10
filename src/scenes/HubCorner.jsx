import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide } from 'three'
import { useLayoutEffect, useMemo, useRef } from 'react'

function Ferns({ nodes }) {
  const ref = useRef(null)
  const placements = useMemo(
    () => Object.values(nodes).filter((node) => node.name.startsWith('GroundFern_')),
    [nodes],
  )
  useLayoutEffect(() => {
    placements.forEach((node, i) => ref.current.setMatrixAt(i, node.matrix))
    ref.current.instanceMatrix.needsUpdate = true
    ref.current.computeBoundingSphere()
  }, [placements])
  return (
    <instancedMesh ref={ref} name="CornerFernInstances" args={[nodes.FernPrototype.geometry, undefined, placements.length]}>
      <meshBasicMaterial vertexColors side={DoubleSide} />
    </instancedMesh>
  )
}

// A full-colour diffuse bake contains lighting already. MeshBasicMaterial keeps
// the temporary hub hemisphere from lighting it twice; glTF supplies UV0 + sRGB.
export default function HubCorner() {
  const { nodes, materials } = useGLTF('/models/hub-corner.glb')
  const gl = useThree((state) => state.gl)
  useLayoutEffect(() => {
    // Preserve paving detail at shallow gameplay angles without larger atlases.
    // Four samples cap the filtering cost on integrated and mobile GPUs.
    const anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
    for (const material of [materials.Corner_Paving, materials.Corner_Baked]) {
      if (material.map.anisotropy !== anisotropy) {
        material.map.anisotropy = anisotropy
        material.map.needsUpdate = true
      }
    }
  }, [gl, materials])
  return (
    <group position={[-8, 0, -9]}>
      <mesh geometry={nodes.Corner_Paving.geometry}>
        <meshBasicMaterial map={materials.Corner_Paving.map} />
      </mesh>
      <mesh geometry={nodes.Corner_Baked.geometry}>
        <meshBasicMaterial map={materials.Corner_Baked.map} />
      </mesh>
      <Ferns nodes={nodes} />
      <mesh geometry={nodes.Corner_Foliage.geometry}>
        <meshBasicMaterial vertexColors side={DoubleSide} />
      </mesh>
      <RigidBody type="fixed" colliders="trimesh" includeInvisible>
        <mesh geometry={nodes.Corner_Collision.geometry} visible={false} />
      </RigidBody>
    </group>
  )
}
