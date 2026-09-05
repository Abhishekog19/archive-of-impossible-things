# Archive of Impossible Things

A 3D web game you play in a browser. Each room runs on a rule that shouldn't
work, and you have to figure out the rule before you can get out.

It is also this developer's portfolio, but that part isn't the pitch and isn't
the point of playing it.

**Status: M2 of 13 — mobile implementation built; real-phone verification pending.**
Touch joystick, Run / Jump / Use, simultaneous keyboard input, quality settings,
adaptive resolution, safe-area layout and a landscape prompt are implemented.
See [verification.md](verification.md) for the final phone checks and existing M1
audit issues. M3 art work starts after the phone gate passes.

A grey test room with a character, a camera, and
movement. No art yet; everything you can see gets deleted at M3. What exists is
the thing the rest is built on: the `look-target.md` §2 camera, collision that
pulls in rather than clipping, slopes and stairs for traversal checks, and a
dev HUD watching the performance budgets from day one.

## Design documents

The thinking happened before the code, and it's checked in:

- [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md)
  — the concept, the laws it has to obey, the architecture.
- [game-flow.md](game-flow.md) — the 95 minutes, minute by minute, and the six
  beats every archive is built from.
- [look-target.md](look-target.md) — the visual target as numbers: camera,
  palette, fog, road dimensions. Every constant in it lives once, in
  [src/config/look.js](src/config/look.js), and scene code never writes a literal.
- [technical-production-spec.md](technical-production-spec.md) — performance
  budgets, device tiers, the asset pipeline, and the known risks.
- [build-roadmap.md](build-roadmap.md) — the 13 milestones, 742 hours, exit
  criteria per milestone, and what gets cut first if it needs to be shorter.

And how the work itself is run:

- [model-plan.md](model-plan.md) — which model builds which part, and why the
  split is about what can be specified rather than what is difficult.
- [working-rules.md](working-rules.md) — session discipline, the build→verify→report
  loop, and the template for briefing work to a model with no project context.
- [verification.md](verification.md) — what to run to prove a milestone passed
  its exit criteria.

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

Then open http://localhost:5173.

**WASD** to move, **shift** to run, **space** to jump, **drag** to turn, **E** at
the post. **H** toggles the dev HUD, **F** toggles fog.

On a phone, use the left joystick and right action buttons; drag the scene to turn.
Settings offers Automatic / High / Medium / Low and a performance HUD toggle.
Keyboard and touch remain available together. Settings pause the simulation.

M2 phone build: [Open the grey room](https://archive-impossible-things-m2.abhishekpandey989828.chatgpt.site).

The HUD reports the `look-target.md` §10 budgets alongside the §2 camera numbers.
The camera ones matter more than they look: the pitch, the 2.2 m camera height and
the 6.5 m canopy underside are all *derived* from the camera offset rather than set
directly, so displaying the live measurement is the only honest way to claim they
still hold.

In dev builds `window.__M1.report()` walks the test course under a stepped clock and
prints M1's exit criteria as pass/fail — see [verification.md](verification.md). It
returns numbers rather than screenshots because a number can be compared to a
threshold and an impression cannot.

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
