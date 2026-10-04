// REF10's cool enclosed palette. Outdoor palette remains in look.js.
export const CAVERN_LOOK = {
  fog: '#4c5e6b', fogNear: 20, fogFar: 100,
  ambientSky: '#8297a6', ambientGround: '#202c36', ambientIntensity: .42,
  opening: '#d5e0e3', openingPosition: [-12, 20.3, -205],
  keyPosition: [-12, 17, -205], keyTarget: [-10, -7.4, -211],
  keyColour: '#c3d7e3', keyIntensity: 2100, keyAngle: .42,
  fillPosition: [-12, 10, -205], fillIntensity: 90,
  shaft: '#b7cbdc', shaftOpacity: .32,
  shaftTopRadius: 1.1, shaftBottomRadius: 3.2,
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
