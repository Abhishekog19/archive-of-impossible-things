import { Html } from '@react-three/drei'

const screenCenter = (_object, _camera, size) => [size.width / 2, size.height / 2]
// Html normally hides when its world-space anchor is behind the camera. This
// overlay is screen UI and must also remain visible on reverse/cavern entries.
const keepVisible = () => {}

export default function ScreenOverlay({ children }) {
  return <Html fullscreen calculatePosition={screenCenter} onOcclude={keepVisible}
    zIndexRange={[18, 18]} style={{ pointerEvents: 'none' }}>{children}</Html>
}
