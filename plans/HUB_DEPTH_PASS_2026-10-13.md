# Hub woodland depth pass — October 13, 2026

This focused REF4 pass adds a middle woodland layer, low terrain shoulders and
branches reaching into the existing eight hub crowns. It is derived from the
established PD11 hub source by the natural-finish generator; the protected
hub-blockout source is never opened or saved.

## Changes and comparison

- Tapered forked branches emerge inside the upper trunks and reach the existing
  leaf sprays. Ground collision and the lower root silhouettes are retained.
- Six smaller trees occupy the rear and western shoulders, between the existing
  near trees and distant woodland. They use opaque vertex-coloured foliage.
- Three low, broad terrain shoulders follow the shared terrain outside the
  walking routes. Their colour uses the existing earth treatment.
- No new texture atlas, runtime light, JavaScript feature or gameplay is added.

The fixed 1280 × 720 reference view and a rear-boundary player-height view were
compared before/after and against REF4. The middle layer reduces open gaps behind
the ruins; the tower remains visible in the wide view and both route mouths stay
readable. Branches now extend into the crowns instead of ending below them.
The new shoulders are subtle under the foliage, not a complete terrain redesign.

REF4 differences remain: the plaza reads too strongly as a disc; distant crowns
and hills are still coarse, masonry and paving are repetitive, and some old
branches have visible tonal transitions into the new wood. The reference has
denser, more integrated woodland and more convincing large-scale terrain. This
pass does not establish the whole-world visual target.

## Validation and cost

All 36 existing automated tests and the production build pass. No JavaScript
implementation changed. Four hub-connection checkpoints and six arrival/overlook
checkpoints pass, with a maximum destination error of 0.31 m.

The resident package, including collision, and all six other zone packages are
byte-for-byte unchanged. Hub: 252,225 triangles / 9,113,828 bytes, an increase of
15,984 triangles / 537,488 bytes. All derived packages total 36,652,652 bytes.
These counts are asset costs; the scheduled weekly review records runtime costs.

The protected hub-blockout SHA-256 remains
`3EF1EBAAB70AA4C11D280F04CFBABE0C20D152426A155FABA79736BA5C805D8A`.
Private material is checked only through Git metadata and remains ignored and
untracked. Local ignored evidence is in `.artifacts/hub-depth-oct13/`.
