// Exports the cake film for Cinema 4D: bakes the scene + animation from cake/cake.html into glTF,
// then Blender (cake/c4d_export.py) turns it into FBX and Alembic.
//
//   node cake/export.mjs [path/to/python-with-bpy]   → out/cinema4d/
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "out", "cinema4d");
const PY = process.argv[2] || "python3";
fs.mkdirSync(OUT, { recursive: true });

const MIME = { ".html": "text/html", ".js": "text/javascript" };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": MIME[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });

for (const mode of ["stepped", "smooth"]) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", e => { console.error("page error:", e.message); process.exitCode = 1; });
  await page.goto(`http://127.0.0.1:${server.address().port}/cake/cake.html?render`);
  await page.waitForFunction(() => window.filmReady);
  const r = await page.evaluate(m => window.FILM.exportScene(m), mode);
  const glb = path.join(OUT, `vtb-cake-logo_${mode}.glb`);
  fs.writeFileSync(glb, Buffer.from(r.glb, "base64"));
  fs.writeFileSync(path.join(OUT, `vtb-cake-logo_${mode}.camera.json`), JSON.stringify({ fps: r.fps, frames: r.frames, width: r.width, height: r.height, fov_vertical_deg: r.fovs, focus_distance: r.focus }));
  console.log("wrote", path.relative(ROOT, glb));
  await page.close();
}
await browser.close();
server.close();

execFileSync(PY, [path.join(ROOT, "cake", "c4d_export.py"), OUT], { stdio: "inherit" });
