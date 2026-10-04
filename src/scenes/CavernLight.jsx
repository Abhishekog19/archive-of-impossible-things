import { useEffect, useMemo } from 'react'
import { Color, Object3D, Quaternion, Vector3 } from 'three'
import { CAVERN_LOOK } from '../config/cavern-look'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import { useGameStore } from '../store'

const vertex = `
  varying vec3 viewDirection, viewNormal;
  varying vec2 shaftUv;
  void main() {
    vec4 point = modelViewMatrix * vec4(position, 1.0);
    viewDirection = -point.xyz;
    viewNormal = normalize(normalMatrix * normal);
    shaftUv = uv;
    gl_Position = projectionMatrix * point;
  }
`
const fragment = `
  uniform vec3 tint;
  uniform float strength;
  varying vec3 viewDirection, viewNormal;
  varying vec2 shaftUv;
  void main() {
    float softEdge = pow(max(dot(normalize(viewNormal), normalize(viewDirection)), 0.0), 2.0);
    float ends = smoothstep(0.0, .14, shaftUv.y) * (1.0 - smoothstep(.93, 1.0, shaftUv.y));
    // Broad uneven bands imply light scattered through a broken slit, without
    // moving noise, particles, bloom, screen-space passes or opaque cone edges.
    float bands = .86 + .14 * sin(shaftUv.x * 31.4159 + shaftUv.y * 1.3);
    gl_FragColor = vec4(tint, strength * softEdge * ends * bands);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
  }
`

/** Low-cost authored light volume; shared by the main and pool-reflection views. */
export default function CavernLight({ openingGeometry }) {
  const tier = useGameStore((s) => s.tier)
  const fogEnabled = useGameStore((s) => s.fogEnabled)
  const setup = useMemo(() => {
    const top = new Vector3(...CAVERN_LOOK.shaftTop)
    const bottom = new Vector3(...CAVERN_LOOK.shaftBottom)
    const direction = top.clone().sub(bottom)
    const target = new Object3D()
    target.position.fromArray(CAVERN_LOOK.keyTarget)
    return {
      target, length: direction.length(), centre: top.clone().add(bottom).multiplyScalar(.5),
      rotation: new Quaternion().setFromUnitVectors(new Vector3(0, 1, 0), direction.normalize()),
      uniforms: { tint: { value: new Color(CAVERN_LOOK.shaft) }, strength: { value: CAVERN_LOOK.shaftOpacity } },
    }
  }, [])
  useEffect(() => { setup.target.updateMatrixWorld() }, [setup])
  return <>
    <primitive object={setup.target} />
    <spotLight layers-mask={WORLD_AND_POOL_LAYERS} position={CAVERN_LOOK.keyPosition}
      target={setup.target} color={CAVERN_LOOK.keyColour} intensity={CAVERN_LOOK.keyIntensity}
      angle={CAVERN_LOOK.keyAngle} penumbra={.8} distance={55} decay={2} />
    <pointLight layers-mask={WORLD_AND_POOL_LAYERS} position={CAVERN_LOOK.fillPosition}
      color={CAVERN_LOOK.keyColour} intensity={CAVERN_LOOK.fillIntensity} distance={48} decay={2} />
    <mesh name="Cavern_Oculus" geometry={openingGeometry} layers-mask={WORLD_AND_POOL_LAYERS}>
      <meshBasicMaterial color={CAVERN_LOOK.opening} toneMapped={false} fog={false} />
    </mesh>
    {fogEnabled && <mesh name="Cavern_SkylightShaft" position={setup.centre} quaternion={setup.rotation}
      scale={[1, 1, .72]} layers-mask={WORLD_AND_POOL_LAYERS} renderOrder={1}>
      <cylinderGeometry args={[CAVERN_LOOK.shaftTopRadius, CAVERN_LOOK.shaftBottomRadius,
        setup.length, tier === 'low' ? 16 : 32, 1, true]} />
      <shaderMaterial vertexShader={vertex} fragmentShader={fragment} uniforms={setup.uniforms}
        transparent depthWrite={false} />
    </mesh>}
  </>
}
