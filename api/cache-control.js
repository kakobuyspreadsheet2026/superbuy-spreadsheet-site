/**
 * HTTP caching for public catalog JSON. s-maxage = shared caches (CDN); max-age = browser.
 */
const PROFILES = {
  categories: "public, max-age=120, s-maxage=300, stale-while-revalidate=86400",
  products: "public, max-age=45, s-maxage=120, stale-while-revalidate=600",
  outfits: "public, max-age=45, s-maxage=120, stale-while-revalidate=600",
};

function setPublicCache(res, profile) {
  const v = PROFILES[profile];
  if (v) res.setHeader("Cache-Control", v);
}

function setNoStore(res) {
  res.setHeader("Cache-Control", "no-store");
}

module.exports = { setPublicCache, setNoStore };
