/**
 * Proxies GET /public/v1/categories (key from MATRIX_API_KEY on Vercel).
 */
const { normalizeCategories } = require("./ml-parse");
const applyCors = require("./cors");
const mem = require("./memory-cache");
const { setPublicCache, setNoStore } = require("./cache-control");

const MEM_KEY = "categories:v2";
const MEM_TTL_MS = 5 * 60 * 1000;

function apiKey() {
  return process.env.MATRIX_API_KEY || process.env.MAISONLOOKS_API_KEY || "";
}

module.exports = async function handler(req, res) {
  if (applyCors(req, res)) return;
  if (req.method !== "GET") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const key = apiKey();
  if (!key) {
    setNoStore(res);
    res.status(503).json({ error: "MATRIX_API_KEY is not configured on the server" });
    return;
  }

  const cached = mem.get(MEM_KEY);
  if (cached) {
    setPublicCache(res, "categories");
    res.status(200).json(cached);
    return;
  }

  try {
    const r = await fetch("https://api.maisonlooks.com/public/v1/categories", {
      headers: { "X-API-Key": key, Accept: "application/json" },
    });
    const text = await r.text();
    let body;
    try {
      body = JSON.parse(text);
    } catch {
      res.status(502).json({ error: "Invalid JSON from upstream", raw: text.slice(0, 200) });
      return;
    }
    if (!r.ok) {
      res.status(r.status).json(body);
      return;
    }
    const list = normalizeCategories(body);
    const payload = { data: list };
    mem.set(MEM_KEY, payload, MEM_TTL_MS);
    setPublicCache(res, "categories");
    res.status(200).json(payload);
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
