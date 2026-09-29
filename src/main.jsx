import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Keep the unapproved neutral character and its local reference out of game routes.
const Entry = import.meta.env.DEV && new URLSearchParams(window.location.search).get('scene') === 'character-study'
  ? (await import('./scenes/CharacterStudy.jsx')).default
  : App

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Entry />
  </StrictMode>,
)
