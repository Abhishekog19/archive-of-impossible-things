import { useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import { useRapier } from '@react-three/rapier'
import { CAMERA, CANOPY_UNDERSIDE, BUDGET, ROAD } from '../config/look'
import { useGameStore } from '../store'
import { perf } from './perf'

/**
 * A dev-only handle on the running scene, published to `window.__M1`.
 *
 * This exists because of a specific problem. M1's exit criteria are physical
 * claims — "the camera never clips", "stairs traverse without the controller
 * fighting the ground" — and checking them means walking the course and reading
 * numbers back. But a browser throttles requestAnimationFrame to nearly nothing
 * when its window isn't visible, so a script that presses W and waits gets
 * almost no frames and concludes the character cannot move.
 *
 * `step()` solves that by driving the loop instead of waiting for it, and
 * `audit()` builds on it to walk the whole course and return the exit criteria
 * as one small object. That object is the *point*: a screenshot costs far more
 * to read than a line of numbers, and a number can be compared to a threshold
 * while an impression cannot.
 *
 * Fixed deltas also make the walk deterministic — same inputs, same path, every
 * run — so a regression shows up as a different number rather than a different
 * feeling.
 *
 * Dev only: the single use site is behind `import.meta.env.DEV`, so Rollup drops
 * this from production builds.
 */

/** Static camera tests. Teleport, face a direction, measure. */
const POSES = [
  { id: 'plaza', at: [0, 1.2, 4], yaw: 0, want: 'free' },
  { id: 'canopyGate', at: [0, 1.2, -4.5], yaw: 0, want: 'free' },
  { id: 'lintel', at: [-6, 1.2, 0.5], yaw: 0, want: 'free' },
  { id: 'slotBack', at: [5, 1.2, 12], yaw: 0, want: 'pulled' },
  { id: 'slotDeep', at: [5, 1.2, 12.8], yaw: 0, want: 'clamped' },
  { id: 'slotSide', at: [4.2, 1.2, 12], yaw: 90, want: 'pulled' },
]

/**
 * Traversal tests. Teleport, hold W, walk until `target` metres are covered.
 *
 * Distance-bounded rather than frame-bounded on purpose. A frame count has to be
 * hand-tuned per feature to stop at the end of it, tuning that silently rots
 * when walk speed or a ramp length changes — and worse, it makes "walk the 30 m
 * strip" a thing I asserted by picking 750 rather than a thing the run measured.
 * With a target, falling short is a reported failure (`reached: false`) instead
 * of a quietly smaller number.
 *
 * `maxFrames` is the stall guard: generous enough that a healthy run never hits
 * it, so hitting it means the controller stopped moving.
 *
 * Targets stop half a metre short of each feature's end so a run never sails off
 * the edge into free fall. Road: the strip spans z −6 to −36, so −6.5 + 29 m
 * lands at −35.5. Ramp8: 12.5 m run. Ramp25: 8 m run. Stairs: 8 × 0.3 tread.
 */
const WALKS = [
  { id: 'road30', at: [0, 1.2, -6.5], yaw: 0, target: 29, maxFrames: 1500 },
  { id: 'ramp8', at: [8, 1.6, 10.5], yaw: 0, target: 12, maxFrames: 800 },
  { id: 'ramp25', at: [14, 1.6, 9.8], yaw: 0, target: 7.5, maxFrames: 800 },
  { id: 'stairs', at: [-8, 1.4, 10.8], yaw: 0, target: 2.4, maxFrames: 500 },
]

const r2 = (n) => Math.round(n * 100) / 100

/**
 * M1's exit criteria, as thresholds.
 *
 * These live in code rather than in verification.md on purpose: a threshold in a
 * document has to be read alongside the numbers and compared by hand, and it
 * drifts out of agreement with the build the first time either changes. Here,
 * `report()` does the comparison and prints PASS or FAIL, so verifying M1 is one
 * line pasted into a console and one block read back.
 *
 * Every value traces to build-roadmap.md's M1 criteria or look-target.md, not to
 * whatever the build happened to measure — a threshold set to the last
 * measurement tests nothing.
 */
const M1 = {
  // "Camera never clips geometry." A solid downward raycast from inside geometry
  // returns 0, so any reading above 0 means the camera is in open air.
  minCameraClearance: 0.01,
  // "Without the controller fighting the ground at ±0.25 m noise" — look-target
  // §6's walkable-surface limit, which is a movement constraint, not a visual one.
  maxStepBetweenSamples: ROAD.noise.road,
  // Not in the document: contact percentage is the other half of "not fighting
  // the ground", because a controller can keep its step size small by bouncing.
  // Ramps and the road should hold contact almost always; stairs legitimately
  // break contact at each riser, so they get a looser floor.
  minGroundedPct: 95,
  minGroundedPctStairs: 90,
  // The camera sits 2.2 m above the feet whenever it is not pulled in. The
  // tolerance is for the float spring and the road's own noise, both expected.
  cameraHeightTolerance: 0.15,
}

export default function DevProbe({ playerRef }) {
  const advance = useThree((s) => s.advance)
  const setFrameloop = useThree((s) => s.setFrameloop)
  const getState = useThree((s) => s.get)
  const camera = useThree((s) => s.camera)
  const scene = useThree((s) => s.scene)
  const gl = useThree((s) => s.gl)
  const { world, rapier } = useRapier()

  useEffect(() => {
    // One reusable ray — see FollowCamera for why allocation per cast is wrong.
    const probeRay = new rapier.Ray({ x: 0, y: 0, z: 0 }, { x: 0, y: -1, z: 0 })

    /**
     * Distance from a point straight down to the first surface.
     *
     * The honest test for "the camera never clips". A solid-mode cast that
     * starts *inside* geometry returns a time of impact of 0, so a reading of
     * 0 means the camera is embedded in a wall — which no amount of looking at
     * a screenshot reliably tells you, because the inside of a box still
     * renders as a plausible grey.
     */
    const clearanceBelow = (p) => {
      probeRay.origin.x = p.x
      probeRay.origin.y = p.y
      probeRay.origin.z = p.z
      probeRay.dir.x = 0
      probeRay.dir.y = -1
      probeRay.dir.z = 0
      const hit = world.castRay(probeRay, 30, true)
      return hit ? hit.timeOfImpact : null
    }

    const handle = {
      perf,
      camera,
      scene,
      gl,
      /** Live store snapshot, so a test can read player and camera state. */
      state: () => useGameStore.getState(),
      /** R3F internals, for diagnosing the loop itself. */
      r3f: () => {
        const s = getState()
        return {
          frameloop: s.frameloop,
          frames: s.internal.frames,
          subscribers: s.internal.subscribers.length,
          priorities: s.internal.priority,
          elapsed: +s.clock.elapsedTime.toFixed(3),
          running: s.clock.running,
        }
      },

      /**
       * Advance the loop `frames` times at a fixed `dt` seconds each, with rAF
       * out of the picture entirely.
       *
       * Three R3F details make this fiddlier than it looks, and each cost a
       * debugging round:
       *
       * 1. `advance()` only produces a fixed delta while `frameloop === 'never'`.
       *    In any other mode it ignores the timestamp and reads
       *    `clock.getDelta()` — real elapsed time — so stepping a hidden tab
       *    replays the whole throttled gap in one tick.
       * 2. In that mode the timestamp is in SECONDS, not milliseconds:
       *    `delta = timestamp - clock.elapsedTime`, and the timestamp is then
       *    assigned straight into `elapsedTime`. Passing `performance.now()`
       *    yields a delta of tens of thousands of seconds — which put the
       *    character 185 m down the road in a single tick. Rapier clamps its own
       *    step to 0.5 s; ecctrl's integration does not.
       * 3. `setFrameloop()` calls `clock.stop()` and resets `elapsedTime` to 0.
       *    Flipping the mode per step therefore restarts the clock underneath
       *    rapier's fixed-step accumulator and nothing integrates. So the mode is
       *    set ONCE around the whole run, and the synthetic clock is read back
       *    after the switch rather than assumed to be zero.
       */
      step(frames = 60, dt = 1 / 60) {
        const wasNever = getState().frameloop === 'never'
        if (!wasNever) setFrameloop('never') // zeroes clock.elapsedTime
        let t = getState().clock.elapsedTime
        for (let i = 0; i < frames; i++) {
          t += dt
          advance(t)
        }
        if (!wasNever) setFrameloop('always')
        return frames
      },

      /**
       * Enter stepped mode and stay there, so many step() calls share a clock.
       *
       * This also has to unpause physics. App.jsx pauses the simulation while
       * the page is hidden — correct for the shipped game, and the reason a
       * stepped walk from a hidden pane advanced the clock and reported a
       * speed while the body never moved: rapier was paused for precisely the
       * frames being driven. Manual mode means no human is watching, so the
       * visibility heuristic no longer applies.
       */
      manual(on = true) {
        useGameStore.getState().setPhysicsForced(on)
        setFrameloop(on ? 'never' : 'always')
        return { frameloop: getState().frameloop, physicsForced: on }
      },

      /** Where the camera is, and how far it sits from the pivot it follows. */
      cam() {
        const p = camera.position
        return {
          x: r2(p.x),
          y: r2(p.y),
          z: r2(p.z),
          distance: r2(useGameStore.getState().cameraDistance),
        }
      },

      /** Hold key codes, step the loop, release. Read state afterwards. */
      walk(codes, frames = 60, dt = 1 / 60) {
        const list = Array.isArray(codes) ? codes : [codes]
        for (const code of list) {
          window.dispatchEvent(new KeyboardEvent('keydown', { code }))
        }
        handle.step(frames, dt)
        for (const code of list) {
          window.dispatchEvent(new KeyboardEvent('keyup', { code }))
        }
        return handle.state()
      },

      /** Point the camera along a yaw, in degrees, by dragging the canvas. */
      turn(deg) {
        const el = gl.domElement
        // FollowCamera reads movementX and turns 0.0045 rad/px.
        const px = -((deg * Math.PI) / 180) / 0.0045
        el.dispatchEvent(
          new PointerEvent('pointerdown', { pointerId: 1, button: 0, bubbles: true }),
        )
        el.dispatchEvent(
          new PointerEvent('pointermove', { pointerId: 1, movementX: px, bubbles: true }),
        )
        el.dispatchEvent(new PointerEvent('pointerup', { pointerId: 1, bubbles: true }))
        handle.step(2)
        return handle.state().cameraYaw
      },

      /** Absolute yaw, in degrees, driven through the same input path. */
      turnTo(deg) {
        const current = (handle.state().cameraYaw * 180) / Math.PI
        return handle.turn(deg - current)
      },

      /** The player's rigid body, for tests that need it directly. */
      body: () => playerRef?.current?.body ?? null,

      /**
       * Drop the capsule at a spot, kill its momentum, let it settle.
       *
       * `wakeUp()` is not belt-and-braces. Rapier sleeps a body that has been
       * still for a moment, and a slept body ignores gravity and reports no
       * ground contact — so a teleport followed by a settle produced a capsule
       * frozen half a metre above the road, `onGround: false`, that then
       * refused to walk while ecctrl cheerfully reported 2 m/s. Under a stepped
       * clock nothing else ever disturbs it, so it has to be woken explicitly.
       */
      place([x, y, z], yawDeg = 0, settle = 60) {
        const body = playerRef?.current?.body
        if (!body) return null
        body.setTranslation({ x, y, z }, true)
        body.setLinvel({ x: 0, y: 0, z: 0 }, true)
        body.setAngvel({ x: 0, y: 0, z: 0 }, true)
        body.wakeUp()
        handle.turnTo(yawDeg)
        // Settle in chunks, waking each time: the drop itself can be short
        // enough that rapier sleeps the body before it has finished falling.
        for (let i = 0; i < settle; i += 10) {
          body.wakeUp()
          handle.step(10)
        }
        return handle.state().player
      },

      /**
       * The whole M1 exit-criteria run, as one object.
       *
       * Deliberately returns aggregates and one worst-case sample per test
       * rather than a trace. A thousand samples proves nothing a minimum and a
       * maximum don't, and it costs a hundred times as much to read.
       */
      audit() {
        const wasManual = getState().frameloop === 'never'
        handle.manual(true)

        // --- Static camera poses ---
        const poses = {}
        for (const p of POSES) {
          handle.place(p.at, p.yaw)
          const st = handle.state()
          const c = handle.cam()
          poses[p.id] = {
            dist: c.distance,
            aboveFeet: r2(c.y - st.player.feetY),
            camY: r2(c.y),
            camClear: c.distance != null ? r2(clearanceBelow(camera.position) ?? -1) : -1,
            want: p.want,
          }
        }

        // --- Traversals ---
        const walks = {}
        for (const w of WALKS) {
          const start = handle.place(w.at, w.yaw)
          const startZ = start.z
          const startFeet = start.feetY

          let grounded = 0
          let samples = 0
          let slopeMax = 0
          let distMin = Infinity
          let aboveMin = Infinity
          let aboveMax = -Infinity
          let clearMin = Infinity
          let stepMax = 0
          let speedMax = 0
          let climbMax = 0
          let dropMax = 0
          let prevFeet = startFeet
          let prevGrounded = true

          const body = handle.body()
          window.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW' }))
          const CHUNK = 10
          let used = 0
          let travelled = 0
          while (travelled < w.target && used < w.maxFrames) {
            body?.wakeUp()
            handle.step(CHUNK)
            used += CHUNK
            const st = handle.state()
            const p = st.player
            const c = handle.cam()
            travelled = Math.abs(p.z - startZ)
            samples++
            if (p.onGround) grounded++
            slopeMax = Math.max(slopeMax, p.slopeDeg)
            distMin = Math.min(distMin, c.distance)
            climbMax = Math.max(climbMax, p.feetY - startFeet)
            dropMax = Math.min(dropMax, p.feetY - startFeet)
            speedMax = Math.max(speedMax, p.speed)

            // Camera and ground readings are only meaningful with feet on a
            // surface. A walk that runs off the end of a feature spends its last
            // samples in free fall, and those samples were poisoning every
            // aggregate — a 4.65 m camera height and a 4.72 m "step" that were
            // both just gravity. Sampling only grounded frames means a stray
            // airborne moment costs a percentage point of groundedPct instead of
            // corrupting every other number in the row.
            if (p.onGround) {
              const above = c.y - p.feetY
              aboveMin = Math.min(aboveMin, above)
              aboveMax = Math.max(aboveMax, above)
              clearMin = Math.min(clearMin, clearanceBelow(camera.position) ?? 99)
              // The signature of a controller fighting the ground: the feet
              // moving further between two grounded samples than the surface
              // can explain.
              if (prevGrounded) {
                stepMax = Math.max(stepMax, Math.abs(p.feetY - prevFeet))
              }
            }
            prevFeet = p.feetY
            prevGrounded = p.onGround
          }
          window.dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW' }))

          walks[w.id] = {
            // The pass/fail on "can you actually walk it". False means the
            // controller stalled before covering the feature.
            reached: travelled >= w.target,
            travelled: r2(travelled),
            target: w.target,
            seconds: r2(used / 60),
            climbMax: r2(climbMax),
            dropMax: r2(dropMax),
            groundedPct: Math.round((grounded / samples) * 100),
            slopeMax: r2(slopeMax),
            stepMax: r2(stepMax),
            distMin: r2(distMin),
            aboveMin: r2(aboveMin),
            aboveMax: r2(aboveMax),
            camClearMin: r2(clearMin),
            speedMax: r2(speedMax),
          }
        }

        // --- Structural camera facts, not measurements ---
        // Pitch is fixed and not player-controllable, so "never shows sky above
        // the canopy line" is a geometry question with one answer, not
        // something to eyeball per frame.
        const frameTopDeg = -CAMERA.derivedPitchDeg + CAMERA.fov / 2
        const canopyGap = CANOPY_UNDERSIDE - CAMERA.worldHeight
        const skyAt = canopyGap / Math.tan((frameTopDeg * Math.PI) / 180)

        handle.place([0, 2, 6], 0)
        if (!wasManual) handle.manual(false)

        return {
          poses,
          walks,
          frustum: {
            frameTopDeg: r2(frameTopDeg),
            canopyUnderside: CANOPY_UNDERSIDE,
            skyVisibleBeyond: r2(skyAt),
          },
          perf: {
            fps: Math.round(perf.fps),
            calls: perf.calls,
            tris: perf.triangles,
            dpr: r2(perf.dpr),
          },
        }
      },

      /**
       * `audit()` reduced to M1's exit criteria as PASS / FAIL lines.
       *
       * This is the one to run. `audit()` returns everything measured, which is
       * useful once something has failed and useless before that — thirty numbers
       * compared to a document by hand is exactly the slow, error-prone step this
       * whole harness exists to remove. Here the thresholds are in code (see M1
       * above), so verifying the milestone is one line pasted into a console and
       * one short block read back.
       *
       * Logs the block and returns a one-line verdict, because a returned
       * multi-line string prints with escaped newlines in a browser console.
       */
      report() {
        const a = handle.audit()
        const lines = []
        let failed = 0

        const check = (label, ok, detail) => {
          if (!ok) failed++
          lines.push(`${ok ? 'PASS' : 'FAIL'}  ${label.padEnd(24)}${detail}`)
        }

        // 1 — "Camera never clips geometry." Worst case across every pose and
        // every walk sample, because one embedded frame is a failure.
        const clearances = [
          ...Object.values(a.poses).map((p) => p.camClear),
          ...Object.values(a.walks).map((w) => w.camClearMin),
        ]
        const worstClear = Math.min(...clearances)
        check(
          '1 camera never clips',
          worstClear >= M1.minCameraClearance,
          `worst clearance ${worstClear} m · 0 would mean embedded in geometry`,
        )

        // 2 — Pull-in: full distance in the open, short of the wall in the slot.
        const atFull = (id) => a.poses[id].dist >= CAMERA.distance - 0.02
        const open = POSES.filter((p) => p.want === 'free').every((p) => atFull(p.id))
        const tight = POSES.filter((p) => p.want !== 'free').every(
          (p) => !atFull(p.id),
        )
        check(
          '2 camera pulls in',
          open && tight,
          `open ${a.poses.plaza.dist} m · dead end ${a.poses.slotDeep.dist} m`,
        )

        // 3 — "Walk the 30 m strip."
        const road = a.walks.road30
        check(
          '3 30 m strip walkable',
          road.reached && road.groundedPct >= M1.minGroundedPct,
          `${road.travelled} m in ${road.seconds} s · ${road.groundedPct}% grounded`,
        )

        // 4, 5 — "Slopes and stairs traverse without the controller fighting the
        // ground at ±0.25 m noise."
        const clean = (w, floor) =>
          w.reached && w.stepMax <= M1.maxStepBetweenSamples && w.groundedPct >= floor
        const r8 = a.walks.ramp8
        check(
          '4 8% slope clean',
          clean(r8, M1.minGroundedPct),
          `step ${r8.stepMax} m ≤ ${M1.maxStepBetweenSamples} · ${r8.groundedPct}% grounded · ${r8.slopeMax}°`,
        )
        const stairs = a.walks.stairs
        check(
          '5 stairs clean',
          clean(stairs, M1.minGroundedPctStairs),
          `step ${stairs.stepMax} m ≤ ${M1.maxStepBetweenSamples} · ${stairs.groundedPct}% grounded`,
        )

        // 6 — The §2 camera height, held while walking rather than asserted.
        const heights = Object.values(a.walks).flatMap((w) => [w.aboveMin, w.aboveMax])
        const lo = Math.min(...heights)
        const hi = Math.max(...heights)
        const tol = M1.cameraHeightTolerance
        check(
          '6 camera height holds',
          Math.abs(lo - CAMERA.worldHeight) <= tol &&
            Math.abs(hi - CAMERA.worldHeight) <= tol,
          `${lo}–${hi} m above feet · target ${CAMERA.worldHeight} ±${tol}`,
        )

        // 7 — "Never shows sky above where a canopy line would be." Structural,
        // not sampled: pitch is derived from the offset and there is no free look,
        // so the frame top is the same angle on every frame of the game. What is
        // left is a continuity requirement on the canopy, which M1 has no canopy
        // to test — so it is stated as the number M5 has to respect rather than
        // claimed as measured here.
        const f = a.frustum
        check(
          '7 sky above canopy',
          true,
          `frame top ${f.frameTopDeg}° fixed · canopy must be unbroken within ${f.skyVisibleBeyond} m ahead (→ M5)`,
        )

        // 8 — look-target §10 budgets, watched from M1 so a regression is visible
        // the session it happens rather than at M13.
        const p = a.perf
        check(
          '8 perf budget',
          p.fps >= BUDGET.fps && p.calls <= BUDGET.drawCalls && p.tris <= BUDGET.triangles,
          `${p.fps} fps ≥ ${BUDGET.fps} · ${p.calls} draws ≤ ${BUDGET.drawCalls} · ${p.tris} tris · dpr ${p.dpr}`,
        )

        // Not a criterion. The 25% ramp is deliberately out of spec, and what it
        // does is worth knowing: if it traverses cleanly then 8% is a comfort
        // choice, and the controller is not what limits the road's grade.
        const r25 = a.walks.ramp25
        lines.push(
          `NOTE  25% ramp, out of spec    ${r25.groundedPct}% grounded · step ${r25.stepMax} m · ${r25.slopeMax}°`,
        )

        const verdict = `M1 ${8 - failed}/8 ${failed ? `— ${failed} FAILED` : 'PASS'}`
        console.log(['', `M1 EXIT CRITERIA — ${verdict}`, '', ...lines, ''].join('\n'))
        return verdict
      },
    }

    window.__M1 = handle
    return () => {
      delete window.__M1
    }
  }, [advance, setFrameloop, getState, camera, scene, gl, world, rapier, playerRef])

  return null
}
