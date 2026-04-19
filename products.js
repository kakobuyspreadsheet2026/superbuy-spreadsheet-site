const ML_PRODUCT = "https://maisonlooks.com/zh/p/";
/** Default batch size on the standalone products page. */
const PAGE_LIMIT = 48;
/** Homepage image grid: fixed cap; “View more” links to MaisonLooks /zh/products. */
const HOME_GRID_MAX_ITEMS = 200;
/** Homepage does not call /api/products — only /initial-products.json (+ localStorage). */
const PAGE_LIMIT_HOME = 100;
/** Homepage: first N cards use eager images + fetchPriority high (~2 rows × 6 cols at lg). */
const HOME_EAGER_IMAGE_COUNT = 12;
/** localStorage mirror of seed JSON (repeat visits skip network when fresh). */
const HOME_SEED_CACHE_KEY = "ml_initial_products_seed_v2";
const HOME_SEED_CACHE_TTL_MS = 7 * 24 * 60 * 60 * 1000;

function pageLimit() {
  return document.body?.classList.contains("page-home") ? PAGE_LIMIT_HOME : PAGE_LIMIT;
}

const state = {
  offset: 0,
  total: null,
  category: "",
  loading: false,
  done: false,
};

function readHomeSeedCache() {
  try {
    const raw = localStorage.getItem(HOME_SEED_CACHE_KEY);
    if (!raw) return null;
    const o = JSON.parse(raw);
    if (!o || typeof o.t !== "number" || o.json == null) return null;
    if (Date.now() - o.t > HOME_SEED_CACHE_TTL_MS) return null;
    return o.json;
  } catch {
    return null;
  }
}

function writeHomeSeedCache(json) {
  try {
    localStorage.setItem(HOME_SEED_CACHE_KEY, JSON.stringify({ t: Date.now(), json }));
  } catch {
    /* quota / private mode */
  }
}

/** Long npm/seed copy is for local debugging only; production gets a short visitor message. */
function showHomeDevHints() {
  try {
    const h = window.location.hostname;
    if (h === "localhost" || h === "127.0.0.1") return true;
    return new URLSearchParams(window.location.search).get("dev") === "1";
  } catch {
    return false;
  }
}

/** Matches fetch-products.mjs + common paginated shapes. */
function normalizeProductList(json) {
  if (Array.isArray(json)) return json;
  if (!json || typeof json !== "object") return [];
  if (Array.isArray(json.data)) return json.data;
  if (Array.isArray(json.products)) return json.products;
  if (Array.isArray(json.items)) return json.items;
  if (Array.isArray(json.results)) return json.results;
  if (json.data && typeof json.data === "object" && Array.isArray(json.data.items)) {
    return json.data.items;
  }
  return [];
}

/** Public API uses `images: string[]`; some payloads may use a single URL field. */
function primaryImageUrl(p) {
  if (!p || typeof p !== "object") return "";
  if (Array.isArray(p.images) && p.images[0]) return String(p.images[0]);
  const single =
    p.imageUrl ||
    p.thumbnailUrl ||
    p.coverImage ||
    p.primaryImage ||
    p.thumbnail ||
    p.image;
  if (typeof single === "string" && single) return single;
  return "";
}

function formatPrice(p) {
  if (p.priceCny != null) return `¥${Number(p.priceCny).toFixed(0)}`;
  if (Array.isArray(p.priceCnyRange) && p.priceCnyRange.length === 2) {
    return `¥${p.priceCnyRange[0]}–${p.priceCnyRange[1]}`;
  }
  if (Array.isArray(p.priceUsdEstimate) && p.priceUsdEstimate.length === 2) {
    return `~$${p.priceUsdEstimate[0]}–${p.priceUsdEstimate[1]}`;
  }
  return "—";
}

/** `homeIndex` (homepage only): 0-based slot so the first tiles use eager + fetchPriority high. */
function cardEl(p, opts = {}) {
  const a = document.createElement("a");
  a.className = "product-card";
  a.href = ML_PRODUCT + encodeURIComponent(p.slug);
  a.target = "_blank";
  a.rel = "noopener noreferrer";

  const img = document.createElement("img");
  img.className = "product-card__img";
  img.src = primaryImageUrl(p);
  img.alt = "";
  img.decoding = "async";
  img.onerror = () => {
    img.removeAttribute("src");
    img.classList.add("product-card__img--placeholder");
  };

  const imageOnly = document.body?.classList.contains("page-home");
  const hi =
    imageOnly &&
    typeof opts.homeIndex === "number" &&
    opts.homeIndex >= 0 &&
    opts.homeIndex < HOME_EAGER_IMAGE_COUNT;
  if (hi) {
    img.loading = "eager";
    if ("fetchPriority" in img) {
      img.fetchPriority = "high";
    }
  } else {
    img.loading = "lazy";
  }
  if (imageOnly) {
    a.classList.add("product-card--image-only");
    const bits = [p.title || p.slug, p.brand, formatPrice(p)].filter(Boolean);
    a.setAttribute("aria-label", bits.join(" · "));
  }

  a.appendChild(img);

  if (!imageOnly) {
    const body = document.createElement("div");
    body.className = "product-card__body";

    if (p.brand) {
      const brand = document.createElement("div");
      brand.className = "product-card__brand";
      brand.textContent = p.brand;
      body.appendChild(brand);
    }

    const title = document.createElement("div");
    title.className = "product-card__title";
    title.textContent = p.title || p.slug;

    const price = document.createElement("div");
    price.className = "product-card__price";
    price.textContent = formatPrice(p);

    body.appendChild(title);
    body.appendChild(price);
    a.appendChild(body);
  }

  return a;
}

