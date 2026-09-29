import { useEffect, useMemo, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Html, useGLTF, useTexture } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide, RepeatWrapping } from 'three'
import manifest from '../config/placed-world.json'
import { desiredAreas, requiredAreas } from '../config/placed-streaming'
import { CAVERN_WATER } from '../config/cavern-water'
import { useGameStore } from '../store'
import { loadPlaced, disposePlaced } from './placedResource'
import { CavernSurfaces } from './CavernStructure'
import CavernWater from './CavernWater'

function Area({ area, detail, report, attempt }) {
  const gl = useThree(s => s.gl)
  const [resource, setResource] = useState(null)
  useEffect(() => {
    const abort = new AbortController()
    const statuses = report.current
    let owned
    loadPlaced(area.url, abort.signal, Math.min(4, gl.capabilities.getMaxAnisotropy()), detail, area.id === 'cavern')
      .then(value => { owned = value; setResource(value); statuses[area.id] = 'ready' })
      .catch(() => { if (!abort.signal.aborted) statuses[area.id] = 'failed' })
    return () => { abort.abort(); delete statuses[area.id]; if (owned) disposePlaced(owned.scene) }
  }, [area, detail, gl, report, attempt])
  // Mesh-cell frustum culling handles visibility. Keep a retained area visible
  // until eviction instead of switching its whole silhouette at a second radius.
  return <group name={`Area_${area.id}`} dispose={null}>
    {resource && (area.id === 'cavern' ? <CavernSurfaces nodes={resource.nodes} collision={false} />
      : <primitive object={resource.scene} />)}
  </group>
}

export default function StreamedWorld({ anchorZ = 6 }) {
  const { scene, nodes } = useGLTF(manifest.resident.url)
  const residentNodes = useMemo(() => { scene.updateMatrixWorld(true); return Object.values(nodes).filter(n => n.isMesh) }, [scene, nodes])
  const detailSource = useTexture('/textures/stone-grain.webp')
  const gl = useThree(s => s.gl)
  const detail = useMemo(() => {
    const texture = detailSource.clone()
    texture.wrapS = texture.wrapT = RepeatWrapping
    texture.anisotropy = Math.min(4, gl.capabilities.getMaxAnisotropy())
    texture.needsUpdate = true
    return texture
  }, [detailSource, gl])
  const [active, setActive] = useState(() => desiredAreas(anchorZ, manifest.zones, [], true))
  const [waiting, setWaiting] = useState('loading')
  const [attempt, setAttempt] = useState(0)
  const report = useRef({})
  const bootstrapped = useRef(false)
  const timer = useRef(0)
  useEffect(() => () => detail.dispose(), [detail])
  useEffect(() => {
    useGameStore.setState({ worldLoading: true })
    return () => useGameStore.setState({ worldLoading: false })
  }, [])
  useFrame(({ camera }, delta) => {
    timer.current += delta
    if (timer.current < .15) return
    timer.current = 0
    const required = requiredAreas(camera.position.z, manifest.zones)
    const ready = required.every(a => report.current[a.id] === 'ready')
    const status = ready ? '' : required.some(a => report.current[a.id] === 'failed') ? 'failed' : 'loading'
    setWaiting(previous => previous === status ? previous : status)
    if (useGameStore.getState().worldLoading !== !ready) useGameStore.setState({ worldLoading: !ready })
    if (ready) bootstrapped.current = true
    setActive(previous => {
      const next = desiredAreas(camera.position.z, manifest.zones, previous, !bootstrapped.current)
      for (const area of required) if (!next.includes(area.id)) next.push(area.id)
      return previous.join() === next.join() ? previous : next
    })
  })
  // Collision is resident even while a visual package downloads or is evicted.
  return <>
    {residentNodes.filter(n => !/Collision|Pool_study/.test(n.name)).map(node =>
      <mesh key={node.name} name={node.name} geometry={node.geometry} material={node.material} matrixAutoUpdate={false} matrix={node.matrixWorld}>
        {node.name.startsWith('WoodlandBackdrop') && <meshBasicMaterial vertexColors side={DoubleSide} />}
      </mesh>)}
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      {residentNodes.filter(n => /Collision/.test(n.name)).map(node =>
        <mesh key={node.name} geometry={node.geometry} visible={false} matrixAutoUpdate={false} matrix={node.matrixWorld} />)}
    </RigidBody>
    {active.map(id => <Area key={`${id}-${attempt}`} area={manifest.zones.find(a => a.id === id)}
      detail={detail} report={report} attempt={attempt} />)}
    <CavernWater geometry={nodes.Pool_study.geometry} shoreline openingLight={CAVERN_WATER.opening} />
    {waiting && <Html fullscreen style={{ pointerEvents: 'none' }}><div style={{ position: 'absolute', bottom: 28,
      left: '50%', transform: 'translateX(-50%)', padding: '12px 18px', borderRadius: 8, background: '#202c36ed',
      color: '#eef0e8', font: '14px system-ui', pointerEvents: 'auto', textAlign: 'center' }}>
      {waiting === 'failed' ? <>This area couldn’t load. <button onClick={() => { report.current = {}; setAttempt(n => n + 1) }}>Retry</button></> : 'Preparing this area…'}
    </div></Html>}
  </>
}
