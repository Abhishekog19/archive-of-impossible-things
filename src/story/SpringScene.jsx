import { useEffect, useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useRapier } from '@react-three/rapier'
import { CatmullRomCurve3, TubeGeometry, Vector3 } from 'three'
import { useGameStore } from '../store'
import { useSpring } from './springStore'
import { SPRING } from './spring'

const PATHS = [
  [[0,.24,0],[-.5,.24,-.2],[-1,.24,-.6],[-1.5,.24,-.9]],
  [[0,.24,0],[0,.24,-.6],[.15,.24,-1.1],[.35,.24,-1.65]],
  [[0,.24,0],[.6,.24,-.3],[1.2,.3,-.7],[1.3,1,-1],[1.1,1.9,-1.1]],
]

/** Disposable prototype dressing; no changes to the authored world or colliders. */
export default function SpringScene() {
  const { world, rapier } = useRapier()
  const root = useRef(null), streams = useRef([]), leaves = useRef(null), stones = useRef([]), bloom = useRef(null)
  const height = useRef(null), clock = useRef(0), check = useRef(0)
  const presentation = useRef({ bend: 0, lift: 0, bloom: 0, flows: [0,0,0] })
  const reducedMotion = useMemo(() => window.matchMedia('(prefers-reduced-motion: reduce)'), [])
  const paths = useMemo(() => PATHS.map(points => new CatmullRomCurve3(points.map(p => new Vector3(...p)))), [])
  const channels = useMemo(() => paths.map(p => new TubeGeometry(p, 28, .095, 6, false)), [paths])
  useEffect(() => () => channels.forEach(g => g.dispose()), [channels])
  const scratchRef = useRef(null)

  useFrame(({ camera, size }, delta) => {
    const game = useGameStore.getState()
    if (!root.current || document.hidden || game.worldLoading || game.settingsOpen) return
    if (!scratchRef.current) scratchRef.current = { ray: new rapier.Ray({ x: SPRING.x, y: 20, z: SPRING.z }, { x: 0, y: -1, z: 0 }), point: new Vector3(), camera: new Vector3(), target: new Vector3() }
    const scratch = scratchRef.current
    if (height.current === null) {
      const hit = world.castRayAndGetNormal(scratch.ray, 35, true, rapier.QueryFilterFlags.EXCLUDE_DYNAMIC | rapier.QueryFilterFlags.EXCLUDE_SENSORS)
      if (!hit) return
      height.current = 20 - hit.timeOfImpact
      root.current.position.y = height.current
      root.current.visible = true
    }
    const dt = Math.min(delta, .05), state = useSpring.getState().progress, p = presentation.current
    clock.current += dt; check.current += dt
    if (check.current > .15) {
      check.current = 0
      useSpring.getState().setProximity(Math.hypot(game.player.x - SPRING.x, game.player.z - SPRING.z) < SPRING.reach && Math.abs(game.player.feetY - height.current) < 3, true)
    }
    if (!game.interactionOpen && Math.abs(game.player.z - SPRING.z) > 40) return
    const smooth = reducedMotion.matches ? 1 : 1 - Math.exp(-dt * 3)
    p.bend += ((state.bent ? 1 : 0) - p.bend) * smooth
    p.lift += ((state.lifted ? 1 : 0) - p.lift) * smooth
    p.bloom += ((state.complete ? 1 : 0) - p.bloom) * smooth
    leaves.current.rotation.z = -.7 * p.bend
    stones.current.forEach((stone, i) => { stone.position.y = .24 + p.lift * (.22 + i * .12) + (reducedMotion.matches ? 0 : p.lift * Math.sin(clock.current * 1.4 + i) * .025) })
    bloom.current.scale.setScalar(.01 + p.bloom * .99)
    const selected = ['leaves','stones','root'].indexOf(state.route)
    streams.current.forEach((drop, i) => {
      const route = Math.floor(i / 6), step = i % 6
      p.flows[route] += (((selected === route || (route === 2 && state.complete)) ? 1 : 0) - p.flows[route]) * smooth / 6
      const t = (((reducedMotion.matches ? 0 : clock.current * .3) + step / 6) % 1) * (route === 2 && !state.complete ? .38 : 1)
      paths[route].getPoint(t, scratch.point)
      scratch.point.y += .1; scratch.point.z += .1
      drop.position.copy(scratch.point)
      drop.visible = p.flows[route] > .05
      drop.scale.setScalar(.6 + p.flows[route] * .4)
    })
    if (game.interactionOpen) {
      scratch.camera.set(SPRING.x + 3.5, height.current + 4.7, SPRING.z + 4.4)
      scratch.target.set(SPRING.x, height.current + .5, SPRING.z - .6)
      // Frame the experiment beside desktop text, or above the mobile sheet.
      if (size.width > 600) { scratch.target.x -= 1.1; scratch.target.z += .85 }
      else { scratch.camera.set(SPRING.x + 5, height.current + 6.5, SPRING.z + 6.3); scratch.target.y -= 1.7 }
      camera.position.lerp(scratch.camera, reducedMotion.matches ? 1 : 1 - Math.exp(-dt * 7))
      camera.lookAt(scratch.target)
    }
  })

  return <group ref={root} position={[SPRING.x, 0, SPRING.z]} visible={false} name="RememberingSpringPrototype">
    <mesh position={[0,.04,-.6]} scale={[2,.13,1.6]}><cylinderGeometry args={[1,1,1,12]} /><meshLambertMaterial color="#747260" /></mesh>
    <mesh rotation={[-Math.PI/2,0,0]} position={[0,.18,0]}><torusGeometry args={[.43,.13,6,16]} /><meshLambertMaterial color="#b8ad89" /></mesh>
    <mesh rotation={[-Math.PI/2,0,0]} position={[0,.2,0]}><circleGeometry args={[.37,20]} /><meshLambertMaterial color="#8da9a0" /></mesh>
    {channels.map((geometry,i) => <mesh key={i} geometry={geometry}><meshLambertMaterial color={i === 2 ? '#615b42' : '#454e43'} /></mesh>)}
    {Array.from({length:18},(_,i) => <mesh key={i} ref={el => { streams.current[i] = el }}><sphereGeometry args={[.07,6,4]} /><meshLambertMaterial color="#c1d8cd" /></mesh>)}
    <group position={[-1.5,.2,-.9]} ref={leaves}>
      {[0,1,2,3,4].map(i => <mesh key={i} rotation={[0,i*1.2,-.55]} position={[0,.25+i*.12,0]} scale={[.22,.5,.07]}><octahedronGeometry args={[1]} /><meshLambertMaterial color={i%2 ? '#7f9452' : '#a5ac6c'} /></mesh>)}
    </group>
    {[0,1,2].map(i => <mesh key={i} ref={el => { stones.current[i] = el }} position={[.35,.24,-1.3-i*.22]} scale={[.28,.12,.2]}><dodecahedronGeometry args={[1,0]} /><meshLambertMaterial color={i%2 ? '#c0b89a' : '#9c9981'} /></mesh>)}
    <group ref={bloom} position={[1.1,1.9,-1.1]} scale={.01}>
      {[0,1,2,3,4].map(i => <mesh key={i} rotation={[0,i*Math.PI*2/5,.9]} scale={[.12,.42,.09]}><octahedronGeometry args={[1]} /><meshLambertMaterial color="#c5ca91" /></mesh>)}
    </group>
  </group>
}
