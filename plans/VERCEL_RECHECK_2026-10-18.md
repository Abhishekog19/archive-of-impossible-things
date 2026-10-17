# Live Vercel follow-up — October 18, 2026

Public test URL: **https://archive-of-impossible-things.vercel.app/**

The live route's sampled HUD readings meet the user's 50–55 FPS working target:
**181 readings at 54–61 FPS**, manual Medium, DPR 1.0, 1280 × 720 viewport.
The earlier 30 FPS plateau did not recur. This is positive live evidence, not a
continuous frame trace or certification of every device and view.

## Method and results

Used normal keyboard and pointer input in the public production site, with its
existing performance HUD. Walked hub → forest → canopy → archive → hall → cavern
entry, then returned to the hub spawn. The six approximately 30-second sampling
blocks plus the final arrival reading span about 241 seconds including gaps.
These read the HUD's rolling FPS; no sustained average or frame percentiles are
derived from them.

| Sample block | Readings | FPS range | Visibility confirmed |
| --- | ---: | ---: | ---: |
| Hub → forest | 30 | 54–60 | 30 |
| Forest → archive | 30 | 60 | 30 |
| Archive → hall → cavern entry | 30 | 57–60 | 21 |
| Cavern ascent → hall | 30 | 60–61 | 0 |
| Archive → forest return | 30 | 58–60 | 0 |
| Connector → hub approach | 30 | 60 | 0 |
| Final hub arrival | 1 | 60 | 0 |

No sampled reading fell below 50 FPS. DPR stayed at 1.0, Medium remained selected,
and the HUD reported no resolution shedding. Peak sampled rendering submissions
were 65. Travel completed without a recovery or captured browser error.

The browser panel visibility API returned true for the first 81 readings, then
false for the remaining 100, beginning about 99 seconds after sampling began.
FPS stayed near 60 after that change. Therefore the previous plateau's cause is
still unproven, and this is not a fully visibility-controlled four-minute test.
An additional focused cavern check was attempted after restoring visibility,
but the tab/session closed before that check could run; no result is claimed.

## Handoff and remaining limits

The October 16 delivery/build-parity, connected-route and narrow Settings checks
remain recorded in [the initial live report](VERCEL_CHECK_2026-10-16.md).
Runtime and assets are unchanged from that check. No new game build or unit-test
run is needed for this documentation-only follow-up.

Use the public URL in a normal foreground browser, start with Automatic quality,
and enable Show performance HUD in Settings. Report the device/browser, area,
FPS/DPR, selected quality and whether an issue happens only on the first visit.
The interrupted test tab retained manual Medium; select Automatic for the user
test. Cold entry-to-playable timing, a fully visible sustained live trace and
physical-phone controls/thermals remain unverified. Startup and triangle budgets
and the existing visual/character acceptance gaps are unchanged.

Ignored local evidence: `.artifacts/vercel-oct18/visible-live-hud.json`,
`summary.json`, `visible-cavern-hud.png`, `visible-hub-return-hud.png` and
`visible-hub-arrival-hud.png`. Screenshot filenames describe the intended test;
per-sample visibility flags above are the authoritative visibility evidence.

No runtime or art changes were made. The pre-existing Blender source edit was
preserved. The next routine broad review remains October 20.
