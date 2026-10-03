# Whole-world visual and roaming audit — October 3, 2026

**Result: the connected routes work, but visual acceptance remains open.** The
world still has visible blockout surfaces, disconnected-looking joins, soft
materials and inconsistent vegetation. This needs coordinated geometry,
material and lighting corrections, not only more small props.

## Scope and evidence

- Audited local desktop development preview at `http://127.0.0.1:5173/`, based on
  commit `60004a8`, at 1280 × 720. This is not a Vercel/Sites parity test.
- Compared all six reference views against REF4/5/6/7/8/10, inspected player-height
  views and turned toward route sides and reverse-facing connections.
- Used development review controls to drive the actual ecctrl/Rapier scene along
  the connected route, four reserved game locations, complete cavern shoreline,
  and return to the hub. These are fixed-step controller tests, not FPS samples
  or proof of the subjective quality of every animation.
- Saved 21 screenshots and route transcripts in
  [the evidence folder](../.artifacts/world-audit-oct03/). These local, ignored
  artifacts are not guaranteed to exist on another checkout.
- Two temporary review routes were added for this audit and then removed by
  restoring the original file byte-for-byte. No production code or art changes
  remain from this audit. The pre-existing modified `hub-blockout.blend` was untouched.
- Private-file safety checked through Git metadata only: ignored and untracked;
  its contents were not read.

This covers the connected playable route and representative surrounding views;
it is not an exhaustive test of every off-path collision face, inaccessible
background surface, device, graphics setting or camera angle.

## Movement results

| Check | Result | Evidence |
|---|---|---|
| Hub → forest → canopy → archive → hall → cavern, including four game locations | 19/19 waypoints passed; maximum recorded destination error 0.31 m | `traversal.txt` |
| Full cavern shore circuit, radius 21 m around X/Z (-12, -195) | 16/16 sectors passed; maximum error 0.30 m | `complete-shoreline.txt` |
| Cavern → hall → forest → hub arrival | 12/12 waypoints passed; maximum error 0.31 m | `return-to-hub.txt` |
| Cavern uphill return and slope jump | Return passed; jump recorded 1.1 m and airborne state | `cavern-return.txt` |
| Forced fall recovery | Passed; returned to cavern spawn | `traversal.txt` |

No route blocker was reproduced on these checks. A visual gap is not automatically
a collider hole. Captured browser logs contained development messages and
deprecation warnings for THREE.Clock and initialization parameters, with no
error-level entry in the retrieved sample. Hardware FPS, sustained memory,
mobile controls and deployment parity were not audited here.

## Location-by-location issue register

P1 = conspicuous unfinished geometry or visual continuity defect to fix first.
P2 = substantial art-quality mismatch. P3 = local polish. Priority reflects this
visual audit, not a claim of a crash or traversal failure. Coordinates are X/Z;
reproduction URLs are relative to the local preview above.

### Hub and arrival — REF4

Reproduce with `?patch=1&view=reference` or `?patch=1&start=hub`, then turn around.

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| H01 | P1 | Plain khaki block shapes remain visible around the hub perimeter and forest connection. | Replace visible blockout faces with finished ruin forms or intentionally conceal them from all playable approaches. | 18-hub-player.png, 09-hub-forest-connector.png |
| H02 | P1 | Reverse arrival view exposes a plain rectangular ramp ending against a broad faceted bank and empty pale backdrop. | Author the arrival boundary, ground transition and skyline as a complete reverse-facing scene. | 19-hub-arrival-reverse.png |
| H03 | P2 | Plaza reads as a separate paved disc; hard rim and sparse transition planting weaken its connection to surrounding ground. | Integrate the rim with terraces, soil, stones and planting while retaining usable exits. | 01-hub-reference.png |
| H04 | P2 | Close paving is pale and soft; sharp flat green shapes read as stickers rather than moss growing through stone. | Establish consistent stone scale, edge wear, roughness and irregular moss blending. | 18-hub-player.png |
| H05 | P2 | Crown clumps repeat; background trunks are bare poles beneath broad flat leaf masses. | Improve branch taper, crown variation and background silhouette depth. | 01-hub-reference.png, 18-hub-player.png |
| H06 | P2 | Column courses and creeping leaves remain visibly repetitive despite the recent pass; forms have rounded, padded surfaces. | Refine fracture language and material response on a representative column before propagating. | 18-hub-player.png |

