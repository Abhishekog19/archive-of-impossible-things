import { useGLTF } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { useEffect, useMemo } from 'react'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'
import { useGameStore } from '../store'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import CavernLight from './CavernLight'
import { shorelineLayer } from './cavernMaterial'

export function CavernSurfaces({ nodes, collision = true, prepared = false }) {
  const gl = useThree((s) => s.gl)
  const tier = useGameStore((s) => s.tier)
  const material = useMemo(() => {
    if (prepared) return nodes.CavernStructure_Rock.material
    const copy = nodes.CavernStructure_Rock.material.clone()
    copy.side = DoubleSide
    copy.normalScale.set(.22, .22)
    copy.onBeforeCompile = shorelineLayer
    copy.customProgramCacheKey = () => 'cavern-wet-stone-v3-enclosed-fog'
    return copy
  }, [nodes, prepared])
  useEffect(() => {
    const anisotropy = Math.min(gl.capabilities.getMaxAnisotropy(), tier === 'low' ? 2 : 8)
    for (const map of [material.map, material.normalMap, material.roughnessMap]) {
      if (map && map.anisotropy !== anisotropy) { map.anisotropy = anisotropy; map.needsUpdate = true }
    }
  }, [gl, material, tier])
  useEffect(() => () => { if (!prepared) material.dispose() }, [material, prepared])
  return <>
    <mesh name="CavernStructure_Rock" layers-mask={WORLD_AND_POOL_LAYERS} geometry={nodes.CavernStructure_Rock.geometry} material={material} />
    <CavernLight openingGeometry={nodes.Cavern_Oculus.geometry} />
    {collision && <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.CavernStructure_Collision.geometry} visible={false} />
    </RigidBody>}
  </>
}

export default function CavernStructure() {
  const { nodes } = useGLTF('/models/cavern-structure.glb')
  return <CavernSurfaces nodes={nodes} />
}
