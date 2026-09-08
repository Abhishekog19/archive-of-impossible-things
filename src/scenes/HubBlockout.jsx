import { useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import HubCorner from './HubCorner'

export default function HubBlockout({ reference = false, cornerView = false }) {
  const { nodes } = useGLTF('/models/hub-blockout.glb')
  const camera = useThree((s) => s.camera)
  useEffect(() => {
    if (!reference) return
    camera.position.set(...(cornerView ? [-8, 5, 1] : [0, 13, 30]))
    camera.lookAt(...(cornerView ? [-8, 1.9, -10] : [0, 4, -8]))
    camera.updateProjectionMatrix()
  }, [camera, reference, cornerView])

  return (
    <>
      <HubCorner />
      {Object.values(nodes).filter((node) => node.isMesh && node.name !== 'Collision').map((node) => (
        <mesh key={node.uuid} geometry={node.geometry} material={node.material} />
      ))}
      <RigidBody type="fixed" colliders="trimesh" includeInvisible>
        <mesh geometry={nodes.Collision.geometry} visible={false} />
      </RigidBody>
    </>
  )
}
