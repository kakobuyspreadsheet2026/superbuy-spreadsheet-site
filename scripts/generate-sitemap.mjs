#!/usr/bin/env node
/**
 * Writes sitemap.xml + robots.txt at repo root from vercel.json rewrites.
 * Run: npm run sitemap
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const BASE = "https://buysspreadsheet.com";

const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, "vercel.json"), "utf8"));
const urls = new Set([`${BASE}/`]);
for (const r of cfg.rewrites || []) {
  if (!r.source || !r.destination) continue;
  if (!String(r.destination).endsWith(".html")) continue;
  const s = r.source;
  if (s === "/initial-products.json" || s === "/favicon.png") continue;
  urls.add(BASE + s);
}

const sorted = [...urls].sort((a, b) => {
  if (a === `${BASE}/`) return -1;
  if (b === `${BASE}/`) return 1;
  return a.localeCompare(b);
});

const today = new Date().toISOString().slice(0, 10);
const body = sorted
  .map(
    (loc) => `  <url>
    <loc>${loc}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${loc === `${BASE}/` ? "1.0" : "0.8"}</priority>
  </url>`
  )
  .join("\n");

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${body}
</urlset>
`;

fs.writeFileSync(path.join(ROOT, "sitemap.xml"), xml);
fs.writeFileSync(
  path.join(ROOT, "robots.txt"),
  `User-agent: *
Allow: /

Sitemap: ${BASE}/sitemap.xml
`
);
console.log("Wrote sitemap.xml (" + sorted.length + " URLs) and robots.txt");
