// Shared pool surface for the REF10 study and connected PD05 cavern.
// Layer 0 is the main view; layer 1 contains only the cavern, its lights/player.
export const WORLD_AND_POOL_LAYERS = 3
export const CAVERN_WATER = {
  deep: '#15232b',
  grazing: '#53636b',
  reflectionSize: { low: 0, medium: 384, high: 512 },
  rippleUv: 0.0012,
  opening: { openingPosition: [-12, 18, -205], openingRadius: 4, opening: '#9caeb8' },
  camera: { position: [-23, -5, -177], target: [-12, -1, -202] },
}
