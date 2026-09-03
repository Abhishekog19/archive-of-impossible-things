# Verification

You verify; I build. This file is what to run and what a good answer looks like.

The protocol is in [working-rules.md](working-rules.md) §3. The short form: I build a
sub-part and hand over a check list; you run it and reply in the report format; I fix
or move on. Each milestone gets a section here as it is built.

---

## The report format

Copy the failures. That is the whole reply.

```
CHECK 3: FAIL — 12.4 m, 61% grounded
CHECK 10: PASS
FEEL: turning is heavier than I expected at low speed
```

If nothing failed: **`ALL PASS`**. Two words.

Subjective observations go under `FEEL:` so they do not get mistaken for a broken
threshold. They are wanted — movement feel is a real M1 exit criterion and no number
captures it — but they are a different kind of information and they should not stop
the build.

Do not send screenshots. Do not describe a number in words. Do not explain what you
think caused it — if the number names the bug, I will see it; if it does not, I will
ask for one specific thing.

---

## M1 · It moves

**Status:** built, lint clean, production build clean. Checks 1–8 measured 8/8 PASS
on my machine; run them on yours, because a different frame rate and GPU are exactly
what a threshold is for.

### Setup

```bash
npm run dev
```

Open the printed URL, then open DevTools (**F12**) and click on the **Console** tab.

Wait for the scene — grey plaza, a road running away from you, a HUD panel top-left.
The HUD reads zeros for a moment while Rapier's WebAssembly initialises; that is
normal and it fills in by itself. Only reload if it is still all zeros after a few
seconds, which means the canvas mounted at zero size.

Two console warnings appear on every load and are **not** failures — both come from
inside three.js and `ecctrl`, not from this project's code:

```
THREE.Clock: This module has been deprecated. Please use THREE.Timer instead.
using deprecated parameters for the initialization function; pass a single object instead
```

The character is a stone capsule with a small amber box on its front — a facing
marker, so you can tell which way you are pointing before there is an animated
character. Not art; it goes at M3 with everything else you can see.

### Checks 1–8 — one line

Paste this into the console and press enter:

```
window.__M1.report()
```

You get a block like this. **Copy any line that says FAIL. If none do, reply
`ALL PASS 1-8`.**

```
M1 EXIT CRITERIA — M1 8/8 PASS

PASS  1 camera never clips    worst clearance 1.72 m · 0 would mean embedded in geometry
PASS  2 camera pulls in       open 4 m · dead end 0.62 m
PASS  3 30 m strip walkable   29.29 m in 13.5 s · 100% grounded
PASS  4 8% slope clean        step 0.16 m ≤ 0.25 · 100% grounded · 4.57°
PASS  5 stairs clean          step 0.23 m ≤ 0.25 · 100% grounded
PASS  6 camera height holds   2.09–2.21 m above feet · target 2.2 ±0.15
PASS  7 sky above canopy      frame top 36.31° fixed · canopy must be unbroken within 5.85 m ahead (→ M5)
PASS  8 perf budget           60 fps ≥ 30 · 19 draws ≤ 150 · 1956 tris · dpr 1.25
NOTE  25% ramp, out of spec    100% grounded · step 0.12 m · 14.04°
```

It takes a few seconds — it is teleporting the character to six camera positions and
walking four features under a stepped clock, about 50 m of walking in total. It puts
the game back to normal play when it finishes, so you can carry straight on to the
manual checks.

For detail on a failure, `window.__M1.audit()` returns every number the report
reduces. Only run it if something failed; paste the one failing row, not the whole
object.

**What the checks mean, in one line each**

| | Criterion | Why it can fail |
|---|---|---|
| 1 | Camera is never inside geometry | Measured by a downward raycast that returns 0 from inside a solid. The inside of a box renders as plausible grey, so this cannot be eyeballed. |
| 2 | Camera pulls in near walls, sits at 4.0 m in the open | A clamp bug can push it *through* a close wall instead of stopping short |
| 3 | The 30 m strip is walkable at full contact | Controller stalling, or fighting the road's ±0.25 m noise |
| 4 | 8% is look-target §6's stated maximum and must feel unremarkable | Float-height tuning |
| 5 | Stairs traverse without catching or hovering | The classic ecctrl float-height question |
| 6 | The §2 camera sits 2.2 m above the feet while walking | Drift between the config and the actual offset |
| 7 | Fixed pitch means the camera cannot be aimed at the sky | Structural. The 5.85 m figure is a canopy-continuity constraint handed to M5 |
| 8 | look-target §10 budgets | Watched from M1 so a regression is visible the session it happens |

