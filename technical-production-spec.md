# Technical Production Spec — Archive of Impossible Things

*Created: 2026-08-24*
*Companion to [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md). The design doc says what we're making; this says how it stays fast.*
*Status: budgets and tiers locked. Items marked ⚠ are unvalidated until the Step 2.5 art spike.*
*Revised for design doc v5: §4.3, §4.5 and §7 changed when the art direction reversed from hard-surface to stylized-natural. §4.6 (foliage overdraw) is new and is the main open technical risk.*

---

## 0. Target Hardware

**The baseline device is the dev machine: Intel Iris Xe (i5-1240P, 16 GB RAM, no discrete GPU).**

This is a deliberate advantage. Building on integrated graphics means performance discipline is enforced by hardware rather than willpower — if it feels good here, it feels good on the large majority of real visitors' machines. A discrete GPU would let bad decisions hide until launch.

Corollary: **never profile only on this machine.** It has a 16-thread desktop-class CPU and no thermal ceiling worth worrying about. Phones have neither. Real-phone testing over the deployed URL is mandatory from Step 2 onward.

---

## 1. Renderer Decision (resolved)

**`WebGLRenderer`, WebGL2, standard materials.**

| Evidence | Value |
|---|---|
| WebGL2 global support | **95.73%** (StatCounter, July 2026) |
| WebGPU global support | 85.56% (83.99% full + 1.57% partial) |
| WebGPU in Firefox | **No shipping version.** Flag-gated from 63 through 157. |
| WebGPU in desktop Safari | *Partial* only, from 26.0 |
| WebGPU in iOS Safari | Full, from 26.0 |
| three.js latest | r185 (July 2026) |

Two independent reasons this isn't close:

1. **A portfolio cannot show a recruiter on Firefox a black screen.** Firefox is the single largest hole in WebGPU coverage, and it's a browser technical people actually use.
2. **The WebGPU/TSL authoring stack is still churning.** three.js r183 (Feb 2026) renamed `PostProcessing` → `RenderPipeline` and `Nodes` → `NodeManager`. Core class renames six months ago is not a foundation for a first-time 3D developer on a multi-month solo project.

`WebGPURenderer` does have a WebGL fallback backend, but using it means authoring in TSL node materials, where the drei/postprocessing ecosystem is far less battle-tested. Not worth the risk for zero visible gain in a stylized, baked-lighting game — WebGPU's wins are in compute and draw-call throughput, and our whole strategy is to *not need* draw-call throughput.

**Revisit only if** a specific effect genuinely requires compute shaders.

---

## 2. Performance Budgets (locked)

Engineering targets to force discipline. Measured with `renderer.info` and Chrome DevTools, not vibes.

| Metric | Budget | Notes |
|---|---|---|
| Draw calls per scene | **< 150** (ideal < 100) | The real bottleneck. See §3. |
| Visible triangles | < 300 K | Generous — we will hit the draw-call wall first |
| Dynamic lights | 0–1 | Everything else baked |
| Real-time shadow maps | **0** | Blob shadow instead. See §4.2. |
| Device pixel ratio | capped **1.0–1.5** | Biggest single knob. See §4.4. |
| Postprocessing passes | ≤ 2 | Bloom + tone map. Nothing else by default. |
| Materials per scene | ≤ 10 | One per atlas |
| Standard textures | 1 K atlas per room | |
| Hero textures | 2 K, selective | 4 K never, in practice |
| Initial download to playable | **≤ 8 MB** | Tightened from the design doc's 10–20 MB |
| Per-archive payload | **≤ 10 MB** | Tightened from 10–30 MB — that was 10–30 s on 4G |
| Full-quality scenes resident | **1** | Hard rule. See §6. |
| Target FPS | 60 desktop / 30 floor on weak mobile | |
| **Transparency layers** *(v5)* | **≤ 3** | Ground cover + mid plants + canopy. See §4.6 — this is the budget most at risk. |

A dev-only HUD showing draw calls, triangles, FPS and texture memory gets added at Step 2 and stays visible for the whole project.

---

## 3. Draw Calls Are The Enemy

Iris Xe will push millions of triangles happily and then fall over at ~1500 draw calls. Triangle count is almost never the problem in a project this size; **state changes are.**

Three rules:

