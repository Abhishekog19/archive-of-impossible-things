# Archive of Impossible Things — Design Document (v5)

*Last updated: 2026-08-24*
*Status: concept, design laws, and production plan locked. Technical questions resolved (§10, §13). v1 scope set to 3 archives. **Personal-layer interview complete — 5 rounds.** Individual archive games intentionally NOT locked. **Step 0 complete** — scaffold built, stack verified, deployed. Next action: Step 1, movement and camera.*

**Companion documents.** This doc holds the concept and the laws. Three others hold the specifics:

| Doc | Holds |
|---|---|
| [technical-production-spec.md](technical-production-spec.md) | Budgets, device tiers, memory discipline, asset pipeline |
| [game-flow.md](game-flow.md) | What the player does, in order, with a clock running |
| [look-target.md](look-target.md) | Camera, palette, fog and canopy as buildable numbers |

Where they conflict with this document, they are wrong and should be corrected — except for `look-target.md`'s numbers, which are *meant* to be revised by what happens on screen.

**⚠ v5 reverses a v4 decision.** §9's art direction has flipped from hard-surface/museum/machinery back to **stylized natural** — rock, soil, canopy, water, weathered structures — because Round 4 of the personal-layer interview established that the futuristic-mechanical look is a stated anti-goal, and re-examination showed v4's production argument was over-generalised. §9 carries the full reasoning, the corrected scripted-vs-sourced split, and the one real new risk (alpha overdraw). §5 gains Laws 13–14, §8 gains a two-layer traversal model, §12 restores the Nature kit, and §7's opening paragraph is flagged for a vocabulary pass.

**v1 scope (new in v4): three archives, then ship.** Feasibility arithmetic at the real time budget (10–15 hrs/week, learning the stack while building) puts foundation at 150–250 hrs and each polished archive at 60–120 hrs — so 3 archives is ~9–11 months, and 9 archives is 1.5–2 years before ideation churn. The modular architecture in §11 was designed so an archive is a clean *delete*; it equally makes one a clean *addition*. Ship three, add more as updates. A live thing that grows beats a dormant branch.

---

## 1. The Core Idea

> Build a genuinely fun, curiosity-driven 3D web adventure first; only at the end reveal that the worlds, struggles, objects, and motifs were indirectly inspired by the person behind the portfolio.

**The guiding sentence:** *We are making a genuinely fun little adventure game first. The fact that it secretly happens to be a portfolio is the twist, not the premise.*

## 2. Priority Order (locked)

1. **Fun** — the activity itself should be worth playing
2. **Curiosity** — what's next, what is this place, who made it
3. **Variety** — mechanics/environments change before they get stale
4. **Story** — glues experiences together, generates momentum
5. **Personal connection** — sits underneath the game, not on top of it
6. **Portfolio reveal** — the real portfolio decodes references the player already experienced

---

## 3. Where This Started, and What Was Discarded

Started as "Ancient Ruins Portfolio": a jungle-temple ruin, a hub connected to seven trial chambers, each chamber directly revealing a résumé category (About, Projects, AI work, Experience, Contact, Skills, Security), non-linear + skip-to-professional-mode, and a final mode-shift into a normal scannable site.

**Discarded:** the specific seven chamber mechanics, and the temple as the framing for the *entire* world (see Section 9 — open question on where/whether the jungle identity survives).

**Survived:** the professional-mode ending, the skip-anytime philosophy, modular level/Archive thinking, and the core tech stack (React + Three.js/R3F, Rapier + ecctrl, Zustand, compressed GLTF, Vercel/Netlify).

## 4. The Major Creative Pivot

This is **not** primarily a résumé or tech/AI-recruitment tool. It's a natural walkthrough of the person behind the work — nature, curiosity, things loved, things built, struggles encountered, how ideas get approached. The player should build a rough subconscious impression of the creator *without* exact tech terms, project explanations, or résumé logic during play. The real portfolio, at the end, references events from the game — producing an "I remember that" recognition rather than a lecture.

| Question | Current answer |
|---|---|
| What should the player feel during the game? | "This is fun." "What is this?" "What happens next?" "Who built this?" |
| What should the player NOT feel? | "I am being walked through someone's résumé." |
| What should the final reveal do? | Retroactively make the journey make sense, without the journey *depending* on the reveal to be worth playing. |
| How should personal traits appear? | Through what the player does and sees — never through labels like "I am persistent." |
| Role of emotional storytelling? | Low to moderate, deliberately. Curiosity and fun are the main objective, not emotional autobiography. |

## 5. Design Laws (locked)

1. **The player is the protagonist.** The creator is the mystery behind the world — the game shouldn't force the player to care about "me" up front.
2. **Never say the trait; demonstrate it.** Persistence through iteration, curiosity through discovery, creativity through unusual systems, love of building through things that can be assembled or understood.
3. **Fun mechanic first, symbolic mapping second.** Never invent a bad puzzle because it neatly maps to a résumé bullet. Prototype something fun, *then* decide if it naturally connects to something real.
4. **Every mission answers one question and opens another.** Curiosity should form a ladder, not a sequence of disconnected rooms.
5. **Don't milk mechanics.** Hazelight philosophy: teach it, let the player enjoy it, twist it, give it a payoff, move on before repetition kills the novelty.
6. **Not every room must mean something.** Some sections simply exist because they're fun — selective personal references hit harder than a forced one-to-one mapping.
7. **The game must work even if the player ignores the story entirely.** The ending gains value from the journey; the journey shouldn't need the ending to justify itself.

**Laws 8–12, added in v4.** These are *derived*, not invented — each came out of the Round 2 interview (see `personal-source-material.md`, gitignored) and each happens to also be good general design practice, which is why they're safe to promote to laws:

