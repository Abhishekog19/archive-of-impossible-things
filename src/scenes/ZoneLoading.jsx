import { useEffect, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { createRoot } from 'react-dom/client'
import { CuboidCollider, RigidBody } from '@react-three/rapier'
import KitBatch from './KitBatch'
import { disposeZone, loadZone } from './zoneResource'
import packages from '../config/zone-packages.json'

const zones = [
  { id: 'ruins', center: -5, enter: 28, exit: 40, gates: [3, -18] },
  { id: 'forest', center: -43, enter: 29, exit: 39, gates: [-20, -62] },
]
const placements = { ruins: {}, forest: {} }
function put(zone, name, x, z, scale = 1, yaw = 0, y = 0) {
  ;(placements[zone][name] ??= []).push({ position: [x, y, z], scale, yaw })
}
for (let row = 0; row < 16; row++) {
  for (let col = 0; col < 4; col++) {
    put('ruins', `Slab_${1 + (row * 3 + col) % 6}`, (col - 1.5) * 1.12,
      2 - row * 1.12, 1, 0, -0.08)
  }
}
put('ruins', 'Arch_Ruin', 0, -12)
for (const [x, z] of [[-4, -4], [4, -7]]) put('ruins', 'Column_Broken', x, z)
for (let i = 0; i < 8; i++) {
  put('ruins', `Masonry_${1 + i % 4}`, -4, 1 - i * 1.1)
}
for (let i = 0; i < 8; i++) {
  const name = ['Tree_Tall', 'Tree_Leaning', 'Tree_Broadleaf'][i % 3]
  const leaves = name === 'Tree_Broadleaf' ? 'Tree_Leaves' : `${name}_Leaves`
  const x = (i % 2 ? -1 : 1) * (5 + Math.sin(i) * 0.5), z = -28 - i * 3.7
  put('forest', name, x, z, 1 + (i % 3) * 0.12)
  put('forest', leaves, x, z, 1 + (i % 3) * 0.12)
}
for (let i = 0; i < 48; i++) {
  put('forest', ['Fern', 'Grass_Tuft', 'Broadleaf_Clump', 'Low_Shrub'][i % 4],
    (i % 2 ? -1 : 1) * (3 + Math.sin(i * 2.4) * 0.7), -24 - i * 0.7,
    0.8 + (i % 3) * 0.15, i * 2.399)
}

function ZoneStatus({ zone, status, children }) {
  const canvas = useThree((s) => s.gl.domElement)
  const root = useRef(null)
  useEffect(() => {
    const container = document.createElement('div')
    canvas.parentElement.appendChild(container)
    const domRoot = createRoot(container)
    root.current = domRoot
    return () => {
      root.current = null
      container.remove()
      // R3F has its own React renderer; finish its commit before unmounting DOM.
      queueMicrotask(() => domRoot.unmount())
    }
  }, [canvas])
  useEffect(() => {
    root.current?.render(<div data-testid={`zone-${zone.id}`} style={{ position: 'absolute', right: 12,
      top: zone.id === 'ruins' ? 60 : 102, padding: '5px 9px', color: '#f0eedf',
      background: '#273023dd', font: '12px monospace', borderRadius: 4, pointerEvents: 'none' }}>
      {zone.id}: {status} {children}
    </div>)
  }, [zone, status, children])
  return null
}

function WaitingGate({ zone }) {
  return <RigidBody type="fixed" colliders={false}>
    {zone.gates.map((z) => <CuboidCollider key={z} args={[8, 4, 0.15]} position={[0, 4, z]} />)}
  </RigidBody>
}

function LoadedZone({ zone, attempt, retry }) {
  const gl = useThree((s) => s.gl)
  const [state, setState] = useState({ status: 'loading', resource: null })
  useEffect(() => {
    const controller = new AbortController()
    let resource
    loadZone(packages.packages[zone.id].url, controller.signal,
      Math.max(1, Math.min(4, gl.capabilities.getMaxAnisotropy())))
      .then((loaded) => {
        if (controller.signal.aborted) { disposeZone(loaded.scene); return }
        resource = loaded
        setState({ status: 'ready', resource })
      }).catch((error) => {
        if (!controller.signal.aborted) setState({ status: 'failed', resource: null, error: error.message })
      })
    return () => { controller.abort(); if (resource) disposeZone(resource.scene) }
  }, [zone, attempt, gl])

  return <group name={`Streamed_${zone.id}`} userData={{ status: state.status }} dispose={null}>
    <ZoneStatus zone={zone} status={state.status}>
      {state.status === 'ready' && `${(state.resource.bytes / 1e6).toFixed(2)} MB`}
      {state.status === 'failed' && <button style={{ pointerEvents: 'auto' }} onClick={retry}>Retry {zone.id}</button>}
    </ZoneStatus>
    {state.status !== 'ready' ? <WaitingGate zone={zone} /> :
      Object.entries(placements[zone.id]).map(([name, transforms]) => {
        const node = state.resource.nodes[name]
        const collision = state.resource.nodes[`Collider_${name}`]
        return <group key={name}>
          <KitBatch node={node} transforms={transforms} />
          {collision && transforms.map(({ position, scale, yaw }, i) =>
            <RigidBody key={i} type="fixed" colliders="trimesh" includeInvisible
              position={position} scale={scale} rotation={[0, yaw, 0]}>
              <mesh geometry={collision.geometry} visible={false} />
            </RigidBody>)}
        </group>
      })}
  </group>
}

function Zone({ zone, active }) {
  const [attempt, setAttempt] = useState(0)
  return active ? <LoadedZone key={attempt} zone={zone} attempt={attempt}
    retry={() => setAttempt((value) => value + 1)} /> : <>
    <ZoneStatus zone={zone} status="unloaded" />
    <WaitingGate zone={zone} />
  </>
}

export default function ZoneLoading({ playerRef, reference = false, view }) {
  const [active, setActive] = useState(() => [true, reference])
  const current = useRef([true, reference])
  const camera = useThree((s) => s.camera)
  useFrame(() => {
    const body = playerRef.current?.body
    if (reference || !body) return
    const z = body.translation().z
    const next = zones.map((zone, i) => Math.abs(z - zone.center) <= (current.current[i] ? zone.exit : zone.enter))
    if (next.some((value, i) => value !== current.current[i])) {
      current.current = next
      setActive(next)
    }
  })
  useEffect(() => {
    if (!reference) return
    if (view === 'zone-forest') { camera.position.set(0.6, 2.8, -20); camera.lookAt(0, 2.8, -48) }
    else { camera.position.set(13, 10, 12); camera.lookAt(0, 1, -18) }
    camera.updateProjectionMatrix()
  }, [reference, camera, view])
  return <>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.03, -24]}>
      <planeGeometry args={[28, 96]} /><meshBasicMaterial color="#4a5340" />
    </mesh>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.02, -24]}>
      <planeGeometry args={[4.8, 90]} /><meshBasicMaterial color="#77735a" />
    </mesh>
    {/* The inspection floor/boundaries remain resident during async loading. */}
    <RigidBody type="fixed" colliders={false}>
      <CuboidCollider args={[8, 0.2, 46]} position={[0, -0.17, -24]} />
      {[-8, 8].map((x) => <CuboidCollider key={x} args={[0.2, 4, 46]} position={[x, 4, -24]} />)}
      {[-70, 22].map((z) => <CuboidCollider key={z} args={[8, 4, 0.2]} position={[0, 4, z]} />)}
    </RigidBody>
    {zones.map((zone, i) => <Zone key={zone.id} zone={zone} active={active[i]} />)}
  </>
}