1. **Merge static geometry per room.** The architectural shell (walls, floors, ceilings, stairs) becomes one merged mesh with one material. Not fifty separate wall pieces.
2. **`InstancedMesh` for every repeat.** Columns, shelves, lamps, gears, books, crates, display cases — this is what the design doc's §10 "instancing" line actually cashes out to.
3. **One material per texture atlas.** Fewer materials = fewer binds = fewer draw calls. Atlas the props rather than giving each its own texture.

---

## 4. Making It Look Good For Free

**Thesis: perceived quality on the web comes from light, colour, composition and silhouette — not polygon count, shader complexity, or resolution.** Nearly everything expensive-looking in a stylized game is cheap if it's baked or faked.

### 4.1 Baked lighting — the single largest win
Bake GI and AO in Blender (Cycles), render in-browser with **zero runtime lights**. Soft shadows, colour bleed, contact darkening — all free at runtime. A fully baked scene routinely looks better *and* runs 5–10× faster than a real-time-lit scene with eight lights.

Two viable strategies:

| | **A — Full bake to atlas** | **B — Tiling albedo × lightmap** |
|---|---|---|
| Materials | `MeshBasicMaterial` + `map` only | `map` (UV0) × `lightMap` (UV1) |
| UV sets | 1 | 2 |
| Texel density | Limited by atlas size | Good — albedo tiles |
| File size | Larger textures | Smaller |
| Complexity | Simplest, no gotchas | Needs `TEXCOORD_1` wiring |

**Use B for the room shell, A-style thinking for hero props.** ⚠ Validate at Step 2.5.

**⚠ The `uv1` gotcha:** lightmaps need a second UV channel. Blender must export the lightmap UV as the *second* UV map so glTF writes `TEXCOORD_1`, which `GLTFLoader` maps to `uv1`; then `material.lightMap.channel = 1` in three. Getting this wrong is the classic silently-invisible-lightmap afternoon.

**⚠ Instancing and lightmapping are in tension** — every instance shares one geometry, so instances cannot have unique lightmap regions. Resolution: bake proper lightmaps only for the **merged static shell**, and light **instanced props** cheaply (baked vertex colours, a hemisphere/gradient ambient term, or per-instance colour tint). Don't try to lightmap instanced geometry.

### 4.2 Zero shadow maps — use a blob shadow
A soft radial-gradient decal projected under the character. One transparent quad, no depth pass, reads perfectly in a stylized game. If a hero machine truly needs a real shadow: one directional light, 1024 map, tight frustum, nothing else in the scene casting.

### 4.3 Cheap effects that read as expensive — reordered in v5 for a natural palette

Design doc §9 (v5) rejected the futuristic/emissive look, which changes the ranking here. **Emissive + bloom was previously listed first; it's now demoted**, because it was serving a sci-fi aesthetic that is now an explicit anti-goal. The replacements are cheaper, not dearer — this reversal costs nothing in performance and arguably saves a post pass.

1. **Dappled light through canopy** — the highest-value effect for this direction. It's a *texture*, not a light: bake the leaf-shadow pattern into the lightmap for static ground, and for movement add one slowly-scrolling multiply/overlay plane. Reads as sunlight through leaves for ~1 draw call and no shadow map.
2. **Light shafts through gaps in the canopy** — the old "fake god rays" trick (additive transparent planes with a soft gradient), which happens to fit a forest better than it ever fit a laboratory. ~2 draw calls, reads as volumetrics.
3. **Exponential fog** — now doing triple duty: mood, draw-distance culling, *and* hiding the far edge of foliage so the canopy can be shallow. See §4.6.
4. **One environment map** (free CC HDRI, downsampled hard) — an overcast or forest HDRI gives soft natural ambient for a single texture. Matches the stated lighting preference directly.
5. **Vertex-shader wind on foliage** — sway driven by vertex position and time, no CPU cost, no extra draw calls. This is what separates a living forest from a plastic one, and it's nearly free.
6. **Dust motes / floating pollen / drifting particles** — near-free, add disproportionate life, and read as natural rather than technological.
7. **Vignette + colour-grading LUT** — still the cheapest way to tie a palette together.
8. **Emissive + selective bloom** — *use sparingly and only where a natural source justifies it* (sun through a gap, sky reflection on water). No glowing seams, no neon, no lit panels (Law 13).