8. **No tutorial text. Teach by perturbation.** Never explain a mechanic in words. Give the player one small working thing they can change, and let the reaction do the teaching. This is the preferred route to §16's "understand the primary mechanic in 30–60 seconds."
9. **Always telegraph "one step away."** The strongest engagement state is visible near-correctness — the idea is obviously possible and exactly one thing is misbehaving. Manufacture that state continuously; avoid binary solved/unsolved presentation.
10. **Comprehension exempts the player from repetition.** The moment a rule is understood, stop asking for it to be performed. Either escalate it, or hand the player a way to automate it. This is the hard-edged version of Law #5 — it names the exact trigger for moving on.
11. **No death, no combat, no game-over, no timers, no punishment.** Failure states must read as *incomplete*, reset instantly, and cost nothing. **This resolves the long-open question of whether combat exists: it doesn't.** Frustration is the only real enemy of curiosity (§16).
12. **Tension comes from inexplicable success, not danger.** The unsettling thing in this world is a machine that simply *works* for no visible reason. This keeps the tone light rather than dark — as required — while still generating unease, and it's a distinctive enough register to be part of the game's identity.
13. **Natural-impossible, never tech-impossible** *(new in v5).* Impossibility is expressed in the vocabulary of the natural world — water running upward, stone holding position with nothing beneath it, roots carrying a structure's weight, a path continuing where it cannot. **Never** holograms, neon, glowing circuitry, screens or exposed machinery. Lighting is diffuse and natural — daylight through canopy, overcast, warm evening — not theatrical, and not a scene full of emissive sources. This is a stated anti-goal, which makes it a harder rule than a preference: if an effect only reads as impossible *because* it looks technological, it's the wrong effect.
14. **The world evolves gradually, in response to what already happened** *(new in v5).* Change arrives as spreading, wearing, reclaiming and settling — never as a snap transformation or an unexplained pop. If the world is different, something the player did should be the cause, and the change should look like time passing rather than a state flag flipping. This is what makes returning to the hub worth doing, and it is the mechanical basis for Act II's "the Archive reacts."
15. **The player meets behaviour, not architecture** *(new in v5).* Everything elegant in this document — the capability registry, compounding archives, the governing fiction, the unfinished-exhibit logic — is invisible to the visitor. They experience what they do, what the world does in response, and what changes as a result. Nothing else exists for them. **The corollary is a warning:** the internal structure feels like the whole project while you're inside building it, and almost all of it disappears for someone arriving for the first time. When time is short, spend it on what the player perceives — behaviour, feedback, feel — and never on machinery that only the builder will ever appreciate.

---

## 6. Four Game Directions Explored (none formally discarded)

| # | Direction | Hook | Feel |
|---|---|---|---|
| 1 | **The Thing You Left Behind** | Wake up, find a broken object someone clearly built, repair it, discover more unfinished creations. "Who built all this, and why?" | Repair, experimentation, traversal, physics, environmental puzzles |
| 2 | **The Archive of Impossible Things** *(current deep-dive — Section 7)* | A mysterious archive stores exhibits that violate normal rules; each can become a radically different kind of game. "What impossible thing is in the next room?" | Anthology of wildly different mechanics, held together by a hidden Curator mystery |
| 3 | **The World That Keeps Changing** | The rules, perspective, or genre change on you repeatedly: exploration → platforming → top-down puzzle → physics → stealth → vehicle... | The surprise itself is the hook |
| 4 | **Follow the Thread** | A glowing thread/recurring clue chains discoveries together — mirrors how real interests unexpectedly lead into new skills and projects, experienced first as a plain adventure mystery | Chain-of-curiosity structure |

Idea 2 has been developed furthest and is the leading concrete world concept, but 1, 3, and 4 remain valid — worth revisiting if Archive prototyping stalls, or as material to fold in later.

---

## 7. Deep Dive: The Archive of Impossible Things

**One-line pitch:** You discover a mysterious archive containing impossible worlds and inventions, and the deeper you explore, the more you realize someone deliberately built the entire place to lead somewhere.

**Opening feel:** No exposition dump. A mechanical structure wakes. The player stands inside something that feels like museum + laboratory + workshop + impossible architecture. Sample system lines: *"Visitor detected." "Archive integrity: 17%." "Curator status: UNKNOWN."* — the goal is immediate questions, not explanation.

> **⚠ v5 revision needed — vocabulary, not fiction.** §9 (v5) rejects the technological register, and this paragraph is the densest concentration of it in the document: *"a mechanical structure wakes,"* *"laboratory,"* and machine-readable status strings all belong to the sci-fi look now ruled out. The *function* of the opening is right and unchanged — no exposition, immediate questions, a place that is clearly mid-something. What has to change is how it announces itself. A natural-register equivalent would state integrity through the environment rather than a readout: how far the growth has come, how much of a structure is still standing, what has been reclaimed. Law 13 applies — the impossible must arrive in natural vocabulary. **Left as an explicit open item rather than rewritten on the spot, because the opening is the single most-read minute of the game and deserves its own pass.**
>
> **→ That pass now exists.** [game-flow.md](game-flow.md) §3 proposes **deleting the text entirely** rather than translating it, on the grounds that a status readout is a machine describing itself — the exact register §9 rejects — while a structure half-eaten by moss carries the same information with no narrator. Awaiting sign-off; accepting it closes this item and the matching entry in §19.

**The Archive as a real place, not a corridor:** a recognizable Central Archive hub with branches/wings, layers beneath the surface, and eventually a Deep Archive. The hub is one of the strongest elements to treat as locked.

### Governing fiction (new in v4): the exhibits are unfinished, not broken

**The rule:** every machine in the Archive works perfectly up to the interesting part — and then simply stops. Nothing here is damaged, decayed, or sabotaged. It was left at the exact point where its unanswered question got answered.

This is the single highest-value structural decision to come out of the interviews, because one rule does an unusual amount of work at once:

- **Explains the opening with zero exposition.** *"Archive integrity: 17%"* stops being a hook that needs justifying and becomes a literal, honest status report.
- **Generates gameplay for free.** The player's job is to finish what the Curator lost interest in. Every exhibit ships with a built-in reason for the player to be there.
- **Makes the Curator legible without dialogue.** You read a personality off what they chose to leave undone — which suits a Curator who is permanently absent and known only through traces.
- **Absorbs §6 Idea #1** ("The Thing You Left Behind"), which was never discarded. It's now the world's premise rather than a competing direction.
- **Gives the Deep Archive a meaning.** It's where the things that were never returned to ended up.
- **Is undecodable during play.** A player cannot reverse-engineer this into a fact about a real person. It only lands in portfolio mode. Exactly the hidden-layer model this project wants.

