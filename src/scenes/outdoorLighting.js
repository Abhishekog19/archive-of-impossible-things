// Continuous world-space grading over the authored diffuse bake. Shared by
// plants, masonry and the character so streaming boundaries cannot change it.
export function addOutdoorLighting(material) {
  const previous = material.onBeforeCompile
  const previousKey = material.customProgramCacheKey()
  material.onBeforeCompile = shader => {
    previous.call(material, shader)
    shader.vertexShader = shader.vertexShader.replace('#include <common>', `
      #include <common>
      varying vec3 lightWorldPoint;
    `).replace('#include <project_vertex>', `
      vec4 lightPoint = vec4(transformed, 1.0);
      #ifdef USE_INSTANCING
        lightPoint = instanceMatrix * lightPoint;
      #endif
      lightWorldPoint = (modelMatrix * lightPoint).xyz;
      #include <project_vertex>
    `)
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', `
      #include <common>
      varying vec3 lightWorldPoint;
      float lightOpening(vec2 p, vec2 centre, vec2 radius) {
        vec2 d = (p - centre) / radius;
        return 1.0 - smoothstep(.12, 1.0, dot(d, d));
      }
    `).replace('#include <color_fragment>', `
      #include <color_fragment>
      vec3 p = lightWorldPoint;
      float woodland = smoothstep(-99.0, -89.0, p.z) * (1.0 - smoothstep(-26.0, -16.0, p.z));
      // This projection follows the baked sun's direction, including tree faces.
      vec2 groundLight = p.xz - p.y * vec2(.5, .667);
      float opening = max(lightOpening(groundLight, vec2(-10.0, -45.0), vec2(5.0, 6.0)),
        max(lightOpening(groundLight, vec2(-12.0, -70.0), vec2(4.0, 5.0)),
          lightOpening(groundLight, vec2(-10.0, -84.0), vec2(4.5, 5.0))));
      vec3 woodlandLight = mix(vec3(.72, .83, .79), vec3(1.16, 1.10, .94), opening);
      diffuseColor.rgb *= mix(vec3(1.0), woodlandLight, woodland);
      // Retain the bright courtyard; cool and deepen the sheltered hall sides.
      float hall = smoothstep(-146.0, -137.0, p.z) * (1.0 - smoothstep(-117.0, -108.0, p.z));
      float nave = 1.0 - smoothstep(1.5, 7.0, abs(p.x + 12.0));
      diffuseColor.rgb *= mix(vec3(1.0), mix(vec3(.78, .84, .87), vec3(1.05, 1.03, .97), nave), hall);
    `)
  }
  material.customProgramCacheKey = () => previousKey + '-outdoor-light-v1'
}
