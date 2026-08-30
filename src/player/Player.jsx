import { forwardRef, useImperativeHandle, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Ecctrl } from 'ecctrl'
import { CHARACTER, PALETTE } from '../config/look'
import { useGameStore } from '../store'
import useMovementInput from './useMovementInput'

/**
 * The player: an ecctrl capsule with a placeholder body.
 *
 * No character art here on purpose. look-target.md §11 item 7 flags that no
 * reference image contains a figure at all, and character work is the weakest
 * part of this pipeline — so M1 tests the *capsule*, at exactly the specified
 * 1.70 m × 0.35 m, and the CC0 rig arrives later. Anything taller or shorter
 * than 1.70 m would invalidate every camera number in §2.
 *
 * The placeholder is deliberately readable rather than a bare capsule: a nose
 * block, because without one you cannot tell which way you are facing, and
 * "which way am I facing" is half of what the 90-second walk gate is judging.
 */

const SPAWN = [0, 2, 6]

/** Feeds ecctrl runtime state into the store for the dev HUD. */
function StateProbe({ controllerRef }) {
  const setPlayerDebug = useGameStore((s) => s.setPlayerDebug)
  // Throttled: the HUD is text, and re-rendering React text 60 times a second
  // to show a number that changes in the third decimal is pure waste.
  const acc = useRef(0)

  useFrame((_, delta) => {
    const c = controllerRef.current
    if (!c) return
    acc.current += delta
    if (acc.current < 0.1) return
    acc.current = 0

    setPlayerDebug({
      speed: c.moveSpeed,
      onGround: c.isOnGround,
      slopeDeg: (c.actualSlopeAngle * 180) / Math.PI,
      feetY: c.currPos.y - (CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius),
      // Position, because a 30 m course you can get lost on is not a course you
      // can report a bug against. "It slides at x = −8" is actionable; "it
      // slides somewhere" is not.
      x: c.currPos.x,
      z: c.currPos.z,
    })
  })

  return null
}

const Player = forwardRef(function Player(_props, ref) {
  const controllerRef = useRef(null)

  useMovementInput(controllerRef)
  useImperativeHandle(ref, () => controllerRef.current, [])

  return (
    <>
      <Ecctrl
        ref={controllerRef}
        position={SPAWN}
        capsuleHalfHeight={CHARACTER.capsuleHalfHeight}
        capsuleRadius={CHARACTER.capsuleRadius}
        floatHeight={CHARACTER.floatHeight}
        // rayCast is the cheapest ground detection and the one ecctrl documents
        // for mobile. It is also the honest thing to test against the ±0.25 m
        // noisy road, since a single ray is what will struggle there — if it
        // survives that surface, shapeCast is available as a straight upgrade.
        groundDetection="rayCast"
        // A walking game. §6 sizes the road and the tree spacing off a walking
        // pace; the traversal verb is still open (design doc §19), and if it
        // turns out faster than walking, fog distance has to grow with it.
        maxWalkVel={2.2}
        maxRunVel={4.2}
      >
        {/* Body. Offset down by the radius so the capsule's straight section is
            centred on the rigid body, matching ecctrl's collider. */}
        <mesh position={[0, 0, 0]} castShadow={false}>
          <capsuleGeometry
            args={[CHARACTER.capsuleRadius, CHARACTER.capsuleHalfHeight * 2, 6, 12]}
          />
          <meshStandardMaterial color={PALETTE.stone} />
        </mesh>

        {/* Facing marker — the "nose". −Z is forward in three.js. */}
        <mesh position={[0, 0.35, -CHARACTER.capsuleRadius - 0.1]}>
          <boxGeometry args={[0.16, 0.16, 0.24]} />
          <meshStandardMaterial color={PALETTE.daylight} />
        </mesh>
      </Ecctrl>

      <StateProbe controllerRef={controllerRef} />
    </>
  )
})

export default Player
