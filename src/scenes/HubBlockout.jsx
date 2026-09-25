import { lazy, useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import HubCorner from './HubCorner'
import worldViews from '../config/world-views.json'
import { CAVERN_WATER } from '../config/cavern-water'
const CavernWater = lazy(() => import('./CavernWater'))
const HubArt = lazy(() => import('./HubArt'))
const ForestPatch = lazy(() => import('./ForestPatch'))
const ForestApproach = lazy(() => import('./ForestApproach'))

export default function HubBlockout({ reference = false, cornerView = false, view = 'reference', legacy = false, waterStudy = false, patch = false }) {
  const { nodes } = useGLTF(legacy ? '/models/hub-blockout.glb' : patch ? '/models/world-art-context.glb' : '/models/world-blockout.glb')
  const camera = useThree((s) => s.camera)
  useEffect(() => {
    if (!reference) return
    const pose = patch && view === 'patch' ? { position: [-12, 3.4, -18], target: [-12, 3.4, -33] }
      : waterStudy && view === 'cavern' ? CAVERN_WATER.camera : worldViews[view] || worldViews.reference
    camera.position.set(...(cornerView ? [-8, 5, 1] : pose.position))
    camera.lookAt(...(cornerView ? [-8, 1.9, -10] : pose.target))
    camera.updateProjectionMatrix()
  }, [camera, reference, cornerView, view, waterStudy, patch])

  return (
    <>
      <HubCorner contextual={patch} />
      {patch && <><ForestPatch /><ForestApproach /><HubArt /></>}
      {Object.values(nodes).filter((node) => node.isMesh && node.name !== 'Collision' && !(waterStudy && node.name === 'Pool_study')).map((node) => (
        <mesh key={node.uuid} geometry={node.geometry} material={node.material} />
      ))}
      {waterStudy && <CavernWater geometry={nodes.Pool_study.geometry} />}
      <RigidBody type="fixed" colliders="trimesh" includeInvisible>
        <mesh geometry={nodes.Collision.geometry} visible={false} />
      </RigidBody>
    </>
  )
}
