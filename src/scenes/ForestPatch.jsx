import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide } from 'three'

// Connected Phase C review, placed in world coordinates before diffuse baking.
export default function ForestPatch() {
  const { nodes, materials } = useGLTF('/models/forest-patch.glb')
  const gl = useThree((s) => s.gl)
  const map = useMemo(() => {
    const owned = materials.ForestPatch_Diffuse.map.clone()
    owned.anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
    owned.needsUpdate = true
    return owned
  }, [gl, materials])
  useEffect(() => () => map.dispose(), [map])
  return <>
    <mesh name="ForestPatch_Baked" geometry={nodes.ForestPatch_Baked.geometry}>
      <meshBasicMaterial map={map} />
    </mesh>
    <mesh geometry={nodes.ForestPatch_Foliage.geometry}>
      <meshBasicMaterial vertexColors side={DoubleSide} />
    </mesh>
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.ForestPatch_Collision.geometry} visible={false} />
    </RigidBody>
  </>
}
