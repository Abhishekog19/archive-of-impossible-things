# Blender pipeline — Phase 0

Verified September 5, 2026. No environment production has begun.

## Installed runtime

- Blender **5.2.1 LTS**: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`.
- Embedded Python **3.13.13**.
- Background Python and Cycles CPU rendering verified.
- glTF export/import verified: 1 metre test cube, one material, two UV layers.
- No Blender MCP connector is required or configured. Scripts use the installed
  Blender executable. Existing user preferences are not modified.

## Commands

From the project root:

```text
npm run blender:version
npm run blender:setup
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

Lightmap bake quality, browser UV/material binding, vegetation instancing, actual
Iris Xe environment performance, reference similarity and phone performance have
not been tested by this setup check. Phase 2 proves the visual pipeline in-browser.

Blender modifiers and procedural materials must become supported exported geometry
and image textures, or have an explicit browser implementation. Static lightmapped
shells, reusable props and simplified colliders should remain distinct export groups.
Blender's default Z-up and glTF's axis conversion must be handled by the exporter;
do not apply a second ad-hoc rotation during loading.

See `environment-september-plan.md` for the dated production gates and scope.
