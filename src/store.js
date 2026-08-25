import { create } from 'zustand'

/**
 * Global game state.
 *
 * zustand is deliberately plain: a store is just a function that returns an
 * object. Components subscribe to *slices* (see App.jsx) so a change to one
 * field doesn't re-render everything that touches the store.
 *
 * For Step 0 this only proves the store is wired end-to-end. The real shape
 * (progress, capability registry per design doc §11, settings, save/load)
 * arrives at Steps 6 and 8.
 */
export const useGameStore = create((set) => ({
  // Number of times the player has poked a physics cube.
  nudges: 0,
  nudge: () => set((state) => ({ nudges: state.nudges + 1 })),

  // Flips true once Rapier's WASM module has loaded and stepped a frame.
  physicsReady: false,
  setPhysicsReady: () => set({ physicsReady: true }),
}))
