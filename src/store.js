import { create } from 'zustand'

/**
 * Global game state.
 *
 * zustand is deliberately plain: a store is just a function that returns an
 * object. Components subscribe to *slices* so a change to one field doesn't
 * re-render everything that touches the store.
 *
 * The real shape (progress, the capability registry per design doc §11,
 * settings, save/load) arrives at M8. Everything here is either M1 debug state
 * or the fog toggle.
 *
 * Debug values are written from useFrame, which means they are written far more
 * often than they need to be read. Both setters below are therefore throttled by
 * their callers, and both bail out when nothing meaningful changed — a store
 * write with a new object identity re-renders every subscriber whether or not
 * the numbers differ.
 */
export const useGameStore = create((set, get) => ({
  // --- M1 dev HUD ------------------------------------------------------------

  // Camera state, so the HUD can prove the §2 numbers rather than assert them.
  cameraY: 0,
  cameraDistance: 0,
  cameraYaw: 0,
  setCameraDebug: (cameraY, cameraDistance, cameraYaw) => {
    const s = get()
    // 1 cm / ~0.5° of change is below what the HUD displays.
    if (
      Math.abs(s.cameraY - cameraY) < 0.01 &&
      Math.abs(s.cameraDistance - cameraDistance) < 0.01 &&
      Math.abs(s.cameraYaw - cameraYaw) < 0.01
    ) {
      return
    }
    set({ cameraY, cameraDistance, cameraYaw })
  },

  player: { speed: 0, onGround: false, slopeDeg: 0, feetY: 0, x: 0, z: 0 },
  setPlayerDebug: (player) => set({ player }),

  // --- Settings --------------------------------------------------------------

  // Fog is the highest-value setting in the scene (look-target §5) but it also
  // hides the far end of a 30 m test course, so M1 can turn it off. The shipped
  // game has no such toggle.
  fogEnabled: true,
  toggleFog: () => set((s) => ({ fogEnabled: !s.fogEnabled })),

  hudVisible: true,
  toggleHud: () => set((s) => ({ hudVisible: !s.hudVisible })),
}))
