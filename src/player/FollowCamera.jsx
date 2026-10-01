import { useEffect, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useRapier } from '@react-three/rapier'
import { Vector3 } from 'three'
import { CAMERA, PIVOT_ABOVE_BODY } from '../config/look'
import { useGameStore } from '../store'
import { cameraClearance, cameraLensRadius, recoverCameraDistance } from './cameraMotion'

/** Fixed-height, yaw-only follow camera; the reference composition is unchanged. */
export default function FollowCamera({ bodyRef }) {
  const camera = useThree(s => s.camera)
  const domElement = useThree(s => s.gl.domElement)
  const { world, rapier } = useRapier()
  const setCameraDebug = useGameStore(s => s.setCameraDebug)
  const yaw = useRef(0)
  const dragging = useRef(null)
  const lastX = useRef(0)
  const scratchRef = useRef(null)

  useEffect(() => {
    const reset = () => {
      const id = dragging.current
      dragging.current = null
      if (id !== null && domElement.hasPointerCapture(id)) domElement.releasePointerCapture(id)
    }
    const onDown = e => {
      const state = useGameStore.getState()
      if (e.button !== undefined && e.button !== 0) return
      if (dragging.current !== null || state.settingsOpen || state.worldLoading) return
      dragging.current = e.pointerId
      lastX.current = e.clientX
      domElement.setPointerCapture?.(e.pointerId)
    }
    const onMove = e => {
      if (dragging.current !== e.pointerId) return
      yaw.current -= (e.clientX - lastX.current) * 0.0045
      lastX.current = e.clientX
    }
    const onUp = e => { if (dragging.current === e.pointerId) reset() }
    domElement.addEventListener('pointerdown', onDown)
    domElement.addEventListener('pointermove', onMove)
    domElement.addEventListener('pointerup', onUp)
    domElement.addEventListener('pointercancel', onUp)
    domElement.addEventListener('lostpointercapture', onUp)
    window.addEventListener('blur', reset)
    document.addEventListener('visibilitychange', reset)
    const unsubscribe = useGameStore.subscribe((s, previous) => {
      if (s.settingsOpen !== previous.settingsOpen || s.worldLoading !== previous.worldLoading) reset()
    })
    return () => {
      reset()
      domElement.removeEventListener('pointerdown', onDown)
      domElement.removeEventListener('pointermove', onMove)
      domElement.removeEventListener('pointerup', onUp)
      domElement.removeEventListener('pointercancel', onUp)
      domElement.removeEventListener('lostpointercapture', onUp)
      window.removeEventListener('blur', reset)
      document.removeEventListener('visibilitychange', reset)
      unsubscribe()
    }
  }, [domElement])

  useFrame((_, delta) => {
    const body = bodyRef.current?.body
    const state = useGameStore.getState()
    if (!body || state.settingsOpen || (document.hidden && !state.physicsForced)) return
    if (!scratchRef.current) scratchRef.current = {
      pivot: new Vector3(), smooth: new Vector3(), dir: new Vector3(), offset: new Vector3(),
      shape: new rapier.Ball(0.2), initialised: false, recovery: -1, distance: 0,
    }
    const s = scratchRef.current
    const p = body.translation()
    s.pivot.set(p.x, p.y + PIVOT_ABOVE_BODY, p.z)
    const snap = !s.initialised || s.recovery !== state.recoveryCount || s.smooth.distanceToSquared(s.pivot) > 64
    if (snap) s.smooth.copy(s.pivot)
    else if (!state.worldLoading) s.smooth.lerp(s.pivot, 1 - Math.pow(1 - CAMERA.damping, Math.min(delta, 0.1) * 60))
    s.initialised = true
    s.recovery = state.recoveryCount
    s.shape.radius = cameraLensRadius(camera.near, camera.fov, camera.aspect)

    // A lagging pivot must not drift through a wall on a sharp turn.
    s.dir.subVectors(s.smooth, s.pivot)
    const lag = s.dir.length()
    if (lag > 0.001) {
      s.dir.divideScalar(lag)
      const safeLag = cameraClearance(world, rapier, s.shape, s.pivot, s.dir, lag, body)
      if (safeLag < lag) s.smooth.copy(s.pivot).addScaledVector(s.dir, safeLag)
    }
    s.offset.set(Math.sin(yaw.current) * CAMERA.distance, CAMERA.heightAbovePivot,
      Math.cos(yaw.current) * CAMERA.distance)
    const fullLength = s.offset.length()
    s.dir.copy(s.offset).divideScalar(fullLength)
    const allowed = cameraClearance(world, rapier, s.shape, s.smooth, s.dir, fullLength, body)
    s.distance = recoverCameraDistance(s.distance, allowed, delta, snap)
    camera.position.copy(s.smooth).addScaledVector(s.dir, s.distance)
    camera.lookAt(s.smooth)
    setCameraDebug(camera.position.y, s.distance * CAMERA.distance / fullLength, yaw.current)
  })
  return null
}
