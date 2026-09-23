import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'

export default function HubArt() {
  const { nodes } = useGLTF('/models/hub-art.glb')
  const gl = useThree((s) => s.gl)
  const surfaces = useMemo(() => ['HubArt_Paving', 'HubArt_Ruins', 'HubArt_Trees'].map((name) => {
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
  </>
}
