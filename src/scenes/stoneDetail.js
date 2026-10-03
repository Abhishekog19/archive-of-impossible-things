// Keep the authored diffuse lighting; add a small shared world-scale mineral layer.
// UV atlas resolution no longer controls this close-distance surface breakup.
export function addStoneDetail(material, texture, study = false) {
  material.onBeforeCompile = (shader) => {
    shader.uniforms.stoneGrain = { value: texture }
    shader.vertexShader = shader.vertexShader.replace('#include <common>', `
      #include <common>
      varying vec3 stonePoint, stoneNormal;
    `).replace('#include <begin_vertex>', `
      #include <begin_vertex>
      stonePoint = (modelMatrix * vec4(position, 1.0)).xyz;
      stoneNormal = normalize(mat3(modelMatrix) * normal);
    `)
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', `
      #include <common>
      uniform sampler2D stoneGrain;
      varying vec3 stonePoint, stoneNormal;
    `).replace('#include <color_fragment>', `
      #include <color_fragment>
      vec3 weights = pow(abs(normalize(stoneNormal)), vec3(4.0));
      weights /= max(dot(weights, vec3(1.0)), .001);
      vec3 samples = vec3(texture2D(stoneGrain, stonePoint.yz * .5).r,
        texture2D(stoneGrain, stonePoint.xz * .5).r,
        texture2D(stoneGrain, stonePoint.xy * .5).r);
      float mineral = dot(samples, weights);
      float closeDetail = 1.0 - smoothstep(18.0, 38.0, distance(cameraPosition, stonePoint));
      diffuseColor.rgb *= 1.0 + (mineral - .78) * .75 * closeDetail;
      ${study ? `
      // Fine mineral pores use metre-scale cells, independent of atlas density.
      vec2 poreUv = stonePoint.xz * 64.0;
      vec2 cell = floor(poreUv);
      float seed = fract(sin(dot(cell, vec2(127.1, 311.7))) * 43758.5453);
      float radius = length(fract(poreUv) - vec2(.3 + seed * .4, .5));
      float aa = max(length(fwidth(poreUv)), .035);
      float pores = (1.0 - smoothstep(.055, .055 + aa, radius)) * step(.58, seed);
      float nearSurface = 1.0 - smoothstep(5.0, 12.0, distance(cameraPosition, stonePoint));
      diffuseColor.rgb *= 1.0 - pores * .22 * nearSurface * weights.y;
      ` : ''}
    `)
  }
  material.customProgramCacheKey = () => study ? 'patch-stone-study-v1' : 'world-stone-detail-v1'
}

// A narrow, metre-scaled directional layer keeps large baked trunk atlases
// readable near the player. Long grain stays quieter than stone grain.
export function addBarkDetail(material, texture, study = false) {
  material.onBeforeCompile = shader => {
    shader.uniforms.barkGrain = { value: texture }
    shader.vertexShader = shader.vertexShader.replace('#include <common>', `
      #include <common>
      varying vec3 barkPoint, barkNormal;
    `).replace('#include <begin_vertex>', `
      #include <begin_vertex>
      barkPoint = (modelMatrix * vec4(position, 1.0)).xyz;
      barkNormal = normalize(mat3(modelMatrix) * normal);
    `)
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', `
      #include <common>
      uniform sampler2D barkGrain;
      varying vec3 barkPoint, barkNormal;
    `).replace('#include <color_fragment>', `
      #include <color_fragment>
      vec3 n = abs(normalize(barkNormal));
      float grainX = texture2D(barkGrain, barkPoint.zy * vec2(3.4, .16)).r;
      float grainZ = texture2D(barkGrain, barkPoint.xy * vec2(3.4, .16)).r;
      float grain = (grainX * n.x + grainZ * n.z) / max(n.x+n.z, .001);
      float fade = (1.0-smoothstep(12.0, 28.0, distance(cameraPosition,barkPoint))) * (1.0-n.y);
      diffuseColor.rgb *= 1.0 + (grain-.78) * .55 * fade;
      ${study ? `
      // Broken longitudinal fissures remain sharp at player distance while the
      // atlas supplies broad colour and canopy shade. Fade/derivatives prevent
      // thin lines from shimmering in the middle distance.
      vec2 tangent = barkPoint.zx;
      vec2 phase = tangent * 73.0 + sin(tangent * 17.0 + barkPoint.y * 1.8) * 1.2
        + sin(barkPoint.y * 3.1 + tangent * 9.0) * .5;
      vec2 signal = abs(sin(phase));
      vec2 aa = max(fwidth(phase), vec2(.045));
      vec2 fissures = (1.0 - smoothstep(vec2(.08), vec2(.16) + aa, signal));
      float furrow = dot(fissures, n.xz) / max(n.x + n.z, .001);
      float broken = smoothstep(.68, .86, texture2D(barkGrain, barkPoint.xy * vec2(.8, 1.8)).r);
      diffuseColor.rgb *= 1.0 - furrow * broken * .24 * fade * (1.0 - smoothstep(.4, .8, n.y));
      ` : ''}
    `)
  }
  material.customProgramCacheKey = () => study ? 'patch-bark-study-v1' : 'world-bark-detail-v1'
}
