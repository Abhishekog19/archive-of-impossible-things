import { useMemo } from 'react'
import { RigidBody } from '@react-three/rapier'
import * as THREE from 'three'
import { PALETTE, ROAD } from '../config/look'
import { roadHeight } from './roadHeight'

/**
 * The ±0.25 m noisy road — the one piece of M1 that can actually fail.
 *
 * look-target.md §6 caps walkable-surface noise at ±0.25 m low frequency, and
 * says the reason is a movement limit rather than a visual one: past that, the
 * character controller fights the ground. M1's exit criterion turns that into a
 * test, so the road has to be a real displaced surface with a real trimesh
 * collider. A flat box with a bumpy texture would pass the eye and prove
 * nothing.
 *
 * The height field itself lives in ./roadHeight.js.
 */

export default function NoisyRoad({
  length = ROAD.maxStraight,
  startZ = -6,
  segments = 60,
}) {
  const geometry = useMemo(() => {
    const totalWidth = ROAD.width + ROAD.verge * 2
    const geo = new THREE.PlaneGeometry(totalWidth, length, 12, segments)
    // PlaneGeometry is born facing +Z; rotate it flat before displacing so the
    // vertex positions we read are already world-ish (x across, y up, z along).
    geo.rotateX(-Math.PI / 2)

    const pos = geo.attributes.position
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i)
      const z = pos.getZ(i)
      // Verges are allowed to be much rougher than the road (§6: ±0.8 m), and
      // the transition has to be gradual or the seam becomes a step the player
      // trips on. Blend the amplitude across the verge instead of switching it.
      const fromCentre = Math.abs(x)
      const t = THREE.MathUtils.smoothstep(fromCentre, ROAD.width / 2, totalWidth / 2)
      const amplitude = THREE.MathUtils.lerp(ROAD.noise.road, ROAD.noise.verge, t)
      pos.setY(i, roadHeight(x, z + startZ - length / 2, amplitude))
    }
    geo.computeVertexNormals()

    return geo
  }, [length, startZ, segments])

  const centreZ = startZ - length / 2

  return (
    <group position={[0, 0, centreZ]}>
      {/* Only the road surface is a collider. The markers below are siblings
          rather than children on purpose: children of a `colliders="trimesh"`
          body each get their own trimesh, so a dozen 4 cm paint stripes would
          become a dozen colliders the player can catch a foot on. */}
      <RigidBody type="fixed" colliders="trimesh">
        <mesh geometry={geometry}>
          <meshStandardMaterial color={PALETTE.road} side={THREE.DoubleSide} />
        </mesh>
      </RigidBody>

      {/* Centreline markers, so "did I drift?" is answerable while walking.
          Not art — these get deleted at M5 when the real road exists. */}
      {Array.from({ length: Math.floor(length / 5) }, (_, i) => {
        const z = -length / 2 + 2.5 + i * 5
        return (
          <mesh key={i} position={[0, roadHeight(0, z + centreZ) + 0.03, z]}>
            <boxGeometry args={[0.12, 0.04, 1.2]} />
            <meshStandardMaterial color={PALETTE.stoneSunlit} />
          </mesh>
        )
      })}

      {/* Width witnesses at the road/verge boundary — 4.5 m apart, so §6's
          "wide enough not to feel like a corridor" claim is checkable by eye. */}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[(s * ROAD.width) / 2, 0.15, 0]}>
          <boxGeometry args={[0.06, 0.04, length]} />
          <meshStandardMaterial color={PALETTE.ground} />
        </mesh>
      ))}
    </group>
  )
}
