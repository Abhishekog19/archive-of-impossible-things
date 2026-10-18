# Character direction — Forest Archivist × Ruin Runner

Latest user decision: the concept design is accepted; character implementation is
deferred while game ideation and environment integration take priority. Preserve
the current runtime model and locomotion until the user resumes character work.

The user's October 18 brief supersedes the earlier Ruin Runner-only costume
restriction. Keep and improve the current explorer; do not replace the avatar
with a literal likeness of Abhishek or a traditional fantasy hero.

## Identity and appearance

A young, curious explorer: slightly mysterious, adventurous, playful and
resourceful. The character represents curiosity, creativity, adaptability and
willingness to explore unfamiliar things. Discovery and experimentation take
priority over fighting.

- Slim, athletic build with readable natural proportions.
- Slightly messy dark hair; youthful, attentive expression.
- Short moss-green hooded cloak. Production assumption: hood down during normal
  play, exposing the hair and face; the folded hood must read clearly from behind.
- Weathered beige tunic, brown trousers, wrapped forearms and practical boots.
- Small leather satchel and restrained wooden accessories.
- Stylized 3D, earthy colors and a readable silhouette. Journey, RiME and Sable
  are mood/style references, not characters or assets to copy.
- No futuristic elements, heavy armor or weapons. Ordinary explorer in an
  extraordinary world; avoid heroic armor shapes and constant combat-ready poses.

## Motion direction

Agile, smooth and responsive, with expression carried by pose rather than input
delay. Retain the physical controller while reviewing its presentation and tuning.

| Moment | Animation target | Check |
| --- | --- | --- |
| Idle / discovery | Small weight shifts and attentive head turns; occasional restrained curiosity gesture | Loops settle without twitching or perpetual garment flutter |
| Start / stop | Clear transfer of weight and short braking recovery | Movement begins promptly; feet do not continue walking after stopping |
| Walk / run | Relaxed exploration walk, energetic compact run, readable arm swing | Stride length/cadence follows actual distance travelled |
| Direction change | Torso and hips lead a planted turn; cloak and satchel follow | No whole-body snap or foot skating during 90/180-degree turns |
| Jump / land | Leg compression, readable ascent/fall, brief weighted landing | Capsule contact and pose agree; no landing animation that traps input |
| Interact | Reach, inspect, experiment, then release naturally | Clear contact target and reliable return to locomotion |

Keep the cape above mid-thigh and clear of the legs. Use a small number of
secondary bones with restrained lag and settling; preserve existing collision
fit, performance tiers and pause/respawn behavior. A cinematic camera must return
control cleanly and remain skippable; it must not compensate for weak locomotion.

## First concept and review

Generated with the built-in image tool using the previous approved turnaround as
a continuity reference. Local concept:
`concept/character/forest-archivist-runner-concept-v1.png` (ignored reference asset).
The original `ruin-runner-approved.png` is preserved.

The concept shows front, side, back and three-quarter views with the requested
earthy costume, slim build, exposed messy hair, folded hood and practical gear.
It is an illustration, not a GLB, orthographic modeling guarantee or final user
approval. The front is slightly turned and the expression is still quite youthful;
confirm proportions in the neutral model rather than copying perspective distortion.
Simplify painted wear into readable material groups for the real-time asset.

Next implementation: compare the current neutral model against this direction,
revise silhouette/hood/hair first, then validate one walk–turn–stop sequence before
expanding appearance detail and the remaining animation clips. Preserve the
existing rig where practical; do not claim improved motion until tested in-browser.

## Exact generation prompt

Use case: stylized-concept. Create one production character turnaround concept sheet for an original young adult explorer, combining Forest Archivist and Ruin Runner, for Archive of Impossible Things. The attached image is a reference for continuity of the existing explorer's youthful face, messy dark hair, slim natural proportions and earthy materials; it is not an edit target and its layout/text should not be copied. Follow this updated design: slim athletic ordinary young explorer, slightly mysterious yet curious and playful expression, short moss-green HOODED cloak with hood resting DOWN visibly folded behind neck, weathered beige tunic, brown trousers, wrapped forearms, practical worn leather boots, small leather satchel, restrained wooden toggle/token accessory. Adventure and problem solving, no combat. Style: polished stylized 3D game character concept, readable sculpted forms, broad material/color shapes and restrained texture detail; contemplative atmosphere inspired by Journey, RiME and Sable while remaining an original character. Avoid anime exaggeration, photorealistic skin and excessive costume microdetail. Composition: wide landscape neutral warm gray studio sheet, four clear full-body views of EXACTLY THE SAME character at matched height and proportions: front, left side, back, three-quarter. Every view has complete feet and hair within frame, no overlaps, no props in hands. Relaxed neutral stance, arms slightly away from body so cloak, wraps, waist and satchel can be modeled. Same hood-down short cloak in all views, hem above mid-thigh so legs remain readable. Plain background, soft diffuse light and subtle grounding shadows, earthy subdued moss/linen/leather palette. Text only small labels FRONT, SIDE, BACK, THREE-QUARTER. No weapons, armor, machinery, neon, futuristic elements, ornate fantasy hero motifs, logos, scenery or invented biographical symbols. This is a concept for review, not a finished model.
