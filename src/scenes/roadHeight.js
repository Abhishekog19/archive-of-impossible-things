import { ROAD } from '../config/look'

/**
 * The road's height field, in its own module.
 *
 * Separate from the component that draws it for two reasons. The mechanical one
 * is that a file exporting both a component and a plain function breaks Vite's
 * fast refresh. The real one is that M5 needs this function outside the mesh —
 * placing a trunk line, a marker or a prop on the road means asking "how high is
 * the ground at (x, z)?" without touching geometry.
 *
 * Deterministic — no RNG, so a bad spot found while walking is still there on
 * the next reload, which is the difference between a bug and a ghost.
 *
 * Low frequency is the load-bearing property. Two sine waves at different
 * wavelengths and no high-frequency term: the surface should read as uneven and
 * *feel* smooth, which look-target.md §6 is explicit are different jobs. If this
 * needed per-vertex random noise to look right, the noise would be fighting the
 * character controller by construction.
 */
export function roadHeight(x, z, amplitude = ROAD.noise.road) {
  const long = Math.sin(z * 0.11) * 0.6 // ~57 m wavelength, the main undulation
  const cross = Math.sin(x * 0.35 + z * 0.05) * 0.4 // camber that wanders
  return (long + cross) * amplitude
}
