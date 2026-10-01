# PD11 acceptance — October 1, 2026

Status: **in progress; not approved for final delivery**. The functional PD09/10
work is usable on the temporary explorer. PD08 remains parked by the user.

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
