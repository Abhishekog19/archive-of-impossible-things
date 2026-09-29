import { Suspense, useLayoutEffect, useRef, useState } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { OrbitControls, useGLTF, Html } from '@react-three/drei'

const VIEWS = {
  Front: { position: [0, .94, 4], target: [0, .88, 0], zoom: 290 },
  Side: { position: [4, .94, 0], target: [0, .88, 0], zoom: 290 },
  Back: { position: [0, .94, -4], target: [0, .88, 0], zoom: 290 },
  Face: { position: [.22, 1.62, 3], target: [0, 1.58, 0], zoom: 1150 },
}

function StudyModel() {
  const { scene } = useGLTF('/models/ruin-runner-study.glb')
  return <primitive object={scene} dispose={null} />
}

function ReviewCamera({ view }) {
  const { get, size, invalidate } = useThree()
  const controls = useRef(null)
  useLayoutEffect(() => {
    const preset = VIEWS[view]
    // R3F's live camera is an imperative Three.js object, retrieved in the effect.
    const camera = get().camera
    camera.position.set(...preset.position)
    camera.zoom = preset.zoom * Math.min(size.height / 600, size.width / 450)
    camera.lookAt(...preset.target)
    camera.updateProjectionMatrix()
    controls.current.target.set(...preset.target)
    controls.current.update()
    invalidate()
  }, [get, size, view, invalidate])
  return <OrbitControls ref={controls} makeDefault enableDamping={false} minZoom={80} maxZoom={2400} />
}

/** Development-only neutral asset review; does not mount the game or controller. */
export default function CharacterStudy() {
  const [view, setView] = useState('Front')
  return <main style={{ height: '100dvh', background: '#242820', color: '#eee9dc', display: 'flex', flexDirection: 'column', fontFamily: 'system-ui' }}>
    <header style={{ padding: '12px 20px', display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
      <strong>PD08 · Ruin Runner study</strong>
      <span style={{ fontSize: 13 }}>Neutral model · not rigged · visual acceptance pending</span>
      <nav aria-label="Character views" style={{ display: 'flex', gap: 6 }}>
        {Object.keys(VIEWS).map(name => <button key={name} onClick={() => setView(name)} aria-pressed={name === view}
          style={{ color: name === view ? '#20251c' : '#eee9dc', background: name === view ? '#d4c9a4' : '#414737', border: 0, borderRadius: 4, padding: '7px 12px', cursor: 'pointer' }}>{name}</button>)}
      </nav>
    </header>
    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', flex: 1, minHeight: 0 }}>
      <figure style={{ margin: 0, minHeight: 0, display: 'flex', flexDirection: 'column', background: '#ddd9d0' }}>
        <figcaption style={{ padding: '8px 16px', color: '#35362e', fontSize: 13 }}>Selected reference · Image 3</figcaption>
        <img src="/concept/character/ruin-runner-approved.png" alt="Approved Ruin Runner front, side and back concept" style={{ width: '100%', flex: 1, minHeight: 0, objectFit: 'contain' }} />
      </figure>
      <section aria-label="Interactive character study" style={{ minWidth: 0, minHeight: 0 }}>
        <Canvas orthographic frameloop="demand" dpr={[1, 1.5]} camera={{ position: [0, .94, 4], zoom: 290, near: .01, far: 30 }}>
          <color attach="background" args={['#a5a093']} />
          <hemisphereLight args={['#fff3de', '#67634e', 1.8]} />
          <directionalLight position={[-3, 4, 4]} color="#fff0d8" intensity={2.4} />
          <directionalLight position={[3, 2, -2]} color="#dbe6f0" intensity={1.5} />
          <Suspense fallback={<Html center>Loading model…</Html>}><StudyModel /></Suspense>
          <ReviewCamera view={view} />
        </Canvas>
      </section>
    </div>
    <footer style={{ fontSize: 12, padding: '8px 20px' }}>Drag to orbit · Scroll to zoom · Compare silhouette, face/hair, garment layering and material separation.</footer>
  </main>
}
