# Look Target

Companion to [archive-of-impossible-things-design-doc.md](archive-of-impossible-things-design-doc.md) §9
and [technical-production-spec.md](technical-production-spec.md) §4.

The design doc names the direction — *stylized natural, not photoreal natural*.
This turns that into numbers you can build against and measure. Anything here is
overridable, but it has to be overridden **here**, not silently in a scene file.

**Status:** written before Step 1. Every number is a starting value chosen to be
argued with once something is on screen. The ones most likely to move are camera
distance and fog density.

**Visual direction locked 2026-08-25** against the reference set in `concept/`.
The set was measured rather than eyeballed — dominant colours sampled per image and
aggregated by screen area. Result: **the palette below already holds.** Every
mid-tone and dark in the reference set falls within tolerance of §3, which is why
the lock required one added value rather than a repaint. See §3.1 and §11.

**The committed record of the target is [visual-reference-sheet.jpg](visual-reference-sheet.jpg)** —
all 11 unique reference images on one sheet, downsampled to 540 px wide each. The
full-resolution originals in `concept/` are gitignored (23 MB) and exist only on the
authoring machine, so the sheet is what survives a fresh clone. It is encoded at
quality 95 with no chroma subsampling: the brightest 5% of pixels measure luminance
211.1 on both the original sheet and the JPEG, zero drift, so it is safe to sample
against §3 and not just to look at.

---

## 1. The one-sentence version

A quiet road under a canopy, in a place made of stone and moss that the forest has
been slowly taking back — flat colours, soft daylight, distance dissolving into
haze, and nothing anywhere that looks manufactured after the fact.

---

## 2. Camera — decide this first, everything else is downstream

Art direction for a 3D game is a function of the camera. These numbers come first
because the tree spacing, fog distance and canopy height are all *derived* from them.

| Property | Value | Why |
|---|---|---|
| Character height | 1.70 m | Capsule; 0.35 m radius |
| Camera pivot | 1.40 m above feet | Chest height, not head — keeps the horizon high in frame |
| Distance behind pivot | 4.0 m | Close enough to feel the body, far enough to show the road |
| Height above pivot | 0.8 m | → camera sits at **2.2 m** world height |
| Pitch | **−11°** (looking slightly down) | Shallow. A steep angle turns a road into a floor. |
| Vertical FOV | **50°** | three.js `fov` is vertical; phone landscape gets a generous horizontal for free |
| Damping | Yes, ~0.12 lag | Camera should arrive slightly late. Instant cameras feel like drones. |
| Collision | Pull in, never clip | See the clearance rule below |

**Derived rule — canopy clearance ≥ 4.0 m above the camera.** With the camera at
2.2 m, the canopy underside sits at **6.5 m**. Foliage hanging lower than that puts
transparent cards directly across the lens, which is both the ugliest and the most
expensive thing that can happen in this game. Camera clipping into leaves is the
classic bug in canopy scenes; this number exists to prevent it.

**On seeing the canopy:** at FOV 50 with −11° pitch, the top of frame reaches about
14° above horizontal — so you never look straight up at leaves. Enclosure comes
from the canopy *converging ahead of you*, not from overhead. That's cheaper and it
reads better.

---

## 3. Palette — six core values, and a hard rule

**The rule: no colour enters a scene unless it is in this table.** A palette only
works if it's a constraint. Adding a colour means editing this file first.

### Core six

| Role | Hex | Notes |
|---|---|---|
| Sky / fog | `#cfd3c4` | **Fog colour must equal sky colour** or the horizon shows a seam |
| Ground / moss | `#4a5340` | The most-seen surface in the game |
| Canopy (shaded) | `#2f3d28` | Overhead mass |
| Foliage (sunlit) | `#7d9a54` | Where light gets through |
| Stone (lit) | `#a8a394` | Structures, worn paving |
| Warm daylight | `#c8a05a` | Light accent only, never a surface fill |

### Supporting three

