# VTB Bank — Cash loan · 17.1 s vertical (1080×1920)

Working animatic of the motion brief (Nov 18, 2026). The film is drawn in code, frame by frame, so every cue in the brief lands on its exact frame.

| File | What |
|---|---|
| `out/vtb-cash-loan-1080x1920-30fps.mp4` | 17.1 s (15.0 s film + 2.1 s VTB logo sting), H.264, voiceover + soft SFX |
| `footage/worker.mp4` | Oil-worker footage (1280×720, 5 s, ping-pong looped). `render.mjs` extracts it to `footage/frames/` |
| `assets/vtb-logo-sting.mp4` | VTB logo animation appended as the ending (first 2.1 s used) |
| `audio/voiceover.wav` | The voiceover the film is timed to |
| `out/style-frames/scene-*.png` | 5 style frames, 1080×1920, one per scene |
| `film.html` | The film (2D canvas + three.js; `vendor/` holds three.js r170, MIT). Open it in a browser (served over http) to play or scrub it. `?f=120` opens on a frame. Includes a safe-area overlay |
| `render.mjs` | `node render.mjs` renders the MP4 and the stills. Also takes `--stills`, `--frames 0,60,120` and `--prores` (ProRes 422 .mov) |
| `sfx.py` | Soft synthesised SFX mixed under the voiceover |

Preview: `npx serve films/vtb-cash-loan` (or any static server), then open `/film.html`.

## Current cut (v5)
- **Footage:** the worker clip replaces the placeholder: full frame, then the top card, then the portrait tile.
- **Colour:** the client gradient `#0250BF → #67C6FF` is the background throughout, with white tiles on it. The "Sürətli" tile grows into VTB navy `#04378F`, which is the first frame of the logo sting.
- **Type:** VTB Group (Book, Demi Bold, Bold, Extra Bold) for all text and the 3D numerals, set about 1.5% tighter.
- **3D objects:** glossy renders generated with Higgsfield (GPT Image 2.6, high 2K, transparent background), stored in `assets/objects/` as `pct`, `shield`, `coin`, `amount`, `phone`, `pin` and `bolt`. The phone screen shows an application form, not a card, because VTB has no card product here. They animate in 2D with springs, float, tilt and breathe; the "100 000" drops in and the coin rolls in. They replace the hand-built three.js models, which are still in the code but no longer used.
- **"Zaminsiz kredit"** sits on its own white tile like the other conditions.
- **Margins:** every tile sits inside 90 px left/right, 200 px top and 150 px bottom (x 90–990, y 200–1770); only the opening full-bleed shot goes edge to edge. The values are `M_L`, `M_R`, `M_T` and `M_B` in `film.html`, and the safe-area toggle in the preview draws this box.
- **986 card removed:** its voiceover line ("Daha ətraflı məlumat üçün 986…") is dropped too. There is no legal line on screen; add one when VTB legal supplies the text.

| Film time | Voiceover phrase | On screen |
|---|---|---|
| 0.0–6.0 s | Bank VTB-dən səhiyyə işçiləri üçün 9,9%-dən başlayan zaminsiz kredit | Worker, then a card, the audience pill, 9,9%-dən and "Zaminsiz kredit" |
| 6.0–9.2 s | 100 min manata dək məbləği | 3D "100 000", the coin and "AZN-dək nağd kredit" |
| 9.0–15.0 s | VTB.az saytından onlayn və ya ən yaxın filialda sürətli rəsmiləşdir | Grid ticks with the voice, then the legal line; the navy tile expands |
| 15.0–17.1 s | — | VTB logo sting |

### Fonts (not in git)
The repo is public, so the licensed **VTB Group** fonts are git-ignored. Put `VTB55.OTF`, `VTB65.OTF`, `VTB75.OTF` and `VTB95.OTF` in `fonts/vtb/` before rendering.

The voiceover still says **səhiyyə işçiləri**, while the screen says **neft və mədənçıxarma işçilərinə**. Re-record the voiceover line to match.

