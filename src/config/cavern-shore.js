import shape from './cavern-shore.json'

// Blender reads the same coefficients for the visible bank and its collider.
export const cavernShoreGLSL = `${shape.radius.toFixed(2)} + ${shape.lobes[0].toFixed(2)} * sin(3.0 * shoreAngle)
  + ${shape.lobes[1].toFixed(2)} * cos(5.0 * shoreAngle) + ${shape.lobes[2].toFixed(2)} * sin(11.0 * shoreAngle)`
