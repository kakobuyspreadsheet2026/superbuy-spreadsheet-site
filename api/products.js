/**
 * Proxies GET /public/v1/products?category=&limit=&offset=
 *
 * When `category` is omitted, aggregates like scripts/fetch-products.mjs:
 * GET /categories, then GET /products?category=… per slug (max 100 per request per MD).
 */
const {
  normalizeCategories,
  normalizeProductList,
  categorySlug,
} = require("./ml-parse");
const applyCors = require("./cors");

const UPSTREAM = "https://api.maisonlooks.com/public/v1";

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

function clampLimit(v) {
  const n = parseInt(String(v), 10);
  if (Number.isNaN(n) || n < 1) return 48;
  return Math.min(n, 100);
}

function clampOffset(v) {
  const n = parseInt(String(v), 10);
  return Number.isNaN(n) || n < 0 ? 0 : n;
}

async function fetchUpstreamJson(url, key) {
  const r = await fetch(url, {
    headers: { "X-API-Key": key, Accept: "application/json" },
  });
  const text = await r.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    return {
      ok: false,
      status: 502,
      json: { error: "Invalid JSON from upstream", raw: text.slice(0, 400) },
    };
  }
  if (!r.ok) return { ok: false, status: r.status, json };
  return { ok: true, status: r.status, json };
}

async function aggregateProductsAcrossCategories(key, limit, offset) {
  const catRes = await fetchUpstreamJson(`${UPSTREAM}/categories`, key);
  if (!catRes.ok) return { status: catRes.status, json: catRes.json };

  const rows = normalizeCategories(catRes.json);
  const slugs = rows.map(categorySlug).filter(Boolean);
  if (!slugs.length) {
    return {
      status: 200,
      json: { data: [], meta: { total: 0, limit, offset } },
    };
  }

  let skip = offset;
  const out = [];
  const PAGE = 100;
  /** Until we get at least one HTTP 200 from /products, surface upstream errors (e.g. 401). */
  let sawSuccessfulProductResponse = false;

  for (const slug of slugs) {
    let catOff = 0;
    while (true) {
      const sp = new URLSearchParams({
        category: slug,
        limit: String(PAGE),
        offset: String(catOff),
      });
      const p = await fetchUpstreamJson(`${UPSTREAM}/products?${sp}`, key);
      if (!p.ok) {
        if (!sawSuccessfulProductResponse) {
          return { status: p.status, json: p.json };
        }
        break;
      }
      sawSuccessfulProductResponse = true;

      const page = normalizeProductList(p.json);
      if (!page.length) break;

      for (const item of page) {
        if (skip > 0) {
          skip--;
        } else {
          out.push(item);
          if (out.length >= limit) {
            return {
              status: 200,
              json: {
                data: out,
                meta: { total: null, limit, offset },
              },
            };
          }
        }
      }

      if (page.length < PAGE) break;
      catOff += page.length;
    }
  }

  return {
    status: 200,
    json: {
      data: out,
      meta: { total: offset + out.length, limit, offset },
    },
  };
}

module.exports = async function handler(req, res) {
  if (applyCors(req, res)) return;
  if (req.method !== "GET") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const key = process.env.MATRIX_API_KEY || process.env.MAISONLOOKS_API_KEY || "";
  if (!key) {
    res.status(503).json({ error: "MATRIX_API_KEY is not configured on the server" });
    return;
  }

  const q = mergeQuery(req);
  const limit = clampLimit(q.limit);
  const offset = clampOffset(q.offset);

  if (q.category) {
    const sp = new URLSearchParams({
      category: String(q.category),
      limit: String(limit),
      offset: String(offset),
    });
    const result = await fetchUpstreamJson(`${UPSTREAM}/products?${sp}`, key);
    if (!result.ok) {
      res.status(result.status).json(result.json);
      return;
    }
    res.status(200).json(result.json);
    return;
  }

  const agg = await aggregateProductsAcrossCategories(key, limit, offset);
  res.status(agg.status).json(agg.json);
};
