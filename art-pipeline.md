# Blender pipeline

Setup verified September 5, 2026; environment production updated September 17.

## Installed runtime

- Blender **5.2.1 LTS**: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`.
- Embedded Python **3.13.13**.
- Background Python and Cycles CPU rendering verified.
- glTF export/import verified: 1 metre test cube, one material, two UV layers.
- Blender MCP is installed and working. Production scripts use the installed
  Blender executable with isolated settings; MCP setup is not modified.

## Commands

From the project root:

```text
npm run blender:version
npm run blender:setup
npm run blender:blockout
npm run blender:corner
npm run blender:kit
npm run blender:zones
```

The runner searches the Blender Foundation installation directory. Set BLENDER_PATH
to an explicit executable to select another installation. Keep 5.2.1 LTS for this
milestone unless a verified blocker requires a version change.

The setup command runs headlessly with factory settings, isolated configuration
under `.artifacts/blender`, and a nonzero exit on Python failure. It does not launch
a visible window, install extensions or change the website.

## Outputs (local, ignored by Git)

- `.artifacts/blender/environment-template.blend`: empty metric scene, 1 unit = 1 m.
  Collections: Terrain, Architecture, Vegetation, Water, Colliders, Landmarks, Cameras.
- `.artifacts/blender/setup-only.glb`: disposable one-metre test cube; not game content.
- `.artifacts/blender/setup-render.png`: tiny CPU render for setup verification.
- `.artifacts/blender/setup-report.json`: measured setup results and untested items.

Setup may be rerun; these named generated outputs are overwritten. Do not author
the environment inside the generated template path. In Phase 1, save editable
production work under `art/source/` with a distinct filename. Scripts remain under
`scripts/blender/`. Export approved runtime assets to `public/models/` later.
No production asset directories are populated during setup.

Keep source `.blend` files and scripts together with the project. Decide how large
binary sources will be versioned/backed up before accumulating them; do not silently
ignore the only editable copy. Generated diagnostics/configuration stay local.
Private personal source material remains outside every export and deployment.

## Phase 2 proof status

Phase 2 proves full-colour diffuse bakes through UV0 into R3F MeshBasicMaterial:
embedded 2K paving and 1K architecture JPEGs, sRGB, with filtering capped at 4x.
Small surface relief is baked into colour; these unlit materials do not apply
runtime normal-map lighting. Canopy foliage uses vertex-tinted opaque geometry.
Twenty-four exported fern markers drive one shared R3F InstancedMesh. Authoring
copies supply baked static shadows without separate runtime plant draw calls.
`art/source/hub-corner.blend` packs the bake and retains hidden editable originals;
`public/models/hub-corner.glb` contains only runtime meshes and collision.
Keep the generated sources in Git with their generators; their current compressed
sizes are small enough for regular Git. Rebuilds replace these named generated
files, so save manually edited versions separately.

Separate lightmap-channel binding, full-world sustained performance acceptance,
final reference quality and real-phone performance remain unproven. Corner-only
measurements and visual limitations are recorded in the current plan.
See `plans/CURRENT_PLAN.md` for the benchmark and next visual review priorities.

Blender modifiers and procedural materials must become supported exported geometry
and image textures, or have an explicit browser implementation. Static lightmapped
shells, reusable props and simplified colliders should remain distinct export groups.
Blender's default Z-up and glTF's axis conversion must be handled by the exporter;
do not apply a second ad-hoc rotation during loading.

See `environment-september-plan.md` for the dated production gates and scope.

## Phase B reusable kit

`npm run blender:kit` reads `art/source/hub-corner.blend` and writes
`art/source/archive-kit.blend`, `public/models/archive-kit.glb` and
`src/config/asset-kit.json`. It does not modify the corner or hub source. The
generated kit packs textures and retains hidden editable originals; save manual
edits separately before regenerating these outputs.

Seventeen stone/wood prototypes share 2K/1K atlases; foliage meshes retain
vertex colours. Pivots use native metre-scale bottom centres, except the tree
trunk origin; the manifest records Blender-space bounds. Exporter axis conversion
is used once. Collider_* proxies accompany masonry, column, arch and trunk; the
preview uses continuous walkable ground beneath decorative paving.

`?scene=kit` proves instancing and inspection collision; `?scene=kit&view=kit` is
the comparison camera. The GLB and its R3F component load only on this route.
Directional diffuse atlases are preview lighting: rebake assembled static zones
with contextual shadows before final art delivery. Remaining variation and
water/zone-loading gates are tracked in the current plan.

The September 17 session adds tall and leaning forms derived from the
broadleaf tree. Apply the same shape function to wood, leaves and trunk proxies
before export; retain the root origin. The preview uses all three silhouettes.
Fern, grass, broadleaf clump and low shrub are opaque vertex-coloured ground cover,
batched separately with deterministic yaw/scale variation. Stone damp islands are
baked into the existing atlas; runtime moss does not add materials or draw calls.

## Zone-loading prototype

After regenerating the kit, run `npm run blender:zones`. This reads the kit source
and overwrites `public/models/zones/{ruins,forest}.glb` plus
`src/config/zone-packages.json`; it does not rewrite a Blender source. Each package
contains its asset family and matching collision proxies, with its own atlas.

`?scene=zones` is the connected loading test. Fixed views are `?scene=zones&view=zones`
and `?scene=zones&view=zone-forest`; these pin both packages for comparison. Runtime
zone mounts own their parsed resources, abort abandoned loads and dispose geometry,
materials, textures and decoded bitmaps on eviction. A permanent inspection floor
and temporary entry gates protect movement while packages load or fail.

This proves lifecycle behaviour with kit-family packages. Full-world zoning,
contextual bakes, LOD and sustained hardware acceptance remain later integration
work; do not treat these test sections as finished environment art.
