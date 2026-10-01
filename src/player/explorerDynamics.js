import { Euler, Quaternion, Vector3 } from 'three'

const clamp = (v, a, b) => Math.max(a, Math.min(b, v))
const up = new Vector3(0, 1, 0)
const ease = t => t * t * (3 - 2 * t)

/** Analytic two-bone solve; unreachable targets stay inside the leg's reach. */
export function solveLeg(hip, target, pole, upper, lower) {
  const axis = target.clone().sub(hip)
  const distance = clamp(axis.length(), Math.abs(upper - lower) + .001, upper + lower - .001)
  axis.normalize()
  if (axis.lengthSq() < .5) axis.set(0, -1, 0)
  const bend = pole.clone().addScaledVector(axis, -pole.dot(axis)).normalize()
  if (bend.lengthSq() < .5) bend.crossVectors(axis, new Vector3(1, 0, 0)).normalize()
  const along = (upper * upper + distance * distance - lower * lower) / (2 * distance)
  const knee = hip.clone().addScaledVector(axis, along)
    .addScaledVector(bend, Math.sqrt(Math.max(0, upper * upper - along * along)))
  return { knee, ankle: hip.clone().addScaledVector(axis, distance) }
}

/** Damped angular spring. Bounded substeps make stops and long frames stable. */
export function stepSpring(state, target, dt, stiffness = 65, damping = 12, limit = .5) {
  let remaining = clamp(dt, 0, .1)
  while (remaining > 1e-8) {
    const h = Math.min(remaining, 1 / 120)
    state.velocity += (stiffness * (target - state.angle) - damping * state.velocity) * h
    state.angle += state.velocity * h
    if (Math.abs(state.angle) > limit) {
      state.angle = clamp(state.angle, -limit, limit)
      if (state.velocity * state.angle > 0) state.velocity = 0
    }
    remaining -= h
  }
  return state.angle
}

function aim(bone, child, target) {
  const origin = bone.getWorldPosition(new Vector3())
  const from = child.getWorldPosition(new Vector3()).sub(origin).normalize()
  const to = target.clone().sub(origin).normalize()
  const world = bone.getWorldQuaternion(new Quaternion())
  world.premultiply(new Quaternion().setFromUnitVectors(from, to))
  bone.quaternion.copy(bone.parent.getWorldQuaternion(new Quaternion()).invert().multiply(world))
  bone.updateWorldMatrix(false, true)
}

const JOINTS = [
  // Length, stiffness, angular limit, outward X bias; meshes remain a single skin.
  ['Cape', .236, 48, .55, .10], ['CapeTip', .36, 36, .65, .06],
  ['Scarf', .262, 65, .40, -.06], ['Hem_L', .234, 80, .40, -.08],
  ['Hem_R', .234, 80, .40, -.08], ['Hair', .099, 110, .18, 0],
  ['Rope', .281, 55, .45, -.07], ['Satchel', .25, 100, .22, 0],
]

/** Post-animation presentation. Never pushes or teleports the physics capsule.
 * groundAt(point) returns {height, normal}, or null for a ledge/invalid surface.
 * Secondary motion is constrained spring-bone animation, not a cloth solver.
 */
