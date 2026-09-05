import { Suspense, useEffect, useRef, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { Physics } from '@react-three/rapier'
import { CAMERA, FOG, PALETTE, TIERS } from './config/look'
import { effectiveDpr } from './config/tiers'
import FollowCamera from './player/FollowCamera'
import Player from './player/Player'
import GreyRoom from './scenes/GreyRoom'
import DevHud from './ui/DevHud'
import DevProbe from './ui/DevProbe'
import PerfProbe from './ui/PerfProbe'
import TierGovernor from './ui/TierGovernor'
import MobileControls from './ui/MobileControls'
import Settings from './ui/Settings'
import { useGameStore } from './store'

/**
 * Does this browser support WebGL2?
 *
 * Design doc §14 requires that a device which can't run the game gets the plain
 * professional portfolio rather than a black screen. Still a placeholder — the
 * real fallback is built at M12.
 */
function hasWebGL2() {
  try {
    const gl = document.createElement('canvas').getContext('webgl2')
    if (!gl) return false
    gl.getExtension('WEBGL_lose_context')?.loseContext()
    return true
  } catch {
    return false
  }
}

/**
 * Fog, and the reason the sky is a flat colour.
 *
 * look-target.md §5 makes fog colour equalling sky colour non-negotiable, and
 * §11 closed the sky question on the back of it: a blue sky forces blue fog,
 * which cools every distant surface and destroys the warm-light-against-
 * cool-shade relationship §4 is built on. So one colour does both jobs here, and
 * `far` is matched to the distance at which that fog is ~95% opaque — drawing
 * past it would be drawing things fog has already erased.
 */
function Atmosphere() {
  const fogEnabled = useGameStore((s) => s.fogEnabled)
  // Density is a tier value (look-target section 9); the store is the one
  // authority on which tier this device is on -- see config/tiers.js.
  const tier = useGameStore((s) => s.tier)
  return (
    <>
      <color attach="background" args={[PALETTE.sky]} />
      {fogEnabled && (
        <fogExp2 attach="fog" args={[FOG.color, TIERS[tier].fogDensity]} />
      )}
    </>
  )
}

/**
 * Is the page actually on screen?
 *
 * This exists because of a bug found the first time M1 was watched rather than
 * read. Hide the tab (or, in this dev setup, collapse the preview pane) and the
 * browser stops calling requestAnimationFrame. Come back and R3F delivers a
 * single frame whose delta is however many seconds you were away. Rapier then
 * integrates that in one step, the capsule teleports several metres, and on a
 * longer absence it tunnels straight through the plaza and falls out of the
 * world — which is exactly what happened, and which reads as "the physics is
 * broken" rather than "the clock jumped".
 *
 * Pausing the simulation while the page is hidden fixes it at the source instead
 * of clamping the symptom, and it is what the shipped game wants anyway: no
 * reason to simulate, or drain a phone battery, for a tab nobody is looking at.
 */
function usePageVisible() {
  const [visible, setVisible] = useState(() => !document.hidden)
  useEffect(() => {
    const onChange = () => setVisible(!document.hidden)
    document.addEventListener('visibilitychange', onChange)
    return () => document.removeEventListener('visibilitychange', onChange)
  }, [])
  return visible
}

export default function App() {
  // The ecctrl handle, shared by the camera (needs the body to follow) and the
  // scene (the post needs to know when the player is close).
  const playerRef = useRef(null)
  const visible = usePageVisible()
  const [webglSupported] = useState(hasWebGL2)
  const settingsOpen = useGameStore((s) => s.settingsOpen)
  // Dev stepping overrides the visibility pause — see store.js.
  const physicsForced = useGameStore((s) => s.physicsForced)
  // The detected/overridden tier and whatever resolution the governor has shed
  // past it. Computed here and passed as a prop so <Canvas dpr> is the single
  // authority on resolution -- TierGovernor never calls setDpr imperatively.
  const tier = useGameStore((s) => s.tier)
  const dprDrop = useGameStore((s) => s.dprDrop)

  if (!webglSupported) {
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
        onCreated={({ gl }) => { gl.domElement.tabIndex = -1 }}
        // Tier-driven (M2): detection order and the demote-only policy live in
        // config/tiers.js; the governor inside the Canvas supplies the evidence.
        dpr={effectiveDpr(tier, dprDrop)}
        // No `shadows`: the project budgets 0 real-time shadow maps
        // (technical-production-spec §4.2). Contact shadow is a blob decal later.
        // `far` is initial only -- TierGovernor maintains it on tier change,
        // matched to where the tier's fog is ~95% opaque (look-target section 5).
        camera={{ fov: CAMERA.fov, near: 0.1, far: TIERS[tier].far }}
        gl={{ antialias: true }}
      >
        <Atmosphere />

        {/* Temporary lighting. The shipped game has zero runtime lights and
            bakes everything (spec §4.1); §4 allows exactly one hemisphere light
            in the blockout, which is what this is. Warm above, cool below —
            the cheapest possible stand-in for warm light against cool shade. */}
        <hemisphereLight args={[PALETTE.sky, PALETTE.ground, 2.2]} />

        <Suspense fallback={null}>
          <Physics paused={(!visible || settingsOpen) && !physicsForced}>
            <GreyRoom playerRef={playerRef} />
            <Player ref={playerRef} />
            <FollowCamera bodyRef={playerRef} />
            {/* Dev-only scene handle for stepping the loop and running the M1
                audit. Inside <Physics> because it raycasts against the same
                world the camera does; dropped from production by this branch. */}
            {import.meta.env.DEV && <DevProbe playerRef={playerRef} />}
          </Physics>
        </Suspense>

        <PerfProbe />
        <TierGovernor />
      </Canvas>

      <DevHud />
      <MobileControls />
      <Settings />
    </>
  )
}
