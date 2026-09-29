# Archive explorer — PD08

Status: rejected character prototype. The user selected the Image 3 Ruin Runner
turnaround on September 29. See plans/CHARACTER_REDESIGN.md; the model below is
retained for continuity until the replacement is ready, not an approved design.

Original character model, rig and six animations authored in this repository by
scripts/blender/explorer.py. No external models, motion capture, textures or rigs
were used; no third-party attribution or license grant is implied.

- Editable source: art/source/explorer.blend. Runtime: public/models/explorer.glb.
- Regenerate: npm run blender:explorer. Validate: npm run verify:explorer.
- Height 1.70 m, feet at origin, glTF +Z forward; one material, one skinned mesh,
  4,644 triangles, 17 bones, 537,556 bytes. No image textures or root translation.
- Sage coat, ochre scarf, linen insert, brown leather satchel/boots and warm skin;
  matte vertex colours keep the silhouette readable without texture downloads.
- Clips: Idle, Walk, Run, Jump, Fall, Land. In-place animation only; ecctrl owns
  the body position, heading and collision. Ground-ray grace prevents animation
  flicker at small paving gaps; run selection has speed hysteresis.
- Runtime placement compensates for the existing floating capsule. Physics and
  camera dimensions are unchanged; initial body yaw faces down the route.
- Local development supports motionPreview=Idle/Walk/Run/Jump/Fall/Land query
  values for art review. Production always uses the live movement state.

PD08 supplies the character and transitions. PD09 tunes locomotion; PD10 owns
foot planting, stride/sliding corrections, joint/camera clipping and final animation
polish. The environment references contain no character: judge this design by
palette, scale, readable clothing and fit with the world, not a fictitious reference
match. Browser evidence is in .artifacts/pd08-*.jpg (local, ignored).
