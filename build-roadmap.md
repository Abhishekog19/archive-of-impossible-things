# Build Roadmap — Archive of Impossible Things

Companion to [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md) (what the game is),
[game-flow.md](game-flow.md) (what the player does) and [look-target.md](look-target.md) (what it looks like).

**This document is the schedule.** Milestones, deliverables, exit criteria, hours,
dates. It is the one file to open when the question is *what am I doing today*.

**Status:** written 2026-08-25, the day the visual direction was locked against the
reference set. M0 is complete. M1 starts next session. The locked target is
[visual-reference-sheet.jpg](visual-reference-sheet.jpg); full-resolution originals
live in the gitignored `concept/` folder on the authoring machine only.

---

## 1. The honest headline

| | |
|---|---|
| Total estimate | **605 – 880 hrs**, midpoint **~740** |
| Baseline pace | **12 hrs/week** |
| Duration at baseline | **~62 weeks ≈ 14 months** |
| Target v1 date | **November 2027** (Jan 2028 with realistic slippage) |
| Scope | 3 archives + hub + Deep Archive + portfolio reveal |

**This is up from the 450–550 hrs in the original feasibility plan, and the reason
is the reference art.** That plan costed a grey blockout with stylized dressing.
The direction now locked is a specific, high-quality look with heavy environmental
dressing. That is the right call — the look is the portfolio — but it is roughly
+40% of art hours and pretending otherwise would just move the disappointment later.

Three things make 14 months survivable, and they're all structural:

1. **Three public releases before v1** (§4). Something real ships at month 3.
2. **Every milestone ends in something visible.** No milestone is pure plumbing.
3. **The scope levers in §8 are pre-decided**, so cutting later is a choice, not a crisis.

---

## 2. Time budget — daily hours

Baseline **12 hrs/week**. Distributed for the *kind* of work, not evenly:

| Day | Block | Hours | Work type |
|---|---|---|---|
| **Tuesday** | evening | 2 | Code — React, store, UI, game logic |
| **Thursday** | evening | 2 | Code |
| **Saturday** | morning | 4 | Art — Blender, bake, export, compare |
| **Sunday** | morning | 4 | Art / integration |
| | | **12** | |

**Why not 2 hrs every day.** Blender and 3D iteration have a high context-reload
cost: open the file, re-run the script, bake, export, reload the browser, compare
to reference, decide, repeat. One loop is 30–60 minutes. A 2-hour block gets you
two loops and no thinking time. A 4-hour block gets you six and a conclusion.

Code is different — it's interruptible, you're already fluent in React, and 2-hour
blocks are genuinely productive there. So: **short slots for code, long blocks for art.**

**The rule that matters more than the schedule:** the weekend blocks are the ones
that must not slip. Missing a Tuesday costs 2 hours. Missing a Saturday costs a
bake-compare cycle, which is where actual progress lives.

---

## 3. Schedule at a glance

At 12 hrs/week, mid estimate:

| | Milestone | Hrs | Cumulative | Done by |
|---|---|---|---|---|
| M0 | Scaffold | — | — | ✅ **complete** |
| M1 | It moves | 30 | 30 | **11 Sep 2026** |
| M2 | It runs on your phone | 18 | 48 | 21 Sep 2026 |
| M3 | It looks like the reference | 50 | 98 | 20 Oct 2026 |
| M4 | The first 40 seconds 🚀 | 35 | 132 | **10 Nov 2026** |
| M5 | The road 🚀 | 62 | 195 | **16 Dec 2026** |
| M6 | Things respond | 30 | 225 | 3 Jan 2027 |
| M7 | The Archive stands | 85 | 310 | 21 Feb 2027 |
| M8 | It remembers you | 35 | 345 | 14 Mar 2027 |
| M9 | Five toys, three survive | 50 | 395 | 12 Apr 2027 |
| M10 | One archive, end to end 🚀 | 90 | 485 | **3 Jun 2027** |
| M11 | Three archives | 125 | 610 | 15 Aug 2027 |
| M12 | The reveal | 60 | 670 | 19 Sep 2027 |
| M13 | Ship | 72 | 742 | **1 Nov 2027** |

🚀 = public release.

---

## 4. The three public releases

