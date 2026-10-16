# Live Vercel verification — October 16, 2026

Public test URL: **https://archive-of-impossible-things.vercel.app/**

The public production alias works without login. GitHub reports successful Vercel
deployment of `8c83cb045285cdce764974a5488d4f72ccafcdb2`, including the cavern resource
cleanup. Its immutable deployment URL redirects to Vercel login; use the public
alias above for user testing. No deployment-protection setting was changed.

## Delivery and build parity: pass

- HTML, six entry JavaScript/CSS resources, all eight resident/area GLBs, the
  streamed-world and cavern-light chunks, and the stone texture respond HTTP 200.
- Downloaded entry JavaScript/CSS and all eight GLBs match local SHA-256 hashes.
  HTML is equivalent after whitespace normalization; the Linux build omits an
  extra blank line present in the local output. Asset references match.
- Sampled responses report Vercel cache HIT. JavaScript/CSS, HTML and models are
  served with Brotli where reported; GLB MIME type is `model/gltf-binary`.
- In the sequential command-line probe, HTML headers arrived in 367 ms; other
  measured headers arrived in 68–98 ms. Complete decoded model responses took
  217–2,228 ms. A repeated resident request succeeded in 1,552 ms. These are
  connection-specific cached CDN requests, not browser cold-start timings,
  transferred compressed byte counts or a loading-screen benchmark.
- The existing 18,871,164-byte startup GLB inventory is unchanged and still
  exceeds the 8 MB goal. Fast CDN responses do not remove client preparation cost.

## Live functional check: pass within tested scope

Used the actual public production build and normal keyboard/pointer input, with
its existing Settings → Show performance HUD control. Walked from the hub through
forest, canopy, archive, hall and cavern descent, then returned to the hub. The
controller stayed on the route, streamed areas appeared, camera turning worked,
and Settings paused/resumed play. This was a manual live route, not a rerun of the
61 automated local checkpoints.

Low/Medium selection and the Settings dialog work at desktop width and 390 × 844.
The console contains no captured errors. Existing Three.Clock and Rapier
initialization deprecation warnings remain. Physical phone touch/thermal testing
is still pending.

## Live FPS: observations recorded; sustained acceptance inconclusive

The intended comparison viewport was 1280 × 720, verified from the canvas DOM.
The initial automatic preset selected Medium at DPR 1.0. Hub HUD readings were
about 60 FPS. A forest entry snapshot dropped to 8 FPS; automatic adaptation later
selected Low at DPR 0.75.

| Sample block | Captured HUD readings |
| --- | --- |
| Canopy → archive, automatic Low | 20 samples, 59–62 FPS |
| Hall → cavern, automatic Low | 25 samples, 56–61 FPS |
| Cavern → hall, manual Medium | 25 samples, 30 FPS |
| Stationary hall, manual Medium | 10 samples, 30 FPS |
| Returned hub, manual Low | 10 samples, 29–30 FPS |

These are approximately one-second reads of the existing HUD's rolling FPS, not
frame-by-frame captures. Do not average them into a claimed sustained FPS result
or derive p95/p99 from them.

During investigation of the 30 FPS plateau, the browser panel visibility API
reported false, including immediately after requests to show it. The page's DOM
visibility still reported visible. Later Low and Medium readings were both near
30 FPS. Browser presentation/throttling is therefore an unresolved confound;
neither a hardware rendering failure nor a visibility cause is proven. The first
browser session also disappeared before reliable evidence was saved.

The user was asked to keep the Codex browser panel visible for a controlled
follow-up. Until that condition can be maintained, **do not certify sustained
50–55 FPS on Vercel** or replace these results with the earlier local 58.64 FPS.
The CDN, asset parity and live travel checks above are independently verified.

## User test and evidence

Open the public URL in a normal foreground browser. In Settings, use Automatic
first and enable Show performance HUD. Check the first forest transition, cavern
entry, return route and a repeat visit. Useful feedback includes device/browser,
quality preset, area, FPS/DPR shown, whether the issue occurs only on the first
visit, and any screenshot of a visual problem.

Local ignored evidence: `.artifacts/vercel-oct16/deployment-http.json`,
`live-hud.json`, `canopy-live-hud.png`, `cavern-live-hud.png`,
`return-hub-live.png`, and `live-narrow-settings.png`.

No runtime or art changes were made in this check. The existing uncommitted
hub-blockout Blender source remains untouched.
