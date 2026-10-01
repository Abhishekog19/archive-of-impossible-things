import { useEffect, useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { Vector3 } from 'three'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { CHARACTER } from '../config/look'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import { useGameStore } from '../store'
import { createExplorerAnimator } from './explorerAnimator'
import { avatarOpacity, dampFactor } from './cameraMotion'

/** Temporary gameplay explorer; PD08 art remains parked and unapproved. */
export default function Explorer({ controllerRef }) {
  const asset = useGLTF('/models/explorer.glb')
  const rig = useMemo(() => {
    const scene = clone(asset.scene)
    scene.name = 'PlayerPresentation'
    const materials = new Map()
    scene.traverse(node => {
      node.layers.mask = WORLD_AND_POOL_LAYERS
      if (node.isSkinnedMesh) node.frustumCulled = false
      if (node.isMesh) {
        const ownMaterial = source => {
          if (!materials.has(source)) {
            const material = source.clone()
            // Dithered coverage avoids transparent mesh sorting and extra passes.
            material.alphaHash = true
            materials.set(source, material)
          }
          return materials.get(source)
        }
        node.material = Array.isArray(node.material) ? node.material.map(ownMaterial) : ownMaterial(node.material)
      }
    })
    return { scene, materials: [...materials.values()] }
  }, [asset])
  const animator = useRef(null)
  const recovery = useRef(-1)
  const visibility = useRef(1)
  const cameraLocal = useRef(new Vector3())
  const preview = import.meta.env.DEV ? new URLSearchParams(window.location.search).get('motionPreview') : null

  useEffect(() => {
    const instance = createExplorerAnimator(rig.scene, asset.animations, import.meta.env.DEV)
    animator.current = instance
    recovery.current = -1
    return () => {
      instance.dispose()
      animator.current = null
      rig.materials.forEach(material => material.dispose())
      rig.scene.traverse(node => { if (node.isSkinnedMesh) node.skeleton.dispose() })
    }
  }, [rig, asset.animations])

  useFrame(({ camera }, delta) => {
    const state = useGameStore.getState()
    const c = controllerRef.current
    if (!c || !animator.current || state.worldLoading || state.settingsOpen || (document.hidden && !state.physicsForced)) return
    if (recovery.current !== state.recoveryCount) {
      animator.current.reset()
      recovery.current = state.recoveryCount
    }
    animator.current.update({ grounded: c.isOnGround, speed: c.moveSpeed || 0,
      verticalSpeed: c.verticalSpeed || 0 }, delta, preview)
    rig.scene.updateWorldMatrix(true, false)
    rig.scene.worldToLocal(cameraLocal.current.copy(camera.position))
    cameraLocal.current.y -= 1.4
    const target = avatarOpacity(cameraLocal.current.length())
    visibility.current = target < visibility.current ? target
      : visibility.current + (target - visibility.current) * dampFactor(12, delta)
    for (const material of rig.materials) material.setValues({ opacity: visibility.current })
  })
  const feet = -(CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius + CHARACTER.floatHeight)
  return <primitive object={rig.scene} position={[0, feet, 0]} dispose={null} />
}
