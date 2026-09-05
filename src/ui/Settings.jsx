import { useEffect, useRef } from 'react'
import { useGameStore } from '../store'
import { resetTouchInput } from '../player/inputState'

export default function Settings() {
  const open = useGameStore((s) => s.settingsOpen)
  const setOpen = useGameStore((s) => s.setSettingsOpen)
  const override = useGameStore((s) => s.tierOverride)
  const setOverride = useGameStore((s) => s.setTierOverride)
  const tier = useGameStore((s) => s.tier)
  const hudVisible = useGameStore((s) => s.hudVisible)
  const toggleHud = useGameStore((s) => s.toggleHud)
  const dialog = useRef(null)

  useEffect(() => {
    if (open) { resetTouchInput(); dialog.current.showModal() }
    else dialog.current.close()
  }, [open])

  return (
    <>
      <button className="settings-toggle" onClick={() => setOpen(true)} aria-haspopup="dialog">Settings</button>
      <dialog ref={dialog} className="settings-panel" aria-labelledby="settings-title"
        onCancel={() => setOpen(false)} onClose={() => setOpen(false)}>
        <h2 id="settings-title">Settings</h2>
        <label htmlFor="quality">Visual quality</label>
        <select id="quality" value={override ?? 'auto'} onChange={(e) => setOverride(e.target.value === 'auto' ? null : e.target.value)}>
          <option value="auto">Automatic (recommended)</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <p>Currently {tier}. Your choice is saved on this device. Resolution may reduce to keep movement smooth.</p>
        <p>Move with the joystick or WASD. Drag the scene to turn. Hold Run or Shift; Jump or Space; Use or E near an object.</p>
        <button onClick={toggleHud}>{hudVisible ? 'Hide' : 'Show'} performance HUD</button>
        <button className="settings-done" onClick={() => setOpen(false)}>Return to game</button>
      </dialog>
    </>
  )
}
