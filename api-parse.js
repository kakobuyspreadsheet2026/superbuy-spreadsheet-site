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
