import { useGLTF } from '@react-three/drei'
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
