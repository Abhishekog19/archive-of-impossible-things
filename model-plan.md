# Model plan

Which model builds which part of this project, and why.

Companion to [build-roadmap.md](build-roadmap.md) (what gets built, when) and
[working-rules.md](working-rules.md) (how to run a session cheaply). This file
answers one question: **for the thing I am about to build, which model, on which
platform?**

---

## 0. Right now

> **M2 · It runs on your phone** — implementation built on 2026-09-05.
> Touch controls, settings persistence, mobile layout and the existing quality
> governor are connected. User will run the actual-phone checks at the end;
> see [verification.md](verification.md) § M2. Prior M1 stair/camera audit failures
> are documented there and reproduced on the previous commit.
>
> **Next: M3 · It looks like the reference.** Start with one test cube through
> the bake/export/load pipeline, then build the stone chamber kit. No M3 art
> or game-content expansion was included in M2.

This section is the one I keep current. If it disagrees with the table below, this
section is right — the table is the plan, this is the state.

---

## 1. The two platforms are not interchangeable

You run **Opus 5 in the Claude Code app** and **Opus 4.6 / Sonnet 4.6 in
Antigravity**. That is not a model choice, it is a *context* choice, and it is the
single most important fact in this file:

| | Claude Code (Opus 5) | Antigravity (Opus / Sonnet 4.6) |
|---|---|---|
| Project context | The whole conversation, all design docs, every decision and dead end | Nothing. Starts cold, every time. |
| Knows why a number is 6.5 and not 6.2 | Yes | Only if the brief says so |
| Can read `personal-source-material.md` | Yes | **Never** — see §5 |
| Cost per hour of work | High | Low |

So the split is **not** "hard work to Opus 5, easy work to 4.6". It is:

> **Work goes to Antigravity when it can be completely specified in a brief.**
> **Work stays in Claude Code when the decision depends on context you cannot paste.**

Difficulty is the second question, not the first. A `bpy` generator for a modular
stone kit is genuinely hard code and belongs in Antigravity, because once the parts
list and dimensions are fixed there is nothing left to decide. Choosing the
character's walk speed is easy code and belongs here, because the answer depends on
the camera distance, the road width, the 90-second walk gate, and three
conversations about how the game should feel.

### The rule that protects quality

**A milestone, or a clearly-bounded sub-part of one, is assigned to exactly one
platform and never split mid-work.** Switching platform in the middle of a sub-part
means the second half is built by something that cannot see the first half's
reasoning — it sees only the code, and re-derives intent from it, usually wrongly.
The seam has to fall on a *file boundary with a written spec across it*, never
inside one problem.

---

## 2. What each model is for

**Opus 5 · Claude Code** — decisions with a long tail, and debugging with no
reference implementation. Architecture that many later milestones depend on;
anything where the failure mode is "we discover in four months that this was
wrong". Novel graphics work. Anything touching source material.

**Opus 4.6 · Antigravity** — hard, well-specified code. The middle tier exists for
one recurring shape in this project: **`bpy` generator scripts**. Those are real
algorithmic work (procedural geometry, UV layout, deterministic scatter) but they
are fully specifiable, because the spec is a parts list and a dimensions table.
Send them here, not to Sonnet, because a subtle geometry bug in a generator
silently poisons every asset it makes.

**Sonnet 4.6 · Antigravity** — volume. Scene assembly, React and store wiring,
dressing placement, UI, settings, audio hookup, config plumbing, throwaway
prototypes. **This is where most of the 742 hours live**, and it is the whole cost
saving. It is not "the cheap model doing worse work" — assembling 40 dressing props
to a written spec is work where a bigger model produces an identical result for
several times the price.

---

## 3. The split, milestone by milestone

Hours are from the roadmap's midpoint column. The **seam** row is the important
one: it says where the handoff falls and what has to exist before the Antigravity
half can start.

### M1 · It moves — 30 hrs — ✅ complete

All Opus 5, in Claude Code. In hindsight the grey room itself (`GreyRoom.jsx`,
`NoisyRoad.jsx`, the HUD) was ~8 hrs of Sonnet work that got done here. What
genuinely needed Opus 5 was the stepped-loop test harness: three separate R3F
timing traps, a physics pause fighting the test that drove it, and a rapier body
sleeping after teleport. None of that is in any documentation.

**Keep as the calibration example.** If a task looks like `GreyRoom.jsx`, it goes
to Antigravity. If it looks like `DevProbe.jsx`, it stays here.

### M2 · It runs on your phone — 18 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 4 | The tier-detection *policy*. What counts as Low; how the FPS probe decides without oscillating between tiers mid-play; how a manual override interacts with `AdaptiveDpr` continuous degradation. Getting this wrong misclassifies real phones for the rest of the project and shows up as "the game is slow" with no obvious cause. |
| **Sonnet 4.6** | 14 | Touch joystick + buttons via `ecctrl/input`, both input paths live at once. Landscape prompt, safe-area insets, `touch-action: none`. Deploy to a login-free URL. Settings persistence. |

