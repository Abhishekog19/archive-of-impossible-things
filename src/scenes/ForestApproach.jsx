import { useEffect, useLayoutEffect, useMemo, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide } from 'three'

function GroundCover({ nodes, family }) {
  const ref = useRef(null)
  const placements = useMemo(() => Object.values(nodes).filter((node) => node.name.startsWith(`ApproachPlant_${family}_`)), [nodes, family])
  useLayoutEffect(() => {
    placements.forEach((node, i) => ref.current.setMatrixAt(i, node.matrix))
    ref.current.instanceMatrix.needsUpdate = true
    ref.current.computeBoundingSphere()
  }, [placements])
  return <instancedMesh ref={ref} args={[nodes[`ApproachPlantPrototype_${family}`].geometry, undefined, placements.length]}>
    <meshBasicMaterial vertexColors side={DoubleSide} />
  </instancedMesh>
}

export default function ForestApproach() {
  const { nodes } = useGLTF('/models/forest-approach.glb')
  const gl = useThree((s) => s.gl)
  const surfaces = useMemo(() => ['Stone', 'Wood', 'Ground'].map((part) => {
    const name = `ForestApproach_${part}`
    const map = nodes[name].material.map.clone()
    map.anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
    map.needsUpdate = true
    return { name, geometry: nodes[name].geometry, map }
  }), [gl, nodes])
  useEffect(() => () => surfaces.forEach(({ map }) => map.dispose()), [surfaces])
  return <>
    {surfaces.map(({ name, geometry, map }) => <mesh key={name} name={name} geometry={geometry}>
      <meshBasicMaterial map={map} />
    </mesh>)}
    <mesh geometry={nodes.ForestApproach_Foliage.geometry}>
      <meshBasicMaterial vertexColors side={DoubleSide} />
    </mesh>
    {['Fern', 'Low_Shrub', 'Grass_Tuft', 'Broadleaf_Clump'].map((family) => <GroundCover key={family} nodes={nodes} family={family} />)}
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.ForestApproach_Collision.geometry} visible={false} />
    </RigidBody>
  </>
}
