import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Color, Matrix4, Mesh, ShaderMaterial, UniformsLib, UniformsUtils, Vector2, Vector3 } from 'three'
import { Reflector } from 'three/addons/objects/Reflector.js'
import { useGameStore } from '../store'
import { CAVERN_WATER } from '../config/cavern-water'
import { cavernWaterView } from '../config/cavern-water-view'

const shader = {
  name: 'CavernPoolStudy',
  uniforms: {
    ...UniformsLib.fog,
    color: { value: new Color(CAVERN_WATER.deep) },
    grazing: { value: new Color(CAVERN_WATER.grazing) },
    tDiffuse: { value: null },
    textureMatrix: { value: new Matrix4() },
    time: { value: 0 },
    reflected: { value: 0 },
    texel: { value: 0 },
    ripple: { value: CAVERN_WATER.rippleUv },
    openingCentre: { value: new Vector3() },
    openingTint: { value: new Color() },
    openingRadius: { value: 0 },
    openingScale: { value: new Vector2(1, 1) },
    shoreline: { value: 0 },
  },
  vertexShader: `
    uniform mat4 textureMatrix;
    varying vec4 projected;
    varying vec3 worldPoint;
    #include <fog_pars_vertex>
    void main() {
      worldPoint = (modelMatrix * vec4(position, 1.0)).xyz;
      projected = textureMatrix * vec4(position, 1.0);
      vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
      gl_Position = projectionMatrix * mvPosition;
      #include <fog_vertex>
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform vec3 color, grazing;
    uniform float time, reflected, texel, ripple, shoreline;
    uniform vec3 openingCentre, openingTint;
    uniform float openingRadius;
    uniform vec2 openingScale;
    varying vec4 projected;
    varying vec3 worldPoint;
    #include <fog_pars_fragment>
    void main() {
      vec3 eye = normalize(cameraPosition - worldPoint);
      float fresnel = pow(1.0 - max(eye.y, 0.0), 3.0);
      float wave = sin(worldPoint.x * .62 + worldPoint.z * .37 + time * .32);
      vec3 surface = mix(color, grazing, fresnel * .32) * (1.0 + wave * .025);
      vec2 fromPool = worldPoint.xz - vec2(-12.0, -195.0);
      float shoreAngle = atan(fromPool.y, fromPool.x);
      float shoreRadius = 15.5 + 1.2 * sin(3.0 * shoreAngle) + .7 * cos(5.0 * shoreAngle);
      float depth = max(0.0, shoreRadius - length(fromPool));
      float shallows = (1.0 - smoothstep(.05, 1.25, depth)) * shoreline;
      float submergedStone = sin(worldPoint.x * 7.2 + sin(worldPoint.z * 3.1))
        * sin(worldPoint.z * 5.8 + sin(worldPoint.x * 2.4));
      // Subtle mineral bed at the edge; deep water stays clear and quiet, without
      // a bright foam outline or an opaque green disk.
      surface = mix(surface, vec3(.035, .055, .065) * (1.0 + submergedStone * .1), shallows * .55);
      if (reflected > .5) {
        vec2 uv = projected.xy / projected.w;
        uv += vec2(wave, sin(worldPoint.z * .83 - worldPoint.x * .21 + time * .24)) * ripple;
        // Bilinear sampling already filters this bounded reflection target.
        // Keep the shore silhouette clear; subtle ripples soften it in motion.
        uv = clamp(uv, vec2(texel * 2.0), vec2(1.0 - texel * 2.0));
        vec3 reflection = texture2D(tDiffuse, uv).rgb;
        surface = mix(surface, reflection * vec3(.93, .97, 1.0), (.28 + fresnel * .58) * (1.0 - shallows * .3));
      } else if (openingRadius > 0.0) {
        // Low: analytic reflection of the opening only, no scene render/texture.
        vec3 ray = reflect(-eye, vec3(0.0, 1.0, 0.0));
        vec2 hit = worldPoint.xz + ray.xz * (openingCentre.y - worldPoint.y) / max(ray.y, .02);
        vec2 offset = (hit - openingCentre.xz) / (openingRadius * openingScale);
        float glow = exp(-dot(offset, offset) * 1.5);
        surface = mix(surface, openingTint, glow * (.12 + fresnel * .34));
      }
      gl_FragColor = vec4(surface, 1.0);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
      #include <fog_fragment>
    }
  `,
}

/** Reuses the authored GLB shoreline; owns only its clone and reflection target. */
export default function CavernWater({ geometry, openingLight = null, shoreline = false }) {
  const group = useRef(null)
  const water = useRef(null)
  const tier = useGameStore((s) => s.tier)
  useEffect(() => {
    const parent = group.current
    const local = geometry.clone()
    local.computeBoundingBox()
    const centre = local.boundingBox.getCenter(new Vector3())
    local.translate(-centre.x, -centre.y, -centre.z)
    local.rotateX(Math.PI / 2) // Reflector's local plane faces +Z.
    const size = CAVERN_WATER.reflectionSize[tier]
    const mesh = size ? new Reflector(local, {
      textureWidth: size, textureHeight: size, multisample: 0,
      clipBias: .003, color: CAVERN_WATER.deep, shader,
    }) : new Mesh(local, new ShaderMaterial({
      ...shader, uniforms: UniformsUtils.clone(shader.uniforms),
    }))
    mesh.name = shoreline ? 'CavernWater' : 'CavernWaterPrototype'
    mesh.position.copy(centre)
    mesh.rotation.x = -Math.PI / 2
    mesh.material.uniforms.reflected.value = size ? 1 : 0
    mesh.material.uniforms.texel.value = size ? 1 / size : 0
    mesh.material.uniforms.shoreline.value = shoreline ? 1 : 0
    mesh.material.fog = true
    if (openingLight) {
      mesh.material.uniforms.openingCentre.value.fromArray(openingLight.openingPosition)
      mesh.material.uniforms.openingTint.value.set(openingLight.opening)
      mesh.material.uniforms.openingRadius.value = openingLight.openingRadius
      mesh.material.uniforms.openingScale.value.fromArray(openingLight.openingScale || [1, 1])
    }
    if (size) {
      const reflect = mesh.onBeforeRender
      mesh.onBeforeRender = function (renderer, scene, camera) {
        const view = cavernWaterView(camera.position, mesh.position, shoreline)
        mesh.material.uniforms.reflected.value = view.reflect ? 1 : 0
        if (!view.reflect) return
        // Connected pool reflections draw only cavern art and the player, not
        // all of the outdoor foliage hidden behind the cave walls.
        if (shoreline) this.getReflectionCamera(camera).layers.set(1)
        // Keep the additional pass in renderer.info; nested render normally resets it.
        const autoReset = renderer.info.autoReset
        renderer.info.autoReset = false
        try { reflect.call(this, renderer, scene, camera) }
        finally { renderer.info.autoReset = autoReset }
      }
    }
    parent.add(mesh)
    water.current = mesh
    return () => {
      water.current = null
      parent.remove(mesh)
      if (size) mesh.dispose()
      else mesh.material.dispose()
      local.dispose()
    }
  }, [geometry, tier, openingLight, shoreline])
  useFrame(({ camera }, delta) => {
    if (water.current) {
      // Keep the water surface through the hall portal; distant views use the
      // existing analytic fallback and never request an extra reflection pass.
      water.current.visible = cavernWaterView(camera.position, water.current.position, shoreline).visible
      water.current.material.uniforms.time.value += Math.min(delta, .1)
    }
  })
  return <group ref={group} />
}