Practical consequence for building: an exhibit's greybox should be authored as *"here is a machine that does something fascinating, and here is where it gives up."* The stopping point is the level design.

**Example archive exhibits explored** (raw material for Phase 10 prototyping — *not final games*):

| Exhibit | Gameplay feel |
|---|---|
| **Scale / Miniature Island** | A glass-contained miniature world mirrors the player; entering it shrinks the character into the island, which becomes a traversal/platforming space |
| **Gravity Archive** | Gravity rotates 90° at a time, moving player and objects across walls/ceilings; escalates into launching, falling objects, larger room rotations |
| **Duplication Archive** | A machine copies objects; grows from a practical puzzle tool into chaos, potentially letting the player duplicate themselves and coordinate multiple versions |
| **Time Archive** | Advance/freeze/rewind controls; puzzles about being in the correct state/timeline rather than ordinary platforming |
| **Mirror Archive** | The reflection stops behaving normally and becomes a controllable/cooperative second self affecting a parallel mirror world |
| **Music/Sound Archive** | The environment is an instrument — tiles/objects produce notes, sound shapes the world; could become rhythm, melody, or sound-driven traversal |
| **Living Garden Archive** | Plants react to the player or sound; a living maze that can escalate into a chase/escape as growth accelerates |
| **Observatory Archive** | Telescope/observatory where the line between observing space and entering it collapses; small planets, orbits, and local gravity become traversal tools |
| **Deep Archive** | Colder, stripped-back, final destination — mystery, the Curator, and the culmination of everything, not just another exhibit |

---

## 8. Story Shape

| Phase | Function |
|---|---|
| **Act I — Discovery** | Playful impossible exhibits; "what is this place?" |
| **Act II — The Archive reacts** | Rooms shift, previous spaces change, the system addresses the player; "why does this place care about me / who built it?" |
| **Act III — The bottom / Deep Archive** | Deepest layer opens, earlier clues align, Curator space, finale recombining prior ideas/mechanics |
| **Reveal — Curator → portfolio** | The world reveals the person behind it; the real portfolio decodes selected references (a machine, a struggle, a world, a motif) back to something real |

**Curiosity ladder** (each rung should close one question and open a better one):
1. What is this machine/exhibit? → 2. Who built it? → 3. Why were these things collected or hidden? → 4. Why is the Archive changing? → 5. What is at the bottom? → 6. Who is the Curator? → 7. Why do these places now feel connected? → 8. Final reveal: the creator is the person behind the portfolio.

### Archives compound (new in v4) — the connective tissue

**The rule:** each Archive leaves the player holding a **portable capability**. Later Archives require *combining* capabilities earned earlier. The finale needs several at once.

This replaces the vaguest line in the original story shape — Act III "recombining prior ideas/mechanics" — with an actual mechanism, and it **absorbs §6 Idea #4 ("Follow the Thread")**, which was never discarded. The thread is no longer a competing direction; it's how the anthology holds together.

Why it matters more than it looks:

- **It's what stops this being a collection of unrelated minigames.** An anthology without carry-over is a menu. With carry-over it's a game.
- **It justifies the hub.** Returning to the Central Archive means something if you return *changed*.
- **It creates the best kind of player moment** — *"the thing I learned in the first world just saved me here"* — which is precisely what It Takes Two does when it reintroduces earlier verbs late.
- **It carries the hidden layer invisibly.** The player never learns why compounding capability is personally meaningful. It just feels good.

**Two tensions, both real, both resolved:**

