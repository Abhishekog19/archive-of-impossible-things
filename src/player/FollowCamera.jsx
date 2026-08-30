import { useEffect, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useRapier } from '@react-three/rapier'
import * as THREE from 'three'
import { CAMERA, PIVOT_ABOVE_BODY } from '../config/look'
import { useGameStore } from '../store'

/**
 * The look-target.md §2 camera.
 *
 * ecctrl 2.x deliberately ships no follow camera — the 1.x camera props are
 * gone, and the README says to "build your own camera follow logic". That turns
 * out to be the right outcome here: §2 specifies exact numbers that no library
 * preset would have matched, so there is nothing to fight.
 *
 * Three decisions worth knowing, because none of them are obvious:
 *
 * 1. PITCH IS NOT SET, IT IS DERIVED. We place the camera 4.0 m back and 0.8 m
 *    up from the pivot and point it at the pivot. That geometry *is* −11.31°.
 *    Setting a pitch value separately would let the two drift apart.
 *
 * 2. PITCH IS ALSO NOT PLAYER-CONTROLLABLE. §2 wants the angle shallow, and
 *    M1's exit criterion is that the camera never shows sky above where a
 *    canopy line would be — which a free-pitch camera fails by definition. Yaw
 *    only. This is the most likely thing in M1 to need revisiting, so it's
 *    flagged rather than hidden.
 *
 * 3. DAMPING IS FRAME-RATE INDEPENDENT. §2's 0.12 reads as a per-frame lerp,
 *    but a raw per-frame lerp makes the camera tighter at 144 fps than at 30 —
 *    so the same build would feel different on a desktop and a phone, which is
 *    exactly the kind of bug that gets blamed on "phone feel". We treat 0.12 as
 *    the factor at 60 fps and correct for the real delta.
 */

/** Per-frame lerp factor `f` (defined at 60 fps) corrected for the real delta. */
function damp(f, delta) {
  return 1 - Math.pow(1 - f, delta * 60)
}

export default function FollowCamera({ bodyRef }) {
  const camera = useThree((s) => s.camera)
  const domElement = useThree((s) => s.gl.domElement)
  const { world, rapier } = useRapier()

  const setCameraDebug = useGameStore((s) => s.setCameraDebug)

  // Yaw is the only orbit axis. Kept in a ref rather than state: it changes
  // every pointer move and must never trigger a React render.
  const yaw = useRef(0)
  const dragging = useRef(false)

  // Scratch objects, allocated once on the first frame. Allocating inside
  // useFrame is the classic R3F garbage-collection stutter — a new Vector3 60
  // times a second per axis is thousands of short-lived objects a minute. The
  // Rapier Ray counts too: its origin and dir are mutable, so one instance is
  // reused forever.
  //
  // A ref rather than useMemo, and filled in on the first frame rather than
  // during render. These objects are mutated every frame, and mutating a value
  // produced during render is exactly what react-hooks' immutability rule
  // exists to catch — a ref is the sanctioned home for per-frame mutable state.
  const scratchRef = useRef(null)
  const initialised = useRef(false)

  // --- Yaw input -------------------------------------------------------------
  // Pointer events rather than mouse events, so a touch drag already works.
  // M2 replaces this with a proper look control alongside the joystick, but the
  // drag path is genuinely shared, so it is worth having correct now.
  useEffect(() => {
    const SENSITIVITY = 0.0045 // radians per pixel

    const onPointerDown = (e) => {
      if (e.button !== undefined && e.button !== 0) return
      dragging.current = true
      domElement.setPointerCapture?.(e.pointerId)
    }
    const onPointerMove = (e) => {
      if (!dragging.current) return
      yaw.current -= e.movementX * SENSITIVITY
    }
    const onPointerUp = (e) => {
      dragging.current = false
      domElement.releasePointerCapture?.(e.pointerId)
    }

    domElement.addEventListener('pointerdown', onPointerDown)
    domElement.addEventListener('pointermove', onPointerMove)
    domElement.addEventListener('pointerup', onPointerUp)
    domElement.addEventListener('pointercancel', onPointerUp)
    return () => {
      domElement.removeEventListener('pointerdown', onPointerDown)
      domElement.removeEventListener('pointermove', onPointerMove)
      domElement.removeEventListener('pointerup', onPointerUp)
      domElement.removeEventListener('pointercancel', onPointerUp)
    }
  }, [domElement])

  // --- Follow ----------------------------------------------------------------
  useFrame((_, delta) => {
    const body = bodyRef.current?.body
    if (!body) return

    if (!scratchRef.current) {
      scratchRef.current = {
        pivot: new THREE.Vector3(),
        smoothedPivot: new THREE.Vector3(),
        desired: new THREE.Vector3(),
        offset: new THREE.Vector3(),
        dir: new THREE.Vector3(),
        ray: new rapier.Ray({ x: 0, y: 0, z: 0 }, { x: 0, y: 0, z: 1 }),
      }
    }
    const scratch = scratchRef.current

    const t = body.translation()
    // The pivot is chest height above the *feet*, not above the body centre.
    scratch.pivot.set(t.x, t.y + PIVOT_ABOVE_BODY, t.z)

    // Snap on the first frame. Without this the camera flies in from wherever
    // the initial camera prop put it, which looks like a bug on every reload.
    if (!initialised.current) {
      scratch.smoothedPivot.copy(scratch.pivot)
      initialised.current = true
    } else {
      scratch.smoothedPivot.lerp(scratch.pivot, damp(CAMERA.damping, delta))
    }

    // Where §2 says the camera goes: distance behind along yaw, height above.
    scratch.offset.set(
      Math.sin(yaw.current) * CAMERA.distance,
      CAMERA.heightAbovePivot,
      Math.cos(yaw.current) * CAMERA.distance,
    )
    scratch.desired.copy(scratch.smoothedPivot).add(scratch.offset)

    // --- Collision: pull in, never clip ---
    // Cast from the pivot outward. If anything is in the way, the camera stops
    // short of it. Casting *from the pivot* rather than from the camera matters:
    // it means the ray starts inside the space the player occupies, so a wall
    // between player and camera is always found, even when the camera has
    // already ended up behind it.
    let distance = CAMERA.distance
    scratch.dir.copy(scratch.offset).normalize()

    const { ray } = scratch
    ray.origin.x = scratch.smoothedPivot.x
    ray.origin.y = scratch.smoothedPivot.y
    ray.origin.z = scratch.smoothedPivot.z
    ray.dir.x = scratch.dir.x
    ray.dir.y = scratch.dir.y
    ray.dir.z = scratch.dir.z

    const hit = world.castRay(
      ray,
      scratch.offset.length(),
      true,
      undefined,
      undefined,
      undefined,
      body, // never collide with the player's own capsule
    )
    if (hit) {
      const pulled = Math.max(
        CAMERA.minDistance,
        hit.timeOfImpact - CAMERA.collisionMargin,
      )
      scratch.desired
        .copy(scratch.smoothedPivot)
        .addScaledVector(scratch.dir, pulled)
      distance = pulled
    }

    camera.position.copy(scratch.desired)
    camera.lookAt(scratch.smoothedPivot)

    // Reported so the HUD can prove the derived pitch still matches §2 rather
    // than us asserting it in a comment.
    setCameraDebug(camera.position.y, distance, yaw.current)
  })

  return null
}