### 4.4 Cap device pixel ratio — do this first
`dpr={[1, 1.5]}` on the R3F `<Canvas>` instead of native (often 2–3 on laptops and phones). DPR 2 → 1.25 is roughly a **2.5× fill-rate saving**, and in a fogged stylized scene is close to invisible. Cheapest large win available; apply before optimising anything else.

### 4.5 Style must match what we can produce — REVISED (v5)

Assets are **procedurally scripted, not sculpted** (zero budget). The v4 version of this section concluded from that constraint that the style had to be hard-surface museum-and-machinery. **That conclusion is reversed** — design doc §9 (v5) carries the full argument. Short version: the constraint is real but much narrower than v4 claimed. Scripting can't author a convincing *individual plant*; it is excellent at terrain, erosion, rock, and at distributing and instancing anything.

| Category | Source | Difficulty |
|---|---|---|
| Architecture, structures, weathered masonry | Scripted `bpy` | Easy — unchanged from v4 |
| **Rock, cliffs, terrain, eroded/uneven ground** | **Scripted `bpy`** — noise displacement on subdivided mesh, boolean, bevel | **Easy.** A pipeline strength. |
| **Water planes** | **Scripted `bpy`** + simple scrolling-normal material | Easy |
| **Scatter and placement of everything** | **Scripted `bpy`** — instanced distribution, curve-following, randomised rotation/scale | **Easy.** The single best thing scripting does. |
| **Trees, plants, foliage cards** | **Free CC0** — Quaternius nature packs, Poly Haven textures | Sourced, same principle as the character |
| Player character, rigged/animated assets | Free CC0 — Quaternius / Mixamo | Sourced |
| Cloth, creatures, hair, hand-painted texture | **Avoid entirely** | The real pipeline boundary |

**Stylized natural, never photoreal natural.** This is the part of v4's reasoning that survives intact, and it matters more than the rest: *geometric styles forgive inexperienced execution; naturalistic styles expose it.* A slightly-wrong clean arch reads as stylistic; a slightly-wrong tree reads as broken. So: simple flat materials, strong silhouettes, colour and light doing the work, no photoreal surface detail. Reference register — Journey, Sable, RiME, Breath of the Wild. Attempting Unreal-forest realism here would look *worse* the closer it got.

The stated lighting preference (soft, diffuse, dappled, *"nothing too theatrical"*) points the same direction and is cheaper than the alternative. Palette and material vocabulary: rock, soil, bark, moss, worn stone, water, weathered wood — irregular and imperfect, but pleasant rather than grim.

### 4.6 Foliage overdraw — the new risk in v5 ⚠

**This is the cost of the §9 reversal, and it's real.** The museum aesthetic carried no transparency load. A canopy does: foliage is alpha-tested cards, cards are fill-rate, and fill-rate is precisely what Iris Xe and mid-range phones have least of. Overlapping leaf cards can shade the same pixel a dozen times over.

Rules, to be validated at Step 2.5:

1. **Alpha-*test*, never alpha-blend, for foliage.** Blending forces sorting and defeats early-Z; testing (`alphaTest: 0.5`, `transparent: false`) keeps depth rejection working. This one choice is most of the win.
2. **Instanced cross-cards, not modelled branches.** Two or three intersecting quads per plant, one `InstancedMesh` per species.
3. **Shallow canopy, deep fog.** Don't build a forest that recedes 200 m and then hide it — build 30 m of it and let exponential fog terminate the view. Fog does the culling, so the geometry never exists.
4. **Cap layered depth.** Ground cover + mid plants + canopy is three transparency layers. A fourth is a budget request, not a free decision.
5. **Canopy overhead is cheaper than canopy ahead.** Cards above the camera cover fewer screen pixels than cards filling the horizon — which happens to suit the target image (enclosure overhead, road open ahead).
6. **Measure the fill-rate proxy, not draw calls.** Draw calls stay low with instancing, so this will look fine right up until frame time says otherwise. Compare frame time at DPR 1.0 vs 1.5 — a large gap between them is the signature of a fill-rate bound, not a geometry bound.

**If Step 2.5 fails these, the fallback is *sparser* nature, not a return to machinery:** open rock and sky, fewer and larger plants, distance carried by fog and silhouette. Losing density is acceptable; losing the natural register is not.

---

## 5. Device Tiers

