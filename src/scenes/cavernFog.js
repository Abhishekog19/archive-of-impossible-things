import { Color } from 'three'
import { CAVERN_LOOK } from '../config/cavern-look.js'

// Fog follows enclosed surfaces, including when viewed through an outdoor portal.
// Only the distance travelled inside the cave contributes to its haze.
export function cavernFog(shader, point, strength = '1.0') {
  shader.uniforms.caveFogColour = { value: new Color(CAVERN_LOOK.fog) }
  shader.fragmentShader = shader.fragmentShader.replace('#include <fog_pars_fragment>', `
    #include <fog_pars_fragment>
    uniform vec3 caveFogColour;
  `).replace('#include <fog_fragment>', `
    #ifdef USE_FOG
      float outdoorFog = smoothstep(fogNear, fogFar, vFogDepth);
      float enclosed = smoothstep(140.0, 150.0, -${point}.z) * ${strength};
      float caveDistance = min(vFogDepth, max(0.0, -${point}.z - 171.0));
      float insideFog = smoothstep(${CAVERN_LOOK.fogNear.toFixed(1)}, ${CAVERN_LOOK.fogFar.toFixed(1)}, caveDistance);
      vec3 mist = mix(fogColor, caveFogColour, enclosed);
      gl_FragColor.rgb = mix(gl_FragColor.rgb, mist, mix(outdoorFog, insideFog, enclosed));
    #endif
  `)
  return shader
}
