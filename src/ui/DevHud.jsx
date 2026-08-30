import { useEffect, useState } from 'react'
import { BUDGET, CAMERA, CANOPY_UNDERSIDE, ROAD } from '../config/look'
import { useGameStore } from '../store'
import { perf } from './perf'

/**
 * The M1 dev HUD.
 *
 * Two jobs, and the second is the less obvious one. It shows the perf budgets
 * from look-target.md §10 so a regression is visible immediately — but it also
 * shows the *derived* camera numbers from §2 next to the live ones. The pitch,
 * the 2.2 m camera height and the 6.5 m canopy underside are all consequences of
 * the offset rather than values we set, so the only honest way to claim they hold
 * is to display the measurement.
 *
 * Sampled at 5 Hz. Anything faster is unreadable and costs renders.
 */

/** A row that knows whether it is inside budget. */
function Row({ label, value, budget, unit = '', invert = false }) {
  const over = budget != null && (invert ? value < budget : value > budget)
  return (
    <div className="hud-row">
      <span className="hud-label">{label}</span>
      <span className={over ? 'hud-value hud-over' : 'hud-value'}>
        {value}
        {unit}
        {budget != null && (
          <span className="hud-budget">
            {' '}
            / {budget}
            {unit}
          </span>
        )}
      </span>
    </div>
  )
}

export default function DevHud() {
  const [, tick] = useState(0)
  // Selected as separate primitives on purpose. A selector returning a new
  // object — `(s) => ({ y: s.cameraY })` — hands zustand v5 a fresh identity on
  // every snapshot comparison, which it treats as a change: infinite re-render.
  const cameraY = useGameStore((s) => s.cameraY)
  const cameraDistance = useGameStore((s) => s.cameraDistance)
  const player = useGameStore((s) => s.player)
  const fogEnabled = useGameStore((s) => s.fogEnabled)
  const toggleFog = useGameStore((s) => s.toggleFog)
  const hudVisible = useGameStore((s) => s.hudVisible)
  const toggleHud = useGameStore((s) => s.toggleHud)

  useEffect(() => {
    const id = setInterval(() => tick((n) => n + 1), 200)
    return () => clearInterval(id)
  }, [])

  useEffect(() => {
    const onKey = (e) => {
      if (e.code === 'KeyH') toggleHud()
      if (e.code === 'KeyF') toggleFog()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [toggleHud, toggleFog])

  if (!hudVisible) {
    // Clickable as well as keyable: a phone has no H key, and M2 tests on a
    // real device rather than an emulator.
    return (
      <button type="button" className="hud hud-collapsed" onClick={toggleHud}>
        H — hud
      </button>
    )
  }

  // The camera should sit at 2.2 m above the player's feet whenever it has not
  // been pulled in by collision. Showing the delta rather than the raw height
  // makes the claim checkable while walking over the noisy road, where the
  // absolute height is supposed to move.
  const heightAboveFeet = cameraY - player.feetY
  const pulledIn = cameraDistance < CAMERA.distance - 0.02

  return (
    <div className="hud">
      <div className="hud-title">M1 · it moves</div>

      <div className="hud-group">
        <Row label="fps" value={perf.fps.toFixed(0)} budget={BUDGET.fps} invert />
        <Row label="frame" value={perf.frameMs.toFixed(1)} unit=" ms" />
        <Row label="draws" value={perf.calls} budget={BUDGET.drawCalls} />
        <Row label="tris" value={perf.triangles.toLocaleString()} />
        <Row label="dpr" value={perf.dpr.toFixed(2)} />
        <Row label="geo / tex" value={`${perf.geometries} / ${perf.textures}`} />
      </div>

      <div className="hud-group">
        <div className="hud-heading">camera · look-target §2</div>
        <Row label="above feet" value={heightAboveFeet.toFixed(2)} unit=" m" />
        <Row label="target" value={CAMERA.worldHeight.toFixed(2)} unit=" m" />
        <Row
          label="distance"
          value={`${cameraDistance.toFixed(2)}${pulledIn ? ' ← pulled in' : ''}`}
          unit=" m"
        />
        <Row label="pitch" value={CAMERA.derivedPitchDeg.toFixed(2)} unit="°" />
        <Row label="canopy floor" value={CANOPY_UNDERSIDE.toFixed(2)} unit=" m" />
      </div>

      <div className="hud-group">
        <div className="hud-heading">player</div>
        <Row label="speed" value={player.speed.toFixed(2)} unit=" m/s" />
        <Row label="slope" value={player.slopeDeg.toFixed(1)} unit="°" />
        <Row label="grounded" value={player.onGround ? 'yes' : 'no'} />
        <Row
          label="at x / z"
          value={`${player.x.toFixed(1)} / ${player.z.toFixed(1)}`}
        />
        <Row label="feet y" value={player.feetY.toFixed(2)} unit=" m" />
        <Row label="road noise" value={`±${ROAD.noise.road}`} unit=" m" />
      </div>

      <div className="hud-hint">
        WASD move · shift run · space jump · drag to turn · E at the post
        <br />
        H hud · F fog {fogEnabled ? 'on' : 'off'}
      </div>
    </div>
  )
}
