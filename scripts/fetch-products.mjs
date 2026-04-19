#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const API_BASE = process.env.MATRIX_API_BASE || "https://api.maisonlooks.com";
const API_KEY = process.env.MATRIX_API_KEY;
const OUT_DIR = process.env.MATRIX_OUT_DIR || "./data";

const args = Object.fromEntries(
  process.argv
    .slice(2)
    .filter((a) => a.startsWith("--"))
    .map((a) => {
      const [k, v] = a.slice(2).split("=");
      return [k, v ?? true];
    }),
);

const PER_PAGE = clamp(parseInt(args.limit ?? "40", 10), 1, 100);
const MAX_PER_CATEGORY = clamp(parseInt(args["max-per-category"] ?? "200", 10), 1, 5000);
const OUTFITS_LIMIT = clamp(parseInt(args.outfits ?? "30", 10), 0, 200);
const ONLY_CATEGORIES = args.categories
  ? String(args.categories)
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
  : null;

if (!API_KEY) {
  console.error("MATRIX_API_KEY required");
  process.exit(1);
}

await fs.mkdir(OUT_DIR, { recursive: true });
const errors = [];
const meta = { pulled_at: new Date().toISOString(), base_url: API_BASE, counts: {} };

let categories = [];
try {
  categories = await api("/public/v1/categories");
  await write("categories.json", categories);
  meta.counts.categories = categories.length;
} catch (e) {
  errors.push(`categories: ${e.message}`);
}

const targets = (ONLY_CATEGORIES ?? categories.map((c) => c.slug)).filter(Boolean);
const products = [];
for (const slug of targets) {
  try {
    let offset = 0;
    while (true) {
      if (
        products.length &&
        products.filter((p) => p.category === slug).length >= MAX_PER_CATEGORY
      )
        break;
      const res = await api(
        `/public/v1/products?category=${encodeURIComponent(slug)}&limit=${PER_PAGE}&offset=${offset}`,
      );
      const page = Array.isArray(res) ? res : res.data ?? [];
      if (!page.length) break;
      products.push(...page);
      if (page.length < PER_PAGE) break;
      offset += PER_PAGE;
    }
  } catch (e) {
    errors.push(`products[${slug}]: ${e.message}`);
  }
}
if (products.length) {
  await write("products.json", products);
  meta.counts.products = products.length;
}

if (OUTFITS_LIMIT > 0) {
  try {
    const res = await api(`/public/v1/outfits?featured=true&limit=${OUTFITS_LIMIT}`);
    const outfits = Array.isArray(res) ? res : res.data ?? [];
    await write("outfits.json", outfits);
    meta.counts.outfits = outfits.length;
  } catch (e) {
    errors.push(`outfits: ${e.message}`);
  }
}

meta.errors = errors;
await write("_meta.json", meta);
process.exit(errors.length === 0 ? 0 : 3);

async function api(p) {
  const r = await fetch(`${API_BASE}${p}`, {
    headers: { "X-API-Key": API_KEY, Accept: "application/json" },
  });
  if (!r.ok)
    throw new Error(`${p} -> HTTP ${r.status} ${(await r.text().catch(() => "")).slice(0, 200)}`);
  return r.json();
}

async function write(name, data) {
  await fs.writeFile(path.join(OUT_DIR, name), JSON.stringify(data, null, 2));
}

function clamp(n, lo, hi) {
  return Number.isNaN(n) ? lo : Math.max(lo, Math.min(hi, n));
}
