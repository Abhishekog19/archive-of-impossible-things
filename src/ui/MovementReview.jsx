import { useState } from 'react'
import { useGameStore } from '../store'

const yieldUI = () => new Promise(resolve => setTimeout(resolve, 20))
const key = (code, down) => window.dispatchEvent(new KeyboardEvent(down ? 'keydown' : 'keyup', { code }))
const release = () => ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ShiftLeft', 'Space'].forEach(code => key(code, false))
const round = n => Number(n.toFixed(2))

// Explicit development UI: drives the real keyboard/controller/physics path.
// No FPS audit. Only mounted with ?movement-review=1 in a development build.
export default function MovementReview() {
  const [busy, setBusy] = useState(false)
  const [results, setResults] = useState([])
  const greyroom = new URLSearchParams(window.location.search).get('scene') === 'greyroom'

  async function run(kind) {
    const probe = window.__M1
    if (!probe?.body()) {
      setResults([{ name: 'Scene readiness', pass: false,
        detail: probe ? 'Controller body is not ready; reload the scene.' : 'Development scene probe is unavailable.' }])
      return
    }
    setBusy(true)
    const rows = []
    const record = (name, pass, detail) => {
      rows.push({ name, pass, detail })
      setResults([...rows])
    }
    const pos = () => probe.body().translation()
    const speed = () => Math.hypot(probe.body().linvel().x, probe.body().linvel().z)
    const steps = async frames => {
      for (let i = 0; i < frames; i += 10) {
        probe.step(Math.min(10, frames - i))
        await yieldUI()
        for (let wait = 0; useGameStore.getState().worldLoading; wait++) {
          if (wait > 500) throw new Error('Area loading did not finish')
          probe.step(10)
          await yieldUI()
        }
      }
    }
    const place = async at => { release(); probe.place(at, 0, 60); await steps(30) }
    try {
      probe.manual(true)
      await yieldUI()
      if (kind === 'dynamics') {
        const avatar = probe.scene.getObjectByName('PlayerPresentation')
        if (!avatar?.userData.readDynamics) throw new Error('Secondary rig is unavailable')
        const read = () => avatar.userData.readDynamics()
        await place([0, 2, 4]); await steps(40)
        record('Idle foot contact', read().contacts === 2 && read().footError < .025,
          `${read().contacts} feet; error ${round(read().footError * 100)} cm`)
        let maxError = 0, peakEnergy = 0, groundedSamples = 0, plantedSamples = 0
        key('KeyW', true)
        for (let i = 0; i < 100; i++) {
          if (i === 40) key('ShiftLeft', true)
          if (i === 70) { key('KeyW', false); key('KeyD', true) }
          await steps(1)
          const d = read()
          if (probe.controller().isOnGround) {
            maxError = Math.max(maxError, d.footError); groundedSamples++
            if (d.contacts > 0) plantedSamples++
          }
          peakEnergy = Math.max(peakEnergy, d.springEnergy)
        }
        release(); await steps(100)
        record('Stride and turn contact', maxError < .06 && plantedSamples > groundedSamples * .5,
          `reach error ${round(maxError * 100)} cm; ${plantedSamples}/${groundedSamples} samples planted`)
        record('Accessories react and settle', read().joints === 8 && peakEnergy > .01 && read().springEnergy < .01,
          `8 joints; peak energy ${round(peakEnergy)} → ${round(read().springEnergy)}`)
        await place([0, 2, 4])
        key('Space', true); await steps(4); key('Space', false)
        const released = read().contacts === 0
        await steps(110)
        record('Jump releases / landing plants', released && read().contacts === 2 && read().footError < .025,
          `air released ${released}; ${read().contacts} feet landed; grounded ${probe.controller().isOnGround}; y ${round(pos().y)}`)
        await place([14, 2, 9.5]); key('KeyW', true); await steps(65); release(); await steps(80)
        record('Slope contact', read().contacts === 2 && read().footError < .035,
          `25% ramp; error ${round(read().footError * 100)} cm`)
        useGameStore.getState().recordRecovery(); await steps(1)
        record('Secondary recovery reset', read().springEnergy < .1 && Number.isFinite(read().footError),
          `energy ${round(read().springEnergy)}`)
      } else if (kind === 'presentation') {
        const avatar = probe.scene.getObjectByName('PlayerPresentation')
        if (!avatar?.userData.readMotion) throw new Error('Player presentation is unavailable')
        const opacity = () => {
          let value = 1
          avatar.traverse(n => { if (n.isMesh) value = Math.min(value, n.material.opacity) })
          return value
        }
        await place([0, 2, 4])
        record('Open camera', probe.state().cameraDistance > 3.9 && opacity() > .99,
          `${round(probe.state().cameraDistance)} m; visibility ${round(opacity())}`)
        key('KeyW', true); await steps(45)
        const walk = avatar.userData.readMotion()
        key('ShiftLeft', true); await steps(45)
        const run = avatar.userData.readMotion()
        release(); await steps(40)
        record('Gait and stop', walk.name === 'Walk' && run.name === 'Run' && avatar.userData.readMotion().name === 'Idle',
          `${walk.name} → ${run.name} → ${avatar.userData.readMotion().name}`)
        useGameStore.getState().setSettingsOpen(true); await yieldUI()
        const pausedTime = avatar.userData.readMotion().time
        const pausedCamera = probe.camera.position.clone()
        await steps(30)
        record('Presentation pause', avatar.userData.readMotion().time === pausedTime &&
          probe.camera.position.distanceTo(pausedCamera) < .001, 'animation and camera stay fixed')
        useGameStore.getState().setSettingsOpen(false); await yieldUI()
        await place([5, 2, 13.25])
        record('Near-wall visibility', probe.state().cameraDistance < .5 && opacity() < .2,
          `camera ${round(probe.state().cameraDistance)} m; visibility ${round(opacity())}`)
        key('KeyW', true)
        let previous = probe.state().cameraDistance, largestOut = 0
        for (let i = 0; i < 120; i++) {
          await steps(1)
          // Position-derived distance is unthrottled, unlike the text HUD.
          const body = pos()
          const distance = Math.hypot(probe.camera.position.x - body.x, probe.camera.position.z - body.z)
          largestOut = Math.max(largestOut, distance - previous)
          previous = distance
        }
        release(); await steps(30)
        record('Camera clears wall', probe.state().cameraDistance > 3.9 && opacity() > .99 && largestOut < .5,
          `restored ${round(probe.state().cameraDistance)} m; largest outward step ${round(largestOut)} m`)
        useGameStore.getState().recordRecovery(); await steps(2)
        record('Recovery pose', avatar.userData.readMotion().name === 'Idle', avatar.userData.readMotion().name)
      } else if (kind === 'controls') {
        await place([0, 2, 4])
        key('KeyW', true); await steps(60)
        const walking = speed(), stopZ = pos().z
        key('KeyW', false); await steps(30)
        record('Walk and stop', walking > 2.7 && speed() < 0.1 && Math.abs(pos().z - stopZ) < 0.7,
          `${round(walking)} m/s; stopping distance ${round(Math.abs(pos().z - stopZ))} m`)
        await place([0, 2, 4])
        key('KeyW', true); key('ShiftLeft', true); await steps(50)
        const running = speed()
        key('ShiftLeft', false); await steps(30)
        record('Hold Shift to run', running > 4.8 && speed() < 3.3,
          `held ${round(running)} m/s; released ${round(speed())} m/s`)
        key('KeyW', false); key('KeyS', true); await steps(30)
        record('Reverse direction', probe.body().linvel().z > 2.5,
          `reverse velocity ${round(probe.body().linvel().z)} m/s`)
        await place([0, 2, 4])
        const floorY = pos().y
        key('Space', true); await steps(1); key('Space', false)
        let peak = floorY, airborne = false
        for (let i = 0; i < 12; i++) {
          await steps(10); peak = Math.max(peak, pos().y)
          airborne ||= !probe.controller().isOnGround
        }
        record('Jump and land', airborne && peak - floorY > 0.45 && probe.controller().isOnGround,
          `rise ${round(peak - floorY)} m; grounded ${probe.controller().isOnGround}`)
        key('KeyW', true); await steps(20)
        useGameStore.getState().setSettingsOpen(true); await yieldUI()
        const paused = pos(); await steps(45)
        const drift = Math.hypot(pos().x - paused.x, pos().y - paused.y, pos().z - paused.z)
        useGameStore.getState().setSettingsOpen(false); await yieldUI(); await steps(30)
        record('Pause and resume', drift < 0.01 && speed() < 0.1,
          `paused drift ${round(drift)} m; resumed speed ${round(speed())} m/s`)
        await place([5, 2, 12])
        key('KeyS', true); await steps(90); release()
        record('Wall blocks capsule', pos().z < 13.4 && pos().z > 12.5, `wall position z=${round(pos().z)}`)
      } else if (kind === 'terrain') {
        for (const [name, at, target, climb] of [
          ['Noisy road', [0, 2, -6.5], 28.5, 0],
          ['8% ramp', [8, 2, 9.5], 11, 0.7],
          ['25% ramp', [14, 2, 9.5], 6.8, 1.3],
          ['18 cm stairs', [-8, 2, 10.6], 2.5, 1.1],
        ]) {
          await place(at)
          const start = pos()
          let maxY = start.y, grounded = 0, samples = 0
          key('KeyW', true)
          while (Math.abs(pos().z - start.z) < target && samples < 140) {
            await steps(10); maxY = Math.max(maxY, pos().y)
            if (probe.controller().isOnGround) grounded++
            samples++
          }
          release()
          const distance = Math.abs(pos().z - start.z)
          record(name, distance >= target && maxY - start.y >= climb && grounded / samples > 0.85,
            `${round(distance)} m; rise ${round(maxY - start.y)} m; grounded ${Math.round(grounded / samples * 100)}%`)
        }
      } else {
        await place(kind === 'return' ? [-12, -5.5, -174] : kind === 'patch' ? [-12, 2, -20] : [0, 2, 6])
        // Connected authored route plus side trips to all four reserved locations.
        const route = kind === 'hub' ? [
          ['Hub centre', 0, -5], ['Hub forest exit', -12, -20],
          ['Hub return', 0, -5], ['Arrival return', 0, 6],
        ] : kind === 'patch' ? [
          ['Connector middle', -12, -30], ['Connector far end', -12, -39],
          ['Connector return', -12, -20],
        ] : kind === 'return' ? [
          ['Cavern ascent', -12, -159], ['Archive return', -12, -138],
          ['Jump on ascent', -12, -149],
        ] : [
          ['Hub game location', 5, 5], ['Hub path', 0, -5], ['Hub exit', -12, -20],
          ['Forest REF5', -12, -43], ['Forest bend', -10, -56],
          ['Canopy REF6', -12, -68], ['Forest game location', -23, -68],
          ['Canopy return', -12, -68], ['Deep forest', -15, -82],
          ['Archive REF7', -12, -98], ['Archive door', -12, -114],
          ['Hall REF8', -12, -123], ['Hall game location', -23, -123],
          ['Hall return', -12, -123], ['Descent', -12, -141],
          ['Cavern REF10', -12, -174], ['North bank', -22, -176],
          ['West bank', -30, -181], ['Cavern game location', -33, -195],
        ]
        const initialRecoveries = useGameStore.getState().recoveryCount
        for (const [name, x, z] of route) {
          let samples = 0
          while (Math.hypot(pos().x - x, pos().z - z) > 0.7 && samples++ < 220) {
            const p = pos()
            probe.turnTo(Math.atan2(p.x - x, p.z - z) * 180 / Math.PI)
            key('KeyW', true); await steps(10)
          }
          release(); await steps(20)
          const distance = Math.hypot(pos().x - x, pos().z - z)
          const pass = distance < 1 && useGameStore.getState().recoveryCount === initialRecoveries
          record(name, pass, `${round(distance)} m from destination; y=${round(pos().y)}`)
          if (!pass) break
        }
        if (kind === 'return' && rows.every(row => row.pass)) {
          probe.turnTo(180)
          key('KeyW', true); await steps(20)
          const floorY = pos().y
          key('Space', true); await steps(1); key('Space', false)
          await steps(15)
          record('Uphill jump', !probe.controller().isOnGround && pos().y - floorY > 0.4,
            `rise ${round(pos().y - floorY)} m; airborne ${!probe.controller().isOnGround}`)
        } else if (kind === 'world' && rows.every(row => row.pass)) {
          const count = useGameStore.getState().recoveryCount
          probe.body().setTranslation({ x: -12, y: -15, z: -195 }, true)
          await steps(90)
          const p = pos()
          record('Cavern recovery', useGameStore.getState().recoveryCount === count + 1 &&
            Math.abs(p.z + 174) < 1 && p.y > -8, `respawn ${round(p.x)}, ${round(p.y)}, ${round(p.z)}`)
        }
      }
    } catch (error) {
      record('Review error', false, error.message)
    } finally {
      release()
      useGameStore.getState().setSettingsOpen(false)
      probe.manual(false)
      setBusy(false)
    }
  }

  return <aside style={{ position: 'fixed', right: 12, top: 12, maxHeight: '85vh', overflow: 'auto',
    zIndex: 40, padding: 12, background: '#17231fed', color: '#f5f2df', font: '13px monospace', maxWidth: 440 }}>
    <strong>Movement / presentation review</strong>
    <div>{greyroom ? <>
      <button disabled={busy} onClick={() => run('presentation')}>Check PD10 camera and animation</button>
      <button disabled={busy} onClick={() => run('dynamics')}>Check PD10 feet and clothing</button>
      <button disabled={busy} onClick={() => run('controls')}>Check controls</button>
      <button disabled={busy} onClick={() => run('terrain')}>Check slopes and steps</button>
    </> : <>
      <button disabled={busy} onClick={() => run('hub')}>Check hub connection</button>
      <button disabled={busy} onClick={() => run('patch')}>Check forest connector</button>
      <button disabled={busy} onClick={() => run('world')}>Walk connected world</button>
      <button disabled={busy} onClick={() => run('return')}>Check cavern return</button>
    </>}</div>
    <p>{busy ? 'Walking the actual physics scene…' : 'Ready — no performance audit'}</p>
    {results.map(row => <p key={row.name}>{row.pass ? 'PASS' : 'FAIL'} {row.name}: {row.detail}</p>)}
  </aside>
}