async function loadCategories() {
  const sel = document.getElementById("filter-cat");
  if (!sel) return;
  try {
    const parsed = await fetchApiJson("/api/categories");
    if (parsed.bodyError) {
      sel.disabled = true;
      const st = document.getElementById("products-status");
      if (st) st.textContent = parsed.bodyError;
      return;
    }
    const data = parsed.json;
    if (!parsed.ok) {
      sel.disabled = true;
      return;
    }
    const list = Array.isArray(data)
      ? data
      : Array.isArray(data?.data)
        ? data.data
        : Array.isArray(data?.categories)
          ? data.categories
          : [];
    const sorted = sortCategoriesApparelFirst(list);
    for (const c of sorted) {
      const opt = document.createElement("option");
      opt.value = c.slug;
      opt.textContent = c.name || c.slug;
      sel.appendChild(opt);
    }
  } catch {
    sel.disabled = true;
  }
}

/**
 * Homepage: paint first batch from static seed (no slow /api round-robin) when possible.
 * Priority: window.__INITIAL_PRODUCTS__ → #initial-products-json → GET /initial-products.json
 * (Build: scripts/generate-initial-products.mjs + SEED_API_URL → public/initial-products.json)
 */
async function hydrateInitialProducts() {
  if (!document.body?.classList.contains("page-home")) return;
  if (state.category) return;

  let json = null;
  if (typeof window.__INITIAL_PRODUCTS__ !== "undefined" && window.__INITIAL_PRODUCTS__ != null) {
    try {
      json =
        typeof window.__INITIAL_PRODUCTS__ === "string"
          ? JSON.parse(window.__INITIAL_PRODUCTS__)
          : window.__INITIAL_PRODUCTS__;
    } catch {
      json = null;
    }
  }
  if (!json) {
    const el = document.getElementById("initial-products-json");
    if (el && el.textContent.trim()) {
      try {
        json = JSON.parse(el.textContent);
      } catch {
        json = null;
      }
    }
  }
  if (!json) {
    json = readHomeSeedCache();
  }
  if (json && !normalizeProductList(json).length) {
    try {
      localStorage.removeItem(HOME_SEED_CACHE_KEY);
    } catch {
      /* */
    }
    json = null;
  }
  if (!json) {
    try {
      /** Static hosts keep files under public/ → URL is /public/… ; root /initial-products.json needs a Vercel rewrite (see vercel.json). */
      let r = await fetch("/initial-products.json", { cache: "no-cache" });
      if (!r.ok) r = await fetch("/public/initial-products.json", { cache: "no-cache" });
      if (r.ok) {
        json = await r.json();
        writeHomeSeedCache(json);
      }
    } catch {
      json = null;
    }
  }
  if (!json) return;

  const items = normalizeProductList(json);
  if (!items.length) return;

  const grid = document.getElementById("product-grid");
  if (!grid) return;

  const meta = json.meta || {};
  if (typeof meta.total === "number") state.total = meta.total;

  const isHome = document.body?.classList.contains("page-home");
  const cap = isHome ? Math.min(HOME_GRID_MAX_ITEMS, items.length) : items.length;
  const slice = items.slice(0, cap);
  slice.forEach((p, i) => {
    grid.appendChild(cardEl(p, { homeIndex: i }));
  });
  state.offset = slice.length;

  const limit = pageLimit();
  if (isHome) {
    state.done = true;
  } else if (items.length < limit || (state.total != null && state.offset >= state.total)) {
    state.done = true;
  } else {
    state.done = false;
  }
}

