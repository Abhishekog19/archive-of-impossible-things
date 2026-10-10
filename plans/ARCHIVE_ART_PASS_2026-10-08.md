# Archive art correction — October 8–9, 2026

This batch follows the forest/canopy pass. It targets the facade/root hierarchy,
courtyard paving and hall masonry/framing against REF7 and REF8. Whole-world
visual acceptance remains open.

## Changes

- Added recessed masonry inside the upper facade arch so the carved seal is
  attached to stone instead of silhouetted against open sky.
- Brought the main hero trunk in front of the left facade and joined its lower
  roots there. Replaced blunt canopy limbs with tapering curves and replaced
  the large crown lobes with smaller leafy groups. Root collision is regenerated
  from the fused source; the post-bake root displacement is removed.
- Replaced the inherited stone treatment with restrained mineral colour and
  short-range contact shading. Bark uses continuous positional colour variation.
  The existing three 2K atlases per archive area are rebaked, with no added atlas.
- Staggered courtyard and hall paving rows. Added wall bearings below surviving
  hall roof fragments, connecting them to the continuous wall core.
- Added a targeted controller route through the root-side apron, courtyard,
  entrance, hall reserved location, rear arch, descent threshold and return.

## Verification

Before/final facade, courtyard and hall captures at 1280 × 720 were compared
with REF7/REF8. The final trunk is visibly continuous in front of the facade,
the seal has a stone backing, and the entrance remains open. Before captures,
export iterations and final evidence are stored locally in the ignored
`.artifacts/archive-art-oct08/` directory.

The production build, changed-JavaScript lint and all nine placed-world tests
pass. Source-to-resident collision equality passes after regenerating the hero
tree/root collider. Hub, connector, forest approach, canopy and cavern packages
are byte-for-byte unchanged. No new texture atlas or runtime lighting pass is
added. All ten controller checkpoints pass, including the root-side apron,
hall reserved location, descent threshold and return; maximum destination error
is 0.29 m with no recovery triggered. The retrieved browser error sample is empty.

| Derived package | Triangles | Bytes |
| --- | ---: | ---: |
| Resident scenery and collision | 229,728 | 7,791,160 |
| Archive exterior | 82,292 | 3,591,976 |
| Archive hall | 144,154 | 6,238,096 |

All derived packages total 35,992,632 bytes, up 60,752 bytes from the forest
batch. These are asset counts, not an FPS measurement.

The first exterior preview confirmed the attached seal and tapered canopy
limbs. It also exposed the trunk being too deeply embedded in the facade and
broad contact shading across the stone faces; both prompted a further revision.

The pre-existing `hub-blockout.blend` edit is excluded. Private material is
checked only through Git metadata and is never read.

## Remaining art work

The masonry still looks softer and more repetitive than REF7/REF8. The facade
needs stronger damage/depth hierarchy, finer root-to-stone transitions and more
natural crown silhouettes. Hall window context, roof fragmentation and the long
axial descent remain simpler than the reference. Lighting and material work
must be judged in further comparisons; this batch does not close visual
acceptance or the existing performance/real-phone/deployment gates.

The next focused batch targets grounded cavern wall fractures, shore joins and
material noise against REF10.
