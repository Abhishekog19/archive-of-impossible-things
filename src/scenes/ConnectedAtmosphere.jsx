import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Color, MathUtils } from 'three'
import { FOG, PALETTE } from '../config/look'
import { CAVERN_LOOK, cavernBlend } from '../config/cavern-look'
import { WORLD_AND_POOL_LAYERS } from '../config/cavern-water'
import { useGameStore } from '../store'

/** One owner for background, fog and ambient light along the connected route. */
export default function ConnectedAtmosphere() {
  const background = useRef(null)
  const fog = useRef(null)
  const ambient = useRef(null)
  const fogEnabled = useGameStore((s) => s.fogEnabled)
  const colours = useMemo(() => ({
    sky: new Color(PALETTE.sky), ground: new Color(PALETTE.ground),
    outdoorFog: new Color(FOG.color), caveFog: new Color(CAVERN_LOOK.fog),
    caveSky: new Color(CAVERN_LOOK.ambientSky), caveGround: new Color(CAVERN_LOOK.ambientGround),
  }), [])
  useFrame(({ camera }) => {
    const blend = cavernBlend(camera.position)
    background.current.copy(colours.sky).lerp(colours.caveFog, blend)
    ambient.current.color.copy(colours.sky).lerp(colours.caveSky, blend)
    ambient.current.groundColor.copy(colours.ground).lerp(colours.caveGround, blend)
    ambient.current.intensity = MathUtils.lerp(1.6, CAVERN_LOOK.ambientIntensity, blend)
    if (fog.current) {
      fog.current.color.copy(colours.outdoorFog).lerp(colours.caveFog, blend)
      fog.current.near = MathUtils.lerp(22, CAVERN_LOOK.fogNear, blend)
      fog.current.far = MathUtils.lerp(115, CAVERN_LOOK.fogFar, blend)
    }
  })
  return <>
    <color ref={background} attach="background" args={[PALETTE.sky]} />
    {fogEnabled && <fog ref={fog} attach="fog" args={[FOG.color, 22, 115]} />}
    <hemisphereLight ref={ambient} layers-mask={WORLD_AND_POOL_LAYERS} args={[PALETTE.sky, PALETTE.ground, 1.6]} />
  </>
}