The NOTE line is not a criterion. The 25% ramp is deliberately out of spec so the
failure edge is visible rather than theoretical — and it traverses cleanly, which
tells us 8% is a comfort choice rather than a controller limit.

### Check 9 — the interactable smoke test

Walk to the grey post to your left. It turns amber as you get close. Press **E**.

- **Expected:** the post lights on approach with no prompt and no label; the slab
  beyond it rises and lightens. Press E again and it drops. Clicking the post
  directly does the same thing.
- **Fails if:** nothing reacts, or a text prompt appears (there should be none — the
  design doc's Law 8 is teach by perturbation, never with words).

### Check 10 — the "too close" marker

Paste:

```
window.__M1.place([5, 1.5, 13.2])
```

That drops you in a three-walled dead-end pocket with the camera against the back
wall. Watch the HUD **distance** row, then walk out with **S** and back in with
**W**.

- **Expected:** distance counts down from `4.00`, shows `← pulled in`, and at the
  deepest point turns red reading `← too close, character clipping`. You will see
  through your own character.
- **That red line is correct, not a bug.** It is a documented trade: M1's criterion
  is "pulls in and never clips", so when a wall is closer than the camera wants, the
  wall wins. A see-through character reads as a camera that got too close; a camera
  inside a wall reads as the world falling apart. Raising the camera or fading the
  character is the real fix and it belongs with the M5 camera work.
- **Fails if:** the view fills with flat grey with no character visible. That means
  the camera is inside the wall and check 1 should have caught it.

### Check 11 — the visibility pause

Note the HUD **at x / z**. Switch to another tab or minimise for **~15 seconds**.
Come back.

- **Expected:** same position. No lurch forward, no falling through the floor.
- **Why you have to do this one:** the automated harness deliberately overrides this
  pause — a hidden pane is exactly when the stepping harness runs — so this is the
  one behaviour the audit structurally cannot test.
- **Fails if:** the character has moved, or has fallen out of the world. A hidden tab
  returns one frame whose delta is the whole absence, and unguarded that integrates
  in a single step and tunnels the capsule through the plaza.

### Check 12 — HUD and fog

Press **H** — the HUD collapses to a button; click it to restore. Press **F** twice.

- **Expected:** fog off, the far end of the road is crisp and you can see a hard edge
  where the ground ends. Fog on, it fades into the sky with **no visible seam at the
  horizon** — the fog colour and sky colour are the same value and look-target §5
  makes that non-negotiable.
- **Fails if:** you can see a line where ground meets sky with fog on.

### Check 13 — the real test

> **Walk with no objective for 90 seconds. Do you want to keep walking?**

Straight from the roadmap, and it is yours alone — nothing I can measure substitutes
for it. Wander. Use the ramps and the stairs. Run with shift. Turn by dragging.

Report `CHECK 13: YES`, or `CHECK 13: NO — <what feels wrong>`.

If the answer is no, the roadmap allows up to **10 more hours** on movement feel
before M2, capped deliberately because this gate can eat unbounded time. It gets
revisited at M5 anyway, with real scenery, where the same question is asked of three
people who are not you. `game-flow.md` §4 bets three minutes of the player's time on
the answer, which is why it is an exit criterion and not a nice-to-have.

Useful vocabulary for a `NO`, since "it feels off" costs a diagnosis round: *floaty*
(too little ground friction), *sticky* (acceleration ramps too slowly), *skatey*
(deceleration too slow when you release), *heavy turn* (camera damping too high),
*jittery camera* (damping too low), *drifting* (the camera lags the character).

### Already done, don't redo

- `npx eslint src --max-warnings=0` — clean
- `npm run build` — clean, 403 ms. `DevProbe` is behind `import.meta.env.DEV`, so
  none of the test harness ships.
- Git — yours. Nothing has been committed or pushed from my side.

### If a check fails

Reply with just the failing lines. Then, unless the fix is obvious to you, wait —
do not start changing thresholds or config to make a number go green. Every threshold
in `report()` traces to a line in `build-roadmap.md` or `look-target.md`, and a
threshold moved to fit a measurement tests nothing.
