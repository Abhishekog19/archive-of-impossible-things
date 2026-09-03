# Working rules

How to run this project cheaply without building a worse version of it.

Read [model-plan.md](model-plan.md) for *which model*. This file is *how to work* —
mostly rules for you, because most of the cost is decided by how a session is run,
not by which model runs it.

---

## 1. Where the money actually goes

This matters more than model choice, so it goes first.

**Every tool call re-sends the entire conversation.** Not the last message — all of
it. When I read a file, run a lint, take a screenshot or make an edit, the whole
accumulated context goes back to the model as input. So the cost of a session is
roughly *turns × context size*, and since context only grows, **turn 50 costs about
fifty times what turn 1 cost.**

Three consequences, and they are the whole basis of the rules below:

1. **A long session is quadratically expensive.** Two 30-turn sessions cost far less
   than one 60-turn session, for the same work.
2. **Anything that enters context stays there and is paid for again every turn
   after.** A screenshot is ~1,500 tokens. Read at turn 10 of a 50-turn session, you
   pay for it 40 more times. This is why M1's test harness returns a line of numbers
   instead of a picture.
3. **Twenty small tool calls cost twenty full context re-sends.** One call that does
   twenty things costs one. Batching is not tidiness, it is the single biggest lever
   inside a session.

Model choice is the *second* lever. It is a large constant factor. Session
discipline is the exponent.

---

## 2. Rules for you

### R1 · One milestone per session. `/clear` at the boundary.

The milestone is the natural unit: it has its own exit criteria, and its context
stops being useful the moment it passes. Carrying M1's debugging history into M2
means paying for it on every M2 turn.

### R2 · If a session passes ~60 turns, stop it deliberately.

Say **"write the handoff and stop"**. I will update
[model-plan.md](model-plan.md) §0 and `build-roadmap.md` §10 with exactly where
things stand and what is next. Then `/clear` and start fresh. The handoff costs one
turn; not doing it costs every remaining turn at full context.

Signs you are past the useful point: I start re-reading files I already read, or the
work slows down without getting harder.

### R3 · Front-load. One big message, not five small ones.

> ❌ "start M2" … then "also add the landscape prompt" … then "and the tier override
> should persist" … then "oh and safe-area insets"
>
> ✅ one message: everything M2 needs, in one go

Each of those follow-ups is a full context re-send, and worse, arriving mid-build
they can force a replan of work already in flight. If you think of something after
sending, hold it until I next report back — unless it invalidates what I am doing,
in which case interrupt immediately. A wasted build is more expensive than an
interruption.

### R4 · Numbers, not screenshots.

Never send an image where a number would do. Never ask me to "look at it and see".
When something looks wrong, run the audit and paste the row.

### R5 · Verify anything you can verify in under a minute yourself.

This is the agreement we made and it is worth about a third of the project's cost.
I build; you check; you report. See §3 for the protocol.

The specific thing to stop asking for: "can you check it works?" — that turns into
me starting a server, reloading, screenshotting, evaluating, and reading output,
which is five or six full-context tool calls to learn something your eyes would have
told you instantly.

### R6 · When reporting a failure, paste evidence, not description.

> ❌ "the camera looks weird near the wall"
>
> ✅ `slotDeep: {"dist":0.62,"camClear":0}` — expected `camClear > 0`

Description costs a diagnosis round. Evidence usually costs none, because the number
often names the bug outright.

Paste the exact error text, not a paraphrase. A stack trace is cheap; three rounds
of "what exactly did it say?" is not.

### R7 · Don't ask for recaps.

"Summarise what we've done", "list everything so far", "remind me where we are" —
these re-send the whole context to produce something that is already written down in
`build-roadmap.md` §10 and `model-plan.md` §0. Read those instead. If they are stale,
say **"update the status files"** — that is a cheap, useful turn; a recap is an
expensive, disposable one.

### R8 · Never paste `personal-source-material.md` into Antigravity.

Not an excerpt, not a paraphrase of a specific memory, not "the thing about the…".
It is gitignored and lives in exactly one place. See [model-plan.md](model-plan.md)
§5.

### R9 · Don't switch platform mid-sub-part.

Finish the bounded piece on the platform that started it. The seam belongs at a file
boundary with a written spec across it — never inside one problem. Half a problem
solved in Claude Code and half in Antigravity produces a second half that re-derives
the first half's intent from the code, usually wrongly.

### R10 · Say "no verification" when you want raw build output.

If you want me to write code and stop — no server, no reload, no screenshot — say so.
Default is that I verify what I can cheaply, because shipping code I have not run is
usually a false economy. But when you would rather check it in the browser yourself,
saying so saves several full-context round trips.

