import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Color, Quaternion, Vector3 } from 'three'
import { useGameStore } from '../store'

// Two authored canopy openings align with the receiver field in outdoorLighting.
const openings = [[-12, -70, 3.1], [-10, -84, 3.1]]
function Shaft({ opening }) {
  const ref = useRef(null)
  const setup = useMemo(() => {
    const [x, z, ground] = opening
    const bottom = new Vector3(x + ground * .5, ground, z + ground * .667)
    const top = bottom.clone().add(new Vector3(5, 10, 6.67))
    const direction = top.clone().sub(bottom)
    return { position: top.clone().add(bottom).multiplyScalar(.5), length: direction.length(),
      rotation: new Quaternion().setFromUnitVectors(new Vector3(0, 1, 0), direction.normalize()),
      uniforms: { tint: { value: new Color('#e0dbaf') } } }
  }, [opening])
  useFrame(({ camera }) => { ref.current.visible = camera.position.distanceToSquared(setup.position) < 42 * 42 })
  return <mesh ref={ref} position={setup.position} quaternion={setup.rotation} renderOrder={1}>
    <cylinderGeometry args={[.65, 2.1, setup.length, 12, 1, true]} />
    <shaderMaterial transparent depthWrite={false} uniforms={setup.uniforms}
      vertexShader={`varying vec3 viewNormal, eye; varying vec2 shaftUv;
        void main() { vec4 p = modelViewMatrix * vec4(position, 1.0);
          viewNormal = normalMatrix * normal; eye = -p.xyz; shaftUv = uv;
          gl_Position = projectionMatrix * p; }`}
      fragmentShader={`uniform vec3 tint; varying vec3 viewNormal, eye; varying vec2 shaftUv;
        void main() { float rim = pow(max(dot(normalize(viewNormal), normalize(eye)), 0.0), 3.0);
          float ends = smoothstep(0.0, .3, shaftUv.y) * (1.0 - smoothstep(.75, 1.0, shaftUv.y));
          float distanceFade = 1.0 - smoothstep(28.0, 40.0, length(eye));
          gl_FragColor = vec4(tint, rim * ends * distanceFade * .065);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`} />
  </mesh>
}
export default function CanopyLight() {
  const enabled = useGameStore(s => s.fogEnabled)
  const tier = useGameStore(s => s.tier)
  return enabled && tier !== 'low' ? openings.map((opening, i) => <Shaft key={i} opening={opening} />) : null
}
