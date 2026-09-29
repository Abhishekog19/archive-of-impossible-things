# Ruin Runner neutral study

PD08 work in progress, based on the user's selected Image 3 turnaround. This is
not an accepted final character and does not replace `explorer.glb` in gameplay.

- Build: `npm run blender:ruin-runner` (installed Blender, isolated runner).
- Editable source: `art/source/ruin-runner-study.blend`, with individually named
  garment/anatomy/accessory parts, UVs and packed textile images.
- Export: `public/models/ruin-runner-study.glb`; dimensions/counts/provenance in
  `src/config/ruin-runner-study.json`. Metres; forward +Z after glTF export.
- Review: `npm run dev`, then `/?scene=character-study`. The local ignored
  `concept/character/ruin-runner-approved.png` is needed only for the reference
  pane. The model still loads without it. Review UI is excluded from production.
- Neutral front/side/back/face Blender renders and browser comparisons are saved
  locally under `.artifacts/ruin-runner/`.

Rebuilding overwrites this study's source/export/manifest/renders. Save manual
model edits under a new source filename before rerunning the generator. It never
opens or modifies the hub source, previous explorer source or its animation clips.

Current geometry deliberately retains separate modeling parts; it needs retopology,
material consolidation, deformation-friendly topology and skinning before use as
the roaming character. Cloth panels are separate meshes, not working cloth physics.
Follow `plans/CHARACTER_REDESIGN.md` for remaining visual mismatches and motion gates.
