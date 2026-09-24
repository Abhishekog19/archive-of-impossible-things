import { useEffect, useLayoutEffect, useMemo, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'

function GroundCover({ nodes, family }) {
  const ref = useRef(null)
  const placements = useMemo(() => Object.values(nodes).filter((n) => n.name.startsWith(`HubPlant_${family}_`)), [nodes, family])
  useLayoutEffect(() => {
    placements.forEach((node, i) => ref.current.setMatrixAt(i, node.matrix))
    ref.current.instanceMatrix.needsUpdate = true
    ref.current.computeBoundingSphere()
  }, [placements])
  return <instancedMesh ref={ref} args={[nodes[`HubPlantPrototype_${family}`].geometry, undefined, placements.length]}>
    <meshBasicMaterial vertexColors side={DoubleSide} />
  </instancedMesh>
}

export default function HubArt() {
  const { nodes } = useGLTF('/models/hub-art.glb')
  const gl = useThree((s) => s.gl)
  const surfaces = useMemo(() => ['HubArt_Paving', 'HubArt_Ruins', 'HubArt_Trees', 'HubArt_CornerPaving', 'HubArt_CornerStone'].map((name) => {
    const node = nodes[name]
    const map = node.material.map.clone()
    map.anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
    map.needsUpdate = true
    return { name, geometry: node.geometry, map }
  }), [gl, nodes])
  useEffect(() => () => surfaces.forEach(({ map }) => map.dispose()), [surfaces])
  // The resident world keeps its smooth floor and original pillar proxies.
  return <>{surfaces.map(({ name, geometry, map }) => (
    <mesh key={name} name={name} geometry={geometry}>
      <meshBasicMaterial map={map} />
    </mesh>
  ))}
    <mesh name="HubArt_Foliage" geometry={nodes.HubArt_Foliage.geometry}>
      <meshBasicMaterial vertexColors side={DoubleSide} />
    </mesh>
    {['Fern', 'Low_Shrub', 'Grass_Tuft', 'Broadleaf_Clump'].map((family) => <GroundCover key={family} nodes={nodes} family={family} />)}
  </>
}
