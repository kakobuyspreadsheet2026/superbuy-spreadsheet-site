/**
 * Parse same-origin /api/* responses. Static servers and file:// return HTML → JSON.parse throws.
 * Load this script before index.js / products.js / outfits.js.
 */
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
        "This page needs the API server. In the project folder run: npx vercel dev — then open the URL it prints (not file:// or python -m http.server). Or use your live Vercel URL with MATRIX_API_KEY set.",
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
