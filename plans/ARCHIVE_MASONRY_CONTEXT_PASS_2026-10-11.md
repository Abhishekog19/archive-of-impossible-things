# Archive masonry and hall context — October 11–12, 2026

This batch follows the cavern form/light refinement. It targets the remaining
REF7/REF8 masonry, roof and window-context differences from the October 8–9 review.
The focused corrections are implemented; whole-world visual acceptance remains open.

## Implementation

- Shared stone finishing now preserves planar faces, clips selected corners and
  applies narrow edge bevels. It replaces independent jitter of bevel vertices.
- Archive limestone uses a quieter, lighter mineral range and shorter contact
  shading distance in its existing diffuse atlases.
- Facade courses are larger, with staggered joints and selected upper setbacks.
  The established openings, trunk and connected root paths are retained.
- Hall roof remnants have cut-back polygonal inner edges and supported crests,
  retaining their connection to the wall bearings.
- Ruined masonry and low woodland beyond both rear lancets provide nearby depth.
  These sit outside the hall boundaries and clear of the descent corridor.
- The first window preview showed no visible masonry. Raising the outer courses
  alone did not resolve it: the oblique camera looked past their narrow span at
  seven metres behind the wall. They were moved to four metres behind the wall
  for another export and comparison, retaining the open descent corridor.

## Verification

Final facade, hall and close-window captures at 1280 × 720 were compared with
REF7/REF8 and their baselines. The final close-window view contains the broken
ruin courses; the main hall view retains sky around the distant fragments.
The close view is more enclosed than the reference, so landscape depth remains
an art gap. All ten archive/hall controller checkpoints pass: root-side apron,
courtyard threshold, doorway, hall aisle, reserved location, aisle return, rear
arch, descent threshold, hall return and courtyard return. Maximum destination
error is 0.32 m. The retrieved browser error sample is empty.

All nine placed-world tests and the final production build pass. This includes
source-to-resident collision equality and decoding every compressed package.
The resident package and the hub, connector, approach, canopy and cavern packages
are byte-for-byte unchanged. The existing three 2K atlases per archive area are
rebaked; no additional atlas or lighting pass is introduced.

| Derived package | Triangles | Bytes |
| --- | ---: | ---: |
| Resident scenery and collision | 229,159 | 7,786,460 |
| Archive exterior | 80,535 | 3,610,648 |
| Archive hall | 151,905 | 6,377,996 |

All derived packages total 36,115,164 bytes, up 158,572 bytes from the previous
batch. Exterior triangles decrease by 1,757; hall triangles increase by 7,751.
These are asset costs, not a new performance measurement. Changing the seeded
stone finishing also redistributes some incidental rubble and planting.

No JavaScript implementation changed. Routine weekly performance
checks remain due October 13; no real-phone or deployment acceptance is implied.
The pre-existing hub source edit is excluded, and private source material is
checked only through Git metadata.

Local ignored evidence: `.artifacts/archive-finish-oct11/`.

## Reference comparison and remaining work

The facade comparison with REF7 and the previous export shows larger, staggered
courses with flatter faces and varied upper setbacks. Its silhouette still has
more regular block divisions than the reference, and the trunk/root transitions
and coarse background crowns need further composition work.

Against REF8, the hall has cut-back roof edges and wall-side crest fragments.
Broad baked shading still makes several stone courses look soft, and the course
pattern remains repetitive. The window backdrop and long axial descent remain
simpler than the reference's layered landscape. These focused corrections do not
establish overall visual acceptance or an invented similarity percentage.

Next focused art work returns to REF4 hub composition: woodland depth, broad
terrain forms and trunk/branch silhouettes. The protected hub blockout source
must remain untouched; use the existing production generators for that work.