### Input
`ecctrl` ships DOM-based touch controls from the `ecctrl/input` subpath — `<Joystick />` and `<VirtualButton id="jump" />` — swappable for custom UI, driving the same stores the keyboard drives (`useJoystickStore.setJoystick(x, y)`, `useButtonStore.setButtonActive("jump", true)`). It also exposes `groundDetection="rayCast"` as explicitly the cheapest ground-detection mode for mobile.

**Detect touch *capability*, not screen width, and keep both paths live** — touchscreen laptops exist, and a desktop user may plug in a gamepad.

Current peer requirements: `three` 0.184+, `@react-three/fiber` 9.4+, `@react-three/rapier` 2.2+.

### Tiers

| Tier | Target | DPR | Post | Shadows | Particles | Textures | Foliage *(v5)* |
|---|---|---|---|---|---|---|---|
| **High** | Discrete-GPU desktop | 1.5 | Bloom + vignette | 1 light @ 1024 | Full | 2 K hero | Full density, 3 layers |
| **Medium** ← *default target* | Integrated GPU / good phone | 1.25 | Bloom only | Blob | Reduced | 1 K | ~60% density, 3 layers |
| **Low** | Weak mobile | 1.0 | None | Blob | None | Half-res, nearer fog | ~30% density, 2 layers, canopy only |
| **Fallback** | Can't run WebGL2 | — | — | — | — | Professional portfolio served directly | — |

**Foliage density is the best new tier knob**, and better than dropping DPR further: scatter counts are a single instance-count parameter per species, so density scales continuously with no asset variants and no visual pop — thinning a forest reads as a different part of the forest, whereas a DPR drop reads as a blurry screen. Pair it with pulling fog nearer so the thinning isn't visible at distance.

### Detection: measure, never sniff
User-agent sniffing is a dead end. Instead:
1. `WEBGL_debug_renderer_info` for a GPU-name hint
2. A **runtime FPS probe during the intro/loading sequence**
3. Auto-select a tier, then expose a user override in settings
4. Degrade **continuously** thereafter via drei's `PerformanceMonitor` / `AdaptiveDpr`

Step 4 matters more than steps 1–3, because of the next section.

### The mobile constraints that aren't FPS
- **Thermal throttling.** A phone holds 60 fps for ~90 s, then halves. *Initial benchmarks lie.* Continuous adaptive degradation is mandatory; short archives with natural pauses help.
- **Memory.** Mobile Safari kills tabs at a few hundred MB of GPU memory. This is why "one scene resident" is a hard rule, not a guideline.
- **iOS.** WebGL2 is fine (Safari 15+). Watch for frame hitches on large texture uploads. **Audio requires a user-gesture unlock** before anything will play — plan the intro around one deliberate click.
- **Viewport.** Prompt for landscape, respect safe-area insets, `touch-action: none` on the canvas.

### Device independence is also a *design* constraint
Mechanics must not demand precision touch can't deliver: **no pixel-perfect platforming, no twitch aiming, no fast camera flicks, no multi-key chords.**

Checked against the design doc's nine candidate exhibits: Gravity, Duplication, Time, Mirror, Sound, Observatory and Garden are all mobile-safe. **Scale / Miniature Island is the one at risk** — it's specified as a traversal/platforming space. Either make its platforming forgiving, or accept it as desktop-favoured.

**⚠ New tension in v5.** Design doc §8 now makes traversal a headline feature with a deliberate skill ceiling — momentum, slope carry, something worth mastering. That pulls directly against the rule above, because *depth* in a movement system usually means *precision*, and precision is what touch lacks.

The resolution is that the two aren't the same axis. **Depth can live in momentum rather than in accuracy** — Rocket League's own skill ceiling is about anticipating a physical system, not about hitting small targets, which is why it works on a controller with two analogue sticks and no mouse. So the traversal verb must be chosen such that mastery means *reading the system well*, not *inputting finely*:

| Acceptable depth | Unacceptable depth |
|---|---|
| Carrying speed through a curve | Landing on a small platform |
| Timing a launch on a slope | Frame-perfect input windows |
| Choosing a line through open space | Precise mid-air corrections |
| Chaining momentum across terrain | Holding an exact heading |

**Acceptance test at Step 1: the movement must be enjoyable on a phone, not merely functional.** If the skill ceiling only exists on keyboard, the two-layer model in §8 is desktop-only and needs rethinking — and that's much cheaper to discover at Step 1 than after three archives are built on top of it.

