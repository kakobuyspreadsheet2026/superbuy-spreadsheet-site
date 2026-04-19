#!/usr/bin/env node
/**
 * Writes public/initial-products.json for instant homepage paint (same shape as GET /api/products).
 * Set SEED_API_URL to your deployed API, e.g.
 *   SEED_API_URL=https://YOUR_PROJECT.vercel.app/api/products?limit=200&offset=0
 * Run locally before deploy, or add as Vercel Build Command with that env var.
 */
import fs from "node:fs/promises";
import path from "node:path";

const outDir = path.join(process.cwd(), "public");
const outFile = path.join(outDir, "initial-products.json");
const url = process.env.SEED_API_URL || process.env.INITIAL_PRODUCTS_URL || "";

async function main() {
  if (!url.trim()) {
    console.warn(
      "generate-initial-products: SEED_API_URL unset — skip (keeps existing public/initial-products.json).",
    );
    return;
  }
  await fs.mkdir(outDir, { recursive: true });
  try {
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const json = await r.json();
    await fs.writeFile(outFile, JSON.stringify(json));
    console.log("Wrote", outFile);
  } catch (e) {
    console.warn("generate-initial-products failed:", e.message || e);
    await fs.writeFile(outFile, JSON.stringify({ data: [], meta: {} }));
  }
}

main();