**Seam** — Opus 5 writes `src/config/tiers.js` plus one spec paragraph per
consumer. Antigravity implements everything that *reads* that file and never edits
it.

### M3 · It looks like the reference — 50 hrs

**The highest-consequence milestone in the project.** Everything visual depends on
it, and the roadmap says outright it is the one most likely to fail.

| | Hours | What |
|---|---|---|
| **Opus 5** | 20 | The bake pipeline end to end: Cycles bake settings, `TEXCOORD_1` export, the `gltf-transform` Meshopt + KTX2 chain, and the debugging when `uv1` does not arrive in three.js. Plus the palette-conformance checker (sample every pixel against the §3 table; desaturate and confirm silhouettes read). |
| **Opus 4.6** | 20 | The `bpy` modular stone kit: walls, floor slabs, niches, the carved channel, the doorway. Hard, and fully specifiable once the parts list and dimensions are fixed. |
| **Sonnet 4.6** | 10 | R3F loading, `MeshBasicMaterial` + `lightMap` swap, the side-by-side comparison page. |

**Seam — and this one is a scheduling rule, not just a handoff.** Opus 5 must prove
one bake end to end **on a single test cube** before any kit work begins.
Otherwise Antigravity generates twenty assets against a pipeline that turns out not
to work, and all twenty need regenerating. Prove the pipeline on the cheapest
possible asset, then fan out.

### M4 · The first 40 seconds 🚀 — 35 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 15 | The water channel that fills as you walk. This is the thesis of the entire game in one mechanic and there is no reference implementation: it runs ahead of you, stops when you stop, wet stone stays wet, it hits a broken section and spills into moss. Shader plus state plus feel. Also the audio-unlock decision (`game-flow.md` §9 #3). |
| **Sonnet 4.6** | 20 | Chamber dressing placement, the black-screen fade-in on a playable frame, deploy, the 8 MB mobile budget check. |

**Seam** — the water is one indivisible piece. Do not split it across platforms or
across sessions if you can avoid it.

### M5 · The road 🚀 — 62 hrs

Second-biggest technical unknown after M3.

| | Hours | What |
|---|---|---|
| **Opus 5** | 28 | Foliage: instanced alpha-tested cross-cards with wind sway in a vertex shader. Dappled canopy light as a scrolling texture — flagged **unproven** in `look-target.md` §11 item 2. Additive light shafts. The fog/sky seam at all three tiers. And the camera revisit: M1 left a known debt where the camera can come closer than `CAMERA.minDistance` and cut through the character. |
| **Opus 4.6** | 14 | Trunk scatter to §6: ±3.5 m, 6–9 m randomised spacing, never regular. Deterministic and specifiable, and "never regular" is a real algorithmic constraint. |
| **Sonnet 4.6** | 20 | Road curvature layout to the 30 m-straight rule, footstep audio by surface, canopy layer counts per tier. |

**Seam** — dappled light gets a **timeboxed spike on Opus 5 before anything else in
M5**. It is the one deliverable here flagged as unproven; if it does not work it
gets cut, and nothing else should have been built assuming it.

### M6 · Things respond — 30 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 12 | The lifecycle contract — `enter / start / complete / fail / reset / exit` — and the no-drift `reset` guarantee. The exit criterion "an archive can be added or deleted without touching any other file" is an architecture claim, and M7, M10 and M11 all pay for it if it is wrong. |
| **Sonnet 4.6** | 18 | The six primitives (pressable, pullable, pickup, passage, inspectable, surface-that-responds) against that contract, plus the grey room exercising all six. |

**Seam** — this is the project's most reusable pattern, so it gets a name:
**one reference implementation, then fan out.** Opus 5 writes the contract *and one
complete primitive* as the worked example. Antigravity writes the other five by
pattern-matching it. Never hand over a contract with no example — an interface
without a reference implementation gets interpreted five different ways.

### M7 · The Archive stands — 85 hrs

Biggest art milestone; the roadmap flags it as most likely to overrun.

| | Hours | What |
|---|---|---|
| **Opus 5** | 20 | **Two dressing states from one geometry** (design doc §12 weathering set) — an architecture problem wearing an art problem's clothes, and it constrains every asset M7 produces. The 0:40 reveal composition, which has to make someone stop walking. The skip-to-portfolio element. |
| **Opus 4.6** | 25 | `bpy` generators for hub geometry and the weathering set. |
| **Sonnet 4.6** | 40 | Dressing volume. Curator traces, the three exits, the unreachable hero structure, title card, budget verification. |

**Seam** — the 40 Sonnet hours are the bulk *and* the cheapest work, which is
convenient, because this is the milestone that overruns. When it does, it overruns
here, and the roadmap's instruction is to shrink the hub footprint rather than
reduce dressing quality.

