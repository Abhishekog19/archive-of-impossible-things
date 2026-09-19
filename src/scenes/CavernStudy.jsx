import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useThree } from '@react-three/fiber'
import { CuboidCollider, RigidBody } from '@react-three/rapier'
import { Color } from 'three'
import CavernWater from './CavernWater'
import { CAVERN_WATER } from '../config/cavern-water'
import { CAVERN_STUDY } from '../config/cavern-study'
import { useGameStore } from '../store'

const shaftVertex = `
  varying vec3 pointWorld, normalWorld;
  varying float height;
  void main() {
    pointWorld = (modelMatrix * vec4(position, 1.0)).xyz;
    normalWorld = normalize(mat3(modelMatrix) * normal);
    height = uv.y;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`
const shaftFragment = `
  uniform vec3 tint;
  uniform float opacity;
  varying vec3 pointWorld, normalWorld;
  varying float height;
  void main() {
    vec3 eye = normalize(cameraPosition - pointWorld);
    float softEdge = pow(abs(dot(normalize(normalWorld), eye)), 2.0);
    float ends = smoothstep(0.0, .15, height) * (1.0 - smoothstep(.87, 1.0, height));
    gl_FragColor = vec4(tint, opacity * softEdge * ends);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
  }
`

export default function CavernStudy({ reference }) {
  const { nodes } = useGLTF('/models/cavern-study.glb')
  const camera = useThree((s) => s.camera)
  const gl = useThree((s) => s.gl)
  const tier = useGameStore((s) => s.tier)
  const map = useMemo(() => {
    const texture = nodes.Cavern_Baked.material.map.clone()
    texture.anisotropy = Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy()))
    texture.needsUpdate = true
    return texture
  }, [nodes, gl])
  const shaftUniforms = useMemo(() => ({
    tint: { value: new Color(CAVERN_STUDY.shaft) },
    opacity: { value: CAVERN_STUDY.shaftOpacity },
  }), [])
  useEffect(() => () => map.dispose(), [map])
  useEffect(() => {
    if (!reference) return
    camera.position.set(...CAVERN_WATER.camera.position)
    camera.lookAt(...CAVERN_WATER.camera.target)
    camera.updateProjectionMatrix()
  }, [camera, reference])
  return <>
    <mesh geometry={nodes.Cavern_Baked.geometry}>
      <meshBasicMaterial map={map} />
    </mesh>
    <CavernWater geometry={nodes.Pool_study.geometry} />
    <mesh position={CAVERN_STUDY.openingPosition} rotation={[Math.PI / 2, 0, 0]}>
      <circleGeometry args={[6, 32]} />
      <meshBasicMaterial color={CAVERN_STUDY.opening} fog={false} />
    </mesh>
    {tier !== 'low' && <mesh position={CAVERN_STUDY.shaftPosition} renderOrder={1}>
      <cylinderGeometry args={[2.8, 6.8, 24, 32, 1, true]} />
      <shaderMaterial uniforms={shaftUniforms} vertexShader={shaftVertex} fragmentShader={shaftFragment}
        transparent depthWrite={false} />
    </mesh>}
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      <mesh geometry={nodes.Cavern_Collision.geometry} visible={false} />
    </RigidBody>
    {/* Keep the extracted study's upper passage closed until it joins the world. */}
    <RigidBody type="fixed" colliders={false} position={[-12, 4, -142]}>
      <CuboidCollider args={[2.8, 4, .5]} />
      <mesh><boxGeometry args={[5.6, 8, 1]} /><meshBasicMaterial color={CAVERN_STUDY.fog} /></mesh>
    </RigidBody>
  </>
}
