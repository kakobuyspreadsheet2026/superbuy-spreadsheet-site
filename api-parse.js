/**
 * Parse same-origin /api/* responses. Static servers and file:// return HTML → JSON.parse throws.
 * Load this script before index.js / products.js / outfits.js.
 *
 * On production domains, requests stay same-origin (/api). __API_ORIGIN__ is only set for localhost / file (see HTML).
 */
function apiUrl(path) {
  if (typeof window === "undefined") return path;
  var custom = window.__API_ORIGIN__;
  if (!custom) return path;
  var base = String(custom).replace(/\/$/, "");
  if (base === window.location.origin) return path;
  return base + path;
}

async function readApiJson(response) {
  const text = await response.text();
  const start = text.trimStart();
  if (
    start.startsWith("<!") ||
    (start.charAt(0) === "<" && /DOCTYPE/i.test(text.slice(0, 256)))
  ) {
    return {
      ok: false,
      status: response.status,
      json: null,
      bodyError:
        "This page needs JSON from /api. Either: (1) run npx vercel dev and open its URL, or (2) keep window.__API_ORIGIN__ in the HTML pointed at your Vercel deployment (MATRIX_API_KEY must be set there).",
    };
  }
  let json;
  try {
    json = JSON.parse(text);
  } catch (e) {
    return {
      ok: false,
      status: response.status,
      json: null,
      bodyError: e.message || "Invalid JSON from server",
    };
  }
  return { ok: response.ok, status: response.status, json };
}

/** Short-lived client cache for GET /api/* (same tab); pairs with server Cache-Control. */
var __apiFetchCache = new Map();
var __API_FETCH_MAX = 80;

function ttlForApiFetchUrl(urlStr) {
  try {
    var u = new URL(urlStr, "http://localhost");
    var p = u.pathname || "";
    if (p.indexOf("/api/categories") !== -1) return 5 * 60 * 1000;
    if (p.indexOf("/api/products") !== -1) return 90 * 1000;
    if (p.indexOf("/api/outfits") !== -1) return 90 * 1000;
  } catch (e) {
    /* ignore */
  }
  return 60 * 1000;
}

function pruneApiFetchCache() {
  while (__apiFetchCache.size > __API_FETCH_MAX) {
    var first = __apiFetchCache.keys().next().value;
    __apiFetchCache.delete(first);
  }
}

/**
 * GET JSON from same-origin /api (or __API_ORIGIN__). Caches parsed result briefly to avoid duplicate work.
 * @param {string} pathOrUrl e.g. "/api/categories" or "/api/products?limit=48&offset=0"
 */
async function fetchApiJson(pathOrUrl) {
  var url =
    typeof pathOrUrl === "string" && pathOrUrl.indexOf("http") === 0
      ? pathOrUrl
      : apiUrl(pathOrUrl);
  var now = Date.now();
  var row = __apiFetchCache.get(url);
  if (row && now < row.exp) {
    return row.parsed;
  }
  var r = await fetch(url);
  var parsed = await readApiJson(r);
  __apiFetchCache.set(url, { parsed: parsed, exp: now + ttlForApiFetchUrl(url) });
  pruneApiFetchCache();
  return parsed;
}
