/**
 * Local static server with the same extensionless rewrites as vercel.json.
 * Live Server / plain file open cannot map /kakobuy -> kakobuy.html — use: npm run dev
 */
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const PORT = Number(process.env.PORT) || 3333;

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".mjs": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".ico": "image/x-icon",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
};

function loadRewrites() {
  const raw = fs.readFileSync(path.join(ROOT, "vercel.json"), "utf8");
  const config = JSON.parse(raw);
  const map = new Map();
  for (const r of config.rewrites || []) {
    if (r.source && r.destination) map.set(r.source, r.destination);
  }
  return map;
}

const REWRITE = loadRewrites();

function send(res, filePath, code = 200) {
  const ext = path.extname(filePath).toLowerCase();
  const type = MIME[ext] || "application/octet-stream";
  try {
    const body = fs.readFileSync(filePath);
    res.writeHead(code, { "Content-Type": type });
    res.end(body);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
  }
}

const server = http.createServer((req, res) => {
  try {
    const u = new URL(req.url || "/", "http://127.0.0.1");
    let pathname = decodeURIComponent(u.pathname);
    if (pathname.includes("\0") || pathname.includes("..")) {
      res.writeHead(400);
      return res.end("Bad path");
    }
    if (pathname !== "/" && pathname.endsWith("/")) pathname = pathname.slice(0, -1) || "/";

    if (pathname === "/") {
      return send(res, path.join(ROOT, "index.html"));
    }

    const viaRewrite = REWRITE.get(pathname);
    if (viaRewrite) {
      const rel = viaRewrite.startsWith("/") ? viaRewrite.slice(1) : viaRewrite;
      return send(res, path.join(ROOT, rel));
    }

    const rel = pathname.startsWith("/") ? pathname.slice(1) : pathname;
    const filePath = path.join(ROOT, rel);
    const normalized = path.normalize(filePath);
    if (!normalized.startsWith(ROOT)) {
      res.writeHead(403);
      return res.end("Forbidden");
    }
    if (fs.existsSync(normalized) && fs.statSync(normalized).isFile()) {
      return send(res, normalized);
    }

    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
  } catch (e) {
    res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
    res.end(String(e.message || e));
  }
});

server.listen(PORT, () => {
  console.log(`Dev server http://127.0.0.1:${PORT}/  (extensionless routes match vercel.json)`);
});
