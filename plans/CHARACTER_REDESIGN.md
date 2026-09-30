# Character redesign — approved direction, September 29

The user rejected the PD08 explorer design and current locomotion. PD08 is reopened.
Image 3 (Ruin Runner turnaround) is the selected reference, locally preserved at
concept/character/ruin-runner-approved.png. The other two supplied images are
supporting costume references; do not blend their faces or bark armour into this design.
The existing explorer is a temporary implementation, not approved final character art.

September 30 user direction: park this redesign and move to PD09. Desktop movement
was implemented and checked with the existing explorer. Model approval, skinning,
final animation and reactive clothing remain open; resume these only when requested.

## Required appearance

- Match the turnaround's youthful stylized face, swept layered dark hair, expressive
  eyes, natural limb proportions and readable hands. Keep the existing metre-scale
  controller fit unless a deliberate documented adjustment is needed.
- Loose off-white tunic with modeled folds and overlapping asymmetric hems; olive
  shoulder scarf/short cape with a woven geometric border and worn edges.
- Rope waist ties and wooden token, diagonal leather strap and side satchel, loose
  brown trousers, calf/forearm wraps and worn leather boots. No bark armour or hood-up
  substitution. The back/side silhouette matters as much as the face.
- Geometry carries anatomy, garment thickness, folds, hair masses and layering.
  Textures carry cloth weave, seams, painted tonal variation, border motifs and
  wear. Do not substitute a recoloured primitive body or uniform procedural noise.

## Production order and review gates

1. Author a reference-matched neutral model; compare front, side, back and face
   close-up before spending effort on the full animation set. Fix proportions,
   face/hair and clothing silhouette first. A compiling GLB is not visual approval.
2. Finish surface detail and skinning: deformation around shoulders, elbows, hips
   and knees; separate cloth panels and secondary bones; retain editable Blender
   source, UVs, textures and asset provenance.
3. Correct locomotion on a small representative route: deliberate acceleration,
   braking, directional turns, speed-matched strides, grounded jumps and landings.
   Fix sliding feet and mismatched facing; tune camera response with the movement.
4. Add reactive secondary motion and compare in the browser. Review an idle breeze,
   start/run/stop, sharp turn, jump/land and wall approach. Clothing must settle
   naturally rather than flutter forever or pass through the torso/legs.
5. Review the complete character at normal player distance in hub/forest/cavern;
   retain detailed resource/FPS/mobile tier checks for the weekly batch and PD11.

## Clothing and accessory motion

Target the weight, lag and settling requested using Wukong/Ghost of Yōtei as feel
references, without claiming to reproduce either game's internal implementation.

- Plan a hybrid approach: authored garment shape and locomotion deformation plus
  spring-driven secondary bone chains on the cape/scarf, hem tails, rope ends,
  hair tips and satchel. Drive inertia from acceleration, turning and landings;
  use restrained wind rather than a constant sine-wave displacement.
- Use simplified body collision constraints and pinned garment roots. Clamp time
  steps and reset simulation on respawn/teleport; pause/resume must not explode it.
- Validate one cape panel and a turn/stop before expanding the system. If its fold
  quality is insufficient, assess a limited cloth solver against measured cost.
  Full garment/self-collision simulation is not assumed affordable on Iris Xe/mobile.
- Blender simulation does not itself constitute a browser physics implementation;
  runtime secondary motion must be implemented and reviewed in R3F.

## Status and scheduling

September 30 garment pass: `scripts/blender/ruin_runner_garments.py` now authors
the gathered shirt, three overlapping tunic pieces, uncapped sleeves/turned cuffs,
folded neck scarf and a separate diagonal back cape. UV textile normal/roughness
maps and edge abrasion accompany the shaped folds. Browser review exposed sleeve
root gaps and rear scalp/cape attachment errors; these were corrected. The new
hair foundation follows the skull surface to prevent the exposed rear crescent.
Satchel strap meshes now follow the shirt/scarf/cape surfaces through geometric
projection; the old fixed-depth path visibly floated in the side comparison.
This is a neutral rest-shape pass, not simulated cloth or a finished character.
Face likeness/naturalness and garment/boot/hand finish still require acceptance
before final topology, skinning and locomotion integration.

