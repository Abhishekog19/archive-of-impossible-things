import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'

// Static placed bakes share the resident world's separate collision geometry.
export default function PlacedArt({ url }) {
  const { nodes } = useGLTF(url)
  const gl = useThree((state) => state.gl)
  const surfaces = useMemo(() => Object.values(nodes).filter((node) => node.isMesh).map((node) => {
    const map = node.material.map?.clone()
    if (map) {
      map.anisotropy = Math.min(4, gl.capabilities.getMaxAnisotropy())
      map.needsUpdate = true
    }
    return { node, map }
  }), [nodes, gl])
  useEffect(() => () => surfaces.forEach(({ map }) => map?.dispose()), [surfaces])
  return surfaces.map(({ node, map }) => <mesh key={node.uuid} name={node.name} geometry={node.geometry}>
    <meshBasicMaterial map={map} vertexColors={!map} side={map ? undefined : DoubleSide} />
  </mesh>)
}
