/**
 * Proxies GET /public/v1/products?category=&limit=&offset=
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

  const sp = new URLSearchParams();
  const q = req.query || {};
  if (q.category) sp.set("category", String(q.category));
  sp.set("limit", q.limit != null ? String(q.limit) : "48");
  sp.set("offset", q.offset != null ? String(q.offset) : "0");

  const url = `https://api.maisonlooks.com/public/v1/products?${sp.toString()}`;

  try {
    const r = await fetch(url, {
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
