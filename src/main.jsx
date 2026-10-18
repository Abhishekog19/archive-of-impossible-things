import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import SceneBoundary from './ui/SceneBoundary.jsx'

// Keep the unapproved neutral character and its local reference out of game routes.
const params = new URLSearchParams(window.location.search)
const Entry = params.get('portfolio') === '1'
  ? (await import('./ui/Portfolio.jsx')).default
  : import.meta.env.DEV && params.get('scene') === 'character-study'
  ? (await import('./scenes/CharacterStudy.jsx')).default
  : (await import('./App.jsx')).default

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SceneBoundary><Entry /></SceneBoundary>
  </StrictMode>,
)