export function createExplorerDynamics(scene, groundAt, diagnostics = false) {
  scene.updateWorldMatrix(true, true)
  const rootRotation = scene.getWorldQuaternion(new Quaternion())
  const hips = scene.getObjectByName('Hips'), spine = scene.getObjectByName('Spine')
  const legs = ['L', 'R'].map((label, index) => {
    const thigh = scene.getObjectByName('Thigh_' + label)
    const shin = scene.getObjectByName('Shin_' + label)
    const foot = scene.getObjectByName('Foot_' + label)
    const hip = thigh.getWorldPosition(new Vector3()), knee = shin.getWorldPosition(new Vector3())
    const ankle = foot.getWorldPosition(new Vector3())
    return { thigh, shin, foot, side: index === 0 ? -1 : 1,
      upper: hip.distanceTo(knee), lower: knee.distanceTo(ankle),
      restRotation: rootRotation.clone().invert().multiply(foot.getWorldQuaternion(new Quaternion())),
      lock: null, swingFrom: null, stance: false, error: 0, contact: false }
  })
  const joints = JOINTS.map(([name, length, stiffness, limit, bias]) => {
    const bone = scene.getObjectByName(name)
    if (!bone) throw new Error(`Explorer secondary rig is missing ${name}`)
    return { name, bone, length, stiffness, limit, bias, rest: bone.quaternion.clone(),
      x: { angle: 0, velocity: 0 }, z: { angle: 0, velocity: 0 } }
  })
  let phase = 0, blend = 0, lastPosition = null, lastVelocity = new Vector3()
  let previousYaw = null, turn = 0, elapsed = 0, contacts = 0
  let maxDeflection = 0, groundBlend = 0
  const reset = () => {
    phase = 0; blend = 0; groundBlend = 0; lastPosition = null; previousYaw = null
    lastVelocity.set(0, 0, 0); turn = 0; elapsed = 0; contacts = 0
    for (const leg of legs) { leg.lock = null; leg.swingFrom = null; leg.stance = false; leg.error = 0; leg.contact = false }
    for (const j of joints) {
      j.x.angle = j.bias; j.x.velocity = j.z.angle = j.z.velocity = 0
      j.bone.quaternion.copy(j.rest)
    }
  }
  const system = {
    reset,
    update({ grounded, velocity, gait }, delta) {
      const dt = clamp(delta, 0, .1)
      if (dt === 0) return
      scene.updateWorldMatrix(true, true)
      const position = scene.getWorldPosition(new Vector3())
      if (lastPosition && position.distanceTo(lastPosition) > 1.5) reset()
      const rotation = scene.getWorldQuaternion(new Quaternion())
      const forward = new Vector3(0, 0, 1).applyQuaternion(rotation)
      forward.y = 0; forward.normalize()
      const yaw = Math.atan2(forward.x, forward.z)
      const yawDelta = previousYaw === null ? 0 : Math.atan2(Math.sin(yaw - previousYaw), Math.cos(yaw - previousYaw))
      turn += (clamp(yawDelta / dt, -8, 8) - turn) * (1 - Math.exp(-10 * dt))
      previousYaw = yaw
      const v = new Vector3(velocity.x, velocity.y, velocity.z)
      const acceleration = lastPosition ? v.clone().sub(lastVelocity).divideScalar(dt).clampLength(0, 22) : new Vector3()
      lastPosition = position.clone(); lastVelocity.copy(v); elapsed += dt
      const speed = Math.hypot(v.x, v.z), running = speed > 3.8
      const direction = speed > .15 ? new Vector3(v.x, 0, v.z).normalize() : forward.clone()
      blend += ((speed > .12 ? 1 : 0) - blend) * (1 - Math.exp(-12 * dt))
      groundBlend += ((grounded ? 1 : 0) - groundBlend) * (1 - Math.exp(-22 * dt))
      const cycle = running ? 1.8 : 1.4, duty = running ? .4 : .5
      phase = (phase + speed / cycle * dt) % 1
      if (gait && (gait.name === 'Walk' || gait.name === 'Run')) phase = gait.phase
      // Flex the knees enough to reach fore/aft contacts without straight-leg snapping.
      const hipWorld = hips.getWorldPosition(new Vector3())
      const centreFloor = grounded ? groundAt(position) : null
      const floorOffset = centreFloor ? clamp(centreFloor.height - position.y, -.2, .2) : 0
      hipWorld.y += (floorOffset - .04 - blend * (running ? .105 : .075)) * groundBlend
      hips.position.copy(hips.parent.worldToLocal(hipWorld))
      spine.quaternion.multiply(new Quaternion().setFromEuler(new Euler(0, 0, clamp(-turn * speed * .008, -.12, .12))))
      scene.updateWorldMatrix(true, true)
      contacts = 0
      for (const leg of legs) {
        const p = (phase + (leg.side > 0 ? .5 : 0)) % 1
        const stance = speed < .12 || p < duty
        const neutral = scene.localToWorld(new Vector3(leg.side * .105, 0, 0))
        const ahead = direction.clone().multiplyScalar(cycle * duty * .5 * blend)
        const landing = neutral.clone().add(ahead)
        const surface = groundAt(landing)
        leg.contact = false; leg.error = 0
        if (!grounded || !surface || Math.abs(surface.height - neutral.y) > .42) {
          leg.lock = null; leg.swingFrom = null; leg.stance = false
          continue
        }
        if (stance && (!leg.stance || !leg.lock)) leg.lock = landing.clone()
        if (!stance && leg.stance) leg.swingFrom = leg.lock?.clone() ?? neutral.clone()
        if (speed < .12 && leg.lock) leg.lock.lerp(neutral, 1 - Math.exp(-8 * dt))
        // Release a planted foot on a sharp turn or extreme reach, never twist a knee backwards.
        if (leg.lock && (Math.abs(yawDelta) > .35 || Math.hypot(leg.lock.x - neutral.x, leg.lock.z - neutral.z) > .46)) {
          leg.lock.copy(landing)
        }
        let sole = stance ? leg.lock.clone() : (leg.swingFrom ?? neutral).clone()
          .lerp(landing, ease(clamp((p - duty) / (1 - duty), 0, 1)))
        const floor = groundAt(sole)
        if (!floor) { leg.lock = null; leg.stance = false; continue }
        const lift = stance ? 0 : Math.sin(Math.PI * clamp((p - duty) / (1 - duty), 0, 1)) * (running ? .20 : .12) * blend
        sole.y = floor.height + lift
        const normal = floor.normal.clone().normalize()
        const ankle = sole.clone().addScaledVector(normal, .155)
        const animatedAnkle = leg.foot.getWorldPosition(new Vector3())
        ankle.lerpVectors(animatedAnkle, ankle, groundBlend)
        const hip = leg.thigh.getWorldPosition(new Vector3())
        const solved = solveLeg(hip, ankle, forward, leg.upper, leg.lower)
        aim(leg.thigh, leg.shin, solved.knee)
        aim(leg.shin, leg.foot, solved.ankle)
        const desired = new Quaternion().setFromUnitVectors(up, normal).multiply(rotation).multiply(leg.restRotation)
        desired.premultiply(leg.foot.parent.getWorldQuaternion(new Quaternion()).invert())
        leg.foot.quaternion.slerp(desired, groundBlend)
        leg.foot.updateWorldMatrix(false, true)
        leg.error = leg.foot.getWorldPosition(new Vector3()).distanceTo(ankle)
        leg.contact = stance; leg.stance = stance
        if (stance) contacts++
      }
      const localAcceleration = acceleration.applyQuaternion(rotation.clone().invert())
      maxDeflection = 0
      for (const j of joints) {
        const wind = Math.sin(elapsed * 1.7 + j.length * 8) * .012
        const targetX = j.bias + clamp(localAcceleration.z * .013 + speed * .015 + wind, -.24, .32)
        const targetZ = clamp(-localAcceleration.x * .013 - turn * .035, -.25, .25)
        const x = stepSpring(j.x, targetX, dt, j.stiffness, 2 * Math.sqrt(j.stiffness) * .72, j.limit)
        const z = stepSpring(j.z, targetZ, dt, j.stiffness, 2 * Math.sqrt(j.stiffness) * .72, j.limit)
        j.bone.quaternion.copy(j.rest).multiply(new Quaternion().setFromEuler(new Euler(x, 0, z)))
        j.bone.updateWorldMatrix(false, true)
        // Coarse garment/body separation in character space. Front panels stay in
        // front of the torso/thighs; cape stays behind; satchel stays outside the hip.
        const tip = j.bone.localToWorld(new Vector3(0, j.length, 0))
        const local = scene.worldToLocal(tip.clone()), constrained = local.clone()
        if (j.name.startsWith('Cape')) constrained.z = Math.min(local.z, -.22)
        else if (j.name === 'Satchel') constrained.x = Math.max(local.x, .22)
        else if (j.name !== 'Hair') constrained.z = Math.max(local.z, .17)
        if (constrained.distanceToSquared(local) > 1e-8) {
          const origin = j.bone.getWorldPosition(new Vector3())
          const correction = new Quaternion().setFromUnitVectors(tip.sub(origin).normalize(),
            scene.localToWorld(constrained).sub(origin).normalize())
          const worldQ = j.bone.getWorldQuaternion(new Quaternion()).premultiply(correction)
          j.bone.quaternion.copy(j.bone.parent.getWorldQuaternion(new Quaternion()).invert().multiply(worldQ))
          j.bone.updateWorldMatrix(false, true)
        }
        maxDeflection = Math.max(maxDeflection, Math.abs(x), Math.abs(z))
      }
    },
    snapshot: () => ({ contacts, footError: Math.max(...legs.map(l => l.error)),
      joints: joints.length, deflection: maxDeflection, turn,
      springEnergy: joints.reduce((n, j) => n + j.x.velocity ** 2 + j.z.velocity ** 2, 0) }),
    dispose() { if (diagnostics) delete scene.userData.readDynamics },
  }
  if (diagnostics) scene.userData.readDynamics = system.snapshot
  return system
}