---

## 3. The build → verify → report loop

The core workflow. Replaces me driving a browser, which was the expensive part.

```
1. You:  the ask, front-loaded, one message
2. Me:   build a whole sub-part, then hand over a CHECK LIST
3. You:  run it, paste the REPORT
4. Me:   fix, or move to the next sub-part
```

### What I owe you at step 2

A check list, never prose. Each item is:

- **exactly what to run** — a command, a console line, or one action to take
- **the expected value**, with a threshold, not a vibe
- **what a failure means**, so a bad number is self-diagnosing

And a milestone is split into **2–4 sub-parts**, so a mistake surfaces after a
quarter of the work rather than all of it.

### What you owe me at step 3

The report format, and nothing else:

```
CHECK <n>: PASS
CHECK <n>: FAIL — <the number or the exact error>
```

That is it. No explanation, no screenshot, no theory about the cause. If everything
passed: **`ALL PASS`** — two words, and I move on.

If you have a subjective observation ("it feels floaty"), that is genuinely valuable
and *not* a check failure — put it at the end under `FEEL:` so it does not get
mistaken for a broken threshold. Movement feel is a real M1 exit criterion and no
number captures it.

### Why this is cheaper

The numbers exist either way. The saving is that *you* read the browser instead of
me: no server management, no reloads, no screenshots entering context permanently,
no evaluate-and-inspect rounds. A check list is one turn out and one turn back.

---

## 4. Handing work to Antigravity

Antigravity starts with **nothing**. Not the design docs, not the conversation, not
the reasons. A brief that assumes any of it produces confident, wrong code.

Ask me for **"an Antigravity brief for X"** and I will produce this, filled in:

```markdown
## Goal
One paragraph. What exists when this is done.

## Model
Sonnet 4.6 | Opus 4.6 — and one line on why.

## Files
- CREATE: src/…
- EDIT:   src/…  (only the named function/section)
- DO NOT TOUCH: <files this must not modify>

## Spec
Every number, explicitly. No "appropriately sized". No "reasonable default".

## Constraints
- Import all constants from src/config/look.js. Never write a numeric literal
  for anything that file defines.
- Match the surrounding comment density and naming. Explain WHY, not what.
- No new dependencies without asking.
- <project rules that apply to this specific piece>

## Reference implementation
Path to the file already doing this correctly. Match its shape.

## Acceptance
- npx eslint src --max-warnings=0 passes
- npm run build passes
- <the specific observable outcome, with numbers>
```

Two parts of that template do the most work:

**Reference implementation.** Pointing at an existing file that already does the
thing correctly is worth more than any amount of prose description. It is why
[R6 in model-plan.md §3](model-plan.md) insists a contract never ships without one
worked example.

**DO NOT TOUCH.** A cold model asked to add a feature will helpfully refactor
things it does not understand the reasons for. Most of the odd-looking code in this
repo is odd for a documented reason.

### After Antigravity work lands

Do not paste the diff into Claude Code to be reviewed — that is a full re-send to
read code that already passes lint and build. Instead run the acceptance checks from
the brief and report in the §3 format. Only bring it here if a check fails.

---

## 5. What not to economise on

Cutting these costs more than it saves.

- **The exit criteria.** They are in `build-roadmap.md` for each milestone. They are
  the definition of done. A milestone that "works" but misses its criteria gets
  rebuilt at the milestone that depended on it, at full price.
- **The subjective gates.** "Walk for 90 seconds — do you want to keep walking?"
  (M1), and the same question asked of three other people at M5. No number
  substitutes, and M5's version can invalidate the whole two-layer design. Better to
  learn that in December 2026 than in June 2027.
- **The de-risking spikes.** M3's single test-cube bake before the kit. M5's dappled
  light spike before the foliage. Both exist so a failure costs one asset instead of
  twenty.
- **Logging actual hours** (roadmap §9 rule 1). The schedule is only useful if the
  estimates get corrected by reality.
- **Writing down decisions.** Every decision recorded in a doc is a decision that
  does not have to be re-derived — here at full context price, or in Antigravity
  where it will be re-derived wrongly.

---

## 6. The short version

Pin this:

1. One milestone per session. `/clear` between.
2. Past ~60 turns: "write the handoff and stop".
3. One big message, not five small ones.
4. Numbers, never screenshots.
5. You verify; report `PASS` / `FAIL — <number>`; subjective notes under `FEEL:`.
6. Source material never enters Antigravity.
7. Never split one problem across two platforms.
8. Ask for "an Antigravity brief for X" rather than pasting context by hand.
