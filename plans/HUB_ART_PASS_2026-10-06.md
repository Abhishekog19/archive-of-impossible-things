# Hub art correction — October 6, 2026

The first art batch after the final local audit concentrates on H03, H05 and
H06 against REF4. It improves these items without closing whole-hub acceptance.

## Changes

- Replaced the eight hub trees' large crown cores with smaller overlapping
  branch sprays, varied heights and folded leaves. Kept opaque geometry.
- Removed selected outer flagstones to interrupt the circular edge. Added
  exposed soil and small planted pockets while preserving the arrival, forest
  and east route mouths and the interior paving joints.
- Tightened seven columns' course alignment, shaped their fractured tops and
  replaced their diffuse bake with clearer flat-face limestone and contact.
- Kept the editable work in `pd12-hub-art.blend`, derived from the unchanged
  PD11 source. The generator reproduces the geometry, bake and GLB export.

## Comparison and verification

Compared REF4 with matching 1280 × 720 hub reference and player-height views.
The accepted view has smaller crown masses and a broken planted paving edge.
The early flat-tier crown and paving-warp trials were rejected. New exposed
soil replaces the old dark baked footprints under removed paving.

All 10 hub/arrival/overlook controller checkpoints pass; maximum destination
error is 0.27 m. The final change after those checks only adjusts decorative
soil colour and low planting. All nine placed-world tests and the final
production build pass. No JavaScript implementation changed. The retrieved
browser error sample is empty.

The resident package, including collision, and all six other zone packages are
byte-for-byte unchanged. Final hub package: 236,241 triangles / 8,576,340 bytes,
up 1,924 triangles and 67,620 bytes from the previous batch. The existing 1K
column atlas is replaced; no additional atlas is introduced. These are asset
counts, not a new FPS measurement. Weekly performance results remain applicable
only to the earlier measured snapshot; no new performance claim is made here.

Evidence is local and ignored in `.artifacts/hub-art-oct06/`: before/after
reference and player views, intermediate trials, route transcripts, package
hash comparisons and generator/prepare/test/build logs.

## Remaining art work

The hub still differs from REF4 in background woodland density, trunk/branch
silhouettes, broad terrain forms, paving/material definition and masonry
variation. The retained corner masonry is outside this bake's scope. The
larger forest/canopy banks, vegetation and depth remain the next art batch,
followed by the archive and cavern differences in the final audit review.

The pre-existing hub-blockout source edit remains untouched and uncommitted.
Private source material was checked through Git metadata only and never read.
