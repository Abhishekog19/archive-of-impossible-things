# Cavern form and light refinement — October 11, 2026

This focused batch follows the October 10 cavern pass and addresses its remaining
detached joint endings, regular shore projections and narrow light distribution.
Reference target: REF10. Whole-world visual acceptance remains open.

## Changes

- Replaced constant-radius wall strips with rising ridge sections that follow the
  shell's narrowing radius and offset. Intermediate heights now rise monotonically;
  the former short strips could fold downwards. Side edges and tapered heads are
  buried in the shell, and feet begin below the shore.
- Applied the same construction to the broad fracture faces. The initial preview
  was too repetitive, so the final generator uses 14 narrow and 19 broad candidates
  with varied placement, width, height and depth, excluding the passage opening.
- Varied shoreline ledge spacing, width and reach. Angled underside facets replace
  the equal-depth rectangular edges. The continuous physical shore remains.
- Widened and softened the existing skylight volume, broadened the spotlight and
  moved the existing fill light deeper into the chamber. Adjusted enclosed haze
  and ambient intensity. No new light, shadow map, atlas or render pass is added.
- Reduced runtime normal-map strength from 0.6 to 0.22 to keep small surface relief
  subordinate to the larger rock forms under the revised light.

## Comparison

Matching 1280 × 720 baseline/final reference views and the final near-shore view
were inspected alongside REF10. The inspected wall faces now connect down to the
shore without the old hanging shelf endings. Broader light makes the rear cliff
and its water reflection more legible. The first dense-ridge study was rejected
because it replaced one repetitive pattern with another.

The final cave still has a rounded dome silhouette, conspicuous angular ridge
intersections, mottled stone and regularly segmented shore plates. REF10 has more
asymmetric rock masses, quieter broad surfaces and richer near-shore fractures.
These differences remain open; no similarity score or final visual acceptance
is claimed.

## Verification

Changed-JavaScript lint, all nine placed-world tests and the production build pass.
The tests include source-to-resident collision equality, physical shore support
and compressed package decoding. All 17 shoreline checkpoints pass, with maximum
destination error 0.30 m and no recovery. All three return checkpoints pass
(maximum error 0.31 m), and the uphill jump records 0.99 m of airborne rise.
The retrieved browser error sample is empty.

Hub, connector, approach, canopy, exterior and hall packages remain byte-for-byte
unchanged. Cavern and resident packages change with the regenerated source.

| Derived package | Triangles | Bytes |
| --- | ---: | ---: |
| Resident scenery and collision | 229,159 | 7,786,460 |
| Cavern | 3,768 | 789,820 |

All derived packages total 35,956,592 bytes, down 11,868 bytes from October 10.
These are asset counts, not measured frame-rate improvements. Broad technical
checks were not repeated: the last completed weekly traversal was October 6,
and the next seven-day review is due October 13. Real-phone and deployment parity
checks remain open.

Local ignored evidence is under `.artifacts/cavern-finish-oct11/`: baseline,
intermediate and final views; shoreline/return transcripts and screenshots;
generator/export logs; package hashes; lint, tests and build output.
The pre-existing hub source edit retains its recorded hash and
is excluded. Private source material was checked through Git metadata only.

The next focused art batch should return to archive masonry/damage hierarchy and
hall window/roof context, using the October 8–9 review's remaining differences.
