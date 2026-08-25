# Archive of Impossible Things

A 3D web game you play in a browser. Each room runs on a rule that shouldn't
work, and you have to figure out the rule before you can get out.

It is also this developer's portfolio, but that part isn't the pitch and isn't
the point of playing it.

**Status: Step 0 of 11 — scaffold only.** There is no game here yet. What exists
is a throwaway smoke-test scene that proves the whole stack runs end to end:
rendering, physics, state, touch input, and a production build.

## Design documents

The thinking happened before the code, and it's checked in:

- [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md)
  — the concept, the laws it has to obey, the roadmap.
- [technical-production-spec.md](technical-production-spec.md) — performance
  budgets, device tiers, the asset pipeline, and the known risks.

The design doc's §17 defines the eleven build steps and what has to be true
before each one is considered done.

## Stack

| Concern | Choice | Why |
|---|---|---|
| Build | Vite + React 19 | SSR buys nothing for a WebGL canvas; dev-server speed matters at part-time pace |
| Rendering | three.js via React Three Fiber | WebGL2, not WebGPU — Firefox still ships no WebGPU, and a portfolio can't show a recruiter a black screen |
| Physics | Rapier via `@react-three/rapier` | WASM, deterministic, actively maintained |
| Character | `ecctrl` | Ships touch controls as a first-class feature, not an afterthought |
| State | zustand | Store slices that both React UI and the 3D scene can read |

## Running it

```bash
npm install
npm run dev
```

Then open http://localhost:5173. Drag to orbit, tap a cube to push it. The
overlay in the top-left reports which parts of the stack came up.

```bash
npm run build && npm run preview   # production build, served locally
npm run lint
```

## Performance notes

The project targets **60 fps on integrated graphics and a 30 fps floor on weak
mobile**, which shapes decisions that would otherwise look arbitrary:

- Device pixel ratio is capped at 1.5, never native. This is the single largest
  lever on integrated GPUs and phones.
- Zero real-time shadow maps. Lighting is baked in Blender; contact shadows come
  from a blob decal.
- Draw calls are the budget that bites, not triangles — hence instancing and
  merged static geometry.

The initial bundle is ~1.15 MB gzipped before any art. Most of that is Rapier,
which inlines its WebAssembly module as base64 rather than fetching a `.wasm`
file. Against the ≤ 8 MB initial-to-playable budget that is fine; if it ever
isn't, the fix is to defer the physics-using scene, not to shrink the chunk.

## License

See [LICENSE](LICENSE).