## Look and motion (v2)
- **Style:** soft app tiles in the manner of the Yandex Pay / Go and WB-bank screens. Each tile has a small header with an icon, a big number or two-line label, and a glossy 3D object cropped at its corner. Tiles use VTB-blue and lavender tints on a light canvas, and the end card is navy.
- **3D:** real 3D objects (three.js, glossy soft plastic with a studio environment): extruded "100 000" numerals, a gold manat coin, a "%" sign, a shield, a calendar and a phone with a VTB app screen.
- **Motion:** spring physics instead of fixed easing curves. Every object keeps floating, swaying and bobbing. Tiles trail each other on the scroll (parallax). Digits fall and flip in, and the coin rolls in. The amount card morphs into its grid slot while the other tiles fly in around it. The checkboxes tick, and the navy tile grows into the end card.
- **Motion blur:** the master averages 4 sub-frames per frame, and 12 on fast moves (`--sub` sets the base count). The browser preview plays without blur.
- **Rendering:** WebGL runs through SwiftShader in headless Chromium. A full render takes about 7 minutes.

## Placeholders to replace
- **Footage**: both shots are illustrated stand-ins. Put `footage/work.jpg` and `footage/portrait.jpg` (9:16) in place and they are used automatically. Moving footage needs a video hookup.
- **Logo**: "VTB" is set in Inter Tight as a stand-in for the logo sting.
- **Colours and type**: these are approximations. Edit `C` in `film.html` to apply the brandbook values.
- **Copy**: the draft Azerbaijani copy sits in `COPY` in `film.html`. The offer figures (100 000 AZN, from 9,9 %, 0 % commission) come from the 4 Sep 2026 vtb.az campaign. Audience line, lockup, headline, tagline and legal all need sign-off.
- **Audio**: replace with the licensed track and SFX.

## VTB cake logo (v3, Nov 19, 2026)
A 9 s vertical film: a knife cuts a whole cake into the VTB logo. The logo's three bars are exactly one slanted slab with two strips taken out, so the cake starts as that slab. The knife makes four cuts, and the two cut strips lift and slide out like the cut-out slice in the reference, leaving the three bars. The background is the client gradient `#0755C2 → #67C6FF`. The cake has a white top, a navy base, sponge layers and a VTB-blue cream layer, with white piped rosettes, sprinkles and nine striped candles (three per bar).

The camera stays in a tight close-up on the knife while it cuts (crops freely, low over the icing and candles). Once the last strip is out, it pulls back and orbits round as it rises, so the cake turns into alignment (a small overshoot, then it lands) and ends straight-on and level, like the flat logo. There is no flat logo overlay.

**3D style (v7):** a soft, plush, felted look, after a fuzzy-wreath reference.
- **Fur:** the icing, sponge, cream layers and piped rosettes grow short, combed fur made of stacked shell layers (`FUR` in `cake/cake.html` sets length, density and layer count per material). Each strand is darker at the root and its shade varies a little.
- **Gloss:** sprinkles and candles are glossy clear-coated candy.
- **Light:** a warm key, a cool rim light from behind and a soft warm front fill.
- **Post:** a bloom pass makes the flames glow, and a depth-of-field pass keeps the knife's focus point sharp. Fore- and background blur strongly in the close-ups and only lightly in the end shot (`LOOK` sets the blur strength, maximum blur radius and bloom).
- **Speed:** each held pose renders once and is reused for its 2–3 frames, so a full render takes about 25 minutes.

**Film look:** a soft navy vignette sits over every frame. Grain is off; set `GRAIN.amount` in `cake/cake.html` to about 0.3 to bring back an animated film grain (`GRAIN.size` sets the grain size in pixels).

**Stepped timing:** like the reference, motion is choppy on purpose. Poses update 12 times a second and are held for 2–3 frames of the 30 fps video, with no motion blur. `STEP` in `cake/cake.html` sets the rate; `?step=0` in the preview URL (or `STEP = 0`) gives smooth motion again.

| Time | What happens |
|---|---|
| 0.0–0.7 s | The knife comes in from the top right; close on the cake's corner |
| 0.7–3.0 s | Cuts 1 and 2 along the first gap (push, then pull) |
| 3.0–4.0 s | That strip lifts and slides out to the right while the knife crosses over |
| 3.8–6.2 s | Cuts 3 and 4 along the second gap |
| 6.2–7.2 s | The second strip slides out to the left; the knife leaves |
| 6.4–8.2 s | The camera pulls out to the whole logo; hold to 9.0 s |

- `cake/cake.html`: the scene (three.js). Open it over http to play it, or use `?f=90` for one frame. Colours are in `C`, candles in the `addCandle` list, cut timing in `LOWER_T`, `CUT_T`, `LIFT_T` and `HOP_T`, the close-up framing in `CLOSE_OFF` and the end shot in `WIDE`.
- `node cake/render.mjs` writes `out/vtb-cake-logo-1080x1920-30fps.mp4` (no audio).
