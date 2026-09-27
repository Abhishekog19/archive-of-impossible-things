import { useGLTF } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide } from 'three'

// PD04 structural preview; rock materials and water follow in PD05/06.
export default function CavernStructure() {
  const { nodes } = useGLTF('/models/cavern-structure.glb')
  return <>
    <mesh name="CavernStructure_Rock" geometry={nodes.CavernStructure_Rock.geometry}>
      <meshBasicMaterial vertexColors side={DoubleSide} />
    </mesh>
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.CavernStructure_Collision.geometry} visible={false} />
    </RigidBody>
  </>
}