### M8 · It remembers you — 35 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 14 | Scene streaming and real `dispose()` of geometry, materials *and* textures, plus the leak hunt. "Flat `renderer.info.memory` across 20 enter/exit cycles" is exactly the bug class that needs reasoning about what still holds a reference. |
| **Sonnet 4.6** | 21 | localStorage save with version migration, settings UI (tier override, audio, controls, reduced motion), diegetic loading. |

### M9 · Five toys, three survive — 50 hrs

| | Hours | What |
|---|---|---|
| **Sonnet 4.6** | 35 | The five toys. Deliberately throwaway grey-room prototypes where speed beats elegance and four of five get deleted — close to ideal Antigravity work. |
| **Opus 5** | 15 | The two-pool collision (fun-first mechanics × recurring motifs) and the keep/cut calls with written reasons, because those decisions set M10 and M11's content. |

**Privacy note** — if the motif pool derives from `personal-source-material.md`,
the collision step is **Claude Code only**. The toys themselves are grey-room
mechanics with no meaning attached yet, so they are safe to brief out.

### M10 · One archive, end to end 🚀 — 90 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 35 | The six-beat structure. The twist specifically: it has to land as a new *consequence of a known rule*, not a new mechanic — an easy constraint to violate without noticing. The stopping point authored as the climax. The portable capability's effect on the hub. |
| **Sonnet 4.6** | 55 | Building the beats out, art assembly, audio hookup, the 8:00→30:00 playable stretch. |

**Seam** — the beat structure is locked in one Opus 5 document before any beat is
built. Beats built before the structure is fixed get rebuilt.

### M11 · Three archives — 125 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 30 | Capability-combination design. Each archive must need prior capabilities *in a new combination, never re-performed unchanged* — the hardest remaining design constraint, and it is cross-archive, so it needs the whole picture at once. |
| **Sonnet 4.6** | 95 | Both archives built to that spec, plus hub states 2 and 3 from the same geometry. |

### M12 · The reveal — 60 hrs

**The one milestone with a hard platform lock. See §5.**

| | Hours | What |
|---|---|---|
| **Opus 5 · Claude Code only** | 25 | The reveal mapping: things the player already touched, decoded back to something real. Requires `personal-source-material.md`, which must never leave this machine or enter Antigravity. |
| **Sonnet 4.6** | 35 | Deep Archive geometry — deliberately barer than anything before it, so the cheapest art in the game. Portfolio mode as a standalone. The WebGL-force-failed fallback path. |

**Seam** — and it is a good one. Opus 5 produces the reveal *content as finished
copy*. That copy ships in the game, so it is not secret; the source material behind
it is. Antigravity builds the UI that displays finished copy it never has to
interpret.

### M13 · Ship — 72 hrs

| | Hours | What |
|---|---|---|
| **Opus 5** | 20 | The perf pass across three tiers on real devices, and triaging whatever the playtest round breaks. |
| **Sonnet 4.6** | 52 | Full audio pass, accessibility (reduced motion, remappable controls, subtitles), README, licences and attribution for every CC0 asset, release mechanics. |

---

## 4. The totals

| Model | Hours | Share |
|---|---|---|
| Opus 5 · Claude Code | 268 | 36% |
| Opus 4.6 · Antigravity | 59 | 8% |
| Sonnet 4.6 · Antigravity | 415 | 56% |
| **Total** | **742** | |

Excluding M1 — which is done, and was 30 hrs of all-Opus-5 — the remaining 712 hrs
are **33% Opus 5**. Treat that as the target. A milestone drifting toward 60% Opus 5
means either the briefs are not specific enough to hand over, or the design was not
settled before the build started. Both are fixable, and both are cheaper to fix
than to pay for.

---

## 5. The privacy lock

`personal-source-material.md` is the decoder ring for the finale. It is gitignored
(`.gitignore` line 49) and must never be committed, shipped, or **pasted into
Antigravity**.

This is why M12's reveal work has no cheaper option. It is not that Sonnet 4.6
could not do it — it is that doing it requires handing the source material to a
second platform, and the file's whole point is that it exists in exactly one place.

Practically: anything whose *input* is that file is Claude Code only. Anything whose
input is finished, shippable output derived from it can go to Antigravity freely.

---

## 6. Choosing, when the table does not cover it

Four questions, in order. The first "yes" decides it.

1. **Does it need `personal-source-material.md`?** → Opus 5, Claude Code. Stop.
2. **Will later milestones be built on top of this decision?** → Opus 5. Architecture
   and contracts are cheap to get right once and expensive to change later.
3. **Is there a working reference implementation, or a spec precise enough to hand
   to someone who has never seen this project?** → Antigravity. Opus 4.6 if it is
   generator or geometry code where a subtle bug propagates; Sonnet 4.6 otherwise.
4. **Otherwise** → Opus 5, and the first thing it produces is the spec that lets the
   rest go to Antigravity.

Question 4 is the one that saves the most money over the project. Most work that
*feels* like it needs Opus 5 actually needs one hour of Opus 5 writing a spec,
followed by ten hours of Sonnet 4.6 executing it.
