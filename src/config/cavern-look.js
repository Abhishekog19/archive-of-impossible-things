// REF10's cool enclosed palette. Outdoor palette remains in look.js.
export const CAVERN_LOOK = {
  fog: '#53616c', fogNear: 9, fogFar: 68,
  ambientSky: '#8297a6', ambientGround: '#202c36', ambientIntensity: .62,
  opening: '#d5e0e3', openingPosition: [-12, 20.3, -205],
  keyPosition: [-12, 17, -205], keyTarget: [-10, -7.4, -211],
  keyColour: '#c3d7e3', keyIntensity: 1500, keyAngle: .52,
  fillPosition: [-12, 10, -205], fillIntensity: 160,
  shaft: '#b7cbdc', shaftOpacity: .22,
  shaftTop: [-12, 18.2, -205], shaftBottom: [-10, -7.65, -211],
}

const smooth = (a, b, value) => {
  const t = Math.max(0, Math.min(1, (value - a) / (b - a)))
  return t * t * (3 - 2 * t)
}

// Camera-space transition through the descent. An outdoor/aerial camera stays
// daylight; returning up the passage restores exactly the outdoor settings.
export function cavernBlend({ y, z }) {
  return smooth(-151, -176, z) * (1 - smooth(3, 12, y))
}
