import { forwardRef, useImperativeHandle, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Ecctrl } from 'ecctrl'
import { CHARACTER, PALETTE } from '../config/look'
import { useGameStore } from '../store'
import useMovementInput from './useMovementInput'

/**
 * The player: an ecctrl capsule with a placeholder body.
 *
 * No character art here on purpose. look-target.md section 11 item 7 flags that
 * no reference image contains a figure at all, and character work is the weakest
 * part of this pipeline -- so M1 tests the *capsule*, at exactly the specified
 * 1.70 m x 0.35 m, and the CC0 rig arrives later. Anything taller or shorter
 * than 1.70 m would invalidate every camera number in section 2.
 *
 * The placeholder is deliberately readable rather than a bare capsule: a nose
 * block, because without one you cannot tell which way you are facing, and
 * "which way am I facing" is half of what the 90-second walk gate is judging.
 */

const SPAWN = [0, 2, 6]

// --- Movement feel (check 13 returned NO, 2026-09-03) ------------------------
//
// The first 90-second walk gate failed on three counts: too slow, the capsule
// read as hovering, and nothing on the body indicated motion. These are feel
// numbers, not look-target numbers, which is why they live here and not in
// config/look.js -- look.js only holds values the document defines.
//
// NOTE for M5: look-target section 6 sizes tree spacing and fog distance off a
// walking pace, and section 11 item 3 warns that speed eats sight distance.
// Walk speed rose from 2.2 to 3.0 here; re-check those numbers when the road
// is real.
const MOVE = {
  maxWalkVel: 3.0, // was 2.2 -- measured as trudging at the walk gate
  maxRunVel: 5.4, // was 4.2 -- keeps roughly the same walk-to-run ratio
}

// Ecctrl floats the physics capsule `floatHeight` above the ground on a spring
// (that float is what makes stairs and bumps feel smooth, and it stays). The
// hovering *look* was the visual mesh being centred on the rigid body, leaving
// a visible air gap under the feet. The fix is visual only: the whole body
// group sits floatHeight lower, so the rendered capsule touches the ground
// while the physics is untouched -- checks 3-5 keep their measured behaviour.
const REST_Y = -CHARACTER.floatHeight

// The walk cycle, as motion on the visual group only. Phase advances with
// distance covered rather than time, so cadence tracks speed for free and
// stops when the character stops.
const BOB = {
  strideLength: 1.1, // metres per full cycle (two footfalls)
  bobAmp: 0.05, // vertical rise between footfalls
  swayAmp: 0.04, // radians of side-to-side roll, alternating per step
  leanAmp: 0.07, // radians of forward lean at full run speed
  settle: 8, // how quickly motion eases in/out (per second)
}

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
      // can report a bug against. "It slides at x = -8" is actionable; "it
      // slides somewhere" is not.
      x: c.currPos.x,
      z: c.currPos.z,
    })
  })

  return null
}

/**
 * Animates the visual body group with a walk cycle: a per-step vertical bob,
 * an alternating sway, and a speed-proportional forward lean. Purely visual --
 * the rigid body and camera pivot never move, so the camera stays steady while
 * the character visibly works, which is the stable-camera / animated-body split
 * that readable third-person movement wants.
 */
function BodyMotion({ controllerRef, groupRef }) {
  const phase = useRef(0)
  const intensity = useRef(0)

  useFrame((_, delta) => {
    const c = controllerRef.current
    const g = groupRef.current
    if (!c || !g) return

    const speed = c.moveSpeed || 0
    const moving = c.isOnGround && speed > 0.15

    if (moving) {
      phase.current += (speed * delta * Math.PI * 2) / BOB.strideLength
    }

    // Intensity eases in and out so stopping mid-stride settles instead of
    // freezing the pose, and airborne frames (stairs, the jump) fade the cycle
    // rather than cutting it.
    const target = moving ? Math.min(speed / MOVE.maxRunVel, 1) : 0
    intensity.current += (target - intensity.current) * Math.min(1, BOB.settle * delta)
    const k = intensity.current

    // abs(sin) gives two footfalls per cycle: the body is lowest at each
    // contact and rises between them, so the feet never visually sink.
    g.position.y = REST_Y + Math.abs(Math.sin(phase.current)) * BOB.bobAmp * k
    g.rotation.z = Math.sin(phase.current) * BOB.swayAmp * k
    // -Z is forward, so leaning forward is a negative rotation about X.
    g.rotation.x = -BOB.leanAmp * k
  })

  return null
}

const Player = forwardRef(function Player(_props, ref) {
  const controllerRef = useRef(null)
  const bodyGroupRef = useRef(null)

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
        // for mobile. It is also the honest thing to test against the noisy
        // road, since a single ray is what will struggle there -- if it
        // survives that surface, shapeCast is available as a straight upgrade.
        groundDetection="rayCast"
        // A walking game. Section 6 sizes the road and the tree spacing off a
        // walking pace; the traversal verb is still open (design doc section
        // 19), and if it turns out faster than walking, fog distance has to
        // grow with it. Values and the check-13 history live in MOVE above.
        maxWalkVel={MOVE.maxWalkVel}
        maxRunVel={MOVE.maxRunVel}
      >
        {/* Visual body group. Sits REST_Y lower than the rigid body so the
            rendered capsule touches the ground the physics floats above, and
            carries the BodyMotion walk cycle. Visual only -- colliders and the
            camera pivot are unaffected. */}
        <group ref={bodyGroupRef} position={[0, REST_Y, 0]}>
          {/* Body. Offset down by the radius so the capsule's straight section
              is centred on the rigid body, matching ecctrl's collider. */}
          <mesh position={[0, 0, 0]} castShadow={false}>
            <capsuleGeometry
              args={[CHARACTER.capsuleRadius, CHARACTER.capsuleHalfHeight * 2, 6, 12]}
            />
            <meshStandardMaterial color={PALETTE.stone} />
          </mesh>

          {/* Facing marker -- the "nose". -Z is forward in three.js. */}
          <mesh position={[0, 0.35, -CHARACTER.capsuleRadius - 0.1]}>
            <boxGeometry args={[0.16, 0.16, 0.24]} />
            <meshStandardMaterial color={PALETTE.daylight} />
          </mesh>
        </group>
      </Ecctrl>

      <StateProbe controllerRef={controllerRef} />
      <BodyMotion controllerRef={controllerRef} groupRef={bodyGroupRef} />
    </>
  )
})

export default Player