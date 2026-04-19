const ML_OUTFIT = "https://maisonlooks.com/zh/outfits/";
const PAGE_LIMIT = 24;

const state = {
  offset: 0,
  total: null,
  loading: false,
  done: false,
  featuredOnly: true,
};

function outfitCard(o) {
  const a = document.createElement("a");
  a.className = "outfit-card";
  a.href = ML_OUTFIT + encodeURIComponent(o.id);
  a.target = "_blank";
  a.rel = "noopener noreferrer";

  const img = document.createElement("img");
  img.className = "outfit-card__img";
  img.src = o.resultImage || "";
  img.alt = "";
  img.loading = "lazy";
  img.decoding = "async";
  img.onerror = () => {
    img.removeAttribute("src");
    img.classList.add("outfit-card__img--placeholder");
  };

  const meta = document.createElement("div");
  meta.className = "outfit-card__meta";
  if (o.likeCount != null) {
    const likes = document.createElement("span");
    likes.className = "outfit-card__likes";
    likes.textContent = "♥ " + o.likeCount;
    meta.appendChild(likes);
  }
  if (o.imageStyle) {
    const st = document.createElement("span");
    st.className = "outfit-card__style";
    st.textContent = o.imageStyle;
    meta.appendChild(st);
  }

  a.appendChild(img);
  if (meta.childNodes.length) a.appendChild(meta);
  return a;
}

async function loadPage() {
  if (state.loading || state.done) return;
  state.loading = true;
  const btn = document.getElementById("load-more-outfits");
  const status = document.getElementById("outfits-status");
  const grid = document.getElementById("outfit-grid");
  if (btn) btn.disabled = true;
  if (status) status.textContent = "Loading…";

  const params = new URLSearchParams({
    limit: String(PAGE_LIMIT),
    offset: String(state.offset),
  });
  if (state.featuredOnly) params.set("featured", "true");

  try {
    const r = await fetch(apiUrl("/api/outfits?" + params.toString()));
    const parsed = await readApiJson(r);
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

    const items = Array.isArray(json.data) ? json.data : Array.isArray(json) ? json : [];
    const meta = json.meta || {};
    if (typeof meta.total === "number") state.total = meta.total;

    if (items.length === 0) {
      state.done = true;
      if (btn) btn.hidden = true;
      if (status)
        status.textContent =
          state.offset === 0 ? "No outfits returned." : "End of list.";
      return;
    }

    for (const o of items) {
      grid.appendChild(outfitCard(o));
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
        status.textContent = `Loaded ${state.offset} outfits`;
      }
    }
  } catch (e) {
    if (status) status.textContent = String(e.message || e);
    state.done = true;
    if (btn) btn.hidden = true;
  } finally {
    state.loading = false;
    if (btn && !state.done) btn.disabled = false;
  }
}

function init() {
  const btn = document.getElementById("load-more-outfits");
  const feat = document.getElementById("filter-featured");
  if (btn) btn.addEventListener("click", () => loadPage());
  if (feat) {
    feat.addEventListener("change", () => {
      state.featuredOnly = feat.checked;
      state.offset = 0;
      state.total = null;
      state.done = false;
      document.getElementById("outfit-grid").innerHTML = "";
      if (btn) {
        btn.hidden = false;
        btn.disabled = false;
      }
      loadPage();
    });
  }
  loadPage();
}

init();
