import { useEffect, useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useRapier } from '@react-three/rapier'
import { DoubleSide, PlaneGeometry, Raycaster, Vector3 } from 'three'
import { CHARACTER } from '../config/look'
import { useGameStore } from '../store'
import { updateContactPatch } from './contactPatch'

/** One tiny opaque-ground receiver; no texture, shadow map or extra scene pass. */
export default function ContactShadow({ controllerRef }) {
  const { world, rapier } = useRapier()
  const mesh = useRef(null)
  const geometry = useMemo(() => new PlaneGeometry(1, 1, 4, 4), [])
  const rayRef = useRef(null)
  const clock = useRef(1)
  const receivers = useRef({ meshes: [], elapsed: 1 })
  const visualRay = useMemo(() => new Raycaster(new Vector3(), new Vector3(0, -1, 0), 0, 3.3), [])
  useEffect(() => () => geometry.dispose(), [geometry])
  useFrame(({ scene }, delta) => {
    const body = controllerRef.current?.body
    const state = useGameStore.getState()
    if (!body || state.settingsOpen || state.worldLoading) return
    clock.current += delta
    if (clock.current < .05) return
    clock.current = 0
    if (!rayRef.current) rayRef.current = new rapier.Ray({ x: 0, y: 0, z: 0 }, { x: 0, y: -1, z: 0 })
    const ray = rayRef.current
    const origin = body.translation()
    // The decorative paving sits above the physics floor. One centre ray finds
    // that visible surface; the cheap physics grid still clips slopes and edges.
    receivers.current.elapsed += .05
    if (receivers.current.elapsed >= .5) {
      receivers.current.elapsed = 0
      receivers.current.meshes = []
      scene.traverse(node => {
        if (node.isMesh && node.visible && !/Collision|Prototype/.test(node.name)
          && /Paving|Forest(?:Patch|Approach|Canopy)_(?:Stone|Ground)|Courtyard|ArchiveHall_Floor|CavernStructure_Rock/.test(node.name)) {
          receivers.current.meshes.push(node)
        }
      })
    }
    visualRay.ray.origin.set(origin.x, origin.y + .3, origin.z)
    const visual = visualRay.intersectObjects(receivers.current.meshes, false)[0]
    ray.origin.x = origin.x; ray.origin.y = origin.y + .3; ray.origin.z = origin.z
    const centre = world.castRayAndGetNormal(ray, 3.3, true, rapier.QueryFilterFlags.EXCLUDE_SENSORS,
      undefined, undefined, body)
    const physicsY = centre ? ray.origin.y - centre.timeOfImpact : origin.y
    const lift = visual ? Math.max(0, Math.min(.35, visual.point.y - physicsY)) : 0
    const opacity = updateContactPatch(geometry, origin, (x, z) => {
      ray.origin.x = x; ray.origin.y = origin.y + .3; ray.origin.z = z
      const hit = world.castRayAndGetNormal(ray, 3.3, true, rapier.QueryFilterFlags.EXCLUDE_SENSORS,
        undefined, undefined, body)
      return hit ? { height: ray.origin.y - hit.timeOfImpact + lift, normal: hit.normal } : null
    }, CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius + CHARACTER.floatHeight)
    mesh.current.material.uniforms.strength.value = opacity
    mesh.current.visible = opacity > .001
    if (import.meta.env.DEV) mesh.current.userData.contact = { opacity,
      triangles: geometry.drawRange.count / 3, lift, groundY: physicsY + lift }
  })
  return <mesh ref={mesh} name="PlayerContactShadow" geometry={geometry} renderOrder={2} frustumCulled={false}>
    <shaderMaterial transparent depthWrite={false} side={DoubleSide}
      uniforms={{ strength: { value: 0 } }}
      vertexShader={`varying vec2 contactUv; void main() { contactUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`}
      fragmentShader={`varying vec2 contactUv; uniform float strength; void main() {
        float r = length((contactUv - .5) * 2.0);
        float alpha = pow(1.0 - smoothstep(.05, 1.0, r), 2.0) * strength;
        gl_FragColor = vec4(.018, .025, .02, alpha);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`} />
  </mesh>
}
