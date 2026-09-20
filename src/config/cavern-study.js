import { CAVERN_WATER } from './cavern-water'

// Temporary REF10 technical proof; final cavern art belongs to Phase E.
export const CAVERN_STUDY = {
  views: {
    cavern: CAVERN_WATER.camera,
    'cavern-west': { position: [-32, -5, -194], target: [-8, -2, -204] },
    'cavern-east': { position: [8, -5, -197], target: [-15, 0, -205] },
    'cavern-shore': { position: [-25, -6.1, -184], target: [-8, -5.5, -207] },
  },
  fog: '#53616c',
  fogNear: 12,
  fogFar: 85,
  opening: '#c1d4e0',
  shaft: '#b7cbdc',
  shaftOpacity: .24,
  openingPosition: [-12, 19.5, -205],
  openingRadius: 6,
  shaftPosition: [-12, 5, -205],
}
