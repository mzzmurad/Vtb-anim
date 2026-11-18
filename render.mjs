// Renders film.html frame-by-frame with headless Chromium, then encodes with ffmpeg.
//
//   node render.mjs                 → out/vtb-cash-loan-1080x1920-30fps.mp4 (+ style frames)
//   node render.mjs --stills        → style frames only
//   node render.mjs --frames 0,60   → just those frames as PNGs in out/check/
//   node render.mjs --prores        → also out/…-prores422.mov (large; not committed)
//
// Needs: playwright (Chromium), ffmpeg, python3 + numpy (for the temp SFX/guide track).
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, "out");
const args = process.argv.slice(2);
const has = f => args.includes(f);
const arg = f => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : null; };

// Style frames: one per scene, each on a held moment.
const STILLS = { "1-person": 12, "2-offer": 128, "3-amount": 180, "4-grid": 286, "5-end-card": 420 };
const SUB = +(arg("--sub") || 4);   // sub-frames per frame for motion blur

const MIME = { ".html": "text/html", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".js": "text/javascript", ".woff": "font/woff" };
const server = http.createServer((req, res) => {
  const p = path.join(DIR, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(DIR) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": MIME[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const url = `http://127.0.0.1:${server.address().port}/film.html?render`;

const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on("pageerror", e => { console.error("page error:", e.message); process.exitCode = 1; });
await page.goto(url);
page.on("console", m => { if (m.type() === "error") console.error("console:", m.text()); });
await page.waitForFunction(() => window.filmReady);
await page.evaluate(() => window.filmReady);
const { FRAMES, FPS } = await page.evaluate(() => ({ FRAMES: window.FILM.FRAMES, FPS: window.FILM.FPS }));

async function grab(f, file, sub = SUB) {
  const b64 = await page.evaluate(([f, sub]) => { window.FILM.renderFrame(f, sub); return document.getElementById("c").toDataURL("image/png").split(",")[1]; }, [f, sub]);
  fs.writeFileSync(file, Buffer.from(b64, "base64"));
}

fs.mkdirSync(path.join(OUT, "style-frames"), { recursive: true });

if (arg("--frames")) {
  const dir = path.join(OUT, "check"); fs.mkdirSync(dir, { recursive: true });
  for (const f of arg("--frames").split(",").map(Number)) await grab(f, path.join(dir, `f${String(f).padStart(3, "0")}.png`));
} else {
  for (const [name, f] of Object.entries(STILLS)) await grab(f, path.join(OUT, "style-frames", `scene-${name}.png`));
  if (!has("--stills")) {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "vtb-frames-"));
    for (let f = 0; f < FRAMES; f++) {
      await grab(f, path.join(tmp, `f${String(f).padStart(4, "0")}.png`));
      if (f % 30 === 0) process.stdout.write(`frame ${f}/${FRAMES}\n`);
    }
    const wav = path.join(tmp, "sfx.wav");
    execFileSync("python3", ["-I", path.join(DIR, "sfx.py"), wav], { stdio: "inherit" });
    const mp4 = path.join(OUT, "vtb-cash-loan-1080x1920-30fps.mp4");
    const dur = String(FRAMES / FPS);
    // voiceover on top, SFX tucked underneath
    const audio = ["-i", wav, "-i", path.join(DIR, "audio", "voiceover.wav"),
      "-filter_complex", "[1:a]volume=0.32[s];[2:a]aresample=48000,volume=1.0[v];[s][v]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95[a]",
      "-map", "0:v", "-map", "[a]"];
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(tmp, "f%04d.png"), ...audio,
      "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", String(FPS),
      "-c:a", "aac", "-b:a", "192k", "-t", dur, "-movflags", "+faststart", mp4], { stdio: "inherit" });
    console.log("wrote", path.relative(DIR, mp4));
    if (has("--prores")) {
      const mov = path.join(OUT, "vtb-cash-loan-1080x1920-30fps-prores422.mov");
      execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(tmp, "f%04d.png"),
        ...audio, "-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le", "-c:a", "pcm_s16le", "-t", dur, mov], { stdio: "inherit" });
      console.log("wrote", path.relative(DIR, mov));
    }
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}
await browser.close();
server.close();
