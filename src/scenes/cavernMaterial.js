import { cavernShoreGLSL } from '../config/cavern-shore.js'
import { cavernFog } from './cavernFog.js'

// Reuse the Blender PBR textures and metre-scaled UVs. The only runtime layer is
// water staining, anchored to the authored shore contour instead of UV islands.
export function shorelineLayer(shader) {
  cavernFog(shader, 'cavernPoint')
  shader.vertexShader = shader.vertexShader.replace('#include <common>', `
    #include <common>
    varying vec3 cavernPoint;
  `).replace('#include <begin_vertex>', `
    #include <begin_vertex>
    cavernPoint = (modelMatrix * vec4(position, 1.0)).xyz;
  `)
  shader.fragmentShader = shader.fragmentShader.replace('#include <common>', `
    #include <common>
    varying vec3 cavernPoint;
  `).replace('#include <color_fragment>', `
    #include <color_fragment>
    vec2 fromPool = cavernPoint.xz - vec2(-12.0, -195.0);
    float shoreAngle = atan(fromPool.y, fromPool.x);
    float shoreRadius = ${cavernShoreGLSL};
    float edge = length(fromPool) - shoreRadius;
    float brokenEdge = sin(cavernPoint.x * 2.3 + sin(cavernPoint.z * 1.7)) * .12;
    float wetStone = (1.0 - smoothstep(-.15, .8, edge + brokenEdge))
      * (1.0 - smoothstep(-7.25, -6.7, cavernPoint.y));
    diffuseColor.rgb *= mix(vec3(1.0), vec3(.72, .80, .82), wetStone);
    // Broad deposits break uniform colour without adding another texture atlas.
    float deposit = sin(cavernPoint.y * 1.7 + sin(cavernPoint.x * .24) + sin(cavernPoint.z * .31));
    diffuseColor.rgb *= 1.0 + deposit * .065;
  `).replace('#include <roughnessmap_fragment>', `
    #include <roughnessmap_fragment>
    roughnessFactor = mix(roughnessFactor, .24, wetStone);
  `)
}