async function loadPage() {
  if (state.loading || state.done) return;
  /** Home grid is 100% seed JSON only; no /api/products on home (that API powers /products.html if opened directly). */
  if (document.body?.classList.contains("page-home")) return;

  state.loading = true;
  const btn = document.getElementById("load-more");
  const status = document.getElementById("products-status");
  const grid = document.getElementById("product-grid");
  if (btn) btn.disabled = true;
  if (status) status.textContent = "Loading…";

  let limit = pageLimit();
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(state.offset),
  });
  if (state.category) params.set("category", state.category);

  try {
    const parsed = await fetchApiJson("/api/products?" + params.toString());
    if (parsed.bodyError) {
      if (status) status.textContent = parsed.bodyError;
      state.done = true;
      if (btn) btn.hidden = true;
      return;
    }
    const json = parsed.json;

    if (!parsed.ok) {
      const msg = json.error || json.message || "Request failed";
      if (status) status.textContent = typeof msg === "string" ? msg : JSON.stringify(msg);
      state.done = true;
      if (btn) btn.hidden = true;
      return;
    }

    if (json && typeof json.error === "string" && json.error && !normalizeProductList(json).length) {
      if (status) status.textContent = json.error;
      state.done = true;
      if (btn) btn.hidden = true;
      return;
    }

    const items = normalizeProductList(json);
    const meta = json.meta || {};
    if (typeof meta.total === "number") state.total = meta.total;

    if (items.length === 0) {
      state.done = true;
      if (btn) btn.hidden = true;
      if (status) {
        if (state.offset === 0) {
          status.textContent = state.category
            ? "No products in this category right now. Try “All categories” or another category."
            : "No products to show for “All categories” yet. Try picking one category from the list.";
        } else {
          status.textContent = "End of list.";
        }
      }
      return;
    }

    let appended = 0;
    for (const p of items) {
      grid.appendChild(cardEl(p));
      appended++;
    }

    state.offset += appended;

    if (items.length < limit || (state.total != null && state.offset >= state.total)) {
      state.done = true;
      if (btn) btn.hidden = true;
    } else if (btn) {
      btn.hidden = false;
    }

    if (status) {
      if (state.total != null) {
        status.textContent = `Showing ${state.offset} of ${state.total}`;
      } else {
        status.textContent = `Loaded ${state.offset} items`;
      }
    }
  } catch (e) {
    const msg = String(e.message || e);
    const hint =
      /failed to fetch|load failed|networkerror/i.test(msg) && window.location.protocol === "file:"
        ? " Open this site over HTTP (e.g. vercel dev or your deployed URL); file:// cannot call /api."
        : /failed to fetch|load failed|networkerror/i.test(msg)
          ? " Check that /api/products is available (Vercel env MATRIX_API_KEY, or run vercel dev)."
          : "";
    if (status) status.textContent = msg + hint;
    state.done = true;
    if (btn) btn.hidden = true;
  } finally {
    state.loading = false;
    if (btn && !state.done) btn.disabled = false;
  }
}

function syncCategoryUrl() {
  const u = new URL(window.location.href);
  if (state.category) u.searchParams.set("category", state.category);
  else u.searchParams.delete("category");
  history.replaceState({}, "", u.pathname + u.search + u.hash);
}

function onFilterChange() {
  const sel = document.getElementById("filter-cat");
  state.category = sel ? sel.value : "";
  state.offset = 0;
  state.total = null;
  state.done = false;
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";
  const btn = document.getElementById("load-more");
  if (btn) {
    btn.hidden = false;
    btn.disabled = false;
  }
  syncCategoryUrl();
  loadPage();
}

async function init() {
  const sel = document.getElementById("filter-cat");
  const params = new URLSearchParams(window.location.search);
  const urlCat = params.get("category");
  /** Only `/products` has a category control; ignore `?category=` on the homepage or it blocks seed hydration. */
  if (sel && urlCat) state.category = urlCat;
  if (sel) sel.addEventListener("change", onFilterChange);

  const isHome = document.body?.classList.contains("page-home");
  const btn = document.getElementById("load-more");
  if (!isHome && btn) btn.addEventListener("click", () => loadPage());

  await loadCategories();
  if (sel && state.category) {
    sel.value = state.category;
    if (sel.value !== state.category) {
      state.category = "";
      syncCategoryUrl();
    }
  }
  await hydrateInitialProducts();
  if (isHome) {
    const grid = document.getElementById("product-grid");
    const emptyEl = document.getElementById("home-grid-empty");
    if (grid && emptyEl && grid.children.length === 0) {
      emptyEl.hidden = false;
      if (showHomeDevHints()) {
        emptyEl.textContent =
          "Homepage products load from /initial-products.json only (no API here). Run npm run seed-products with SEED_API_URL or commit public/initial-products.json, then redeploy. Or browse MaisonLooks: https://maisonlooks.com/zh/products";
      } else {
        emptyEl.innerHTML =
          'Preview couldn’t load. <a href="https://maisonlooks.com/zh/products" target="_blank" rel="noopener noreferrer">Open MaisonLooks all products</a>.';
      }
    }
  } else {
    await loadPage();
  }
}

init();
