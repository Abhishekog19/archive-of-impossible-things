import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stats } from '@react-three/drei'
import SmokeTestScene from './scenes/SmokeTestScene'
import { useGameStore } from './store'

/**
 * Does this browser support WebGL2?
 *
 * Design doc §14 requires that a device which can't run the game gets the
 * plain professional portfolio rather than a black screen. This is the
 * cheapest possible placeholder for that path — enough to prove the failure
 * mode is handled. The real fallback is built at Step 10.
 */
function hasWebGL2() {
  try {
    return !!document.createElement('canvas').getContext('webgl2')
  } catch {
    return false
  }
}

/** Small overlay so the smoke test is readable on a phone, not just a laptop. */
function StatusOverlay() {
  const nudges = useGameStore((s) => s.nudges)
  const physicsReady = useGameStore((s) => s.physicsReady)

  return (
    <div className="status-overlay">
      <strong>Step 0 — stack smoke test</strong>
      <span>render: three + R3F ✓</span>
      <span>physics: {physicsReady ? 'Rapier WASM ✓' : 'loading…'}</span>
      <span>state: zustand ✓ ({nudges} nudges)</span>
      <span className="hint">drag to orbit · tap a cube to push it</span>
    </div>
  )
}

export default function App() {
  if (!hasWebGL2()) {
    return (
      <div className="fallback">
        <h1>Archive of Impossible Things</h1>
        <p>
          This browser can&apos;t run WebGL2, so the interactive version
          won&apos;t load. The written portfolio will live here.
        </p>
      </div>
    )
  }

  return (
    <>
      <Canvas
        // dpr capped per spec §4.4 — the single biggest performance knob.
        // Native DPR is 2–3 on most phones and many laptops; 1.5 is close to
        // invisible in a stylized scene and roughly 2.5x cheaper to fill.
        dpr={[1, 1.5]}
        // No `shadows` prop: the project budgets 0 real-time shadow maps
        // (spec §4.2). Contact shadows come from a blob decal later.
        camera={{ position: [7, 6, 10], fov: 50 }}
        gl={{ antialias: true }}
      >
        {/* Suspense catches the async Rapier WASM load. Without it, React
            throws when the physics module suspends on first render. */}
        <Suspense fallback={null}>
          <SmokeTestScene />
        </Suspense>

        <OrbitControls makeDefault enableDamping target={[0, 1, 0]} />

        {/* Temporary FPS panel. Replaced at Step 2 by a proper dev HUD
            showing draw calls, triangles and texture memory. */}
        <Stats />
      </Canvas>

      <StatusOverlay />
    </>
  )
}