Not arbitrary. Each is the earliest point at which something is genuinely worth
showing a stranger, and each doubles as a portfolio artifact while the rest is built.

| Release | After | When | What a stranger gets | Why it's worth shipping |
|---|---|---|---|---|
| **R1 — "the opening"** | M4 | ~Nov 2026 | 40 seconds: fade in, walk, the channel fills with water behind you, fade out | Proves the art pipeline and the core idea in one link. This is the single highest ratio of impression to hours in the whole project. |
| **R2 — "the walk"** | M5 | ~Dec 2026 | 4 minutes: the opening, then the canopy road | Answers the riskiest question in the design — *is walking enough?* — with real players instead of opinion. |
| **R3 — "one archive"** | M10 | ~Jun 2027 | ~30 minutes: opening, hub, road, a complete archive with all six beats | A real vertical slice. From here the project is demonstrably a game and not a demo. |

R1 and R2 are also insurance. If the project stalls at any point after M5, what
exists is still a beautiful, finished, three-minute thing with your name on it —
not an unplayable branch.

---

## 5. Milestones in detail

Each has **deliverables** (what exists afterwards) and **exit criteria** (how you
know it's done, stated so it can fail).

---

### M1 · It moves — 25–35 hrs · by 11 Sep 2026

Grey room, character, camera, movement. No art. The locked next step in the design doc.

**Deliverables**
- `ecctrl` character with the camera from `look-target.md §2`: pivot 1.40 m, 4.0 m back, 0.8 m up, −11°, FOV 50, 0.12 damping
- Grey test room: flat ground, slopes to 8%, stairs, a 30 m straight, one 4.5 m-wide road strip
- Camera collision that pulls in and never clips
- One interactable object as a smoke test
- Dev HUD: FPS, draw calls, triangles

**Exit criteria**
- Walk the 30 m strip. Camera never clips geometry, never shows sky above where a canopy line would be.
- Slopes and stairs traverse without the controller fighting the ground at ±0.25 m noise
- **The real test:** walk with no objective for 90 seconds. Do you want to keep walking? If no, spend up to 10 more hours on movement feel before M2. This gate exists because `game-flow.md §4` bets three minutes of the player's time on it.

**Risk** — the movement-feel gate is subjective and can eat unbounded time. Cap it at +10 hrs, then move on and revisit at M5 with real scenery.

---

### M2 · It runs on your phone — 15–20 hrs · by 21 Sep 2026

Cheap now, painful to retrofit.

**Deliverables**
- `ecctrl/input` touch joystick + buttons, both input paths live simultaneously
- Three-tier system (High/Medium/Low) per `look-target.md §9`, auto-detected via `WEBGL_debug_renderer_info` + an FPS probe, with a manual override in settings
- `PerformanceMonitor` / `AdaptiveDpr` for continuous degradation
- Landscape prompt, safe-area insets, `touch-action: none`
- Deployed to a login-free URL

**Exit criteria**
- Played on your actual phone over the deployed URL, not an emulator
- Holds 30 fps for 3 continuous minutes on the phone — **this is the thermal test**, and a 30-second benchmark does not substitute for it
- Tier override survives a reload

---

### M3 · It looks like the reference — 40–60 hrs · by 20 Oct 2026

**The highest-value de-risking step in the project.** Everything visual depends on
whether this works. The target is the stone-chamber image on
[visual-reference-sheet.jpg](visual-reference-sheet.jpg), chosen because it is the
cheapest image in the reference set *and* it is minute 0:00 of the game.

**Deliverables**
- Blender installed; `bpy` scripting conventions written into `art-pipeline.md`
- A scripted modular stone kit: walls, floor slabs, niches, a carved channel, a doorway
- Cycles lightmap bake → `TEXCOORD_1` export → `uv1` in three.js
- `gltf-transform` pipeline: Meshopt + KTX2 (ETC1S colour, UASTC data)
- The chamber loaded in R3F with `MeshBasicMaterial` + `lightMap`, zero runtime lights
- A side-by-side comparison shot: your render next to the stone-chamber reference

**Exit criteria**
- Side by side, it is recognisably the same place — same palette, same shadow shapes, same light direction
- ≤ 3 MB, < 100 draw calls, < 300 K triangles
- 60 fps on Iris Xe at DPR 1.25, 30 fps on the phone
- Every sampled pixel is inside the `look-target.md §3` palette
- Desaturate the screenshot: every silhouette still reads

**Risk — this is the milestone most likely to fail outright.** The `uv1` /
`TEXCOORD_1` export is the classic afternoon-eating bug. Budget for it explicitly.
If baking proves unworkable after 60 hrs, the fallback is vertex-baked AO plus a
flat gradient — visibly worse, but it ships.

---

### M4 · The first 40 seconds 🚀 — 30–40 hrs · by 10 Nov 2026

`game-flow.md` minute 0:00 to 0:40, playable, in final art. **Release 1.**

**Deliverables**
- Black screen, water sound, fade in on a playable frame — no cutscene, no title card, no prompt
- The chamber from M3, dressed
- **The water channel that fills as you walk**: runs ahead of you, stops when you stop, wet stone stays wet, hits a broken section at ~15 m and spills into moss
- Audio unlock on the click that starts the game (`game-flow.md §9` open question #3)
- Deployed, shared

**Exit criteria**
- A person who has never seen the project walks forward without being told to
- They notice the water. Nobody explains it to them.
- No text appears anywhere in the 40 seconds
- Works on a phone, cold-loaded, over mobile data, in under 8 MB

**Why this is the release to ship first** — it is the entire thesis of the game in
40 seconds: something impossible, in natural material, that you caused and did not
earn, with no text. If that doesn't land, better to learn it in month 3 than month 12.

---

### M5 · The road 🚀 — 50–75 hrs · by 16 Dec 2026

The canopy road. **The riskiest content in the game** and **the second-biggest
technical unknown after M3.** Release 2.

**Deliverables**
- Foliage system: instanced alpha-tested cross-cards, wind sway in a vertex shader
- Trunk scatter to `look-target.md §6`: ±3.5 m, 6–9 m randomised spacing, never regular
- Canopy at 6.5 m underside, 2 layers (3 on High)
- `FogExp2` at 0.038, colour `#cfd3c4` exactly matching sky
- Dappled canopy light as a scrolling texture — **the unproven effect** (`look-target.md §11` item 2)
- Additive-plane light shafts
- Road curvature: never more than ~30 m of straight visible
- Footstep audio that changes with surface

**Exit criteria**
- **Walk the road with no objective. Do you want to keep walking?** Asked of at least three people who aren't you, with no explanation given.
- ~6 tree pairs visible; no visible fog/sky seam at any tier
- Frame-time ratio DPR 1.0 vs 1.5 is well under 2× (over 2× means overdraw-bound)
- 30 fps floor on the phone for a full 3-minute traversal
- Camera never clips a leaf card

**Risk** — if the answer to the walking question is *no*, the two-layer design in
the design doc §8 is wrong and the flow needs rework before M7. That is a
significant redesign, and finding out here rather than at M10 is the entire reason
this milestone sits before the hub.

---

### M6 · Things respond — 25–35 hrs · by 3 Jan 2027

Generic interaction framework. Reused by every archive; built once.

**Deliverables**
- `enter / start / complete / fail / reset / exit` lifecycle per design doc §11
- Primitives: pressable, pullable, pickup, passage, inspectable, surface-that-responds
- All mobile-safe — no precision touch, no twitch input, no key chords
- A grey room exercising all six

**Exit criteria**
- An archive can be added or deleted without touching any other file
- Every primitive works identically on touch and keyboard
- `reset` returns to exact initial state, 20 times in a row, no drift

---

### M7 · The Archive stands — 70–100 hrs · by 21 Feb 2027

The Central Archive hub, in final art. **The biggest single art milestone**, and the
one where the reference set's dressing density gets paid for.

**Deliverables**
- Hub geometry: reclaimed stone, standing structures, a tree through a collapsed roof, water channels
- Three exits: one walkable, two impassable by growth and by a gap — *not locked*, no doors, no keys
- Curator traces: a tool set down mid-task, a step worn smooth then nothing, something sorted then abandoned half-sorted
- One unreachable hero structure, visible from most of the hub
- Title card on the reveal — the first text in the game
- Skip-to-portfolio element, shown once then collapsed to an icon
- **Two dressing states from one geometry** (design doc §12 weathering set)

**Exit criteria**
- The 0:40 reveal makes someone stop walking
- Nobody asks which way to go, and nobody is told
- Both dressing states load from identical geometry with no new models
- Budgets hold at Medium tier
- A player who was not paying attention still finds state 2 slightly more open

**Risk — this is where the schedule is most likely to overrun**, because the cost is
dressing volume rather than any single hard problem. If it exceeds 100 hrs, shrink
the hub footprint rather than reducing dressing quality. Density is what makes the
reference art work; area is negotiable.

---

### M8 · It remembers you — 30–40 hrs · by 14 Mar 2027

**Deliverables**
- Scene streaming, one environment resident, real `dispose()` of geometry, materials *and* textures
- Diegetic loading — no spinner
- localStorage save/progression
- Settings: tier override, audio, controls, reduced motion

**Exit criteria**
- Enter and exit environments 20 times: flat `renderer.info.memory`, no GPU-memory growth in DevTools
- The mobile-Safari tab-kill test: 15 minutes of continuous play, no reload
- Save survives a browser restart and a version bump

---

### M9 · Five toys, three survive — 40–60 hrs · by 12 Apr 2027

Candidate mechanics as throwaway grey-room toys. **Hours each, not levels.**
Design doc Law #3: fun first, meaning second.

**Deliverables**
- 5 candidate mechanics, grey rooms, no art, no story
- Each judged mobile-safe and producible in scripted Blender
- The two-pool collision: fun-first mechanics × recurring motifs — only natural pairings survive
- 3 chosen and written up; 2 discarded with a written reason

**Exit criteria**
- Each toy played by someone who is not you, with **no explanation given**
- They work out what to do without being told
- Three are actually fun as toys, before any meaning is attached
- Nothing was kept because it was symbolically neat

---

### M10 · One archive, end to end 🚀 — 70–110 hrs · by 3 Jun 2027

Archive 1, complete, all six beats. **Release 3 — the vertical slice.**

**Deliverables**
- All six beats from `game-flow.md §5`: Exterior, Teach, Escalate, Twist, Stopping point, Payoff
- The stopping point authored as the climax — the place the Curator quit the moment their question was answered
- One portable capability that changes the hub afterwards
- Final art, audio, the full 8:00→30:00 stretch playable

**Exit criteria**
- A player reaches the payoff without hints
- The twist lands as a new *consequence* of a known rule, not a new mechanic
- Once the rule is understood, the game stops asking for it to be performed (Law 10)
- No text explains the mechanic at any point
- 30 minutes of continuous phone play without a thermal collapse

---

### M11 · Three archives — 100–150 hrs · by 15 Aug 2027

Archives 2 and 3. Faster per archive than M10 because the tooling, kit and
framework all exist.

**Deliverables**
- Archive 2 (35:00–55:00): a different rule; needs archive 1's capability *in a new combination*, never re-performed unchanged
- Archive 3 (58:00–75:00): shorter, denser, assumes fluency; needs both prior capabilities at once
- Hub states 2 and 3; the hero structure becomes reachable at 75:00

**Exit criteria**
- No archive re-performs an earlier one unchanged (design doc §8)
- Difficulty curve verified by someone playing all three cold, in order
- Each hub state loads from the same geometry

---

### M12 · The reveal — 50–70 hrs · by 19 Sep 2027

**Deliverables**
- Deep Archive (78:00–90:00): bare rock, still water, deliberately less decorative than anything before it. The cold-cavern reference image is the target — the second-cheapest image in the reference set.
- The reveal: things the player already touched decoded back to something real
- Portfolio mode: standalone, works with WebGL force-failed
- The skip-to-portfolio path from 1:10 lands somewhere finished

**Exit criteria**
- The reveal recontextualises things the player *actually touched* — nothing invented for the ending
- Portfolio mode is genuinely usable by a recruiter with four minutes and no interest in the game
- WebGL disabled → portfolio serves immediately, no error screen
- Someone who skipped at 1:10 and someone who played 95 minutes both get a coherent ending

---

### M13 · Ship — 60–85 hrs · by 1 Nov 2027

**Deliverables**
- Full audio pass: ambience, footsteps by surface, water, interaction, music
- Perf pass across all three tiers on real devices
- Playtest round with fresh players, end to end, then fixes
- Accessibility: reduced motion, remappable controls, subtitles where any audio carries meaning
- README, licences and attributions for every CC0 asset
- Release

**Exit criteria**
- Three people finish it without help
- 30 fps floor on the weakest target device, whole game
- Every third-party asset correctly attributed
- Cold load to playable ≤ 8 MB

---

## 6. What is deliberately not in this plan

Same discipline as the design doc: absence is a decision.

- **Archives 4–9.** Post-v1 additions. The §11 architecture makes an archive an addition, not a rewrite.
- **Which mechanics the three archives use.** Decided at M9 from playable toys, per Law #3.
- **The personal layer's specific mappings.** Emerges from the motif work; mapped backwards at M12 from what the player already touched.
- **Multiplayer, achievements, localisation, analytics.** Not v1.

---

## 7. Pace scaling

Pick a row. Everything else in this document rescales from it.

| Pace | Daily shape | Weeks | Duration | v1 date | +15% slip |
|---|---|---|---|---|---|
| 10 hrs/wk | 2+2 weekday, 3+3 weekend | 74 | 17.1 mo | Jan 2028 | Apr 2028 |
| **12 hrs/wk** ← baseline | **2+2 weekday, 4+4 weekend** | **62** | **14.2 mo** | **Nov 2027** | **Jan 2028** |
| 15 hrs/wk | 2+2+2 weekday, 4½+4½ weekend | 50 | 11.4 mo | Aug 2027 | Sep 2027 |
| 20 hrs/wk | 3×2 weekday, 7+7 weekend | 37 | 8.5 mo | May 2027 | Jun 2027 |

**20 hrs/week is not recommended as a standing pace** alongside other commitments —
sustained 20-hour weeks on a side project for eight months is where side projects
die. 12 is chosen to be *boring and survivable*. Sprinting into M3 and M5 (the two
unknowns) and coasting through M6 and M8 (the two most routine) is a better use of
extra energy than raising the baseline.

---

## 8. If it needs to be shorter

Pre-decided, so cutting later is a choice rather than a panic. In the order I'd cut:

| Lever | Saves | Cost |
|---|---|---|
| **2 archives instead of 3** | ~60 hrs | Least damage by far. Design doc §8 compounding still works with two. |
| **Fold the Deep Archive into archive 3's ending** | ~35 hrs | Loses a distinct space; keeps the reveal intact. |
| **Smaller hub footprint** (same dressing density) | ~30 hrs | Nearly invisible. Density is what reads, not area. |
| **Cut hub state 3** | ~20 hrs | Two increments instead of three. |
| **Drop High tier** — ship Medium and Low only | ~15 hrs | Desktop users lose bloom and a canopy layer. |

Cutting all five: ~160 hrs → **~580 hrs, ~48 weeks, v1 by Aug 2027.**

**Not on the list, ever:** the opening 40 seconds, the road, dressing density, the
palette discipline, or the phone target. Those are the project.

---

## 9. Rules for editing this plan

1. **Log actual hours per milestone.** The estimates are guesses; after M3 you'll have a personal multiplier worth more than anything here.
2. **Re-estimate at every release**, not continuously. R1, R2, R3 are the three points where the schedule gets honestly redrawn.
3. **A milestone is done when its exit criteria pass** — not when it feels done, and not when the hours run out.
4. **Overruns cut scope, never quality bars.** §8 exists for this.
5. **If a milestone overruns by more than 50%, stop and write down why** before continuing. Twice on the same cause means the plan is wrong, not the execution.

---

## 10. Right now

| | |
|---|---|
| **Current milestone** | M1 — It moves |
| **Next session** | `ecctrl` + the `look-target.md §2` camera in a grey room |
| **First gate** | Walk 90 seconds with no objective. Do you want to keep walking? |
| **Open sign-offs** | Design doc §19: delete §7's status text; 75–95 min v1 duration |
| **Locked 2026-08-25** | Visual direction, against [visual-reference-sheet.jpg](visual-reference-sheet.jpg) |
