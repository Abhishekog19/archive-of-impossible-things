# Blender pipeline

Setup verified September 5, 2026; environment production updated September 8.

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

## Not yet proven

Phase 2 now proves a full-colour diffuse bake through UV0 and an embedded 1K JPEG
into R3F MeshBasicMaterial. Foliage uses separate vertex-tinted opaque geometry.
`art/source/hub-corner.blend` packs the bake and retains hidden editable originals;
`public/models/hub-corner.glb` contains only runtime meshes and collision.
Keep the generated sources in Git with their generators; their current compressed
sizes are small enough for regular Git. Rebuilds replace these named generated
files, so save manually edited versions separately.

Separate lightmap-channel binding, reusable vegetation instancing, sustained Iris Xe
performance, final reference quality and phone performance remain unproven.
See `plans/CURRENT_PLAN.md` for the benchmark and next visual review priorities.

Blender modifiers and procedural materials must become supported exported geometry
and image textures, or have an explicit browser implementation. Static lightmapped
shells, reusable props and simplified colliders should remain distinct export groups.
Blender's default Z-up and glTF's axis conversion must be handled by the exporter;
do not apply a second ad-hoc rotation during loading.

See `environment-september-plan.md` for the dated production gates and scope.
