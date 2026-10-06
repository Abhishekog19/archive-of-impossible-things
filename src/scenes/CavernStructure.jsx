import { useGLTF } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { useEffect, useMemo } from 'react'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'
import { useGameStore } from '../store'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import CavernLight from './CavernLight'
import { cavernShoreGLSL } from '../config/cavern-shore'
import { cavernFog } from './cavernFog'

// Reuse the Blender PBR textures and metre-scaled UVs. The only runtime layer is
// water staining, anchored to the authored shore contour instead of UV islands.
function shorelineLayer(shader) {
  cavernFog(shader, 'cavernPoint')
  shader.vertexShader = shader.vertexShader.replace('#include <common>', `
    #include <common>
    varying vec3 cavernPoint;
  `).replace('#include <begin_vertex>', `
    #include <begin_vertex>
    cavernPoint = (modelMatrix * vec4(position, 1.0)).xyz;
  `)
  shader.fragmentShader = shader.fragmentShader.replace('#include <common>', `
    #include <common>
    varying vec3 cavernPoint;
  `).replace('#include <color_fragment>', `
    #include <color_fragment>
    vec2 fromPool = cavernPoint.xz - vec2(-12.0, -195.0);
    float shoreAngle = atan(fromPool.y, fromPool.x);
    float shoreRadius = ${cavernShoreGLSL};
    float edge = length(fromPool) - shoreRadius;
    float brokenEdge = sin(cavernPoint.x * 2.3 + sin(cavernPoint.z * 1.7)) * .12;
    float wetStone = (1.0 - smoothstep(-.15, .8, edge + brokenEdge))
      * (1.0 - smoothstep(-7.25, -6.7, cavernPoint.y));
    diffuseColor.rgb *= mix(vec3(1.0), vec3(.72, .80, .82), wetStone);
    // Broad deposits break uniform colour without adding another texture atlas.
    float deposit = sin(cavernPoint.y * 1.7 + sin(cavernPoint.x * .24) + sin(cavernPoint.z * .31));
    diffuseColor.rgb *= 1.0 + deposit * .065;
  `).replace('#include <roughnessmap_fragment>', `
    #include <roughnessmap_fragment>
    roughnessFactor = mix(roughnessFactor, .24, wetStone);
  `)
}

export function CavernSurfaces({ nodes, collision = true }) {
  const gl = useThree((s) => s.gl)
  const tier = useGameStore((s) => s.tier)
  const material = useMemo(() => {
    const copy = nodes.CavernStructure_Rock.material.clone()
    copy.side = DoubleSide
    copy.normalScale.set(.6, .6)
    copy.onBeforeCompile = shorelineLayer
    copy.customProgramCacheKey = () => 'cavern-wet-stone-v3-enclosed-fog'
    return copy
  }, [nodes])
  useEffect(() => {
    const anisotropy = Math.min(gl.capabilities.getMaxAnisotropy(), tier === 'low' ? 2 : 8)
    for (const map of [material.map, material.normalMap, material.roughnessMap]) {
      if (map) { map.anisotropy = anisotropy; map.needsUpdate = true }
    }
  }, [gl, material, tier])
  useEffect(() => () => material.dispose(), [material])
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
