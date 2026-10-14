import { useEffect, useMemo, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useTexture } from '@react-three/drei'
import { RigidBody } from '@react-three/rapier'
import { DoubleSide, Group, Mesh, MeshBasicMaterial, RepeatWrapping } from 'three'
import manifest from '../config/placed-world.json'
import { desiredAreas, requiredAreas, startupAreas } from '../config/placed-streaming'
import { CAVERN_WATER } from '../config/cavern-water'
import { useGameStore } from '../store'
import { loadPlaced, disposePlaced } from './placedResource'
import { CavernSurfaces } from './CavernStructure'
import CavernWater from './CavernWater'
import { addBarkDetail, addStoneDetail } from './stoneDetail'
import { addOutdoorLighting } from './outdoorLighting'
import { prepareScene } from './prepareScene'
import ScreenOverlay from '../ui/ScreenOverlay'
import { batchStaticMeshes } from './staticBatches'

function Area({ area, detail, report, attempt }) {
  const gl = useThree(s => s.gl)
  const camera = useThree(s => s.camera)
  const scene = useThree(s => s.scene)
  const [resource, setResource] = useState(null)
  useEffect(() => {
    const abort = new AbortController()
    const statuses = report.current
    let owned, preparing = true
    const onStage = stage => { if (!abort.signal.aborted) statuses[area.id] = stage }
    const cavern = area.id === 'cavern'
    const anisotropy = Math.min(gl.capabilities.getMaxAnisotropy(), cavern ? useGameStore.getState().tier === 'low' ? 2 : 8 : 4)
    async function prepare() {
      try {
        owned = await loadPlaced(area.url, abort.signal, anisotropy, detail, cavern, onStage, gl.extensions.has('WEBGL_multi_draw'))
        await prepareScene(gl, owned.scene, camera, scene, abort.signal, onStage, [detail])
        abort.signal.throwIfAborted()
        setResource(owned)
        onStage('ready')
      } catch {
        onStage('failed')
      } finally {
        preparing = false
        if (abort.signal.aborted && owned) disposePlaced(owned.scene)
      }
    }
    prepare()
    return () => {
      abort.abort(); delete statuses[area.id]
      // compileAsync still polls the material's program. Keep it alive until
      // preparation settles, even when travel/retry unmounts this area early.
      if (!preparing && owned) disposePlaced(owned.scene)
    }
  }, [area, detail, gl, camera, scene, report, attempt])
  // Mesh-cell frustum culling handles visibility. Keep a retained area visible
  // until eviction instead of switching its whole silhouette at a second radius.
  return <group name={`Area_${area.id}`} dispose={null}>
    {resource && (area.id === 'cavern' ? <CavernSurfaces nodes={resource.nodes} collision={false} prepared />
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
  const boundaryMaterials = useMemo(() => Object.fromEntries(['Stone', 'Wood', 'Foliage'].map(kind => {
    const material = new MeshBasicMaterial({ vertexColors: true, side: DoubleSide })
    if (kind === 'Stone') addStoneDetail(material, detail)
    if (kind === 'Wood') addBarkDetail(material, detail)
    addOutdoorLighting(material)
    return [kind, material]
  })), [detail])
  useEffect(() => () => Object.values(boundaryMaterials).forEach(material => material.dispose()), [boundaryMaterials])
  const residentRoot = useRef(null)
  useEffect(() => {
    const parent = residentRoot.current, group = new Group()
    const backdrop = new MeshBasicMaterial({ vertexColors: true, side: DoubleSide })
    for (const node of residentNodes.filter(n => !/Collision|Pool_study/.test(n.name))) {
      const material = node.name.startsWith('HubBoundary_') ? boundaryMaterials[node.name.split('_')[1]]
        : node.name.startsWith('WoodlandBackdrop') ? backdrop : node.material
      const mesh = new Mesh(node.geometry, material)
      mesh.name = node.name
      mesh.matrix.copy(node.matrixWorld)
      mesh.matrixAutoUpdate = false
      group.add(mesh)
    }
    // Without multi-draw, keep ordinary meshes instead of adding vertex-texture
    // work for the same number of submissions on a less capable browser.
    const batches = gl.extensions.has('WEBGL_multi_draw') ? batchStaticMeshes(group) : []
    group.updateMatrixWorld(true)
    group.traverse(node => { node.matrixAutoUpdate = false; node.matrixWorldAutoUpdate = false })
    parent.add(group)
    return () => {
      parent.remove(group)
      batches.forEach(batch => batch.dispose())
      backdrop.dispose()
      // Original resident geometry/materials belong to the useGLTF cache.
    }
  }, [residentNodes, boundaryMaterials, gl])
  const entry = useMemo(() => startupAreas(anchorZ, manifest.zones), [anchorZ])
  const [active, setActive] = useState(() => startupAreas(anchorZ, manifest.zones))
  const [waiting, setWaiting] = useState({ status: 'loading', ready: 0, total: 1, stage: 'download', entered: false })
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
    if (!bootstrapped.current) for (const id of entry) {
      const area = manifest.zones.find(a => a.id === id)
      if (!required.includes(area)) required.push(area)
    }
    const ready = required.every(a => report.current[a.id] === 'ready')
    const status = ready ? '' : required.some(a => report.current[a.id] === 'failed') ? 'failed' : 'loading'
    const finished = required.filter(a => report.current[a.id] === 'ready').length
    const stage = report.current[required.find(a => report.current[a.id] !== 'ready')?.id] || 'download'
    const entered = bootstrapped.current || ready
    setWaiting(previous => previous.status === status && previous.ready === finished && previous.total === required.length && previous.stage === stage && previous.entered === entered
      ? previous : { status, ready: finished, total: required.length, stage, entered })
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
    <group ref={residentRoot} dispose={null} />
    <RigidBody type="fixed" colliders="trimesh" includeInvisible>
      {residentNodes.filter(n => /Collision/.test(n.name)).map(node =>
        <mesh key={node.name} geometry={node.geometry} visible={false} matrixAutoUpdate={false} matrix={node.matrixWorld} />)}
    </RigidBody>
    {active.map(id => <Area key={`${id}-${attempt}`} area={manifest.zones.find(a => a.id === id)}
      detail={detail} report={report} attempt={attempt} />)}
    <CavernWater geometry={nodes.Pool_study.geometry} shoreline openingLight={CAVERN_WATER.opening} />
    {/* Loading UI stays in screen space while the third-person camera settles. */}
    {waiting.status && <ScreenOverlay><div className={`world-loading ${waiting.entered ? 'world-loading-travel' : ''}`} role="status" aria-live="polite">
      <strong>{waiting.entered ? 'Preparing the path ahead' : 'Entering the Archive'}</strong>
      {waiting.status === 'failed' ? <><p>This area couldn’t load.</p><button onClick={() => { report.current = {}; setAttempt(n => n + 1) }}>Retry</button></>
        : <><p>{{ download: 'Loading the landscape…', decode: 'Unpacking the scenery…', textures: 'Preparing textures…', shaders: 'Preparing light and materials…' }[waiting.stage] || 'Preparing the landscape…'}</p>
          <span>{waiting.ready} of {waiting.total} nearby areas ready</span></>}
    </div></ScreenOverlay>}
  </>
}
