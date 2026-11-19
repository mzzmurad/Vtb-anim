// Renders cake/cake.html frame by frame in headless Chromium, then encodes with ffmpeg.
//
//   node cake/render.mjs                → out/vtb-cake-logo-1080x1920-30fps.mp4
//   node cake/render.mjs --frames 0,60  → just those frames as PNGs in out/check/
//   node cake/render.mjs --sub 6        → sub-frames per frame for motion blur (default 4)
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "out");
const args = process.argv.slice(2);
const arg = f => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : null; };
const SUB = +(arg("--sub") || 4);

const MIME = { ".html": "text/html", ".js": "text/javascript", ".png": "image/png" };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": MIME[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));

const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on("pageerror", e => { console.error("page error:", e.message); process.exitCode = 1; });
page.on("console", m => { if (m.type() === "error") console.error("console:", m.text()); });
await page.goto(`http://127.0.0.1:${server.address().port}/cake/cake.html?render`);
await page.waitForFunction(() => window.filmReady);
const { FRAMES, FPS } = await page.evaluate(() => ({ FRAMES: window.FILM.FRAMES, FPS: window.FILM.FPS }));

async function grab(f, file, sub = SUB) {
  const b64 = await page.evaluate(([f, sub]) => { window.FILM.renderFrame(f, sub); return document.getElementById("c").toDataURL("image/png").split(",")[1]; }, [f, sub]);
  fs.writeFileSync(file, Buffer.from(b64, "base64"));
}

if (arg("--frames")) {
  const dir = path.join(OUT, "check"); fs.mkdirSync(dir, { recursive: true });
  for (const f of arg("--frames").split(",").map(Number)) await grab(f, path.join(dir, `cake-f${String(f).padStart(3, "0")}.png`), 1);
} else {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "vtb-cake-"));
  for (let f = 0; f < FRAMES; f++) {
    await grab(f, path.join(tmp, `f${String(f).padStart(4, "0")}.png`));
    if (f % 30 === 0) console.log(`frame ${f}/${FRAMES}`);
  }
  fs.mkdirSync(OUT, { recursive: true });
  const mp4 = path.join(OUT, "vtb-cake-logo-1080x1920-30fps.mp4");
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(tmp, "f%04d.png"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart", mp4], { stdio: "inherit" });
  console.log("wrote", path.relative(ROOT, mp4));
  fs.rmSync(tmp, { recursive: true, force: true });
}
await browser.close();
server.close();
