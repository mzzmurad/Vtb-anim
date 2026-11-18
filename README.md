# VTB Bank — Cash loan · 10 s vertical (1080×1920)

Working animatic of the motion brief (Nov 18, 2026). The film is drawn in code, frame by frame, so every cue in the brief lands on its exact frame.

| File | What |
|---|---|
| `out/vtb-cash-loan-1080x1920-30fps.mp4` | 10.0 s, 300 frames, H.264 + temp audio |
| `out/style-frames/scene-*.png` | 5 style frames, 1080×1920, one per scene |
| `film.html` | The film (2D canvas + three.js; `vendor/` holds three.js r170, MIT). Open it in a browser (served over http) to play or scrub it. `?f=120` opens on a frame. Includes a safe-area overlay |
| `render.mjs` | `node render.mjs` renders the MP4 and the stills. Also takes `--stills`, `--frames 0,60,120` and `--prores` (ProRes 422 .mov) |
| `sfx.py` | Temp sound: synthesised SFX on the brief's cue frames plus a quiet 120 BPM guide pulse |

Preview: `npx serve films/vtb-cash-loan` (or any static server), then open `/film.html`.

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
