import { create } from 'zustand'
import { TIERS } from './config/look'
import {
  PROBE,
  detectAutoTier,
  detectInitialTier,
  persistAutoTier,
  persistOverride,
  tierBelow,
} from './config/tiers'

// Resolved once, at module load, so the first Canvas mount already renders at
// the right cost. Order: override > saved > GPU hint > medium (tiers.js rule 1).
const initialTier = detectInitialTier()

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

  // --- Tiers (M2) --------------------------------------------------------------
  //
  // The policy lives in config/tiers.js; the state lives here so every consumer
  // (Canvas dpr, fog density, camera far, the HUD, later the settings panel)
  // reads one authority. tierSource exists for the HUD and for bug reports:
  // "low / demoted" and "low / override" are different situations.

  tier: initialTier.tier,
  tierSource: initialTier.source,
  tierOverride: initialTier.source === 'override' ? initialTier.tier : null,
  // Resolution shed by the governor once there is no tier left below (or the
  // tier is pinned), in DPR units. Never persisted -- it describes a thermal
  // state, not the device.
  dprDrop: 0,

  demoteTier: () => {
    const s = get()
    if (s.tierOverride) return // rule 5: an override freezes the tier
    const next = tierBelow(s.tier)
    if (!next) return
    persistAutoTier(next) // next session starts here instead of re-failing
    set({ tier: next, tierSource: 'demoted', dprDrop: 0 })
  },

  shedDpr: () =>
    set((s) => ({
      dprDrop: Math.min(
        s.dprDrop + PROBE.dprStep,
        Math.max(0, TIERS[s.tier].dpr - PROBE.dprFloor),
      ),
    })),

  // The manual override, cycled from the HUD (T) until the M2 settings panel
  // lands: high -> medium -> low -> auto. Auto clears the pin and re-detects.
  cycleTierOverride: () => {
    const s = get()
    const order = ['high', 'medium', 'low', null]
    const next = order[(order.indexOf(s.tierOverride) + 1) % order.length]
    persistOverride(next)
    if (next) {
      set({ tier: next, tierSource: 'override', tierOverride: next, dprDrop: 0 })
    } else {
      const auto = detectAutoTier()
      set({ tier: auto.tier, tierSource: auto.source, tierOverride: null, dprDrop: 0 })
    }
  },

  // --- Dev stepping ----------------------------------------------------------

  // The simulation pauses while the page is hidden, which is correct for the
  // shipped game and wrong for a test that steps the loop by hand from a hidden
  // pane — physics would be paused for exactly the frames the test is driving.
  // DevProbe.manual() raises this to keep rapier running anyway. Dev only.
  physicsForced: false,
  setPhysicsForced: (physicsForced) => set({ physicsForced }),
}))
