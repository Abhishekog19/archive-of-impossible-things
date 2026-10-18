# Interactive portfolio — next production milestone

Status: direction brief and phased build plan, October 18, 2026.

Latest steering: the user accepts the character concept and parks character work.
Start with gameplay experiments in the existing environment; the character phase
below is deferred. **The Remembering Spring** now prototypes the first rule-combining
interaction and Saansation connection. A direct portfolio renders the public
profile and project summaries. See [the prototype review](SPRING_PROTOTYPE_2026-10-18.md).
The other chapter candidates remain unbuilt proposals.

Update: the user supplied public profile/project summaries, now stored in
`src/content/portfolio.json`, and selected the existing explorer evolved into a
Forest Archivist × Ruin Runner. See [the character brief](CHARACTER_EXPLORER_2026-10-18.md).
The website integration has not yet been implemented.

The user considers environment building finished and has authorized gameplay,
personal storytelling, character improvements, sounds and animations between game
moments. Use the existing connected environment. Environment approval is a scope
decision, not a claim that every earlier art, geometry or device target passed.

## Experience direction

Keep the Archive of Impossible Things: a visitor explores a place shaped by its
absent creator. Let the visitor experience a way of thinking, then discover a
specific example from the creator's real work. The player is still the visitor;
the Curator is the creator. A creator-inspired avatar can be chosen without
requiring first-person biography or an on-screen speaking Curator.

Proposed rhythm: **discover → experiment → surprising consequence → personal
connection → real evidence**. Avoid solving a puzzle merely to unlock a skill
label. Each interaction must be enjoyable without its portfolio explanation.
No combat, death, failure timer, grinding or mandatory precision platforming.
Retain the natural visual vocabulary: stone, water, roots, light and wind.

Provide two immediately accessible routes: Explore and View portfolio. Written
projects, résumé and contact information never depend on completing the game.
Keep the essential portfolio readable without starting the WebGL scene.

Propose a 5–8-minute first journey with optional exploration, replacing the old
75–95-minute pacing proposal for this portfolio release. This is a playtest target,
not a promise or an approved change to the entire anthology. Leave the longer
archive structure available for future expansion if the first chapter earns it.

## Candidate chapters — not claims about the creator

| Place / proposed chapter | Visitor action and surprising payoff | Potential personal connection, only if supported by public work |
| --- | --- | --- |
| Hub / The Invitation | Footsteps wake a small water channel; its flow points toward the first discovery. A brief title introduces the Archive. | Name and public role are visible in the portfolio; the world gradually suggests its maker. |
| Forest / A Different Way Through | Redirect one stream among three shallow channels. Water begins climbing a root, bending a branch into a new path. Choices can be reversed immediately. | A project where an unconventional approach solved a real constraint. |
| Archive / More Than the Pieces | Place three stone fragments; each changes the behavior of the others. Their combined shadow becomes a structure the pieces alone do not explain. | A project showing systems thinking, engineering or the combination of design and code. |
| Cavern / What Remains | Carry a behavior learned earlier into the final chamber. Water and reflected light gradually reveal a scene connected to the creator's work. | A short personal statement, selected project evidence and an invitation to collaborate. |

The forest interaction is the recommended first prototype because its cause and
effect can be tested with a few reusable objects in an existing area. Use one
deliberate interaction button and generous targets; no timed camera tricks.
Prototype with moving water markers and a single animated branch before creating
new art. Keep the reveal localized rather than altering existing route colliders.
If people do not voluntarily try a second arrangement, revise the mechanic before
producing its final animation or expanding to another chapter.

These are creative candidates, not three approved mini-games. Preserve the older
design document's rule that mechanics are chosen through playable experiments.
Personal mapping follows the mechanic and the user's real evidence, not generic
labels such as intelligence, creativity or persistence attached without support.

## Production phases and completion criteria

### 1. Character feel and identity

Reopen the existing character review. The current runtime has Idle, Walk, Run,
Jump, Fall and Land clips, gait phase blending, a follow camera and secondary
clothing motion. Existing features are a starting point, not evidence of quality.

- Capture the same short route before/after: idle, start, stop, 90/180-degree
  turn, walk/run change, jump/land, slope and wall approach.
- Check foot sliding against travelled distance; tune clips and blend timing
  together. Improve weight shift, turning and landing recovery without input lag.
- Review silhouette, proportions, face/hair, hands, garment layers and materials
  at gameplay distance plus neutral front/side/back views. Use the approved Ruin
  Runner reference until the user selects a different identity direction.
- Finish one representative animation and deforming garment before expanding
  the clip set. Separate visual rig work from physical controller changes.
