import { useEffect, useState } from 'react'
import { Joystick, VirtualButton } from 'ecctrl/input'
import { resetTouchInput } from '../player/inputState'
import { useGameStore } from '../store'

const wrapper = { position: 'relative', width: 64, height: 64, zIndex: 'auto' }
const cap = { width: 56, height: 56, background: 'rgba(18,21,15,.7)', color: '#e8e6df', border: '1px solid #8f8877' }

export default function MobileControls() {
  const settingsOpen = useGameStore((s) => s.settingsOpen)
  const [touch, setTouch] = useState(() => window.matchMedia('(any-pointer: coarse)').matches || navigator.maxTouchPoints > 0)
  const [epoch, setEpoch] = useState(0)

  useEffect(() => {
    const query = window.matchMedia('(any-pointer: coarse)')
    const detect = () => setTouch(query.matches || navigator.maxTouchPoints > 0)
    const onPointer = (event) => { if (event.pointerType === 'touch') setTouch(true) }
    // Remount as well as clearing stores: ecctrl retains the captured pointer
    // internally, which may never receive pointerup after an OS interruption.
    const reset = () => { resetTouchInput(); setEpoch((n) => n + 1) }
    query.addEventListener('change', detect)
    window.addEventListener('pointerdown', onPointer)
    window.addEventListener('blur', reset)
    window.addEventListener('resize', reset)
    document.addEventListener('visibilitychange', reset)
    return () => {
      query.removeEventListener('change', detect)
      window.removeEventListener('pointerdown', onPointer)
      window.removeEventListener('blur', reset)
      window.removeEventListener('resize', reset)
      document.removeEventListener('visibilitychange', reset)
      resetTouchInput()
    }
  }, [])

  if (!touch || settingsOpen) return null
  return (
    <div className="touch-controls" key={epoch}>
      <div className="movement-control" aria-label="Touch movement joystick">
        <Joystick id="move" joystickMaxRadius={44}
          joystickWrapperStyle={{ position: 'relative', width: 144, height: 144, zIndex: 'auto' }}
          joystickBaseStyle={{ width: 104, height: 104, border: '1px solid #8f8877', background: 'rgba(18,21,15,.4)' }}
          joystickKnobStyle={{ width: 48, height: 48, background: 'rgba(207,211,196,.75)' }} />
      </div>
      <div className="touch-actions" aria-label="Touch actions">
        <VirtualButton id="run" label="Run" buttonWrapperStyle={wrapper} buttonCapStyle={cap} />
        <VirtualButton id="jump" label="Jump" buttonWrapperStyle={wrapper} buttonCapStyle={cap} />
        <VirtualButton id="interact" label="Use" buttonWrapperStyle={wrapper} buttonCapStyle={cap} />
      </div>
      <p className="landscape-prompt" role="status">Turn your phone sideways for more room to explore.</p>
    </div>
  )
}
