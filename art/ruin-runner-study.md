# Ruin Runner neutral study

PD08 work in progress, based on the user's selected Image 3 turnaround. This is
not an accepted final character and does not replace `explorer.glb` in gameplay.
The first study was rejected for cartoon-like appearance. The current revision
uses `scripts/blender/ruin_runner_head.py` for connected facial relief, fitted eye
patches/lids, lips, skin detail and closed textured hair locks. These eye surfaces
are a neutral sculpt technique, not production eye/face deformation topology.
The outfit adds a draped cowl and flat overlapping cloth bindings.
`scripts/blender/ruin_runner_garments.py` replaces the initial cowl and uniform
tunic with a folded scarf, separate back cape, gathered shirt, three cut tunic
pieces and open cuffs. Cloth normals/roughness and worn edges export in the GLB.
These shapes are authored rest poses; no Blender or browser cloth solver is active.
The latest head pass uses asymmetric upper/lower lids that blend into the face,
a shallow lid crease and ten authored swept hair groups with attached split tips.
It addresses the ringed eyes and uniform fringe; natural likeness is still pending.

- Build: `npm run blender:ruin-runner` (installed Blender, isolated runner).
- Editable source: `art/source/ruin-runner-study.blend`, with individually named
  garment/anatomy/accessory parts, UVs and packed textile images.
- Export: `public/models/ruin-runner-study.glb`; dimensions/counts/provenance in
  `src/config/ruin-runner-study.json`. Metres; forward +Z after glTF export.
- Review: `npm run dev`, then `/?scene=character-study`. The local ignored
  `concept/character/ruin-runner-approved.png` is needed only for the reference
  pane. The model still loads without it. Review UI is excluded from production.
  Face mode crops the supplied portrait in the UI without editing the reference.
  Studio lights and ground shadows are confined to this review route.
- Neutral front/side/back/face Blender renders and browser comparisons are saved
  locally under `.artifacts/ruin-runner/`.

Rebuilding overwrites this study's source/export/manifest/renders. Save manual
model edits under a new source filename before rerunning the generator. It never
opens or modifies the hub source, previous explorer source or its animation clips.

Current geometry deliberately retains separate modeling parts; it needs retopology,
material consolidation, deformation-friendly topology and skinning before use as
the roaming character. Cloth panels are separate meshes, not working cloth physics.
Follow `plans/CHARACTER_REDESIGN.md` for remaining visual mismatches and motion gates.