| Tension | Resolution |
|---|---|
| Reuse vs. Laws 5 and 10 (don't milk mechanics / comprehension exempts repetition) | A verb returning in a **new context or new combination is escalation, not repetition.** What's banned is re-performing a known verb *unchanged*. Carry-over must always arrive with a twist attached. |
| Carry-over vs. §11's "an Archive is a clean delete" | Capabilities live in a **central registry**, never in Archive-to-Archive dependencies. See §11. |

### Two layers (new in v5) — masterable traversal beneath varied archives

The doc has always specified one layer: constantly changing mechanics, It Takes Two style, nothing overstaying its welcome. Round 4 revealed a second thing wanted just as sincerely — Rocket League, *"one simple idea that becomes extremely fun because of movement, physics and mastery."* Those are opposite design philosophies, so the instinct is to pick one. Don't.

**They occupy different layers:**

| Layer | Register | Rule |
|---|---|---|
| **Traversal** — the hub, the connections between archives, the space between everything | Rocket League: one simple physical system, deep, masterable, never explained | Constant across the whole game. Gets *better* with repetition, never replaced. |
| **Archives** — the exhibits themselves | It Takes Two / Split Fiction: varied, surprising, discarded before they wear out | Changes every time, per Law 5. |

Why this matters beyond taste: **it fixes a structural problem the doc already had.** A hub-and-spoke layout forces repeated transit, and Law 10 says that once a player understands something, repeating it is boring. That's a real conflict — unless the transit is *pleasurable to move through* rather than something to solve. Movement-pleasure is the one form of repetition that survives comprehension; it's why Rocket League absorbs thousands of hours with no new mechanics.

**The image to build toward** is a quiet road under a tree canopy — enclosed, continuous, nobody around, and worth walking or cycling for its own sake. Not a corridor between content. The passage *is* content.

⚠ Consequence for Step 1: "movement must feel good before anything else exists" was already the plan, but it was being treated as hygiene. It's now a **headline feature** and deserves proportionally more time — including whatever gives movement a skill ceiling (momentum, slope carry, a traversal verb worth getting good at), not merely competent walk-and-jump.

---

## 9. Theme/Identity Per Archive — RE-RESOLVED (v5)

**Visual DNA rule:** reuse ~60–70% of a master Archive architecture/prop kit; give each world ~30–40% unique identity. Proposed colour/identity assignments, revised in v5 toward a natural palette:

- Central Archive — stone, moss and warm daylight; orderly but reclaimed; one iconic hero structure
- Surreal/scale archive — cool green-blue, altered scale or physics, expressed through terrain and growth
- Mechanical/time-like world — amber and weathered wood; wear, sediment and slow motion rather than gears and brass
- Music-like world — light and vegetation responding; expressive *movement*, not glowing surfaces
- Living/garden-like world — full green, sunlight through canopy, spreading growth (now a leading candidate, not a marginal one)
- Observatory/cosmic world — night sky over open natural ground; huge perceived scale from emptiness, not from technology
- Deep Archive — colder, sparser, bare rock and still water; intentionally less decorative

### The v4 decision is reversed

**v4 resolved this as option (b): organic-heavy worlds retired for v1, on the grounds that scripted Blender cannot produce convincing vegetation.** Round 4 of the personal-layer interview then established that natural, weathered, environmental space is the actual aesthetic preference, and that futuristic-mechanical is a stated *anti*-goal — *"I don't want the game to look like a sci-fi lab full of holograms, neon strips, glowing circuitry and metallic machinery everywhere."*

Both positions cannot stand. This is not a case of taste overriding engineering — it's that **the v4 argument was correct about its mechanism and wrong in its conclusion.** It generalised from a narrow true premise ("scripting cannot author a convincing individual plant") to a much broader claim ("therefore the aesthetic must be museum and machinery"). Three things break that inference:

1. **Scattering is not sculpting.** The hard part of a forest is authoring one good tree — and scripted Blender is *excellent* at the other part: distributing, instancing, randomising rotation and scale, and placing along curves. Individual plants come from free CC0 sources, exactly as the player character already does. Nothing new is being conceded here; it's the same sourced-vs-scripted split applied to one more asset class.
2. **Rock, terrain, worn stone and eroded ground are among the *easiest* things to script**, not the hardest — noise displacement on a subdivided mesh, plus boolean and bevel, gets there directly. The stated material preferences (rock, soil, bark, moss, uneven ground, no perfect symmetry) sit almost entirely inside what `bpy` does well. What scripting genuinely can't do is *soft* organics: cloth, creatures, hair, and anything needing hand-painted texture.
3. **The expensive part of a forest is a runtime problem, not a production problem** — and v4 conflated the two. See the risk below.

### The corrected split

| Category | Source | Notes |
|---|---|---|
| Architecture, structures, machinery | Scripted `bpy` | Unchanged |
| **Rock, cliffs, terrain, eroded and worn surfaces, water planes** | **Scripted `bpy`** | Noise displacement; this is a strength, not a compromise |
| **Placement and scatter of everything** | **Scripted `bpy`** | Instanced distribution is what scripting is best at |
| **Trees, plants, foliage cards** | **Free CC0** (Quaternius, Poly Haven textures) | Same principle as the character |
| Player character, rigged/animated assets | Free CC0 (Quaternius, Mixamo) | Unchanged |
| Cloth, creatures, hair, hand-painted texture | **Avoid entirely** | The real boundary of the pipeline |

### Stylized-natural, not photoreal-natural — and this part is non-negotiable

The strongest surviving argument from v4 is one it never actually made: **geometric styles forgive inexperienced execution and naturalistic styles expose it.** A slightly-wrong clean arch reads as stylistic. A slightly-wrong tree reads as broken. For a first-time 3D developer this is a real hazard, and it is the reason the direction is *stylized* natural — simple flat materials, strong silhouettes, colour and light carrying the image, no photoreal surface detail. Reference register: Journey, Sable, RiME, Breath of the Wild. Not Unreal-forest realism, which is unreachable here and would look worse the closer it got.

Conveniently, the stated lighting preference points the same way: soft, diffuse, dappled daylight, *"nothing too theatrical."*

### The new risk this introduces — state it plainly

**Alpha overdraw.** Foliage is transparent cards, transparent cards are fill-rate, and fill-rate is exactly what Iris Xe and weak phones have least of. This is a genuine new cost that the museum-and-machinery direction did not carry. Mitigations, all known but none yet proven here: alpha-*test* rather than alpha-blend, instanced cross-cards, aggressive exponential fog to cut draw distance, tight canopy layering, and the existing DPR cap doing double duty. Tracked in `technical-production-spec.md` §4.5, and **this is now what Step 2.5 must test** — per §16, prototype the assumption that can kill it.

### What still stands from v4

- The paid Temple asset pack reference stays dropped — it was a budget item, and that reason is unaffected.
- The player character still comes from a free rigged source.
- **§7's opening feel needs revising**: *"museum + laboratory + workshop + impossible architecture"* and the system line *"Archive integrity: 17%"* both now read as the technological register this section just rejected. Flagged in §7; the fiction survives, the vocabulary doesn't.

---

## 10. Web Performance Strategy

**Core principle:** never load or render the entire game at once. Only the current environment is fully resident; the next preloads quietly while the previous one is disposed.

| Technique | Why it matters |
|---|---|
| Scene streaming | Treat each Archive as a level: load current → preload next → dispose previous |
| Diegetic loading | Elevators, doors, portals, tunnels, shrinking sequences, blackouts double as disguised loading boundaries |
| Stylized HD over photoreal | Strong composition/lighting/materials/hero objects/atmosphere reads as expensive without extreme geometry |
| Instancing | Reuse columns, shelves, lamps, gears, books, plants via GPU-friendly instancing |
| LOD | High-detail near camera, simpler silhouettes farther away |
| Texture strategy | Selective 1K–2K; higher resolution only for true hero objects; atlases for repeated props |
| KTX2/Basis textures | GPU-friendly compressed texture pipeline — needs a KTX2Loader + Basis transcoder worker in the Three.js setup, a bit more pipeline work than plain compressed images, but meaningfully smaller download/VRAM footprint |
| GLB + Meshopt/Draco | Compress model geometry |
| Baked lighting | Bake GI/static shadows for architecture; real-time lights reserved for the player, hero machines, interactive objects |
| Cheap "expensive" effects | Emissive + bloom, fog, particles, baked reflections/environment maps, careful color grading |
| Sight-line control | Architecture + fog make the world feel huge without needing kilometers of simultaneously visible geometry |
| Graphics tiers | High/Medium/Low so an RTX desktop and an older integrated-graphics laptop can both play |
| Graceful fallback | Devices that can't run the game well get the normal professional portfolio directly |

**Performance budget — TIGHTENED (v4).** The baseline device is now known: the dev machine is **Intel Iris Xe integrated graphics** (i5-1240P, 16 GB RAM, no discrete GPU). That's a deliberate advantage — perf discipline gets enforced by hardware instead of willpower. Full detail in [technical-production-spec.md](technical-production-spec.md).

| Metric | Target | Change from v3 |
|---|---|---|
| **Draw calls per scene** | **< 150** (ideal < 100) | **New — this is the actual bottleneck, not triangles** |
| Visible triangles | < 300 K | New |
| Initial playable download | **≤ 8 MB** | ↓ from ~10–20 MB |
| Individual archive | **≤ 10 MB** compressed | ↓ from ~10–30 MB (30 MB was 30 s on 4G) |
| Full-quality environments resident at once | 1 | unchanged — now a *hard* rule, enforced with real `dispose()` |
| Next environment | Lightweight/preloaded only | unchanged |
| Main texture resolution | 1 K atlas per room | clarified: atlas, not per-object |
| Hero textures | Selective 2 K | 4 K dropped entirely |
| Target FPS / fallback FPS | 60 / 30 | unchanged |
| Dynamic lights | **0–1** | ↓ from "very few" |
| **Real-time shadow maps** | **0** — blob shadow instead | **New** |
| **Device pixel ratio** | capped **1.0–1.5** | **New — biggest single perf knob on integrated GPUs** |
| **Postprocessing passes** | ≤ 2 | **New** |
| Static lighting | Baked (Cycles → lightmaps, rendered unlit) | unchanged, now specified |
| Geometry | LOD + modular reuse + instancing | unchanged |
| Model format | GLB + **Meshopt** | Meshopt chosen over Draco: faster decode, better with instancing/animation |
| Texture compression | KTX2 — **ETC1S** colour, **UASTC** normals | specified |

---

## 11. System Architecture

```
Website / React shell
├─ Game Core
│  ├─ Character & camera
│  ├─ Physics
│  ├─ Interactions
│  ├─ Audio
│  └─ Shared effects/UI
├─ Scene / Archive Manager
│  ├─ Load current archive
│  ├─ Preload next
│  ├─ Dispose previous
│  └─ Cache shared assets
├─ Story Manager
│  ├─ Clues
│  ├─ Unlocks
│  └─ Hub/world changes
├─ Progress / Save State
└─ Professional Portfolio
```

Every Archive is a self-contained module with a simple lifecycle: `enter() / start() / complete() / fail() / reset() / exit()`, exposing `archiveId / completed / storyFragment / nextUnlock`. The core game never needs to know what gameplay happens inside — a mediocre Archive is a delete, not a rewrite.

**Why modularity is essential:** the games are still being ideated. The architecture must let us replace a mediocre Archive later without rewriting the hub, save system, story state, or professional portfolio.

**Capability registry (new in v4).** §8's compounding rule would normally destroy the deletability above — if Archive C's puzzle needs "the thing you learned in Archive A," deleting A breaks C. So capabilities never pass Archive-to-Archive. Instead:

- A central `capabilities` store holds granted capabilities as flat data (`{ id, grantedBy, verb }`).
- An Archive **declares what it grants** on `complete()` and **declares what it requires** to unlock. It never names another Archive.
- An Archive with unmet requirements simply stays locked; the hub reads the registry, not the Archive list.
- Deleting an Archive therefore only removes its grant. Anything that required it becomes unreachable rather than broken — and re-granting that capability from a different Archive fixes it with a one-line change.

Same idea as a permissions system: rooms check for a key, not for who gave it out.

## 12. Reusable Kits

- **Architecture kit** — walls, columns, arches, stairs, railings, floors, doors, windows
- **Archive props** — desks, books, lamps, crates, shelves, instruments, machinery, display cases
- **Mechanical kit** — gears, rings, pipes, pistons, cables, energy cores
- **Nature kit** — *restored to a first-class kit in v5 (see §9).* Rock, cliffs, terrain, eroded ground, water planes and all scatter/placement are scripted in `bpy`; trees, plants and foliage cards come from free CC0 sources. On current direction this is likely the **most-used kit in the game**, not an accent.
- **Weathering set** — a shared vocabulary for Law 14's gradual evolution: moss spread, wear on stone, root intrusion, sediment, reclaimed edges, deepening growth. Authored as instanced scatter plus material tint so **one room can be re-dressed at several stages of overgrowth without new geometry** — which is what makes a visibly evolving world affordable.

Each world = reusable kit + a small number of unique hero assets + one dominant identity (Section 9).

## 13. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Rendering | Three.js r185 + React Three Fiber, **`WebGLRenderer` / WebGL2** | Dominant ecosystem; R3F is the declarative-3D standard for React. **v4 correction:** the earlier note that "WebGPU is now baseline everywhere" was wrong — see the resolved row below. |
| Physics + character controller | `@react-three/rapier` + `ecctrl` | Capsule colliders, floating-character physics, keyboard *and* touch controls, animation-state syncing, follow camera, out of the box |
| State | `zustand` | Maps directly onto the Progress/Save State system above |
| Geometry compression | Draco/Meshopt via `gltf-pipeline`/`gltf-transform` | Keeps reusable kits fast to load |
| Texture compression | KTX2/Basis Universal | Needs KTX2Loader + Basis transcoder worker; smaller VRAM/download footprint |
| Framework | **Vite + React** | **RESOLVED (v4).** Next.js's SSR/SEO buys nothing for a WebGL canvas; the portfolio text pages are the only SEO-relevant surface and can be static or pre-rendered. Vite's faster iteration matters at 12 hrs/week. |
| Hosting | Vercel or Netlify | CDN-backed, generous free tiers |
| Save system | `localStorage` | `completedArchives`, `unlockedArchives`, `storyProgress`, `settings`, `graphicsPreset`, `portfolioUnlocked` — no login, no database needed initially |
| Renderer choice (WebGPU vs WebGL2-first) | **WebGL2-first** | **RESOLVED (v4).** WebGL2 is at 95.73% global support (StatCounter, July 2026); WebGPU at 85.56% — but **Firefox ships it in no version** (flag-gated through 157) and desktop Safari is only *partial* from 26. A portfolio cannot show a recruiter on Firefox a black screen. Separately, three.js r183 (Feb 2026) renamed `PostProcessing`→`RenderPipeline` and `Nodes`→`NodeManager`; the WebGPU/TSL stack is still churning. Revisit only if an effect genuinely needs compute. |

**Reference repos:** https://github.com/adrianhajdin/project_3D_developer_portfolio · https://github.com/adrianhajdin/threejs-portfolio
**Character controller:** https://github.com/pmndrs/ecctrl · live touch demo: https://ecctrl.app/ · tutorial: https://wawasensei.dev/tuto/third-person-controller-react-three-fiber-tutorial
Actively maintained under pmndrs. Peers: `three` 0.184+, `@react-three/fiber` 9.4+, `@react-three/rapier` 2.2+. Ships DOM-based touch controls (`<Joystick />`, `<VirtualButton />`) from the `ecctrl/input` subpath — so phone input is largely free.

**Asset sources (v4 — zero budget):** environment geometry scripted in Blender via `bpy` · player character from Quaternius (CC0) or Mixamo (free rigs + animations, which also supply the clips `ecctrl` syncs) · HDRIs and surface textures from Poly Haven (CC0).
*The paid Temple pack previously referenced here is dropped — see §9.*

## 14. Device Independence

| Tier | Experience |
|---|---|
| Desktop | Full game |
| Powerful tablet/mobile | Touch controls + reduced effects |
| Weak device | Reduced graphics |
| Doesn't support the game well | Professional portfolio immediately available |

No visitor should ever hit a wall that blocks them from the actual content.

## 15. Audio

First-class system, not an afterthought — sound can make the game feel significantly more expensive than it is: footsteps, machinery/ambient soundscapes, spatial audio, distant Archive noises, UI feedback, portal sounds, short musical motifs per Archive, deliberate silence where it earns weight.

## 16. Quality Rules for Future Archives

Every major Archive should satisfy most of:
- Introduces a clear primary mechanic quickly (~30–60 seconds to understand)
- Fun even without knowing the story
- Strong visual or mechanical identity distinct from the previous Archive
- At least one escalation or twist
- At least one memorable payoff/set-piece if scope allows
- Resets quickly after failure — frustration shouldn't kill curiosity
- No mechanic gets more content just because it was expensive to build
- Can be removed or replaced cleanly if playtesting says it isn't fun

**Process rule:** every new Archive starts as an ugly greybox (no art) to test whether the mechanic is fun *before* any environment art is built.

**Two more process rules (new in v4):**

**The stranger test.** Before an Archive gets art, answer honestly: *"if someone else had built this, would I want to explore it?"* Not "is it clever," not "does it mean something" — would I keep playing. This is the only reliable filter against the failure mode this whole project is most exposed to: a room that is interesting to the person who made it and inert to everyone else. Where possible, hand it to an actual stranger with zero explanation and watch (see also the Step 7 verification rule).

**Prototype the killing assumption first.** Every Archive rests on one assumption that, if wrong, invalidates the whole room — a mechanic that isn't readable without text, a physics behaviour rapier won't do stably, a mobile input that needs precision touch can't deliver, an art form that scripted Blender can't produce. Identify that assumption *before* building, and build the ugliest possible test of it first. Never polish outward from an untested centre.

*(This rule is why Step 2.5 exists: the art pipeline is the killing assumption for the entire project, so it gets tested before any content depends on it.)*

**Three more process rules (new in v5):**

**Satisfying the requirements is not the same as being good.** This document is now long, and every law and budget in it is defensible — which is exactly the condition under which a thing can be fully *compliant* and still dead. So: **lock the mandatory requirements early and deliberately reserve time for one or two ideas that go beyond them.** Not leftover time — reserved time, protected in advance. An archive that ticks every box in this section and adds nothing of its own has failed, and this section cannot detect that. Re-read this rule before building each archive.

**Watch for interaction, not compliments.** The observable form of the stranger test. When someone plays it, *"that looks good"* is the **null result** — it means nothing landed. What counts is whether they start doing things you didn't prompt, poke at the system to see what else it responds to, or begin proposing what it could also do. Someone reaching for the thing unprompted is the only reliable signal; anything they say about it is not.

**Spend on what the player perceives.** From Law 15. Given a choice between deepening internal structure and improving how something feels to do, the second wins every time. The architecture exists to make the game changeable, not to be admired.

---

## 17. Development Roadmap — REVISED (v4)

Restructured for the real constraint: 10–15 hrs/week, learning Three.js/R3F/physics while building, zero budget. **Two structural changes.** First, the art-pipeline spike moves from old-Phase-8 to Step 2.5 — the no-budget scripted-Blender pipeline is the least-proven part of this project, everything visual depends on whether it works, and proving it early also produces the first genuinely good-looking thing, which matters for momentum over a 9-month build. Second (new in v5), **Step 8 is a vertical slice rather than "build all three archives"** — one archive taken all the way through to a portfolio callback before the other two begin.

Every step must end in something runnable and visible. No step is allowed to be pure plumbing with no on-screen payoff — that's the main defence against learning-curve stalls.

| Step | Build | Why now |
|---|---|---|
| 0 | Repo scaffold: Vite + React + R3F + rapier + zustand, `git init`, deploy-to-Vercel smoke test | Prove the whole chain end-to-end while it's trivial to debug |
| 1 | Grey room + `ecctrl` character + camera + collisions + one interactable — **plus a real pass on movement feel and skill ceiling** (§8 two-layer model) | Traversal is a headline feature in v5, not hygiene. Momentum, slope carry, something worth getting good at. |
| 2 | Touch controls + tier system + `PerformanceMonitor` + dev perf HUD | Cheap now, painful to retrofit; also enables real-phone testing from day one |
| **2.5** | **Art-pipeline spike — retargeted in v5 to the hard case.** Install Blender; script an **outdoor canopy-road segment**: displaced rock/terrain, instanced CC0 foliage as alpha-tested cross-cards, one water plane, Cycles bake of dappled daylight, `TEXCOORD_1` export, `gltf-transform` → Meshopt + KTX2, load in-browser | **Highest-value de-risking step in the plan.** v4 planned an interior modular room — the easy case. §9 (v5) makes foliage overdraw the project's killing assumption, and §16 says test that first. |
| 3 | Interaction framework — button, lever, pickup, door, portal, inspectable | Generic, reused by every archive (old Phase 3) |
| 4 | Greybox Central Archive hub + locked doors + transitions + return flow | old Phase 4 |
| 5 | Scene streaming + `dispose()` discipline + diegetic loading | Enforce the memory rule *before* there's content to leak (old Phases 6 + 10) |
| 6 | Save/progression via `localStorage` + settings | old Phase 7 |
| 7 | Candidate-mechanic toys — throwaway greybox toys in one grey room, hours each, **not levels** | Judge fun before art (old Phase 10, compressed — full greybox levels are too expensive at this time budget) |
| **8** | **Vertical slice — archive #1 only, all the way through.** Build the one winning mechanic, grant its capability, return to a **visibly changed** hub (Law 14), and wire **one real portfolio callback** plus the skip-to-portfolio path | **New in v5.** Proves the entire chain end-to-end while only one archive's worth of work is at risk. See below. |
| 9 | Archives #2 and #3, now that the chain is proven | The chain is a known quantity; these are content, not architecture |
| 10 | Portfolio mode completed — remaining callbacks, professional pages, fallback path | old Phase 15, minus the callback already built at Step 8 |
| 11 | Audio, polish, perf pass, playtest, release | old Phases 16–19 |

**Why Step 8 is a vertical slice (new in v5).** The v4 roadmap was horizontal: build all the infrastructure, then all three archives, then portfolio mode. That defers the full chain — hub → archive → capability granted → changed hub → portfolio callback — until very late, and a flaw anywhere in it would then be discovered with three archives already built on top of the flaw. Building it once, narrow and complete, means any structural problem surfaces when the cost of fixing it is one archive rather than three.

This is a rule taken directly from hackathon experience: *five impressive half-built features are useless if you can't demonstrate any one of them properly.* One complete flow first.

**Where we are:** pre-Step-0. **The interview phase is complete (5 rounds).** The remaining ideation work is the two-pool collision process in §18 — which happens alongside building, not before it. **Immediate next action is Step 0.**

**Step 2.5 acceptance criteria (v5):** a scripted, baked, KTX2-compressed outdoor canopy segment that (a) looks good enough to be proud of, (b) holds 60 fps on Iris Xe at DPR 1.25 **and 30 fps on a real mid-range phone**, (c) is ≤ 3 MB, (d) is under 100 draw calls. If foliage overdraw fails these, the fallback is not a return to v4's machinery aesthetic — it's *sparser* nature: open rock, fewer and larger plants, distance handled by fog rather than by canopy depth.

*The original 19-phase roadmap is preserved in Appendix C.*

---

## 18. Personal Layer: Interview Process (new in v4)

Design Law #3 says *fun mechanic first, symbolic mapping second*. So this process must **not** be "motif → invent a mechanic to match it" — that is precisely how forced, unfun puzzles get made. Two pools get generated independently, and only natural collisions survive.

| Round | Territory |
|---|---|
| **1 — Formative** | Childhood obsessions. What got taken apart. What got built that nobody asked for. What you were bad at. What you quit, and what you came back to. |
| **2 — Working style** | How you attack a problem you don't understand. What you do when stuck. What kind of problem delights you. What bores you instantly. What you do that others find strange. |
| **3 — Turning points** | Struggles that changed how you think. What you're proud of that nobody noticed. Something you had wrong for a long time. |
| **4 — Texture & taste** | Objects, places, sounds, materials, films, games, music that feel like *you*. Recurring images. What you find beautiful. |

Then:

1. Extract **5–8 recurring motifs** — patterns, not biography.
2. Separately, assemble a pool of **candidate mechanics chosen purely for fun**, filtered by three hard constraints: mobile-safe (no pixel-perfect platforming, twitch aiming, fast camera flicks or multi-key chords), producible in scripted Blender (§9), and satisfying §16.
3. **Find the collisions** — where a genuinely fun mechanic happens to embody a motif. Forced pairings get dropped, per Law #6.
4. Shortlist 4–5 → build as Step 7 toys → keep the 3 that are actually fun.
5. Map survivors to portfolio callbacks **last**, working backwards from what the player already experienced.

---

## 19. Decision Matrix: Locked vs. Intentionally Open

**Locked:**
Fun and curiosity as the two primary design goals · personal storytelling indirect and secondary during gameplay · the player is the protagonist, creator/Curator is the mystery · "Archive of Impossible Things" as the leading concrete world concept (Ideas 1, 3, 4 not discarded) · persistent Central Archive hub · multiple radically different playable experiences · third-person character-driven exploration · frequent mechanic change, none overstay their welcome · curiosity-driven story with a Curator and a Deep Archive destination · game → real portfolio transition with callbacks · early skip-to-portfolio path · modular Archive architecture · scene streaming and performance-aware rendering · greybox before polished art · professional portfolio stays accessible on devices that can't run the full game.

**Newly locked in v4:**
**v1 ships with 3 archives** (more as post-launch additions) · **hard-surface/architectural art identity, organic-heavy worlds retired for v1** (§9) · **Vite + React** (§13) · **WebGL2-first with `WebGLRenderer`** (§13) · **tightened perf budgets incl. 0 shadow maps, DPR cap 1.0–1.5, <150 draw calls** (§10) · **Iris Xe integrated graphics as the baseline target device** · **three device tiers with measured (not sniffed) detection + continuous degradation** · **environment geometry scripted in Blender, character from free CC sources** (§13) · **art-pipeline spike moved early to Step 2.5** (§17) · **mobile-safety as a design constraint on mechanic selection** — rules out pixel-perfect platforming, twitch aiming, fast camera flicks, multi-key chords · **two-pool interview process for the personal layer** (§18).

**Locked after the Round 2 interview:**
**Design Laws 8–12** (§5) — teach by perturbation, telegraph one-step-away, comprehension exempts repetition, no punishment, tension from inexplicable success · **the governing fiction: exhibits are unfinished, not broken** (§7) · **no combat, no death, no game-over, no timers** — previously open, now closed · **§6 Idea #1 ("The Thing You Left Behind") absorbed into the world premise** rather than remaining a competing direction · **the Curator is permanently absent, known only through traces** · **the anthology structure itself carries the personal layer**, which means individual archives are under no obligation to mean anything.

**Locked after the Round 3 interview:**
**Archives compound — each grants a portable capability, later archives require combinations, the finale requires several** (§8) · **§6 Idea #4 ("Follow the Thread") absorbed as the anthology's connective tissue** rather than remaining a competing direction · **capabilities live in a central registry so compounding doesn't cost archive deletability** (§11) · **the stranger test** — *"would I explore this if someone else built it?"* — as a gate before art (§16) · **prototype the killing assumption before polishing around it** (§16).

**Locked after the Round 4 interview (v5) — including one reversal:**
**Art direction is stylized natural, not hard-surface/mechanical** (§9) — *this reverses the v4 §9 resolution*; the production argument behind it was over-generalised, and the futuristic look is a stated anti-goal · **Laws 13–14** (§5) — natural-impossible never tech-impossible with diffuse natural light; the world evolves gradually in response to what happened · **two-layer design** (§8) — a simple masterable traversal system that never changes, beneath archives that change constantly · **traversal promoted to a headline feature**, which is what resolves the hub-transit-vs-Law-10 conflict · **Nature kit restored to first-class, plus a weathering set** (§12) · **corrected scripted-vs-sourced split** — terrain, rock, erosion and all scatter are scripted; trees and plants come from CC0 like the character; cloth, creatures and hair avoided entirely (§9) · **Step 2.5 retargeted to the outdoor canopy case** because foliage overdraw is now the project's killing assumption (§17) · **no personal-object symbolism in the art** — declined outright by the user, the cycle included.

**Locked after the Round 5 interview (v5):**
**Law 15 — the player meets behaviour, not architecture** (§5), with its corollary that internal elegance the visitor never perceives is not worth time · **Step 8 is a vertical slice** — archive #1 runs all the way through to a changed hub and one real portfolio callback before archives #2 and #3 begin (§17) · **lock requirements early, then reserve protected time for ideas beyond them** — compliance with this document is not the same as being good (§16) · **watch for unprompted interaction, not compliments** — *"that looks good"* is the null result (§16) · **spend on what the player perceives** (§16).

**Intentionally open (should emerge from prototypes, not be picked now):** Exact mini-games/mechanics · exact Archive order · whether the nine example exhibits (Scale, Gravity, Duplication, Time, Mirror, Sound, Garden, Observatory) survive — note **Scale/Miniature Island is now flagged as the one mobile-risky candidate**, since it's specified as a platforming space, and **Living Garden is upgraded from marginal to a leading candidate** by §9 (v5) · exact personal mapping per world · final character design · final Archive names · finale mechanic · whether all Archives are mandatory · exact ending dialogue · which archives get added after v1 · which capabilities each archive grants, and what the finale combines (follows from §8, but the specific verbs wait for the Step 7 toys) · **the traversal verb** that gives movement its skill ceiling.

**Open, but now with a concrete proposal awaiting sign-off:**

| Item | Proposal | Where |
|---|---|---|
| §7's opening vocabulary | Delete the status text entirely rather than translate it | [game-flow.md](game-flow.md) §3 |
| Exact v1 duration | 75–95 minutes | [game-flow.md](game-flow.md) header |
| Camera, palette, fog, canopy dimensions | Specified numerically as starting values, explicitly meant to be revised by what appears on screen | [look-target.md](look-target.md) |

---

## Appendix A — Historical Original Trial Concept (reference only, superseded)

| Old chamber | Old purpose |
|---|---|
| The Sealed Threshold | Rotate rune dials; About/bio |
| The Overgrown Archive | Clear vines from tablets; Projects |
| The Golem's Riddle | Simon-says rune repair; AI/agent projects |
| The Star Chart | Connect stars chronologically; Experience/timeline |
| The Offering Altar | Ceremonial contact form |
| The Crumbling Bridge | Timed/safe-tile traversal; Skills |
| The Ward Trial | Memory pressure-plate path; Security work |

## Appendix B — Visual Explorations Note

Generated concept images (Central Archive hub, Scale/miniature-island exhibit, environment moodboards) were used to test atmosphere and in-game feel only — not to lock exact production assets. Target: strong architecture and atmosphere, implemented with modular geometry, baked light, compressed textures, limited real-time effects, and scene streaming suitable for the web.

## Appendix C — Original 19-Phase Roadmap (superseded by §17 in v4, kept for reference)

| Phase | Build | Purpose |
|---|---|---|
| 0 | Game design bible | Lock principles, not games |
| 1 | Repo + renderer foundation | Technical foundation |
| 2 | Character controller | Make movement feel good before art |
| 3 | Reusable interaction framework | Generic interactables |
| 4 | Greybox Central Archive | Hub, doors, transitions, return flow |
| 5 | Greybox Archive #1 | Prove the full gameplay loop |
| 6 | Scene streaming | Smooth load/unload/preload |
| 7 | Save/progression | Persist state |
| 8 | Visual benchmark | Establish the graphics/performance ceiling |
| 9 | Reusable art kit | Shared architecture, props, machinery, nature |
| 10 | Prototype candidate games | Greybox mechanics; judge on fun before art |
| 11 | Select final Archives | Lock the winning games and sequence |
| 12–14 | Build Acts I, II, III | Opening, escalation, finale |
| 15 | Portfolio mode | Real portfolio + callbacks |
| 16 | Audio/polish | Game feel |
| 17 | Performance pass | LOD, textures, memory, draw calls, presets |
| 18 | Playtesting | Remove boring, confusing, overlong parts |
| 19 | Release | Deployment and fallback validation |

Changes made in v4: visual benchmark pulled forward to Step 2.5 (art pipeline is the biggest unknown); Phase 10 compressed from greybox *levels* to greybox *toys*; Phases 5 and 9 folded into Steps 7 and 2.5 respectively; scope capped at 3 archives for v1.

---

*This document is updated in place as the project develops.*
