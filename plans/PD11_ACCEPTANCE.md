# PD11 acceptance — October 2, 2026

Status: **in progress; not approved for final delivery**. The latest completion
request resumed character work. The fitted Ruin Runner now replaces the old
explorer, and its focused movement/presentation checks pass. Remaining visual gaps
and the scheduled technical gate are explicit below; no invented match score.

## October 2 production and integration

- Denser clustered planting and embedded stones around the hub, woodland,
  archive exterior and hall; a second iteration rounds and darkens the new leaves.
  Additional middle canopy layers frame the approach. Decorative foliage keeps
  existing paths and collision proxies separate.
- Exterior roots have asymmetrical ridges; shared close-range directional bark
  detail supplements the baked atlases without another texture allocation.
- Cavern ridges now follow the narrowing shell, with non-coplanar faces buried
  into the wall instead of detached rectangular plates. Added discontinuous pool
  ledges and reduced ambient/fog washout. Regenerated collision is included in
  the resident package; source-versus-resident identity check passes.
- Separate editable pd11-*.blend files preserve original area sources. Export
  replacement handles Windows cloud-file rename failures. Seven streamed visual
  packages plus resident data total 26,913,064 bytes; this is transfer size, not
  GPU memory or a hardware performance claim.
- Character: refined facial relief/lids/irises/brows/mouth, darker hair and deeper
  tunic folds; separate runtime mesh reduced from 189,480 to 70,949 triangles,
  19 materials, 25 bones and six clips. Semantic weights pin garment attachments.
  Fitted secondary-bone lengths and body limits support cape, scarf, hems, hair,
  rope and satchel. This uses spring bones, not AAA cloth simulation.
- A browser failure at sharp turns exposed excessive leg reach. Steps now shorten
  along the ground when the previous planted target is outside the leg arc.
  Retest: idle/slope grounding, stride/turn contact (88/100 samples planted),
  jump/landing, accessory settling and recovery pass. Camera visibility, pause,
  walk/run/idle transitions and wall clearance pass on the replacement.
- 28 focused tests pass, covering actual replacement weights/deformation, existing
  motion/input/camera logic, entry routing and streamed resource/collision checks.
  Changed-JavaScript lint and production build pass. No incidental FPS audit.
- Six final reference views are saved locally as `.artifacts/pd11/REF*-final.png`;
  motion/camera results are `runner-motion.txt` and `runner-camera.txt` there.
- Final changed-route check passes cavern ascent, archive return, repositioning on
  the ascent and an uphill jump (1.16 m rise) with the replacement character and
  regenerated resident collision. Evidence: `runner-cavern-return.txt` there.

## Remaining acceptance work

The production pass is usable but does not close the requested visual-quality gap.
The neutral character comparison still shows simplified facial anatomy and garment
folds/wear compared with Image 3. The world still has flat canopy masses, simplified
terrain/background silhouettes and repetitive high-contrast masonry. These are
artwork corrections, not merely a request for user sign-off. The cavern wall change
removes the detached-tile appearance, but broad rock forms and light still differ
from REF10. Preserve these gaps until corrected; do not mark PD11 fully complete.

Weekly hardware/resource/deployment/mobile-layout review remains October 3.
Real-phone controls/thermals remain user-led at the end. The subsequent October 2
user request adds PD12 for a focused hub visual correction pass. PD11's overall
acceptance gaps remain open; games and phone controls are deferred.

The October 1 review below is historical and its parked-character/unchanged-
collision statements are superseded by this update.

## Release entry pass

- Plain `/` now opens the assembled, streamed six-area environment. `?patch=1`
  remains compatible; `?patch=0` and explicit study scenes preserve older views.
- Performance HUD starts hidden; Settings or H opens it, and `?hud=1` requests
  it on entry. Removed the collapsed debug button from the normal player view.
- Initial scene suspension has a loading message. Asset/render exceptions have
  an outer error boundary with a reload action; unsupported WebGL has useful
  fallback text. Network-failure injection and context-loss recovery have not
  been browser-tested in this pass.
- Settings retains the existing quality controls, pause/resume and scrollable
  small-screen layout. Removed the unused interaction instruction; gameplay and
  phone-control redesign remain outside this milestone's current work.
- Routing tests, changed-JS lint and production build pass. The browser plain-URL
  view opens the assembled hub; Settings opens and returns to the scene.

## Six-reference review

Fresh fixed-camera screenshots use the existing reference poses and are saved
locally in `.artifacts/pd11/REF4.png` through `REF8.png`, plus `REF10.png`.
`default-entry.png` records the player view. These are comparison evidence, not
visual approval. No similarity percentage is inferred.

| Area | Visible acceptance gap |
|---|---|
| REF4 hub | Sparse shoulders, faceted terrain/banks and flat connector surfaces; plaza is much barer and less organically framed than the concept. |
| REF5 forest | Bark is soft/blotchy; repeated trunks and flat leaf clusters reduce the layered woodland effect. |
| REF6 canopy | Opening toward the archive is too exposed; canopy depth and directional sunlight are weaker than the reference. |
| REF7 exterior | Root shapes are smooth tubes and masonry is very regular; the facade lacks the reference's integrated tree/ruin silhouette. |
| REF8 interior | Repetitive masonry, overly strong edge shading and limited warm-light/cool-shadow separation. |
| REF10 cavern | Regular shoreline arc, flat attached wall plates and uniform stone treatment; light shaft exists but the chamber needs stronger depth/value separation. |

Address the largest shared problems in this order, comparing screenshots after
each production pass: (1) hub shoulders/connecting terrain; (2) forest silhouette,
bark and canopy layering; (3) archive roots/masonry breakup; (4) cavern wall and
shore silhouettes; (5) coherent lighting/material values. This is environment
finishing work still required for acceptance, not optional post-release polish.

## Gate evidence and outstanding work

- Reuse PD09's complete six-area/four-reservation keyboard route, stairs, slopes,
  cavern return and recovery evidence. Collision assets did not change here.
- A focused browser check through the new plain entry passes cavern ascent,
  archive return, repositioning on the ascent and an uphill jump (1.07 m rise).
  Evidence: `.artifacts/pd11/return-results.txt`. No full-world replay or FPS run.
- Reuse PD10's 14 passing focused tests and browser foot/camera/clothing results.
  These establish temporary-rig behavior, not final character appearance.
- Character: PD08 art approval, replacement-rig fitting and its movement/clothing
  comparison remain outstanding. Do not approve the temporary character by proxy.
- Weekly hardware/resource/deployment/mobile-layout review remains October 3;
  do not substitute incidental screenshot FPS counters for that review. Real-phone
  controls/thermals remain user-led at the end.
- Final release needs the environment corrections above, character acceptance,
  and remaining technical gate evidence. Git pushes are not proof of hosted build
  parity or final release approval.
