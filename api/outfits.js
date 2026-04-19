/**
 * Proxies GET /public/v1/outfits (query params forwarded).
 */
function mergeQuery(req) {
  const q = { ...(req.query || {}) };
  const urlStr = req.url || "";
  try {
    const u = new URL(urlStr, "http://localhost");
    u.searchParams.forEach((v, k) => {
      if (q[k] == null || q[k] === "") q[k] = v;
    });
  } catch (_) {
    /* ignore */
  }
  return q;
}

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

  const q = mergeQuery(req);
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(q)) {
    if (v === undefined || v === "") continue;
    if (Array.isArray(v)) v.forEach((x) => sp.append(k, String(x)));
    else sp.set(k, String(v));
  }
  if (!sp.has("limit")) sp.set("limit", "24");
  if (!sp.has("offset")) sp.set("offset", "0");

  const url = `https://api.maisonlooks.com/public/v1/outfits?${sp.toString()}`;

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