| Role | Hex | Notes |
|---|---|---|
| Deep shade | `#12150f` | Already the `theme-color` in `index.html` |
| Water | `#5d7a72` | Channels, still pools |
| Road / worn stone | `#8f8877` | Distinct from structure stone, slightly warmer |

### 3.1 The one value the reference lock added

Measuring `concept/REF*.png` found exactly one gap. The brightest 5% of pixels in
the reference set — the sunlit-stone tier — sits at **luminance 206–222** with
warmth (R−B) of **+16 to +32**. The brightest *surface* in §3 was stone `#a8a394`
at luminance 161. Nothing in the table could carry a lit stone highlight, so sky
was the only bright value on screen.

| Role | Hex | Notes |
|---|---|---|
| **Stone (sunlit)** | `#cdccb6` | **Added 2026-08-25.** Lum 203, warmth +23. Directly sunlit paving and walls only. |

**Ceiling rule: sunlit stone must stay below sky.** Sky `#cfd3c4` is lum 209;
`#cdccb6` is 203. The first candidate sampled straight from the reference set came
out at lum 210 — *above* sky — which inverts the ladder and makes the ground read as
brighter than the air above it. Any future brightening of this value has to move sky
first.

This is why my own generated set read as flat and dead while the reference reads as
flat and *designed*: same palette, no key light. Stone `#a8a394` becomes the **shaded**
stone value, and `#cdccb6` is what the sun does to it. The pair is the whole
warm-light-against-cool-shade idea in §4, expressed as two swatches.

Note `#cdccb6` is a *surface* value, unlike warm daylight `#c8a05a` which stays a
light accent — the reference set's highlights measure at warmth +23, nowhere near
`#c8a05a`'s +110. That much warmth on a large fill would read as sunset.

### Value discipline

Stylized flat colour lives or dies on *value* separation, not hue variety. Ordered
lightest to darkest, with measured luminance, and this order must survive:

```
sky #cfd3c4 209  >  sunlit stone #cdccb6 203  >  stone #a8a394 163
  >  foliage #7d9a54 143  >  road #8f8877 136  >  water #5d7a72 115
  >  ground #4a5340  80  >  canopy #2f3d28  57  >  shade #12150f  20
```

*Corrected 2026-08-25:* this ladder previously put road above foliage. Measured, it's
the other way round — and they sit only **7 luminance apart**, the tightest gap in
the table. A road edge running against sunlit foliage will very nearly lose its
silhouette. Either separate them with the verge (§6 gives 1.0 m of it) or push road
darker. Flagged rather than fixed, because which way to resolve it depends on how the
verge actually reads in the M5 build.

If two adjacent surfaces land on the same value, the silhouette disappears — and
silhouette is doing most of the work in this style.

---

## 4. Light — warm direct, cool fill

The trick that makes flat colours look good is not more colours. It's **warm light
against cool shade.**

| Property | Value |
|---|---|
| Sun elevation | 38° |
| Sun azimuth | Roughly along the road, so light rakes down its length rather than across it |
| Sun colour | `#ffe9c4` warm |
| Sky / ambient fill | `#b8c9d4` cool |
| Runtime lights in the shipped game | **0** — everything baked (spec §4.1) |
| Runtime lights in the blockout | 1 hemisphere light, temporary |

Shade should be *cooler* than light, never just darker. A surface in shadow tinted
toward blue reads as daylight; the same surface merely darkened reads as dirty.

**Explicitly ruled out:** theatrical lighting, hard rim lights, coloured spot
lights, anything dramatic. Round 4: *"nothing too theatrical."*

---

## 5. Fog — three jobs at once

Exponential fog (`FogExp2`) sets mood, hides the draw-distance cutoff, and cuts
fill cost. It's the highest-value single setting in the scene.

`fogFactor = 1 − exp(−(density × depth)²)`

| Tier | Density | ~95% opaque at | Haze at 18 m |
|---|---|---|---|
| High | 0.030 | 58 m | 25% |
| **Medium (baseline)** | **0.038** | **46 m** | **37%** |
| Low | 0.050 | 35 m | 55% |