Latest user correction: the first study was rejected as low quality/cartoon-like.
Keep Image 3's identity and costume, but pursue more believable anatomy and material
response. Additional polygons or detail maps are not evidence of matching the reference.

The second study replaces the oval head/separate pin-like nose with a continuous
facial relief surface (cheeks, sockets, nose bridge/tip, chin and jaw). Added fitted
eyelids, lip surfaces, ear cartilage, restrained skin colour variation/freckles and
pore normals. Closed swept hair locks now carry directional colour/normal detail.
Replaced tube-like collar/wrap rings with a folded cowl and overlapping flat cloth
bindings. The review's Face view includes the reference portrait at close range;
studio ground shadows and fill light are review-only, not gameplay lighting changes.

Visual review still finds a likeness gap: eye/brow expression, cheek/jaw character,
natural hair grouping and believable garment drape require further art direction.
The study is not accepted, photoreal, rigged or runtime-budget compliant. Continue
the reference comparison before adding more microdetail or promoting it into gameplay.

Latest continuation removes the raised oval eye rims in favour of asymmetric
upper/lower transitions and a shallow superior-lid crease. Broader tapered brows,
a wider subtly asymmetric mouth, rounded chin and softer nose replace the previous
forms. Ten individually shaped primary hair groups and attached split tips replace
the repeated comb fringe. These changes improve specific defects, but the face
still reads as a simplified sculpt; the user's requested naturalness is not achieved.

Alternate-base tooling was checked without changing Blender setup: Blender MCP
could not reach its add-on. The installed Higgsfield CLI can list the existing
workspace after network access, but that workspace reports zero credits and none
is selected. No generation job, purchase, installation or account change was made.
The procedural study remains an editable checkpoint, not proof that a generated
or manually sculpted higher-quality base has been obtained.

September 29: neutral-model production started. `npm run blender:ruin-runner`
creates the separate editable `art/source/ruin-runner-study.blend`, UV-textured
`public/models/ruin-runner-study.glb` and four local review renders. The development
route `/?scene=character-study` compares Image 3 beside the exported GLB, with
front/side/back/face cameras and orbit controls. Reference stays in ignored concept/;
the review route is development-only and requires that local reference file.

Built shaped head/hair, hands, short linen sleeves, overlapping tunic panels,
asymmetric olive mantle, rope belt/token, side satchel/diagonal strap, gathered
trousers, wraps and boots. Browser comparison prompted tunic/leg intersection fixes,
recessed eyes, narrower upper-body proportions and lighter exported textile colours.
This is still an unapproved neutral study, not a finished replacement.

Largest remaining mismatches, in order: facial likeness and cheek/eye expression;
hair volume and natural lock grouping; convincing loose garment folds and overlapping
shoulder cloth; worn boot construction; painted material variation/seams/wear.
Flat criss-cross bindings now exist but still need an authored wear pass.
The current study retains separate modeling parts
and substantially more geometry/materials than the live explorer; merge/bake and
retopology are required before gameplay integration. Do not ship it as-is.

No skinning, new locomotion, reactive cloth or production-player replacement in
this checkpoint. Existing production character remains live until the replacement
has passed the relevant visual and deformation checks. PD09/10 expand to include
the above movement and secondary-motion work. Games and phone controls remain deferred.

The previous 1–2 active-day completion forecast is withdrawn: it assumed acceptance
of the rejected character. Re-estimate after the neutral-model and one-panel motion
proof. Continue small reviewable build increments; do not claim AAA fidelity or an
invented reference-similarity percentage.
