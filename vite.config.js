import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        /*
          Split the two large, rarely-changing dependencies into their own
          chunks. This does not reduce total bytes — it makes them cacheable
          across deploys, so shipping a gameplay change re-downloads only the
          app chunk instead of ~3 MB of engine.

          `three` and `@dimforge/rapier3d-compat` are both dependency leaves
          (nothing in the graph imports back into app code from them), so
          splitting them can't create a chunk init-order problem.

          Note on rapier's size: rapier3d-compat inlines its WebAssembly
          module as a base64 string rather than shipping a .wasm file. That is
          a single ~2 MB literal in the bundle and it is not compressible the
          way JS is. It is also why there is no .wasm network request at
          runtime. If the initial payload ever needs to shrink, the lever is
          to lazy-load the physics-using scene (Step 5, scene streaming) so
          the hub can render before rapier arrives — not to try to shrink the
          chunk itself.
        */
        manualChunks(id) {
          if (id.includes('@dimforge/rapier3d')) return 'rapier'
          if (id.includes('node_modules/three/')) return 'three'
        },
      },
    },
    /*
      Raised from Vite's 500 kB default, which the rapier chunk can never
      meet. Set just above the known chunk so genuinely new bloat still
      warns. The budget that actually matters is design doc §10 / spec §2:
      ≤ 8 MB initial-to-playable, measured over the wire, not per chunk.
    */
    chunkSizeWarningLimit: 2400,
  },
})