Fog density is the best mobile knob after DPR, because reducing it removes work
without removing any asset — it just stops distant geometry mattering. Pair it with
a matching camera `far` plane so nothing is drawn that fog has already erased.

**Fog colour = `#cfd3c4`, identical to sky.** Non-negotiable.

---

## 6. The canopy road — buildable dimensions

Derived from the camera, the fog and the clearance rule.

| Element | Value | Notes |
|---|---|---|
| Walkable road width | 4.5 m | Wide enough not to feel like a corridor |
| Soft verge each side | 1.0 m | Transition from road to undergrowth |
| Trunk line | ±3.5 m from centreline | |
| Trunk spacing along road | 6–9 m, randomised | **Never regular.** Round 4: no perfect symmetry. |
| Canopy underside | 6.5 m | Camera clearance rule, §2 |
| Canopy layers over the road | **2** (absolute max 3) | Spec §4.6 caps transparency depth at 3 |
| Road curvature | Never more than ~30 m of straight visible | You should always be walking toward something you can't see yet |
| Road grade | ≤ 8% | Comfortable to travel continuously |
| Visible tree pairs ahead | ~6 | Falls out of 46 m fog ÷ 7.5 m spacing |

That last row is the useful one: **fog distance and tree spacing together decide
how many trees exist on screen.** Six pairs is a dozen trunks and two canopy
layers — which is a scene that can hold 30 fps on a phone.

### Ground irregularity

Round 4 asked for uneven natural surfaces. There's a limit, and it's a movement
limit, not a visual one:

| Surface | Noise amplitude | Why |
|---|---|---|
| Walkable road | **±0.25 m**, low frequency | More than this and the character controller fights the ground |
| Verges | ±0.8 m | |
| Off-road terrain | ±1.5 m+ | Free to be as rough as it likes |

The road should read as uneven and *feel* smooth. Those are different jobs — do the
first with texture, shading and edge irregularity, not with geometry the player's
feet have to negotiate.

---

## 7. Effects, in the order they get built

From spec §4.3, cheapest and most valuable first. Anything below the line is
optional and gets cut without argument.

| # | Effect | How it's done | Cost |
|---|---|---|---|
| 1 | Baked light and AO | Cycles lightmap → `MeshBasicMaterial` + `lightMap` | Zero at runtime |
| 2 | Dappled canopy light | A scrolling/breathing **texture**, not lights | One texture lookup |
| 3 | Light shafts | Additive transparent planes, soft gradient | ~2 draw calls |
| 4 | Fog | `FogExp2` | Negative — saves work |
| 5 | Wind sway | Vertex shader on foliage | Zero CPU |
| 6 | Dust / pollen motes | Small particle system | Near-free, disproportionate life |
| 7 | Vignette + LUT grade | One post pass | Cheap |
| — | *— line —* | | |
| 8 | Selective bloom | Sparingly | **Demoted in v5** — bloom is what makes things read as sci-fi |

**Contact shadow:** a soft radial-gradient blob decal under the character. One
transparent quad. Zero real-time shadow maps in the entire game (spec §4.2).

---

## 8. Reference register — what to take, specifically

Named so the target is checkable, not vibes. The instruction is *take this one
thing*, not *look like this game*.

| Reference | Take exactly this | Don't take |
|---|---|---|
| **Sable** | Flat unlit colour fills with hard-edged shade shapes; how few colours a scene needs | Its outlines / comic register |
| **Journey** | Distance handled entirely by atmosphere; scale from emptiness | Sand shader complexity |
| **RiME** | Warm stone against cool shade; ruins that are reclaimed rather than broken | Its high colour saturation |
| **Breath of the Wild** | Canopy and grass as flat instanced cards; wind as motion, not detail | Its scale, art headcount, and shader budget |

### Anti-goals — stated, because they're the failure modes

Neon · holograms · glowing circuitry · metallic machinery · visible UI in the world ·
status readouts · lens flares · chromatic aberration · heavy bloom · photoreal
foliage · PBR metal/roughness surfacing · anything that looks manufactured after
the ruins were built.

