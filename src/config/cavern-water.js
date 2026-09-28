import { CAVERN_LOOK } from './cavern-look'

// Shared pool surface for the REF10 study and connected PD05 cavern.
// Layer 0 is the main view; layer 1 contains only the cavern, its lights/player.
export const WORLD_AND_POOL_LAYERS = 3
export const CAVERN_WATER = {
  deep: '#111d27',
  grazing: '#475b69',
  reflectionSize: { low: 0, medium: 384, high: 512 },
  rippleUv: 0.0012,
  opening: { openingPosition: CAVERN_LOOK.openingPosition, openingRadius: 4,
    openingScale: [.55, 1.35], opening: CAVERN_LOOK.opening },
  camera: { position: [-23, -5, -177], target: [-12, -1, -202] },
}
