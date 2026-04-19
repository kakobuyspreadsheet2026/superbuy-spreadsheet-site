/**
 * Proxies GET /public/v1/categories (key from MATRIX_API_KEY on Vercel).
 */
const { normalizeCategories } = require("./ml-parse");

function apiKey() {
  return process.env.MATRIX_API_KEY || process.env.MAISONLOOKS_API_KEY || "";
}

module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const key = apiKey();
  if (!key) {
    res.status(503).json({ error: "MATRIX_API_KEY is not configured on the server" });
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
    res.status(200).json({ data: list });
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
