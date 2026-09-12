import { useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import HubCorner from './HubCorner'
import worldViews from '../config/world-views.json'

export default function HubBlockout({ reference = false, cornerView = false, view = 'reference', legacy = false }) {
  const { nodes } = useGLTF(legacy ? '/models/hub-blockout.glb' : '/models/world-blockout.glb')
  const camera = useThree((s) => s.camera)
  useEffect(() => {
    if (!reference) return
    const pose = worldViews[view] || worldViews.reference
    camera.position.set(...(cornerView ? [-8, 5, 1] : pose.position))
    camera.lookAt(...(cornerView ? [-8, 1.9, -10] : pose.target))
    camera.updateProjectionMatrix()
  }, [camera, reference, cornerView, view])

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
