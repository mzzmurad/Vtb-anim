# VTB Bank — Cash loan · 10 s vertical (1080×1920)

Working animatic of the motion brief (Nov 18, 2026). The film is drawn in code, frame by frame, so every cue in the brief lands on its exact frame.

| File | What |
|---|---|
| `out/vtb-cash-loan-1080x1920-30fps.mp4` | 10.0 s, 300 frames, H.264 + temp audio |
| `out/style-frames/scene-*.png` | 5 style frames, 1080×1920, one per scene |
| `film.html` | The film. Open it in a browser (served over http) to play or scrub it. `?f=120` opens on a frame. Includes a safe-area overlay |
| `render.mjs` | `node render.mjs` renders the MP4 and the stills. Also takes `--stills`, `--frames 0,60,120` and `--prores` (ProRes 422 .mov) |
| `sfx.py` | Temp sound: synthesised SFX on the brief's cue frames plus a quiet 120 BPM guide pulse |

Preview: `npx serve films/vtb-cash-loan` (or any static server), then open `/film.html`.

## Built to the brief
- Five scenes change at f60 / 135 / 195 / 240, all on 120 BPM beats. There are no cuts or crossfades: every transition is a card or the camera moving.
- Easing: entrances use cubic-bezier(0.16,1,0.3,1). Exits are ease-in over 8–10 f. Pops go 85→103→100 % over 10 f. Siblings are staggered by 3 f. Text appears with mask wipes (8 f per line). The camera moves over 15 f ease-in-out, and the scroll has 6–8 px of vertical motion blur.
- Layout: 64 px margins. Text stays inside y 250–1520. Corners are 48 px, gaps 32 px, and there is one shadow (16 px down, 40 blur, 8 % navy). The checkbox is 40 px and the pill label 36 px.
- 3D objects: glossy amount numerals with azure depth, a gold manat coin (rolls in, leans, gleams) and a glossy "0%" for the benefit.
- Type: Inter Tight 800/600 (OFL) with the latin-ext subset. Azerbaijani caps are typed by hand (KOMİSSİYASIZ, KREDİT).

## Placeholders to replace
- **Footage**: both shots are illustrated stand-ins. Put `footage/work.jpg` and `footage/portrait.jpg` (9:16) in place and they are used automatically. Moving footage needs a video hookup.
- **Logo**: "VTB" is set in Inter Tight as a stand-in for the logo sting.
- **Colours and type**: these are approximations. Edit `C` in `film.html` to apply the brandbook values.
- **Copy**: the draft Azerbaijani copy sits in `COPY` in `film.html`. The offer figures (100 000 AZN, from 9,9 %, 0 % commission) come from the 4 Sep 2026 vtb.az campaign. Audience line, lockup, headline, tagline and legal all need sign-off.
- **Audio**: replace with the licensed track and SFX.
