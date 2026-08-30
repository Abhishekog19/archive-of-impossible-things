/**
 * The numbers from look-target.md, in code, once.
 *
 * look-target.md opens with a rule: anything in it is overridable, but it has to
 * be overridden *there*, not silently in a scene file. This module is how that
 * rule is enforced — scene code imports these names and never writes a literal.
 * If a value here disagrees with the document, the document is right and this
 * file is a bug.
 *
 * Section references below point at look-target.md.
 */

// --- §2 Camera ---------------------------------------------------------------
//
// These are not independent numbers. The character is 1.70 m with a 0.35 m
// capsule radius; the pivot sits at chest height rather than head height to keep
// the horizon high in frame; and the camera's −11° pitch is not something we
// set, it *falls out* of sitting 4.0 m back and 0.8 m up and looking at the
// pivot: atan(0.8 / 4.0) = 11.31°. Writing the pitch as its own value would let
// it drift out of agreement with the offset. So the offset is the truth here and
// the pitch is a consequence — see CAMERA.derivedPitchDeg, which exists only so
// the dev HUD can prove it still matches the document.

export const CHARACTER = {
  height: 1.7,
  radius: 0.35,
  // Ecctrl takes a capsule as half-height plus radius, where the half-height is
  // the straight middle section only: 2 × 0.5 + 2 × 0.35 = 1.70.
  capsuleHalfHeight: 0.5,
  capsuleRadius: 0.35,
  // Ecctrl floats the capsule above the ground on a spring rather than resting
  // it, which is what makes stairs and bumps feel smooth. It also means the
  // capsule bottom is never the visual foot position.
  floatHeight: 0.2,
}

// Distance from the rigid body's centre up to the camera pivot. The body centre
// sits (halfHeight + radius) above the capsule bottom, and the pivot is 1.40 m
// above the feet, so: 1.40 − (0.5 + 0.35) = 0.55.
export const PIVOT_ABOVE_BODY =
  1.4 - (CHARACTER.capsuleHalfHeight + CHARACTER.capsuleRadius)

export const CAMERA = {
  pivotAboveFeet: 1.4,
  distance: 4.0,
  heightAbovePivot: 0.8,
  fov: 50, // three.js `fov` is vertical; landscape phones get horizontal free
  damping: 0.12, // the camera should arrive slightly late, never instantly
  // Derived, for display and assertion only — never used to aim the camera.
  derivedPitchDeg: -(Math.atan2(0.8, 4.0) * 180) / Math.PI, // ≈ −11.31°
  worldHeight: 1.4 + 0.8, // 2.2 m — the number canopy clearance derives from
  // §2's clearance rule: nothing may hang lower than 4.0 m above the camera,
  // because transparent foliage cards across the lens are the ugliest and most
  // expensive thing that can happen in this game.
  minClearanceAboveCamera: 4.0,
  // Camera collision: pull in, never clip. The margin keeps the near plane off
  // the surface we pulled in to.
  collisionMargin: 0.25,
  minDistance: 0.9,
}

// CANOPY_UNDERSIDE is derived from the camera but also needs the road's noise
// amplitude, so it lives below ROAD — see the end of the §6 block.

// --- §3 Palette --------------------------------------------------------------
//
// The rule: no colour enters a scene unless it is in this table. Ordered here
// lightest to darkest to match §3's value ladder, because the ladder — not the
// hue variety — is what makes flat colour read.

export const PALETTE = {
  sky: '#cfd3c4', // 209 · fog MUST equal this or the horizon seams (§5)
  stoneSunlit: '#cdccb6', // 203 · added by the 2026-08-25 reference lock
  stone: '#a8a394', // 163 · the shaded stone value
  foliage: '#7d9a54', // 143
  road: '#8f8877', // 136 · only 7 from foliage — the tightest gap in the table
  water: '#5d7a72', // 115
  ground: '#4a5340', //  80 · the most-seen surface in the game
  canopy: '#2f3d28', //  57
  shade: '#12150f', //  20 · already the theme-color in index.html
  daylight: '#c8a05a', // light accent only, never a surface fill
}

// --- §5 Fog ------------------------------------------------------------------
//
// The highest-value single setting in the scene: it sets mood, hides the draw
// distance cutoff, and cuts fill cost all at once. Density is per tier (§9).

export const FOG = {
  color: PALETTE.sky, // non-negotiable
  density: { high: 0.03, medium: 0.038, low: 0.05 },
  // The depth at which each density is ~95% opaque, from
  // fogFactor = 1 − exp(−(density × depth)²). Camera `far` is matched to this
  // so nothing is drawn that fog has already erased.
  opaqueAt: { high: 58, medium: 46, low: 35 },
}

// --- §6 The canopy road ------------------------------------------------------

export const ROAD = {
  width: 4.5, // wide enough not to feel like a corridor
  verge: 1.0, // each side
  trunkLine: 3.5, // ±from centreline
  maxStraight: 30, // never more than this visible — always walking toward
  maxGrade: 0.08, // 8%, comfortable to travel continuously
  // §6 ground irregularity. This is a *movement* limit, not a visual one: more
  // than ±0.25 m on a walkable surface and the controller fights the ground.
  noise: { road: 0.25, verge: 0.8, offRoad: 1.5 },
}

// §2 says "with the camera at 2.2 m, the canopy underside sits at 6.5 m", and
// §6's dimensions table locks 6.5 m. But 2.2 + 4.0 is 6.2, so the document
// states two things that can't both be arithmetic. 6.5 is the one locked in two
// places, and the missing 0.3 has an obvious home: §6 allows ±0.25 m of road
// noise, so the camera's *world* height is 2.2 m only on flat ground and as much
// as 2.45 m over a crest. Clearing 4.0 m at the worst case of that noise gives
// 6.45 m, which is what 6.5 rounds from. So the noise term is written in
// explicitly rather than left as an unexplained 0.3.
//
// Flagged for §19 sign-off: if 6.2 was the intent and 6.5 is a slip, this is the
// line to change — but §6's dimensions table changes with it.
export const CANOPY_UNDERSIDE =
  Math.ceil(
    (CAMERA.worldHeight + ROAD.noise.road + CAMERA.minClearanceAboveCamera) * 10,
  ) / 10 // 6.5 m

// --- §9 Tiers ----------------------------------------------------------------
// M1 hard-codes medium. The real detection and override arrive at M2.

export const TIERS = {
  high: { dpr: 1.5, fogDensity: FOG.density.high, far: FOG.opaqueAt.high },
  medium: { dpr: 1.25, fogDensity: FOG.density.medium, far: FOG.opaqueAt.medium },
  low: { dpr: 1.0, fogDensity: FOG.density.low, far: FOG.opaqueAt.low },
}

// --- §10 Budgets -------------------------------------------------------------
// Watched by the dev HUD from M1 onward so a regression is visible the session
// it happens, not at M13.

export const BUDGET = { drawCalls: 150, triangles: 300_000, fps: 30 }
