import { create } from 'zustand'
import { directSpring, EMPTY_SPRING, readSpring, SPRING_KEY } from './spring'

function initial() {
  try { return readSpring(localStorage.getItem(SPRING_KEY)) } catch { return { ...EMPTY_SPRING } }
}
function save(state) {
  try { localStorage.setItem(SPRING_KEY, JSON.stringify({ version: 1, ...state })) } catch { /* Play remains available without storage. */ }
}
export const useSpring = create(set => ({
  progress: initial(), near: false, ready: false,
  setProximity: (near, ready) => set(s => s.near === near && s.ready === ready ? s : { near, ready }),
  direct: route => set(s => { const progress = directSpring(s.progress, route); save(progress); return { progress } }),
  reset: () => { const progress = { ...EMPTY_SPRING }; save(progress); set({ progress }) },
}))