### Hub connector and forest — REF5

Reproduce with `?patch=1&start=patch` near (-12, -20) and
`?patch=1&start=forest` near (-12, -43); rotate sideways.

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| F01 | P1 | Route-side banks have abrupt rectangular ends and near-vertical plain green faces. | Reshape exposed banks and blend them into roots, rock and soil. | 08-forest-side.png, 09-hub-forest-connector.png |
| F02 | P2 | Connector paving has thin overlapping-looking edge layers and dark triangular slits. | Inspect slab intersections, thickness and supporting ground; close unintended visible gaps. | 09-hub-forest-connector.png, 07-forest-player.png |
| F03 | P2 | Bark appears blurry/mottled with weak directional structure; root flanges have dark triangular seams. | Correct texture scale and trunk/root transitions; inspect seam geometry before hiding it with foliage. | 02-forest-reference.png, 08-forest-side.png |
| F04 | P2 | Ferns and shrubs read as large flat polygon cutouts; ground alternates between flat green and dark patches. | Improve plant silhouettes and placement, add ground-material variation and contact. | 07-forest-player.png, 17-return-forest.png |
| F05 | P2 | Looking across the route exposes sparse trunks directly against pale fog, reducing woodland depth. | Add deliberate background layers and better crown enclosure before adjusting fog. | 08-forest-side.png |

### Deep canopy — REF6

Reproduce with `?patch=1&start=canopy` near (-12, -67), and `view=canopy`.

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| C01 | P1 | A straight tree trunk visibly intersects a stone remnant in the side view without a convincing growth/breakage relationship. | Reposition or author a deliberate root-and-ruin junction. | 11-canopy-side.png |
| C02 | P2 | Another large plain bank and exposed pale side background break the enclosed corridor composition. | Complete side terrain and canopy coverage from gameplay angles. | 11-canopy-side.png |
| C03 | P2 | Lighting lacks the reference's layered shade and directed shafts; paving and repeated low walls dominate. | Improve canopy openings, light direction and atmospheric depth after geometry is coherent. | 03-canopy-reference.png, 10-canopy-player.png |

### Archive exterior and courtyard — REF7

Reproduce with `?patch=1&start=exterior` near (-12, -98), rotate sideways,
and compare `view=exterior`.

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| E01 | P1 | Roots resemble separate smooth hoses with abrupt tips and dark cut-like intersections; some appear detached from the tree/building. | Rebuild key root silhouettes and connected junctions, with believable taper and stone displacement. | 04-exterior-reference.png, 12-exterior-player.png |
| E02 | P1 | A hard rectangular boundary separates dark forest paving from pale courtyard paving. | Blend geometry, material scale, soil and wear across the transition. | 14-exterior-side.png |
| E03 | P2 | Facade is shallow and regular, with soft bevel blocks, dark repeated mortar and little hierarchy of damage. | Improve major stone forms and relief before adding fine marks. | 04-exterior-reference.png, 12-exterior-player.png |
| E04 | P2 | Large foreground leaf polygons obstruct the hero-building reference composition. | Reframe or reposition foreground plants while retaining natural layering. | 04-exterior-reference.png |
| E05 | P2 | Side courtyard exposes a near-vertical green bank and loosely placed blocks with little soil/rubble integration. | Finish side terrain and embed ruins in the ground. | 14-exterior-side.png |
| E06 | P1 | Looking through the archive shows a bright blank opening from outside, while the hall view reveals a grey tunnel surface. Visual continuity is poor. | Inspect portal sightlines and zone visibility together. Streaming/culling is a possible cause, not confirmed by this audit. | 12-exterior-player.png, 13-hall-player.png |

### Archive hall — REF8

