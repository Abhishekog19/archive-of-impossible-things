// Keep the authored diffuse lighting; add a small shared world-scale mineral layer.
// UV atlas resolution no longer controls this close-distance surface breakup.
export function addStoneDetail(material, texture) {
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
    `)
  }
  material.customProgramCacheKey = () => 'world-stone-detail-v1'
}