---

## 6. Memory Discipline

The single most common web-3D leak: disposing meshes but not their GPU resources.

On archive exit, for everything in the unloaded scene:
- `geometry.dispose()`
- `material.dispose()` — and every texture on it: `map`, `lightMap`, `aoMap`, `normalMap`, `emissiveMap`, `envMap`
- Remove from the scene graph
- Clear any drei/loader cache entry for the asset (`useGLTF.clear(url)`)
- Verify: `renderer.info.memory.geometries` and `.textures` return to baseline

**Acceptance test:** enter and exit archives 20 times; `renderer.info.memory` must be flat and DevTools must show no GPU-memory growth.

---

## 7. Asset Pipeline

⚠ Entire section unvalidated until Step 2.5. Commands are the intended shape, to be confirmed against installed tool versions.

**Prerequisites to install (all free):**
- **Blender** — current stable, from blender.org. Not currently installed.
- **`@gltf-transform/cli`** — `npm i -g @gltf-transform/cli`
- **KTX-Software** — provides the `toktx` binary that gltf-transform's KTX2 commands depend on

**Flow:** `bpy` script generates geometry → Cycles bake → export GLB (both UV sets) → `gltf-transform` for Meshopt + KTX2 → load via drei `useGLTF`.

| Stage | Choice | Why |
|---|---|---|
| Geometry compression | **Meshopt** over Draco | Faster decode, better with instancing and animation |
| Colour textures | KTX2 **ETC1S** | Much smaller; quality is fine for albedo |
| Normal/data maps | KTX2 **UASTC** | ETC1S mangles normals |
| ⚠ Transcoder | Copy basis transcoder files into `public/basis/`, `ktx2Loader.setTranscoderPath('/basis/')` | Required for KTX2 to decode in-browser |

**Baking on this machine:** Cycles has no GPU to use (Iris Xe), so bakes are CPU-bound — but 16 threads makes that workable. Keep lightmaps at 512–1024, use low sample counts with denoising, and bake overnight if a scene ever needs more.

**What gets scripted vs sourced free:**

| Asset | Source |
|---|---|
| Architecture, structures, weathered masonry (design doc §12 kits) | Scripted in `bpy` |
| **Terrain, rock, cliffs, eroded ground, water planes** | **Scripted in `bpy`** — noise displacement (new in v5) |
| **All scatter and placement** | **Scripted in `bpy`** — instanced distribution (new in v5) |
| **Trees, plants, foliage** | **Quaternius nature packs (CC0) + Poly Haven textures** — sourced, not scripted (new in v5) |
| **Player character (rigged + animated)** | Quaternius (CC0) or Mixamo — free, and supplies the animation clips `ecctrl` expects to sync |
| HDRIs, surface textures | Poly Haven (CC0) |

Scripted generation cannot produce convincing **characters, cloth, creatures, hair, or hand-painted texture** — that's the real boundary, and it's why the split above exists. It *can* do terrain and rock well; the v4 claim that it was bad at organic forms generally was too broad (see §4.5).

**⚠ Outdoor baking differs from interior baking.** §4.1's strategy table was written for a room shell. For outdoor ground: bake dappled canopy shadow and AO into the lightmap (strategy B — tiling albedo × lightmap, so terrain texel density stays usable across large areas), but **do not attempt to lightmap the foliage itself** — instanced cards can't hold unique lightmap regions (§4.1's instancing tension). Light plants with a cheap gradient/hemisphere term plus per-instance colour variation instead. Validate at Step 2.5.

---

## 8. Stack Summary

| Layer | Choice | Status |
|---|---|---|
| Build tool | **Vite + React** | Resolved. Next.js's SSR/SEO buys nothing for a WebGL canvas; the portfolio text pages are the only SEO surface and can be static. Vite's faster iteration matters at 12 hrs/week. |
| Rendering | three.js r185 + React Three Fiber, `WebGLRenderer` | Resolved (§1) |
| Physics + controller | `@react-three/rapier` + `ecctrl` | From design doc §13 |
| State / save | `zustand` + `localStorage` | From design doc §13 |
| Helpers | `@react-three/drei`, `@react-three/postprocessing` | |
| Hosting | Vercel | |
