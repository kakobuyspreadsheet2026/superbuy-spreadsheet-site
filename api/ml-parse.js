/**
 * Normalize MaisonLooks public API JSON — shapes differ slightly between endpoints / versions.
 */

function firstArray(...candidates) {
  for (const c of candidates) {
    if (Array.isArray(c)) return c;
  }
  return [];
}

function normalizeCategories(body) {
  if (Array.isArray(body)) return body;
  if (!body || typeof body !== "object") return [];
  const nested = firstArray(
    body.data,
    body.categories,
    body.items,
    body.results,
    body.data && body.data.categories,
    body.data && body.data.data,
    body.data && body.data.items,
  );
  if (nested.length) return nested;
  return [];
}

function normalizeProductList(body) {
  if (Array.isArray(body)) return body;
  if (!body || typeof body !== "object") return [];
  const nested = firstArray(
    body.data,
    body.products,
    body.items,
    body.results,
    body.records,
    body.list,
    body.content,
    body.data && body.data.items,
    body.data && body.data.rows,
    body.data && body.data.records,
    body.data && body.data.products,
    body.data && body.data.data,
  );
  return nested;
}

function categorySlug(c) {
  if (!c || typeof c !== "object") return "";
  return String(c.slug || c.categorySlug || c.id || "").trim();
}

module.exports = { normalizeCategories, normalizeProductList, categorySlug };
