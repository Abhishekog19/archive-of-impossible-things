# Game Flow — Minute by Minute

Companion to [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md).
The design doc says *what the game is*. This says *what the player does, in order,
with a clock running*.

**Status:** first draft, written before Step 1. Timings are targets to build
against and to be corrected by playtesting, not predictions.

**Scope:** the v1 shape — hub, three archives, Deep Archive, reveal. Minute 0 to
minute 8 is specified tightly because it's the most-read part of the game. Archive
1 is specified as a *shape* with fixed beats and timings; its actual mechanic is
chosen at Step 7 and deliberately left open here (design doc §19, Law #3).

**Proposed v1 duration: 75–95 minutes.** Design doc §19 lists exact duration as
open; this is the first concrete proposal. It matters now because it sets how big
the hub can afford to be.

---

## 1. What this document is allowed to decide

| Decides | Doesn't decide |
|---|---|
| Order of events, and when | Which puzzle archive 1 is |
| How long each stretch lasts | Which capability it grants |
| When the player is taught vs. left alone | Final art, final names |
| When text appears (and it barely does) | Anything personal-layer |

---

## 2. Constraints this flow has to obey

Carried from the design doc, listed here so the flow can be checked against them:

- No exposition dump. No tutorial text. (§7)
- No combat, no death, no game-over, no timers. (§19, locked)
- Every machine works perfectly up to the interesting part, then stops. Nothing
  is damaged or decayed. (§7 governing fiction)
- The Curator is permanently absent, known only through traces. (§19)
- The impossible arrives in natural vocabulary, never technological. (Law 13)
- The world changes gradually in response to what happened, never snap-transforms. (Law 14)
- Once a rule is understood, stop asking for it to be performed. (Law 10)
- Tension comes from inexplicable success, not from threat. (Law 12)
- A skip-to-portfolio path exists early and stays available. (§19, locked)

---

## 3. The opening — a proposal that closes an open item

Design doc §7 currently opens with *"A mechanical structure wakes"* and system
lines like *"Visitor detected. Archive integrity: 17%. Curator status: UNKNOWN."*
§9 (v5) rejected that whole register, and §19 lists the replacement as open.

**Proposal: delete the text entirely.** Not rewrite it — delete it. Each of those
three lines has a physical equivalent that the environment can state better than
a caption can:

| The old line | What says it instead |
|---|---|
| *"Visitor detected"* | The place physically responds to being walked on |
| *"Archive integrity: 17%"* | How much structure is still standing vs. reclaimed by growth — visible in one glance |
| *"Curator status: UNKNOWN"* | A tool left mid-use. A path worn smooth by repeated walking that stops abruptly. |

This is stronger than a vocabulary swap, because a status readout is a *machine*
telling you about itself — which is the register we just ruled out — while a
building half-eaten by moss is the same information with no narrator.

⚠ **Pending sign-off.** If accepted, this closes "§7's opening vocabulary" in §19
and §7's ⚠ block gets rewritten.

---

## 4. Minute 0 to 8 — specified tightly

### 0:00–0:15 · Before control

Black screen. One sound: water moving somewhere, close but not visible.

Fade in. The character is already standing — no waking-up animation, no cutscene.
Camera is already in its gameplay position behind them. The first frame of the
game is a playable frame.

What's on screen: a stone floor, a shallow dry channel cut into it, daylight
falling across it from somewhere ahead. Nothing else. No UI. No title. No prompt.

**Why:** the player's first question should be *where am I*, and they should have
to move to answer it.

### 0:15–0:40 · The place responds

The player moves — that's the only available verb, and no one told them to.

As they walk, **the dry channel in the floor fills with water, running in the
direction they walked.** It stays a step or two ahead of them. If they stop, it
stops. If they turn back, it doesn't retreat — the wet stone stays wet.

This is the whole design of the game in twenty seconds:

- Something impossible, stated in entirely natural material (Law 13)
- The player caused it and did nothing to earn it (Law 12 — inexplicable success)
- No text explained it
- It teaches the only control they have by rewarding its use (Law 8, teach by perturbation)

The channel is also the integrity readout: it runs strongly for about fifteen
metres, then hits a broken section and spills sideways into moss. The place used
to work. It mostly doesn't now.

### 0:40–1:10 · The reveal

The channel leads through a gap in a wall, and the space opens.

**The Central Archive hub.** Large — the first thing since the fade-in that the
camera has to pull back for. Cut stone and standing structures, all of it
half-reclaimed: moss in the joints, roots through the paving, a tree growing
through what used to be a roof. Canopy above, letting daylight down in patches.
Water channels running through it, most of them broken.

Title appears here, small, low, over the reveal. **This is the first text in the
game.** It fades.

### 1:10–1:20 · The way out, offered once

A small unobtrusive element appears in a corner: the way to skip straight to the
written portfolio. Shown once, plainly, then collapses to a small persistent icon
that never expands again.

**Why here and not the main menu:** a recruiter with four minutes should not have
to play a game to read a CV, and should not have to hunt for the exit either.
Offering it *after* the reveal rather than before means they've at least seen the
best image in the first ninety seconds.

### 1:20–5:00 · The hub, unguided

No objective marker. No quest. The player is left alone in a large interesting
place with one verb.

What the space communicates by layout alone:

- **Three paths lead out.** One is walkable. Two are not — growth too dense to
  push through, and a gap in the stone too wide to cross. Nothing is *locked*;
  things are simply not yet possible. (Natural register: no doors, no keys.)
- **Traces of the Curator.** A workbench with a tool set down mid-task. A worn
  groove in a step from being used thousands of times. A stack of something
  sorted carefully, and beside it the same thing abandoned unsorted halfway.
- **One hero structure**, visible from most of the hub, that the player cannot
  reach or understand yet. It is the answer to "what's at the bottom" and it
  will be the last thing they touch.

Expect players to spend 1–4 minutes here depending on temperament. Nothing pushes
them. The walkable path is the only exit and it is obvious without being signposted.

### 5:00–8:00 · The road

The canopy road. Design doc §8: *"the passage is content."*

Three minutes of walking with **nothing to solve.** No pickups, no collectibles,
no dialogue, no hazard. Trees both sides, canopy closing overhead, road curving
enough that you never see more than a stretch ahead, fog taking the rest. Sound
is leaves, water, footsteps on different surfaces as they change.

**This stretch is the single riskiest thing in the flow**, and it's deliberate. If
three minutes of walking with nothing to do is boring, the two-layer design in §8
has failed and we need to know at Step 1 — not at Step 8. The traversal layer
either carries this or it doesn't.

**Step 1 acceptance test, stated as a question:** *walk this road with no
objective. Do you want to keep walking?* If no, movement needs more depth before
anything else gets built.

---

## 5. Archive 1 — shape fixed, mechanic open

**8:00–30:00, about 22 minutes.** The mechanic is chosen at Step 7 from playable
toys, not here. What's fixed is the beat structure (design doc §16) and the clock.

| Beat | Clock | What happens | Rule it serves |
|---|---|---|---|
| **Exterior** | 8:00–10:00 | The archive is visible before it's entered. You can see the rule operating from outside without understanding it. | Telegraph one step away (Law 9) |
| **Teach** | 10:00–14:00 | The rule is discovered by poking, not by being told. Safe, consequence-free, unlimited retries. | Teach by perturbation (Law 8) |
| **Escalate** | 14:00–20:00 | Same rule, harder context. Two or three steps, each adding one variable. | Law 5 |
| **Twist** | 20:00–25:00 | The rule turns out to do something you hadn't considered. Not a new mechanic — a new consequence of the one you have. | §16 |
| **The stopping point** | 25:00–28:00 | You reach the place where the Curator stopped. The machine works perfectly up to here. Finishing it is your job. | §7 governing fiction |
| **Payoff** | 28:00–30:00 | It completes. You keep a portable capability. | §8 compounding |

**Where the level design lives:** the stopping point. The Curator quit at the
exact moment their question got answered, and *that point is the level's climax.*
Building an archive means deciding what stopped being interesting, and when.

> **ILLUSTRATION ONLY — not a proposal, not locked, do not build this.**
> Purely to show what the beats look like when filled in. Using the Living Garden
> candidate (§9 v5 upgraded it to a leading candidate):
> plants grow toward where you have walked, so your own trail is the tool.
> *Teach:* walk a loop, watch growth follow, realise the path is drawn by you.
> *Escalate:* growth must reach across a gap, so the trail has to be planned.
> *Twist:* growth also follows the water from the opening — and water can be
> redirected, so you are not the only thing making paths.
> *Stopping point:* the Curator got growth to cross a gap once and left. Crossing
> it twice at the same time is the thing they never tried.
> *Capability kept:* the world responds to your trail, and it comes with you.

---

## 6. 30:00–35:00 · The return, and the hub has changed

The player walks back down the same road. **Same stretch, and this is the test of
whether it works** — a road you enjoy walking is a road you'll walk twice.

The hub is different, and it is different *gradually* (Law 14, never
snap-transforms):

- The water channels run further than they did. Not all of them. Further.
- Growth has advanced somewhere it wasn't, and receded somewhere it was.
- One of the two impassable paths is now passable — because of the capability
  earned, not because a door unlocked.
- The hero structure is unchanged. It stays out of reach.

**No cutscene marks any of this.** The change is authored so a player who was
paying attention notices and a player who wasn't simply finds the world slightly
more open. Design doc §12's weathering set exists to make this cheap: same
geometry, re-dressed scatter and material tint, no new models.

---

## 7. The rest of v1, compressed

Specified loosely on purpose — these get their own pass once archive 1 is real
(§17 Step 8 is a vertical slice for exactly this reason).

| Stretch | Clock | Function |
|---|---|---|
| **Archive 2** | 35:00–55:00 | Same beat structure, different rule. Requires the capability from archive 1 *in a new combination*, never re-performed unchanged (§8). |
| **Hub, changed again** | 55:00–58:00 | Second increment. The third path opens. |
| **Archive 3** | 58:00–75:00 | Shorter, denser, assumes fluency. Both prior capabilities needed at once. |
| **Hub, third state** | 75:00–78:00 | The hero structure becomes reachable. It has been visible for 75 minutes. |
| **Deep Archive** | 78:00–90:00 | Colder, sparser, bare rock and still water. Intentionally less decorative than anything before it (§9). Not another exhibit. The things that were never returned to ended up here. |
| **Reveal → portfolio** | 90:00–95:00 | The world reveals the person behind it. Selected things the player already touched are decoded back to something real (§8). |

**Curiosity ladder checkpoints** (§8) — each rung should close a question and open
a better one:

| Rung | Answered by |
|---|---|
| What is this place? | 0:40 reveal |
| Who built it? | The traces at 1:20–5:00 |
| Why is it changing? | The hub at 30:00 |
| What's at the bottom? | The hero structure, visible from minute 1, reachable at 75:00 |
| Who is the Curator? | Deep Archive |
| Why do these places feel connected? | The compounding capabilities |
| Final | Portfolio |

---

## 8. What this flow commits us to building

Reading the clock as a build list:

| Needed by | What | Roadmap step |
|---|---|---|
| 0:15 | Character, camera, movement, one collision surface | Step 1 |
| 0:15 | Movement that's worth 3 minutes with no objective | Step 1 |
| 0:20 | Something that responds physically to being walked on | Step 3 |
| 0:40 | Camera that can handle an intentional reveal | Step 1 |
| 1:10 | Skip-to-portfolio element | Step 9 (stubbed at Step 0) |
| 5:00 | Canopy road, fog, layered foliage | Step 2.5 |
| 8:00 | One archive, all beats, end to end | Step 8 |
| 30:00 | Hub in two dressing states from one geometry | Step 4 + §12 weathering set |

**Nothing in the first 8 minutes needs an archive mechanic to exist.** That's the
useful finding: the most-read part of the game is buildable from movement, camera,
one responsive surface and the road — all of it Steps 1 through 2.5, none of it
blocked on the Step 7 toy decisions.

---

## 9. Open questions this raised

1. **Does the water-response at 0:20 give away too much too early?** It states the
   game's whole thesis in twenty seconds. That may be exactly right, or it may
   spend the best card first.
2. **Is 3 minutes of road too long for a first-time player** who doesn't yet trust
   that walking is the point? Might want 90 seconds on the first pass and the full
   3 minutes on the return.
3. **Where does audio unlock happen?** Browsers require a user gesture before any
   sound plays, and this flow opens with sound over a black screen. Needs a
   gesture before 0:00 — probably the click that starts the game.
4. **Does the hero structure survive being visible for 75 minutes** without either
   becoming wallpaper or frustrating the player?
