/**
 * Proxies GET /public/v1/products?category=&limit=&offset=
 *
 * When `category` is omitted: round-robin across category slugs (cat0[0], cat1[0], … catN-1[0], cat0[1], …)
 * so early pages look like MaisonLooks “全部商品” (mixed), not “all of category A then B”.
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

const PAGE = 100;

/**
 * Global merged index g → round-robin: category slugs[g % n], item floor(g/n) within that category.
 */
async function aggregateRoundRobinAllCategories(key, limit, offset) {
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

  const n = slugs.length;
  const cache = new Map();

  async function loadBatch(slug, batchBase) {
    const keyStr = `${slug}:${batchBase}`;
    if (cache.has(keyStr)) return cache.get(keyStr);
    const sp = new URLSearchParams({
      category: slug,
      limit: String(PAGE),
      offset: String(batchBase),
    });
    const p = await fetchUpstreamJson(`${UPSTREAM}/products?${sp}`, key);
    if (!p.ok) {
      cache.set(keyStr, { err: p });
      return cache.get(keyStr);
    }
    const list = normalizeProductList(p.json);
    cache.set(keyStr, { list });
    return cache.get(keyStr);
  }

  const batchKeys = new Set();
  for (let i = 0; i < limit; i++) {
    const g = offset + i;
    const catIdx = g % n;
    const idxInCat = Math.floor(g / n);
    const slug = slugs[catIdx];
    const batchBase = Math.floor(idxInCat / PAGE) * PAGE;
    batchKeys.add(`${slug}:${batchBase}`);
  }

  let firstFailure = null;
  await Promise.all(
    [...batchKeys].map(async (keyStr) => {
      const last = keyStr.lastIndexOf(":");
      const slug = keyStr.slice(0, last);
      const base = parseInt(keyStr.slice(last + 1), 10);
      const res = await loadBatch(slug, base);
      if (res.err && !firstFailure) firstFailure = res.err;
    }),
  );

  const out = [];
  for (let i = 0; i < limit; i++) {
    const g = offset + i;
    const catIdx = g % n;
    const idxInCat = Math.floor(g / n);
    const slug = slugs[catIdx];
    const batchBase = Math.floor(idxInCat / PAGE) * PAGE;
    const localIdx = idxInCat - batchBase;
    const keyStr = `${slug}:${batchBase}`;
    const entry = cache.get(keyStr);
    if (!entry || entry.err) {
      if (i === 0 && entry && entry.err) {
        return { status: entry.err.status, json: entry.err.json };
      }
      if (i === 0 && firstFailure) {
        return { status: firstFailure.status, json: firstFailure.json };
      }
      break;
    }
    const list = entry.list || [];
    const item = list[localIdx];
    if (!item) break;
    out.push(item);
  }

  return {
    status: 200,
    json: {
      data: out,
      meta: { total: null, limit, offset },
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

  const agg = await aggregateRoundRobinAllCategories(key, limit, offset);
  res.status(agg.status).json(agg.json);
};
