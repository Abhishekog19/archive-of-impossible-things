import { forwardRef, useImperativeHandle, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Ecctrl } from 'ecctrl'
import { CHARACTER } from '../config/look'
import Explorer from './Explorer'
import { useGameStore } from '../store'
import useMovementInput from './useMovementInput'

/** ecctrl owns movement and collision; Explorer supplies skinned visual art. */
const SPAWN = [0, 2, 6]
const CORNER_SPAWN = [-8, 2, -4]
const WORLD_SPAWNS = {
  patch: [-12, 2.5, -20],
  forest: [-12, 3.5, -43], canopy: [-12, 3.5, -67],
  exterior: [-12, 3.5, -98], interior: [-12, 3.5, -116],
  cavern: [-12, -5.5, -174],
}

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

/** Feeds ecctrl runtime state into the store for the dev HUD. */
function StateProbe({ controllerRef, recoverFalls, respawn = SPAWN }) {
  const setPlayerDebug = useGameStore((s) => s.setPlayerDebug)
  // Throttled: the HUD is text, and re-rendering React text 60 times a second
  // to show a number that changes in the third decimal is pure waste.
  const acc = useRef(0)

  useFrame((_, delta) => {
    const c = controllerRef.current
    if (!c?.body) return
    if (recoverFalls && c.body.translation().y < -12) {
      c.body.setTranslation({ x: respawn[0], y: respawn[1], z: respawn[2] }, true)
      c.body.setLinvel({ x: 0, y: 0, z: 0 }, true)
      c.body.setAngvel({ x: 0, y: 0, z: 0 }, true)
    }
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

const Player = forwardRef(function Player({ recoverFalls = false, recoverToStart = false, cornerStart = false, start }, ref) {
  const controllerRef = useRef(null)

  useMovementInput(controllerRef)
  useImperativeHandle(ref, () => controllerRef.current, [])

  return (
    <>
      <Ecctrl
        ref={controllerRef}
        rotation={[0, Math.PI, 0]}
        position={cornerStart ? CORNER_SPAWN : Object.hasOwn(WORLD_SPAWNS, start) ? WORLD_SPAWNS[start] : SPAWN}
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
        <Explorer controllerRef={controllerRef} />
      </Ecctrl>

      <StateProbe controllerRef={controllerRef} recoverFalls={recoverFalls}
        respawn={recoverToStart && Object.hasOwn(WORLD_SPAWNS, start) ? WORLD_SPAWNS[start] : SPAWN} />
    </>
  )
})

export default Player
