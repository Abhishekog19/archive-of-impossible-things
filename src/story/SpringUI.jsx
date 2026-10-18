import { useEffect, useRef, useState } from 'react'
import { useButtonStore } from 'ecctrl/input'
import { useGameStore } from '../store'
import { resetTouchInput, isUiTarget } from '../player/inputState'
import { useSpring } from './springStore'
import { springMessage } from './spring'
import profile from '../content/portfolio.json'
import './story.css'

export default function SpringUI() {
  const near = useSpring(s => s.near), ready = useSpring(s => s.ready), progress = useSpring(s => s.progress)
  const open = useGameStore(s => s.interactionOpen), loading = useGameStore(s => s.worldLoading), settings = useGameStore(s => s.settingsOpen)
  const dialog = useRef(null), [project, setProject] = useState(false), [confirmReset, setConfirmReset] = useState(false)
  const canOpen = near && ready && !loading && !settings
  const close = () => useGameStore.getState().setInteractionOpen(false)
  useEffect(() => {
    const element = dialog.current
    if (open) { resetTouchInput(); element.showModal() }
    else if (element.open) { element.close(); document.querySelector('canvas')?.focus() }
  }, [open])
  useEffect(() => {
    const activate = () => { if (canOpen && !useGameStore.getState().interactionOpen) useGameStore.getState().setInteractionOpen(true) }
    const onKey = e => { if (e.code === 'KeyE' && !e.repeat && !isUiTarget(e.target)) { e.preventDefault(); activate() } }
    window.addEventListener('keydown',onKey)
    const unsubscribe = useButtonStore.subscribe(s => !!s.buttons.interact, pressed => { if (pressed) activate() })
    return () => { window.removeEventListener('keydown',onKey); unsubscribe() }
  }, [canOpen])
  useEffect(() => () => useGameStore.getState().setInteractionOpen(false), [])
  const saansation = profile.projects.find(p => p.id === 'saansation')
  return <>
    {!open && !settings && <aside className="chapter-note"><span>Story experiment · 01</span><strong>The Remembering Spring</strong><p>{canOpen ? 'A small spring waits beside the path.' : 'Follow the forest path to the shallow spring.'}</p>
      {canOpen && <button onClick={() => useGameStore.getState().setInteractionOpen(true)}>Examine the spring <kbd>E</kbd></button>}
    </aside>}
    <dialog className="spring-panel" ref={dialog} aria-labelledby="spring-title" onCancel={close} onClose={close}>
      <header><span>An experiment in curiosity</span><button aria-label="Leave the spring" onClick={close}>×</button></header>
      <h1 id="spring-title">The Remembering Spring</h1>
      <p>Water learns from whatever it touches.</p>
      <div className="spring-routes" aria-label="Direct the water">
        {[['leaves','Leaves'],['stones','Stones'],['root','Root']].map(([id,label]) => <button key={id} aria-pressed={progress.route === id} onClick={() => { setProject(false); setConfirmReset(false); useSpring.getState().direct(id) }}>{label}</button>)}
      </div>
      <p className="spring-response" role="status">{springMessage(progress)}</p>
      <p className="spring-memory">{progress.bent ? 'Curve remembered' : 'Curve undiscovered'} · {progress.lifted ? 'Lift remembered' : 'Lift undiscovered'}</p>
      {progress.complete && <div className="spring-discovery"><strong>A new possibility</strong><p>Two small discoveries, combined into something neither could do alone.</p></div>}
      <button className="spring-project" aria-expanded={project} onClick={() => setProject(!project)}>{project ? 'Back to the spring' : 'From this experiment to real work ↗'}</button>
      {project && <section aria-label="Project connection"><span>Abhishek Pandey · Selected work</span><h2>{saansation.title}</h2><p>{saansation.description}</p><p>This experiment makes a hidden process visible. Explore a real project about understanding our environment.</p><a href="?portfolio=1#saansation">Read the portfolio</a></section>}
      <footer><button onClick={close}>Keep exploring</button><button onClick={() => { if (confirmReset) { useSpring.getState().reset(); setConfirmReset(false) } else setConfirmReset(true) }}>{confirmReset ? 'Confirm restart' : 'Restart experiment'}</button></footer>
    </dialog>
  </>
}
