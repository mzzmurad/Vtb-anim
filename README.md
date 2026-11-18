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
