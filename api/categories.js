/**
 * Proxies GET /public/v1/categories (key from MATRIX_API_KEY on Vercel).
 */
module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const key = process.env.MATRIX_API_KEY;
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
      body = { error: "Invalid JSON from upstream", raw: text.slice(0, 200) };
    }
    res.status(r.status).json(body);
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
