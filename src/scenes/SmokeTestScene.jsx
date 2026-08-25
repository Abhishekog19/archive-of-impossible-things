import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Physics, RigidBody } from '@react-three/rapier'
import { useGameStore } from '../store'

/**
 * STEP 0 SMOKE-TEST SCENE — throwaway.
 *
 * Its only job is to prove every link in the stack works, on desktop and on a
 * real phone, deployed. Nothing here is production art or production physics.
 *
 * What each part proves:
 *   three + R3F   — anything renders at all
 *   Rapier        — the WASM module loads and simulates (a real deploy risk)
 *   zustand       — React state and the 3D scene can talk to each other
 *   touch input   — tapping a cube works the same as clicking it
 */

/** A cube that falls under gravity and can be poked. */
function PokeableCube({ position, color }) {
  const body = useRef(null)
  const nudge = useGameStore((s) => s.nudge)

  const handlePoke = () => {
    // applyImpulse is an instantaneous push, unlike a continuous force.
    // The `true` wakes the body if the simulation had put it to sleep.
    body.current?.applyImpulse({ x: 0, y: 3.5, z: 0 }, true)
    nudge()
  }

  return (
    <RigidBody ref={body} position={position} colliders="cuboid" restitution={0.4}>
      <mesh onPointerDown={handlePoke}>
        <boxGeometry args={[1, 1, 1]} />
        {/* Temporary: the real game bakes its lighting and uses
            MeshBasicMaterial with zero runtime lights (spec §4.1). */}
        <meshStandardMaterial color={color} />
      </mesh>
    </RigidBody>
  )
}

/** Reports once the physics world has actually stepped. */
function PhysicsProbe() {
  const setPhysicsReady = useGameStore((s) => s.setPhysicsReady)
  const done = useRef(false)

  useFrame(() => {
    if (!done.current) {
      done.current = true
      setPhysicsReady()
    }
  })

  return null
}

export default function SmokeTestScene() {
  return (
    <>
      {/* Temporary lights. The real game has 0–1 and bakes the rest. */}
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 8, 3]} intensity={1.6} />

      <Physics>
        <PhysicsProbe />

        {/* Ground. `type="fixed"` means infinite mass — it never moves. */}
        <RigidBody type="fixed">
          <mesh position={[0, -0.5, 0]}>
            <boxGeometry args={[30, 1, 30]} />
            <meshStandardMaterial color="#4a5340" />
          </mesh>
        </RigidBody>

        <PokeableCube position={[-1.6, 4, 0]} color="#8fae6b" />
        <PokeableCube position={[0.2, 6, 0.4]} color="#c8a05a" />
        <PokeableCube position={[1.7, 8, -0.3]} color="#7a8b9c" />
      </Physics>
    </>
  )
}
