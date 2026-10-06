# World audit correction and verification review — October 6, 2026

The October 5–6 correction pass extends Phase 5 across all six environment areas.
The local verification pass follows it in the same authorized session. This is
not an 80% similarity score, final character acceptance or real-phone approval.

## Corrections implemented

- Hub: dressed the east path and plaza rim, reduced large flat moss patches,
  tightened the weathered column courses, folded ground-cover leaves and replaced
  flat distant crowns with layered volumes. The preceding boundary batch already
  dressed the arrival, overlook and exposed wall proxies.
- Forest/canopy: finished the full bank skins and grounded rock masses, sampled
  the actual bank surface for roots, extended woodland layers, separated trees
  from retained ruins, and reduced/folded leaves. A curated opening now frames the
  archive. Bark fissures and stone pores from the connector study apply to the
  other outdoor/hall stone and wood meshes at close distance.
- Archive: rebuilt connected tapered roots, capped their ends and recalculated
  normals before union. Added matching simplified root collision and removed
  replaced source colliders. Courtyard paving widens gradually over irregular
  soil. Smaller stone bevels, folded ivy and unobstructed facade framing improve
  the inspected front view. Rear hall windows have nearby woodland context.
- Portal: hall and descent are required from the forest's first archive sightline
  (camera Z -37 through -144), including cold entry. Enclosed-surface fog now
  preserves dark passage depth when seen from outdoors.
- Cavern: replaced pointed repeated wall protrusions with broader fractures,
  authored an irregular shore with matching upward collision, and shared its
  contour with the water/wet-stone shaders. Water extends beneath the bank.
  Reduced normal-map strength and adjusted cave fill/fog make surfaces clearer.
  Trial roof brows were removed after comparison exposed bright outline bands.
- Export pipeline: complete temporary GLBs replace their destinations; identical
  derived files are retained to avoid unnecessary OneDrive replacement failures.

## Audit disposition

These are observations from the saved views, not exhaustive off-route coverage.

| Audit IDs | Result in this pass |
|---|---|
| H01/H02 | Named hub proxies and reverse arrival are replaced; preceding boundary evidence remains applicable. |
| H03/H04/H06 | Rim, moss size and course gaps improved. Plaza still has a strong disc silhouette; close masonry remains softer and more regular than REF4. |
| H05/F04/F05/C02 | Layered crowns, folded leaves, bank dressing and background depth implemented. Coarse crown cores, some large plants and broad bank planes remain reference-quality gaps. |
| F01/E05 | Bank ends and full visible skins replaced, with grounded outcrops and attached roots. Side-bank composition still needs further art refinement. |
| F02/F03/X02 | Covered skins removed, source root unions retained and close stone/bark detail propagated. Some paving joints and baked root/branch shading remain conspicuous. |
| C01 | Tree placement now clears the retained ruin footprints; side-view comparison and connected route pass. |
| C03 | Existing canopy shafts/lighting retained; folded canopy and framing opening improve the composition. REF6 lighting/foliage acceptance remains open. |
| E01/E02/E03 | Attached roots, tapered courtyard transition and sharper masonry implemented. Root/facade hierarchy still differs from REF7. |
| E04/E06 | Obstructing foreground leaves removed from the inspected facade view; cold forest/canopy portal views show the hall/descent. |
| I01/I02/I03 | Earlier seam/core fixes retained; column drums have tighter joints and sharper edges. Main arch remains connected. Texture softness and repeated masonry remain visible. |
| I04 | Folded ivy and rear-window trees added; nearby foliage replaces part of the blank window field. Full exterior context remains simpler than REF8. |
| I05/V01 | Passage reads as an open, dark descent; embedded floor/wall joins retained. The long axial corridor and distant lit shore remain composition differences. |
| V02/V03/V04 | Broader fractures, irregular physical shore, shared wet edge and quieter normals implemented. Rock masses and near-shore plate detail remain simpler than REF10. |
| V05/V06 | Existing bounded reflection pass retained; water contact, cave fog and fill revised. Reference light distribution and rock/reflection detail are not fully matched. |
| X01 | Contact shading verified in all six areas and through jump/landing. |
| X03 | Separate character art acceptance remains open; no character or gameplay scope was added. |

## Local validation

- All 36 automated tests pass. These include compressed package decoding,
  source-to-resident collision equality, cold portal loading, GPU resource
  disposal and the new 64-angle shore-support/empty-pool regression check.
- Changed JavaScript lint and the production build pass.
- Actual ecctrl/Rapier connected route: 19/19 destinations plus recovery pass;
  maximum destination error 0.32 m.
- Complete shore circuit: start plus 16 sectors pass; maximum error 0.32 m.
- Return to hub: 12/12 destinations pass, maximum error 0.25 m.
- Cavern return and uphill jump pass (0.99 m rise). Six-area contact shading,
  jump fade and landing restoration pass.
- Weekly live traversal: 180.01 seconds, 85 waypoints, zero hidden frames,
  38.96 average FPS on Medium at 1280 × 720 / DPR 1.25. The 175 approximately
  one-second samples range from 25.17–49.23 FPS; seven are below 30 FPS.
  This is a development-server measurement on this desktop, not proof of the
  60 FPS target or a production/real-phone hardware benchmark.
- Sampled render counts range from 31–290 calls and 150,663–759,253 triangles.
  Geometry counts range from 227–409 and textures from 52–68. Counts fall as
  areas unload; comparable later geometry peaks rise slightly (407 to 409),
  so this short run does not establish long-term resource stability. One sample
  records an area loading state; traversal continues through it.
- Production preview loads the hub; Settings fits at 390 × 844, Low quality
  switches successfully and returning to Medium works. This narrow desktop
  viewport check does not exercise physical touch controls. The retrieved
  browser error sample is empty. The final UI-copy correction was linted and
  rebuilt; production chunk hashes stayed unchanged.
- Final derived package size: 34,915,760 bytes. Resident: 206,371 triangles /
  6,830,244 bytes. Hub: 234,317 / 8,508,720. Canopy: 100,127 / 3,403,196.
  Hall: 141,529 / 6,219,968. Cavern: 4,350 / 821,160. These are asset counts,
  not simultaneous rendered counts. Background crowns use 47,628 triangles.
- Existing hub source edit retains SHA-256
  `3EF1EBAAB70AA4C11D280F04CFBABE0C20D152426A155FABA79736BA5C805D8A`.
  It is excluded from commits. Private source material remains ignored/untracked;
  its contents were never read.

Evidence is local and ignored under `.artifacts/phase5-completion-oct05/`:
six reference comparisons, side/window/portal captures, route transcripts and
generation/package/test/lint/build logs. Earlier boundary evidence is under
`.artifacts/phase5-boundaries-oct05/`. The performance capture interrupted by an
approval-service usage limit is excluded; its result was not retrieved.

## Remaining acceptance gates

Whole-world reference quality remains open for the explicit differences above.
The 60 FPS target also remains open; prioritize the forest portal loading region
and return-view render counts in the next optimization batch.
Real-phone input/thermal behavior and Vercel-versus-Sites performance parity
require separate evidence. No accessible deployment URL was available in the
current repository plans; local results do not resolve the earlier deployment
performance report. No Archive gameplay was implemented.
