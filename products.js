const ML_PRODUCT = "https://maisonlooks.com/zh/p/";
const PAGE_LIMIT = 48;

const state = {
  offset: 0,
  total: null,
  category: "",
  loading: false,
  done: false,
};

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

function cardEl(p) {
  const a = document.createElement("a");
  a.className = "product-card";
  a.href = ML_PRODUCT + encodeURIComponent(p.slug);
  a.target = "_blank";
  a.rel = "noopener noreferrer";

  const img = document.createElement("img");
  img.className = "product-card__img";
  img.src = (p.images && p.images[0]) || "";
  img.alt = "";
  img.loading = "lazy";
  img.decoding = "async";
  img.onerror = () => {
    img.removeAttribute("src");
    img.classList.add("product-card__img--placeholder");
  };

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

  a.appendChild(img);
  a.appendChild(body);
  return a;
}

async function loadCategories() {
  const sel = document.getElementById("filter-cat");
  if (!sel) return;
  try {
    const r = await fetch("/api/categories");
    const data = await r.json();
    if (!r.ok) {
      sel.disabled = true;
      return;
    }
    const list = Array.isArray(data) ? data : data.data || [];
    const sorted = [...list].sort((a, b) =>
      String(a.name || a.slug).localeCompare(String(b.name || b.slug)),
    );
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

async function loadPage() {
  if (state.loading || state.done) return;
  state.loading = true;
  const btn = document.getElementById("load-more");
  const status = document.getElementById("products-status");
  const grid = document.getElementById("product-grid");
  if (btn) btn.disabled = true;
  if (status) status.textContent = "Loading…";

  const params = new URLSearchParams({
    limit: String(PAGE_LIMIT),
    offset: String(state.offset),
  });
  if (state.category) params.set("category", state.category);

  try {
    const r = await fetch("/api/products?" + params.toString());
    const json = await r.json();

    if (!r.ok) {
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
      if (status) status.textContent = state.offset === 0 ? "No products in this filter." : "End of list.";
      return;
    }

    for (const p of items) {
      grid.appendChild(cardEl(p));
    }

    state.offset += items.length;

    if (items.length < PAGE_LIMIT || (state.total != null && state.offset >= state.total)) {
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
  const params = new URLSearchParams(window.location.search);
  const urlCat = params.get("category");
  if (urlCat) state.category = urlCat;

  const sel = document.getElementById("filter-cat");
  if (sel) sel.addEventListener("change", onFilterChange);
  const btn = document.getElementById("load-more");
  if (btn) btn.addEventListener("click", () => loadPage());

  await loadCategories();
  if (sel && state.category) {
    sel.value = state.category;
    if (sel.value !== state.category) {
      state.category = "";
      syncCategoryUrl();
    }
  }
  loadPage();
}

init();
