import { useEffect, useMemo, useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { RigidBody } from '@react-three/rapier'
import * as THREE from 'three'
import { CANOPY_UNDERSIDE, PALETTE, ROAD } from '../config/look'
import NoisyRoad from './NoisyRoad'
import { useButtonStore } from 'ecctrl/input'
import { useGameStore } from '../store'
import { isUiTarget } from '../player/inputState'

/**
 * M1's grey test room. Every piece here exists to answer one exit criterion,
 * and nothing here is art — it all gets deleted at M3.
 *
 * Laid out along −Z because that is where the camera looks on spawn, so the
 * 30 m straight is the first thing you see and the walk gate starts immediately
 * rather than after a hunt for the test course.
 *
 * The palette is the real §3 palette rather than placeholder greys. That costs
 * nothing and buys an early read on look-target.md §3's open item 5: road
 * (#8f8877, lum 136) and foliage (#7d9a54, lum 143) are only 7 luminance apart,
 * the tightest gap in the table, on two large adjacent fills. There is no
 * foliage yet, so this is not the real test — but the road-against-ground edge
 * is here, and if *that* pair fails to separate the problem is worse than
 * documented.
 */

/** A slab that is either a floor or a wall. Boxes are exact — no collider
 *  surprises — which is what a blockout wants. */
function Slab({ position, size, color = PALETTE.stone, rotation }) {
  return (
    <RigidBody type="fixed" colliders="cuboid" position={position} rotation={rotation}>
      <mesh>
        <boxGeometry args={size} />
        <meshStandardMaterial color={color} />
      </mesh>
    </RigidBody>
  )
}

/**
 * A ramp at a given grade, positioned so its foot meets the plaza at y = 0.
 * Grade rather than degrees because §6 specifies the road in percent, and
 * converting in one place is better than eyeballing an angle per ramp.
 */
function Ramp({ grade, run, x, z, color }) {
  const rise = run * grade
  const angle = Math.atan(grade)
  const length = Math.hypot(run, rise)
  return (
    <Slab
      position={[x, rise / 2, z - run / 2]}
      rotation={[angle, 0, 0]}
      size={[4.5, 0.4, length]}
      color={color}
    />
  )
}

/** Eight steps. Stair traversal is the classic ecctrl float-height question:
 *  too low and the capsule catches, too high and it hovers up kerbs. */
function Stairs({ x, z, steps = 8, rise = 0.18, tread = 0.3 }) {
  return Array.from({ length: steps }, (_, i) => (
    <Slab
      key={i}
      position={[x, rise * (i + 1) - rise / 2, z - tread * i]}
      size={[3, rise, tread]}
      color={i % 2 ? PALETTE.stone : PALETTE.stoneSunlit}
    />
  ))
}

/**
 * The interactable smoke test. Design doc Law 8 says teach by perturbation and
 * never with words, so there is no prompt and no label: walking close lights the
 * post, and pressing E moves the slab. "The thing reacted" is the whole lesson.
 * The real interaction framework arrives at M6.
 *
 * The proximity check is a per-frame distance test that only calls setState when
 * it *crosses* the threshold. Reading the player position through React state
 * instead would re-render this subtree 60 times a second to change nothing.
 */
function Post({ position, playerRef, onToggle, active }) {
  const [near, setNear] = useState(false)
  const nearRef = useRef(false)
  const origin = useMemo(() => new THREE.Vector3(...position), [position])

  useFrame(() => {
    const p = playerRef?.current?.currPos
    if (!p) return
    const isNear = origin.distanceTo(p) < 2.4
    if (isNear !== nearRef.current) {
      nearRef.current = isNear
      setNear(isNear)
    }
  })

  useEffect(() => {
    const onKey = (e) => {
      if (e.code === 'KeyE' && !e.repeat && !isUiTarget(e.target) && nearRef.current && !useGameStore.getState().settingsOpen) onToggle()
    }
    window.addEventListener('keydown', onKey)
    const unsubscribe = useButtonStore.subscribe(
      (s) => !!s.buttons.interact,
      (pressed, previous) => {
        if (pressed && !previous && nearRef.current && !useGameStore.getState().settingsOpen) onToggle()
      },
    )
    return () => { window.removeEventListener('keydown', onKey); unsubscribe() }
  }, [onToggle])

  return (
    <RigidBody type="fixed" colliders="cuboid" position={position}>
      {/* Tapping also works, so the smoke test covers the touch path too. */}
      <mesh position={[0, 0.6, 0]} onClick={() => {
        if (nearRef.current && !useGameStore.getState().settingsOpen) onToggle()
      }}>
        <boxGeometry args={[0.4, 1.2, 0.4]} />
        <meshStandardMaterial
          color={near || active ? PALETTE.daylight : PALETTE.stone}
        />
      </mesh>
    </RigidBody>
  )
}

export default function GreyRoom({ playerRef }) {
  const [raised, setRaised] = useState(false)

  return (
    <>
      {/* Plaza — the spawn area and the flat-ground control case. */}
      <Slab position={[0, -0.2, 4]} size={[24, 0.4, 20]} color={PALETTE.ground} />

      {/* The 30 m straight, with §6's ±0.25 m walkable noise. */}
      <NoisyRoad />

      {/* Slopes. 8% is §6's stated maximum and must feel unremarkable; 25% is
          deliberately out of spec, present so the failure edge is visible rather
          than theoretical. */}
      <Ramp grade={ROAD.maxGrade} run={12.5} x={8} z={10} color={PALETTE.road} />
      <Ramp grade={0.25} run={8} x={14} z={10} color={PALETTE.water} />

      {/* Stairs, climbing away from the plaza. */}
      <Stairs x={-8} z={10} />

      {/* Camera-clearance witnesses. The tall gate sits at §2's derived canopy
          underside (6.5 m) and the camera must never touch it. The low lintel is
          3.0 m — below the 2.2 m camera plus its clearance — and exists so the
          pull-in can be seen working rather than assumed. */}
      <Slab
        position={[0, CANOPY_UNDERSIDE + 0.25, -4]}
        size={[10, 0.5, 0.6]}
        color={PALETTE.canopy}
      />
      <Slab position={[-6, 3.0, 2]} size={[5, 0.4, 0.6]} color={PALETTE.canopy} />
      {[-1, 1].map((s) => (
        <Slab
          key={s}
          position={[-6 + s * 2.2, 1.5, 2]}
          size={[0.4, 3, 0.6]}
          color={PALETTE.stone}
        />
      ))}

      {/* A dead-end slot, 2.5 m across, behind the spawn. Walk in, turn around,
          and the camera has nowhere to go — the only way to prove "pull in,
          never clip" on a *lateral* surface. The overhangs above test it
          vertically, and a vertical pull-in can pass while a sideways one clips.

          Placed at +Z rather than out along the course because everything else
          is already spoken for, and slot walls that intersect another collider
          would corrupt the one thing this room exists to measure. The two
          rejected spots, so they don't get retried: x ≈ 8 puts the walls
          through the 8% ramp (which spans z −2.5…10 and is 4.5 m wide), and
          x ≈ −9 puts them through the stairs (x −9.5…−6.5). Here, z starts at
          10.25 — a quarter-metre clear of the ramp's far end — and the whole
          slot sits inside the plaza, so it has a floor. */}
      <Slab position={[3.5, 1.5, 12]} size={[0.5, 3, 3.5]} color={PALETTE.stone} />
      <Slab position={[6.5, 1.5, 12]} size={[0.5, 3, 3.5]} color={PALETTE.stone} />
      <Slab position={[5, 1.5, 13.9]} size={[3.5, 3, 0.5]} color={PALETTE.stone} />

      {/* Interactable + the thing it moves. */}
      <Post
        position={[-3, 0, 3]}
        playerRef={playerRef}
        onToggle={() => setRaised((v) => !v)}
        active={raised}
      />
      <Slab
        position={[-3, raised ? 1.4 : 0.15, -1]}
        size={[3, 0.3, 3]}
        color={raised ? PALETTE.stoneSunlit : PALETTE.stone}
      />
    </>
  )
}