Reproduce with `?patch=1&start=interior` near (-12, -116), look sideways,
and compare `view=interior`.

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| I01 | P1 | Bright slit at the base of an entrance-side pillar/wall exposes a conspicuous seam; smaller light seams occur between masonry courses. | Inspect and seal unintended geometry joins without changing clearances. Physical collision failure was not observed. | 15-hall-side.png |
| I02 | P1 | Overhead arch stones are visibly separated by daylight gaps, giving a floating/unsupported construction impression. | Make the main arch structurally legible; reserve broken gaps for intentionally supported ruins. | 05-hall-reference.png |
| I03 | P2 | Columns resemble stacked padded segments; masonry shares soft mottled texture and repetitive deep seams. | Improve column profiles, joint scale and stone material definition. | 05-hall-reference.png, 15-hall-side.png |
| I04 | P2 | Windows reveal a mostly blank pale exterior; vines repeat as thin strips and planting intersects plinths. | Add exterior context and curate vegetation attachment/scale. | 05-hall-reference.png, 15-hall-side.png |
| I05 | P1 | Rear entrance reads as a grey barrier from the hall, with a small bright triangular seam at its base, though the route is traversable. | Shape and light the descent entrance so its depth and walkable opening are obvious. | 05-hall-reference.png, 13-hall-player.png |

### Descent and cavern — REF10

Reproduce with `?patch=1&start=cavern` near (-12, -174), turn around for the
descent, and compare `view=cavern`. Shore circuit centred at (-12, -195).

| ID | Priority | Observation | Correction direction | Screenshot |
|---|---|---|---|---|
| V01 | P1 | Descent is a long straight-sided corridor with abrupt floor/wall joins and stretched-looking surface detail. | Author the rock transition, entrance silhouette and local material scale. | 21-cavern-tunnel-reverse.png |
| V02 | P2 | Cavern walls use repeated triangular/wedge-like protrusions against a uniform chamber; some faces appear inserted rather than part of a rock mass. | Establish larger stratified rock formations and connected fractures before small detail. | 06-cavern-reference.png, 16-cavern-shore-walk.png |
| V03 | P2 | Shore resembles a regular constructed kerb around a circular pool; angular plates and black edges break natural rock-to-water contact. | Vary shore silhouette and depth, embed plates and add controlled wetness at contact. | 20-cavern-player.png |
| V04 | P2 | Walls, floor and shore share soft noisy shading with insufficient surface distinction; thin slab seams stand out at player height. | Separate material scale/roughness for cliff, path and wet shore; resolve slab intersections. | 16-cavern-shore-walk.png, 20-cavern-player.png |
| V05 | P2 | Reflections exist but appear smeared; water edge lacks the reference's subtle depth and wet transition. | Tune reflection clarity, colour/depth and shoreline contact as one material study. | 06-cavern-reference.png, 20-cavern-player.png |
| V06 | P2 | Broad grey-blue illumination flattens chamber depth; skylight is weaker as a focal feature than REF10. | Rebalance ambient fill, directed light and fog with the reference camera and player view. | 06-cavern-reference.png |

### Cross-world observations

- **X01 / P2 — Grounding:** character and props often lack convincing contact
  shading, which creates a floating impression even where movement tests pass.
  Do not confuse this observation with proven controller suspension or clipping.
- **X02 / P2 — Material consistency:** blurred stone/bark, large flat moss patches
  and inconsistent surface scale recur across several zones. Fix representative
  materials and their UV density first; blindly raising texture resolution alone
  will not repair geometry, blending or lighting.
- **X03 / P2 — Character acceptance remains separate:** the reverse hub view still
  shows a simplified face/outfit compared with the selected Ruin Runner reference.
  This audit does not close PD08 character art or certify cloth/animation quality.

## Recommended next production order

1. **Visible structure and connections:** H01/H02, F01, C01, E01/E02/E06,
   I01/I02/I05 and V01. Remove exposed blockouts, finish reverse views and seal
   unintended seams. Keep collision routes that already work.
2. **One convincing stone/bark/ground material study:** close gameplay distance,
   coherent texture scale, irregular moss, correct edge wear and contact.
   Validate before applying across every zone.
3. **Natural terrain, roots and vegetation:** connected root forms, banks,
   planted ruin bases, dimensional foliage and layered background silhouettes.
4. **Lighting and water:** establish reference-specific contrast and depth,
   improve contact, then tune cavern reflections and shore wetness.
5. **Focused comparison and acceptance:** recheck the largest 3–5 mismatches
   per iteration. Tiny decals/accessories come after the above. Keep broad
   hardware/performance/deployment verification in the weekly batch.

The 31 area-specific observations plus three cross-world items are an audit
register, not 34 independent production tasks: many share the same asset or
material correction. No completion date or similarity percentage is inferred
from the passing movement results.
