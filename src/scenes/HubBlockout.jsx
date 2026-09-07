import { useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'

export default function HubBlockout({ reference = false }) {
  const { nodes } = useGLTF('/models/hub-blockout.glb')
  const camera = useThree((s) => s.camera)
  useEffect(() => {
    if (!reference) return
    camera.position.set(0, 13, 30)
    camera.lookAt(0, 4, -8)
    camera.updateProjectionMatrix()
  }, [camera, reference])

  return (
    <>
      {Object.values(nodes).filter((node) => node.isMesh && node.name !== 'Collision').map((node) => (
        <mesh key={node.uuid} geometry={node.geometry} material={node.material} />
      ))}
      <RigidBody type="fixed" colliders="trimesh" includeInvisible>
        <mesh geometry={nodes.Collision.geometry} visible={false} />
      </RigidBody>
    </>
  )
}