- Completion: visibly better gait/turn/contact and a reviewed identity direction,
  with the representative route still walkable. Final likeness needs user review.

### 2. One complete playable chapter

Build hub introduction → one forest interaction → short payoff → one real project
card → return to exploration. Ship the direct portfolio route alongside it.
Do not build all chapters or a general-purpose quest system first.

- A clear nearby interaction prompt, keyboard and touch activation, pause/resume,
  reversible experimentation and a deterministic completed state.
- Show the project's real problem, the creator's contribution, the tradeoff made,
  outcome and public evidence/link. No fabricated metrics or placeholder résumé
  claims in production. Missing content stays out of the public release.
- One versioned local progress record; reload preserves completion, and reset is
  explicit. Chapter completion is independent of whether an animation finishes.
- Completion: a visitor can understand the interaction, reach the payoff, open
  the real project and return; skipping the game reaches the same information.

### 3. Sound and short story transitions

Include basic sound/transition hooks in phase 2; finish the mix and animation here.
Use a small regional palette: hub breeze, forest leaves, cavern water; stone/soil
footsteps; tactile interaction sounds; one restrained musical motif that develops.
Tie footsteps to animation contact events and suppress them when airborne or idle.

Proposed transition: 3–6 seconds of branch/water motion and a gentle camera reveal,
then seamless return to control. Keep an immediate Skip control and a reduced-
motion alternative. Skipping, pausing or leaving must release camera/input locks
and apply the same completed state. No mandatory cinematic before first control.

Start audio after visitor interaction; provide separate music/effects controls,
mute and saved preferences. No essential clue is audio-only. Fade ambience across
areas, limit simultaneous voices and release inactive assets. Track licenses and
attribution before shipping any sourced audio; do not assume generated or found
assets are approved. Spoken narration is optional and not part of the first slice.

### 4. Expand the personal journey

Only after phase 2's complete chapter works, select the next two distinct mechanics.
Carry one earned capability into a later interaction so the chapters feel related.
Connect each chapter to different evidence from the user's public projects or
experience. End with a concise creator reveal and useful contact/project links.
Do not add environment zones merely to create résumé sections.

### 5. Portfolio release review

Check first-time clarity, return visits, skip/reduced-motion behavior, keyboard and
touch access, readable project pages, audio controls and source attribution.
Run the broad performance/deployment check as a batch against the 50–55 FPS target.
Require actual phone evidence for phone claims. Evaluate the complete journey
before adding more content; preserve the existing Vercel deployment workflow.

## Implementation boundaries

Keep new chapter progress/content separate from the existing diagnostic state.
Use the existing React/R3F/Rapier/Zustand stack and streaming boundaries. Integrate
interaction, presentation and completion through a small explicit chapter state
machine. The character/camera must respond to one shared pause/transition policy.
Avoid loading all chapter media at entry; preload only the imminent payoff.

No runtime, model or sound changes were made in this planning pass. No gameplay
or personal facts are claimed to be implemented. The current environment and
uncommitted hub Blender source remain untouched.

## Public content and proposed story connections

Abhishek Pandey is an Electronics and Telecommunication Engineering student,
full-stack developer and technology enthusiast. His stated skills span React,
Next.js, Node.js, Python/Computer Vision, AI integration, embedded systems and
robotics. The audience is recruiters, fellow developers and potential collaborators.
The story should demonstrate curiosity, versatility and learning through building.

| Public project | Candidate story connection | What the project panel may currently say |
| --- | --- | --- |
| Worker–Client Platform | Bringing separate needs together; a chapter about connections and complementary behaviors | Service marketplace with intelligent matching, communication and payments |
| Saansation | Making an invisible natural process understandable; water/light behavior offers a possible visual metaphor | Air-quality dashboard with pollutant visualizations and environmental insights |
| Smart Music Player | Separate elements forming a useful whole; a musical motif could connect discoveries without making hearing mandatory | Local libraries, playlists, Spotify integration and offline functionality |

These metaphors are proposals, not locked puzzles or evidence of undocumented
technical details. Do not infer which stack each project uses from the general
skills list. Links, individual contributions, implementation details and outcomes
have not yet been supplied. Omit them until provided; do not invent success metrics,
clients, users, employment or contact details.

The character choice is settled at the direction level: keep and improve the
explorer using the new hybrid brief. The generated concept and final model still
need visual review. Only user-approved public material goes into copy. The
protected personal source file remains unread and excluded from Git; this plan
does not authorize its use.

Related: [Character review](CHARACTER_REDESIGN.md),
[original design](../archive-of-impossible-things-design-doc.md),
[earlier flow proposal](../game-flow.md),
[latest live performance evidence](VERCEL_RECHECK_2026-10-18.md).
