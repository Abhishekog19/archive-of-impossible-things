import { useGLTF } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { useEffect, useMemo } from 'react'
import { useThree } from '@react-three/fiber'
import { DoubleSide } from 'three'
import { useGameStore } from '../store'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'

// Reuse the Blender PBR textures and metre-scaled UVs. The only runtime layer is
// water staining, anchored to the authored shore contour instead of UV islands.
function shorelineLayer(shader) {
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
    float shoreRadius = 15.5 + 1.2 * sin(3.0 * shoreAngle) + .7 * cos(5.0 * shoreAngle);
    float edge = length(fromPool) - shoreRadius;
    float brokenEdge = sin(cavernPoint.x * 2.3 + sin(cavernPoint.z * 1.7)) * .12;
    float wetStone = (1.0 - smoothstep(.1, 1.1, edge + brokenEdge))
      * (1.0 - smoothstep(-7.25, -6.7, cavernPoint.y));
    diffuseColor.rgb *= mix(vec3(1.0), vec3(.48, .57, .59), wetStone);
    // Broad deposits break uniform colour without adding another texture atlas.
    float deposit = sin(cavernPoint.y * 1.7 + sin(cavernPoint.x * .24) + sin(cavernPoint.z * .31));
    diffuseColor.rgb *= 1.0 + deposit * .065;
  `).replace('#include <roughnessmap_fragment>', `
    #include <roughnessmap_fragment>
    roughnessFactor = mix(roughnessFactor, .29, wetStone);
  `)
}

export default function CavernStructure() {
  const { nodes } = useGLTF('/models/cavern-structure.glb')
  const gl = useThree((s) => s.gl)
  const tier = useGameStore((s) => s.tier)
  const material = useMemo(() => {
    const copy = nodes.CavernStructure_Rock.material.clone()
    copy.side = DoubleSide
    copy.onBeforeCompile = shorelineLayer
    copy.customProgramCacheKey = () => 'cavern-wet-stone-v1'
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
    {/* Bounded material fill from the actual opening; shaft/fog art follows in PD06. */}
    <pointLight layers-mask={WORLD_AND_POOL_LAYERS} position={[-12, 13, -205]} color="#c3d7e3" intensity={420} distance={48} decay={2} />
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.CavernStructure_Collision.geometry} visible={false} />
    </RigidBody>
  </>
}
