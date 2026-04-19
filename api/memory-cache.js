/**
 * Best-effort in-memory TTL cache for serverless (warm instance only).
 * Reduces duplicate upstream calls under burst traffic; edge + browser use Cache-Control.
 */
const store = new Map();
const MAX_ENTRIES = 200;

function get(key) {
  const e = store.get(key);
  if (!e) return undefined;
  if (Date.now() > e.exp) {
    store.delete(key);
    return undefined;
  }
  return e.value;
}

function set(key, value, ttlMs) {
  while (store.size >= MAX_ENTRIES) {
    const first = store.keys().next().value;
    store.delete(first);
  }
  store.set(key, { value, exp: Date.now() + ttlMs });
}

module.exports = { get, set };