The first six are a direct anti-goal from Round 4. The last few are the ways a
first-time 3D scene usually goes wrong: reaching for realism and landing in the
uncanny middle. §9 is blunt about why — *a slightly-wrong clean arch reads as
stylistic, a slightly-wrong tree reads as broken.*

---

## 9. Tier settings

Extends spec §5 with the values this document introduces.

| | High | Medium (baseline) | Low |
|---|---|---|---|
| DPR | 1.5 | 1.25 | 1.0 |
| Fog density | 0.030 | 0.038 | 0.050 |
| Canopy layers | 3 | 2 | 2 |
| Scatter density | 100% | 60% | 30% |
| Postprocessing | Vignette + LUT + light bloom | Vignette + LUT | None |
| Dust motes | Yes | Reduced | No |
| Wind sway | Yes | Yes | Yes (it's free) |

**Scatter density is the best knob** — it scales continuously and needs no asset
variants. Wind sway stays on at every tier because it costs nothing and its absence
is the single most obvious sign of a cheap scene.

---

## 10. How this gets checked

Measured, not eyeballed — except where eyeballing is the actual test.

| Claim | Test |
|---|---|
| Camera works | Walk the road. Camera never clips foliage, never shows sky above the canopy line. |
| Palette holds | Screenshot, sample every pixel, confirm nothing outside §3 |
| Values separate | Desaturate the screenshot. Every silhouette must still read. |
| Fog matches sky | No visible horizon seam at any tier |
| Fill rate is safe | Frame time at DPR 1.0 vs 1.5. Ratio ≫ 2 means overdraw-bound (spec §4.6). |
| Budgets hold | `renderer.info`: < 150 draw calls, < 300 K triangles |
| It's good | **Walk the road with no objective. Do you want to keep walking?** |

The last row is the only one that can fail while all the others pass, and it's the
one that matters. §16: *satisfying the requirements is not the same as being good.*

---

## 11. Known open

1. **Camera distance 4.0 m is a guess.** Canopy scenes often want closer for
   enclosure. Expect to change it in the first hour of Step 1.
2. **Dappled light as a texture is unproven here.** It's the second-highest-value
   effect and the one most likely to look wrong. Step 2.5 tests it.
3. **The traversal verb is undecided** (§19). If it turns out to be faster than
   walking, fog distance and tree spacing both have to grow — speed eats sight
   distance. This is the number most likely to invalidate §6.
4. ~~**No sky treatment specified.**~~ **Closed 2026-08-25 by the reference lock:
   flat pale `#cfd3c4`, no clouds, no gradient.** The reference set is split — some
   images have blue sky with clouds, and those are the ones that fight the look. §5
   requires fog colour to equal sky colour, so a blue sky forces blue fog, which
   cools every distant surface and destroys the warm-light-against-cool-shade
   relationship in §4. The pale flat-sky images in the set are both cheaper *and*
   better, which is a rare combination. Flat wins on both counts.

### Opened by the reference lock

5. **Road and sunlit foliage are 7 luminance apart** (§3 value discipline). The
   tightest gap in the palette, and both are large adjacent fills on the most-seen
   screen in the game. Resolve during M5 once the verge is real.
6. **Dressing density is the schedule risk, not the technical one.** The reference
   images get their quality from dressing volume — vines, ferns, rubble, moss,
   cracked slabs. Cheap to draw when instanced, expensive to author and place. This
   is why [build-roadmap.md](build-roadmap.md) §8 lists hub *footprint* as a cut
   lever and dressing *density* as never-cut. Density is what reads.
7. **No character exists in any reference image.** Every one is an empty
   environment. Adding a 1.70 m figure at 2.2 m camera height changes the read
   completely, and character art is the weakest part of this pipeline — v1 takes a
   free CC0 rig. Mitigation: silhouette-first, no facial detail, and check it against
   these images early rather than at M13.
