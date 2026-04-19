/**
 * Fills #topbar-cats from GET /api/categories (same-origin proxy on Vercel).
 */
async function initTopbarCategories() {
  const nav = document.getElementById("topbar-cats");
  if (!nav) return;

  try {
    const r = await fetch("/api/categories");
    const data = await r.json();
    if (!r.ok) {
      nav.innerHTML =
        '<span class="topbar-cats__fallback">Categories unavailable — check MATRIX_API_KEY on the server.</span>';
      return;
    }

    const list = Array.isArray(data) ? data : data.data || [];
    nav.innerHTML = "";

    const sorted = [...list].sort((a, b) =>
      String(a.name || a.slug).localeCompare(String(b.name || b.slug)),
    );

    for (const c of sorted) {
      const a = document.createElement("a");
      a.className = "topbar-cats__link";
      a.href = "products.html?category=" + encodeURIComponent(c.slug);
      a.textContent = c.name || c.slug;
      nav.appendChild(a);
    }
  } catch {
    nav.innerHTML =
      '<span class="topbar-cats__fallback">Could not load categories.</span>';
  }
}

initTopbarCategories();
