import { forwardRef, useImperativeHandle, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Ecctrl } from 'ecctrl'
import { CHARACTER } from '../config/look'
import Explorer from './Explorer'
import ContactShadow from './ContactShadow'
import { useGameStore } from '../store'
import useMovementInput from './useMovementInput'
import { MOVEMENT, SPAWN, CORNER_SPAWN, WORLD_SPAWNS, reachedCheckpoint } from './movement'

function StateProbe({ controllerRef, active, recoverFalls, checkpoints, respawn }) {
  const setPlayerDebug = useGameStore((s) => s.setPlayerDebug)
  const safeSpawn = useRef(respawn)
  const acc = useRef(0)

  useFrame((_, delta) => {
    const c = controllerRef.current
    if (!active || !c?.body) return
    const position = c.body.translation()
    if (checkpoints) {
      const next = reachedCheckpoint(position, c.isOnGround, c.verticalSpeed)
      if (next) safeSpawn.current = next
    }
    if (recoverFalls && position.y < -12) {
      const [x, y, z] = safeSpawn.current
      c.body.setTranslation({ x, y, z }, true)
      c.body.setLinvel({ x: 0, y: 0, z: 0 }, true)
      c.body.setAngvel({ x: 0, y: 0, z: 0 }, true)
      c.body.resetForces(true)
      c.body.resetTorques(true)
      useGameStore.getState().recordRecovery()
    }
    acc.current += delta
    if (acc.current < 0.1) return
    acc.current = 0
    setPlayerDebug({
      speed: c.moveSpeed, onGround: c.isOnGround,
      slopeDeg: (c.actualSlopeAngle * 180) / Math.PI,
      feetY: c.currPos.y - (CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius),
      x: c.currPos.x, z: c.currPos.z,
    })
  })
  return null
}

/** ecctrl owns the capsule; the existing explorer remains until PD08 is approved. */
const Player = forwardRef(function Player({ active = true, recoverFalls = false,
  recoverToStart = false, cornerStart = false, start }, ref) {
  const controllerRef = useRef(null)
  const spawn = cornerStart ? CORNER_SPAWN : Object.hasOwn(WORLD_SPAWNS, start) ? WORLD_SPAWNS[start] : SPAWN
  useMovementInput(controllerRef, active)
  useImperativeHandle(ref, () => controllerRef.current, [])

  return (
    <>
      <Ecctrl ref={controllerRef} enable={active} rotation={[0, Math.PI, 0]}
        position={spawn} capsuleHalfHeight={CHARACTER.capsuleHalfHeight}
        capsuleRadius={CHARACTER.capsuleRadius} floatHeight={CHARACTER.floatHeight}
        {...MOVEMENT}>
        <Explorer controllerRef={controllerRef} />
      </Ecctrl>
      <ContactShadow controllerRef={controllerRef} />
      <StateProbe controllerRef={controllerRef} active={active} recoverFalls={recoverFalls}
        checkpoints={recoverFalls && !recoverToStart} respawn={spawn} />
    </>
  )
})
export default Player
