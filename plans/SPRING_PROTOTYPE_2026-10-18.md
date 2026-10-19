# The Remembering Spring — first playable experiment

October 19 live handoff: Vercel reports successful production deployment of
`70b8b8482cad3b4e022aa4ac9d6ec8c481d7371b` (deployment `7155647203`).
Public experiment: https://archive-of-impossible-things.vercel.app/?chapter=spring&start=forest
Public portfolio: https://archive-of-impossible-things.vercel.app/?portfolio=1

The public production site was checked directly: entry, E/open, premature root
feedback, both lessons and combined root payoff work. The Saansation panel links
to the public portfolio. No captured application errors in this bounded live
check. Evidence: `.artifacts/spring-oct19/vercel-payoff.png`. This confirms the
prototype flow, not its final art quality, enjoyment or sustained FPS.

The user explicitly prioritizes game ideation/environment integration and parks
the accepted explorer concept. This experiment tests one small idea before a full
Archive is built: an ordinary natural material learns behaviors and combines them.

## What to play

Open `?chapter=spring&start=forest`. Walk near the spring on the forest path and
press E or the on-screen Examine button (the existing touch Use input also opens
it). Direct water to leaves or stones; each teaches a visible behavior. The root
only reveals its full response after both lessons. All choices remain repeatable.
Close with Escape or Keep exploring; restart requires a second explicit button
press. Versioned local progress remembers discoveries after reload.

The project connection is available even before completion. It introduces
Saansation using only the user-supplied description, then links to the direct
portfolio at `?portfolio=1#saansation`. The portfolio also includes Worker–Client
Platform and Smart Music Player. No guessed stack per project, project URLs,
contact details, work history or performance metrics have been added.

## Integration and scope

- Opt-in story query; the normal environment has links to the experiment and
  portfolio. Reference/study views do not mount the chapter.
- A shallow spring, three paths, bending leaves, lifted stones and an opening
  leaf use simple runtime geometry. These are prototype props, not final art.
- Props sit on a raycast ground height. First placement intersected foliage;
  moved to clearer paving. The new dressing has no physics colliders and is not
  intended as a platforming obstacle; authored scenery/collision assets are intact.
- Inspection pauses the controller, character and normal camera, uses a dedicated
  camera view, and returns control when closed. Desktop framing leaves room for
  the side panel; narrow framing leaves room for the bottom sheet.
- Water markers are offset above the channels after a check found them hidden
  inside the tubes. The mobile camera was widened to include the whole experiment.
- OS reduced-motion preference removes camera easing, stone bobbing and moving
  water markers; textual responses still carry every rule. No audio dependency.
- Direct portfolio entry imports the page independently of the game module and
  renders no canvas. Unsupported WebGL and the scene error boundary also offer
  the portfolio. Page zoom is enabled; canvas touch behavior remains controlled.
- No character art/gait changes, no generated environment assets, no new package
  dependencies, no sound or authored cinematics in this prototype.

## Verification

The three domain tests cover both lesson orders, premature root attempts,
repetition, completion persistence and malformed/version-mismatched saves. The
existing movement-input and entry tests are included: 10 passing tests total.
Changed JavaScript lint and the final production build pass.

Browser checks cover normal approach/E interaction, premature root feedback,
combining lessons, the visible payoff, persistence on reload, Saansation expansion
and navigation to the written portfolio. At 390 × 844 the experiment fits above
the scrollable sheet; portfolio content has no horizontal overflow and no canvas.
Screenshots are in ignored `.artifacts/spring-oct18/`. Physical phone behavior,
fully controlled FPS and subjective enjoyment are not established by these checks.
Broad performance review remains a separate scheduled batch.

Explicit restart/confirmation, Escape, resumed walking and a second complete
discovery also pass. No captured browser console errors. The desktop test used
the current 762 × 668 panel; the temporary 390 × 844 override was reset afterward.

## Next design decision

Play this as a toy, not as a completed level. Does discovering the combination
make you want to experiment further? If not, change the rule before adding art.
The current three-button interface exposes the choices deliberately; a stronger
version could let visitors redirect the flow physically through nearby objects.

Candidate next experiments (not implemented): Worker–Client Platform could connect
complementary needs across the archive; Smart Music Player could let several
independent natural rhythms form a composition, with visual equivalents for sound.
Retain each mechanic only if it is interesting without the portfolio explanation.
