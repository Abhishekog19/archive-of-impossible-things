# Cavern art correction — October 10, 2026

Status: exported, compared in the browser and verified on the affected controller
routes. This focused batch is complete; whole-world visual acceptance remains open.

## Changes

- Replaced three bands of overlapping wall wedges with taller fracture faces
  whose feet begin below the shore. Their outlines follow the narrowing shell.
- Reduced medium/fine colour noise and vein contrast in the existing 1K stone
  colour tile. Normal and roughness maps retain their established treatment.
- Corrected the broad shoreline plates' top-face winding and narrowed their
  joints. The continuous walkable shore remains beneath the decorative plates.
- Regenerated the editable cavern source, GLB, resident collision and streamed
  cavern package. The changed generator sequence also changes downstream
  procedural variation; affected movement needs a fresh check.

## Completed verification

All nine placed-world tests and the production build pass. Source-to-resident
collision equality, shoreline physical support and compressed package decoding
pass. No JavaScript changed in this batch; the archive batch's passing changed-file
lint remains applicable.

All 17 shoreline checkpoints pass with no recovery and a maximum destination
error of 0.28 m. All three cavern return checkpoints pass (maximum error 0.08 m),
and the uphill jump records 1.03 m of airborne rise. The retrieved browser error
sample is empty. Routine FPS/mobile/deployment checks were not repeated.

Hub, connector, approach, canopy, exterior and hall GLBs remain byte-for-byte
unchanged. Cavern and resident packages change. All derived packages total
35,968,460 bytes, down 24,172 bytes from the archive batch.

| Derived package | Triangles | Bytes |
| --- | ---: | ---: |
| Resident scenery and collision | 229,368 | 7,788,372 |
| Cavern | 3,990 | 799,776 |

The protected pre-existing hub source edit is unchanged and excluded. Private
material is checked through Git metadata only.

## Visual comparison and remaining gaps

REF10, baseline and final reference/shore views were compared at 1280 × 720.
The new tall wall faces remove the stacked wedge bands, while the foreground
shore presents broad upward-facing surfaces. The mineral colour change is subtle;
normal relief and the existing runtime treatment still dominate the stone.

Chamber massing, the narrow light shaft, dark repetitive wall surfaces and regular
shore edges remain visibly simpler than REF10. Some older vertical joints still
terminate in conspicuous dark ledges. These remain further art work; this batch
does not establish whole-world visual acceptance. Sustained performance,
real-phone testing and deployment parity remain separate open gates.

Local evidence: `.artifacts/cavern-art-oct09/` contains the baseline captures,
final reference/shore captures, shoreline and return results/screenshots,
generation/preparation logs, package hash comparison, tests and build output.
