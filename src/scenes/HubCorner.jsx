import { useGLTF } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide } from 'three'

// A full-colour diffuse bake contains lighting already. MeshBasicMaterial keeps
// the temporary hub hemisphere from lighting it twice; glTF supplies UV0 + sRGB.
export default function HubCorner() {
  const { nodes, materials } = useGLTF('/models/hub-corner.glb')
  return (
    <group position={[-8, 0, -9]}>
      <mesh geometry={nodes.Corner_Baked.geometry}>
        <meshBasicMaterial map={materials.Corner_Baked.map} />
      </mesh>
      <mesh geometry={nodes.Corner_Foliage.geometry}>
        <meshBasicMaterial vertexColors side={DoubleSide} />
      </mesh>
      <RigidBody type="fixed" colliders="trimesh" includeInvisible>
        <mesh geometry={nodes.Corner_Collision.geometry} visible={false} />
      </RigidBody>
    </group>
  )
}
