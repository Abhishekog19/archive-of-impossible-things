import { useEffect, useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { AnimationMixer, LoopOnce, LoopRepeat } from 'three'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { CHARACTER } from '../config/look'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import { useGameStore } from '../store'
import { EXPLORER_CLIPS, advanceAnimation, animationRate, initialAnimation } from './explorerAnimation'

/** The skinned art follows ecctrl's body rotation (+Z forward); no root motion. */
export default function Explorer({ controllerRef }) {
  const asset = useGLTF('/models/explorer.glb')
  const rig = useMemo(() => {
    const scene = clone(asset.scene)
    scene.traverse(node => {
      node.layers.mask = WORLD_AND_POOL_LAYERS
      // The animated figure can extend beyond its bind-pose bounds near a wall.
      if (node.isSkinnedMesh) node.frustumCulled = false
    })
    const mixer = new AnimationMixer(scene)
    const actions = Object.fromEntries(asset.animations.map(clip => {
      const action = mixer.clipAction(clip)
      const once = clip.name === 'Jump' || clip.name === 'Land'
      action.setLoop(once ? LoopOnce : LoopRepeat, once ? 1 : Infinity)
      action.clampWhenFinished = once
      return [clip.name, action]
    }))
    return { scene, mixer, actions }
  }, [asset])
  const motion = useRef(initialAnimation())
  const current = useRef(null)
  // Local art review only; production always follows the live controller.
  const preview = import.meta.env.DEV ? new URLSearchParams(window.location.search).get('motionPreview') : null

  useEffect(() => {
    motion.current = initialAnimation()
    current.current = null
    return () => {
      rig.mixer.stopAllAction()
      rig.mixer.uncacheRoot(rig.scene)
      // Skeleton clones own bone textures; geometry/materials belong to useGLTF.
      rig.scene.traverse(node => { if (node.isSkinnedMesh) node.skeleton.dispose() })
    }
  }, [rig])

  useFrame((_, delta) => {
    const state = useGameStore.getState()
    const controller = controllerRef.current
    if (!controller || state.worldLoading || state.settingsOpen || document.hidden) return
    const speed = controller.moveSpeed || 0
    motion.current = advanceAnimation(motion.current, {
      grounded: controller.isOnGround, speed, verticalSpeed: controller.verticalSpeed || 0,
    }, delta)
    const name = EXPLORER_CLIPS.includes(preview) ? preview : motion.current.name
    const next = rig.actions[name]
    if (!next) return
    if (current.current !== next) {
      current.current?.fadeOut(.14)
      next.reset().setEffectiveWeight(1).fadeIn(.14).play()
      current.current = next
    }
    next.setEffectiveTimeScale(preview ? 1 : animationRate(name, speed))
    rig.mixer.update(Math.min(delta, .05))
  })
  const feet = -(CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius + CHARACTER.floatHeight)
  return <primitive object={rig.scene} position={[0, feet, 0]} dispose={null} />
}
