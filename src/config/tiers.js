import { TIERS } from './look'

/**
 * The tier-detection POLICY. config/look.js owns what each tier looks like
 * (the look-target section 9 numbers); this file owns how a device ends up on
 * one. Every consumer reads the decision from the store -- nothing else in the
 * codebase is allowed to guess at device capability.
 *
 * The policy, in five rules (technical-production-spec section 5):
 *
 * 1. RESOLUTION ORDER: manual override (persisted) > tier saved by a previous
 *    session > GPU-name hint > medium. The GPU string is only ever a *starting*
 *    guess -- names lie (a "good phone" and a "weak phone" can share an Adreno
 *    label), so the probe corrects what the name got wrong.
 *
 * 2. DEMOTE-ONLY, ALWAYS. Automatic tier movement only ever goes down, never
 *    up, within a session. This is the anti-oscillation guarantee, and it is
 *    structural rather than tuned: phones hold 60 fps for ~90 s and then
 *    thermally throttle, so any policy that promotes on recovery ping-pongs
 *    exactly at the thermal boundary. Promotion paths are a fresh session
 *    (which starts from the saved tier) or the user override.
 *
 * 3. SUSTAINED EVIDENCE. The five-second average must fall below 50 FPS.
 *    Individual healthy readings cannot hide an alternating fast/slow frame
 *    pattern. Loading and pauses reset the probe; an eight-second cooldown
 *    follows each action. performance.js owns the sampling policy.
 *
 * 4. RESOLUTION FIRST. Reduce DPR in small steps before changing effects.
 *    At the resolution floor, an automatic tier can move down. Demotion keeps
 *    the current resolution, so it never makes the next frame more expensive.
 *
 * 5. OVERRIDE FREEZES THE TIER, NOT THE GOVERNOR. A user who pins High has
 *    asked for High's assets and effects and gets them -- but DPR shedding
 *    stays active, because a thermally-collapsed slideshow serves nobody and
 *    a DPR step is visually subtle where a tier pop is not.
 *
 * Demotions persist (STORAGE.auto), so a device that proved too weak starts
 * the next session at the tier it settled on instead of replaying a bad first
 * minute. Clearing site data or setting an override resets that.
 */

export const TIER_ORDER = ['high', 'medium', 'low']

export const PROBE = {
  // Resolution shedding before changing effects or while the tier is pinned.
  dprStep: 0.125,
  dprFloor: 0.75,
}

export const STORAGE = {
  override: 'aoit.v1.tierOverride',
  auto: 'aoit.v1.tierAuto',
}

/** localStorage, guarded: private windows and some webviews throw on access. */
function readStorage(key) {
  try {
    return window.localStorage.getItem(key)
  } catch {
    return null
  }
}

function writeStorage(key, value) {
  try {
    if (value === null) window.localStorage.removeItem(key)
    else window.localStorage.setItem(key, value)
  } catch {
    /* nothing to do -- the tier just won't persist */
  }
}

const isTier = (t) => TIER_ORDER.includes(t)

/**
 * A starting tier from the GPU name -- a hint, never a verdict.
 *
 * Discrete desktop parts and Apple silicon start High. Software renderers
 * start Low. Everything else -- Intel integrated, every mobile GPU, and any
 * name we have never seen -- starts Medium, which is the project's baseline
 * target, and the probe demotes the ones that cannot hold it. Phones are
 * deliberately NOT started Low: the spec's Medium column is "integrated GPU /
 * good phone", and a good phone started Low would never climb back up under a
 * demote-only policy.
 */
export function classifyGpu(name) {
  const n = (name || '').toLowerCase()
  if (/swiftshader|llvmpipe|software|microsoft basic render/.test(n)) return 'low'
  if (/nvidia|geforce|rtx|gtx|quadro|radeon rx|radeon pro|apple m|apple gpu/.test(n)) {
    return 'high'
  }
  return 'medium'
}

/** The GPU name via WEBGL_debug_renderer_info, or '' when masked. */
export function gpuName() {
  try {
    const gl = document.createElement('canvas').getContext('webgl2')
    if (!gl) return ''
    const info = gl.getExtension('WEBGL_debug_renderer_info')
    const name = info
      ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL)
      : gl.getParameter(gl.RENDERER)
    // Free the context rather than waiting for GC -- this canvas is throwaway.
    gl.getExtension('WEBGL_lose_context')?.loseContext()
    return String(name || '')
  } catch {
    return ''
  }
}

/** Rule 1's resolution order, skipping the override (used when the user cycles
 *  back to "auto" and the saved override has just been cleared). */
export function detectAutoTier() {
  const saved = readStorage(STORAGE.auto)
  if (isTier(saved)) return { tier: saved, source: 'saved' }
  const name = gpuName()
  if (name) return { tier: classifyGpu(name), source: 'gpu' }
  return { tier: 'medium', source: 'default' }
}

/** The full resolution order, override first. Called once, at store creation. */
export function detectInitialTier() {
  const override = readStorage(STORAGE.override)
  if (isTier(override)) return { tier: override, source: 'override' }
  return detectAutoTier()
}

export function persistOverride(tier) {
  writeStorage(STORAGE.override, tier)
}

export function persistAutoTier(tier) {
  writeStorage(STORAGE.auto, tier)
}

/** The tier one step down, or null when already at the floor. */
export function tierBelow(tier) {
  const i = TIER_ORDER.indexOf(tier)
  return i >= 0 && i < TIER_ORDER.length - 1 ? TIER_ORDER[i + 1] : null
}

/** The DPR a tier renders at after the governor's shedding is applied. */
export function effectiveDpr(tier, dprDrop) {
  return Math.max(PROBE.dprFloor, TIERS[tier].dpr - dprDrop)
}
