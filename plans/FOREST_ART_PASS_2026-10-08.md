# Forest and canopy art correction — October 7–8, 2026

This batch follows the hub art pass and addresses F01, F04/F05, C02 and the
forest portion of E05. It is a focused production batch, not whole-world visual
acceptance. Reference targets are REF5 and REF6.

## Changes

- Reduced approach/canopy plant instance scales and rebaked their existing
  three 2K atlases per area so ground shadows agree with the smaller plants.
- Added relief to the continuous bank skins, lightened their stone colour and
  replaced tall narrow outcrops with broader, lower masses. Collision is retained.
- Added low woodland layers above the banks and a five-lobe distant crown
  profile. Existing default crown generation is preserved for other areas.
- Replaced bank root chords that disappeared inside the rock with small folded
  leaves sampled directly onto its surface. The intermediate spherical hanging
  foliage was rejected in the close browser comparison.
- Added a close bank review camera and an eight-checkpoint forest/canopy
  controller route, including the reserved clearing and the return journey.
- Fixed Blender's temporary export directory after an image-conversion write
  failure. The approach bake/source had saved successfully and was reused;
  subsequent canopy bake and both finished exports succeeded.

## Comparison and verification

The October 7 browser review was interrupted by an automatic approval usage
limit. Browser access resumed on October 8. Matching 1280 × 720 REF5/REF6 views
confirm smaller ground plants, broader bank rocks and additional woodland
layers while preserving the archive sightline. Close bank iterations replaced
disconnected root stubs and spherical foliage with surface-fitted leaves;
the final foliage spacing and angles are irregular rather than aligned rows.

All eight forest/canopy controller checkpoints pass, including the reserved
clearing, archive approach and return. The maximum destination error is 0.30 m,
with no recovery triggered. The only subsequent edit varies decorative creeper
leaf spacing/angles. The retrieved browser error sample is empty. This is a
bounded route check, not exhaustive collision or performance acceptance.

The final production build, nine placed-world tests and changed-JavaScript lint
pass. Final resident collision retains all 24,275 world-space triangles and its
baseline SHA-256 fingerprint. Hub, connector, exterior, hall and cavern packages
are byte-for-byte unchanged. No new atlas, realtime shadow or transparency is
introduced.

| Derived package | Triangles | Bytes |
| --- | ---: | ---: |
| Resident scenery and collision | 230,127 | 7,793,140 |
| Forest approach | 113,113 | 3,606,612 |
| Canopy | 100,127 | 3,396,412 |

All eight derived packages total 35,931,880 bytes, up 948,500 bytes. The resident
package grows by 23,756 triangles and 962,896 bytes; smaller rebaked area textures
offset 14,396 bytes. This increases shared scenery cost and must be assessed in
the next scheduled weekly performance review. No new FPS claim is made.

Local ignored evidence is in `.artifacts/forest-art-oct07/`: before/after forest,
canopy and bank-detail captures, rejected studies, generator/prepare logs and
the collision fingerprint baseline. The original protected hub source edit is
preserved; private material is checked only through Git metadata.

## Remaining reference differences

The banks still read as broad faceted surfaces, with less natural layering than
REF5/REF6. Overhead foliage is too open and some crowns remain coarse. Bark and
masonry shading are soft, paving joints remain conspicuous, and lighting lacks
the references' enclosed forest depth. No similarity score or completed visual
acceptance is claimed. Archive and cavern art differences remain subsequent
focused batches. Weekly FPS, deployment parity and real-phone checks are not
replaced by this daily affected-area review.
