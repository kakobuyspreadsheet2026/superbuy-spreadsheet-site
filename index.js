/**
 * Fills #topbar-cats from GET /api/categories (same-origin proxy on Vercel).
 */
async function initTopbarCategories() {
  const nav = document.getElementById("topbar-cats");
  if (!nav) return;

  try {
    const parsed = await fetchApiJson("/api/categories");
    if (parsed.bodyError) {
      nav.innerHTML = "";
      const span = document.createElement("span");
      span.className = "topbar-cats__fallback";
      span.textContent = parsed.bodyError;
      nav.appendChild(span);
      return;
    }
    const data = parsed.json;
    if (!parsed.ok) {
      nav.innerHTML =
        '<span class="topbar-cats__fallback">Categories unavailable — check MATRIX_API_KEY on the server.</span>';
      return;
    }

    const list = Array.isArray(data)
      ? data
      : Array.isArray(data?.data)
        ? data.data
        : Array.isArray(data?.categories)
          ? data.categories
          : [];
    nav.innerHTML = "";

    const sorted = sortCategoriesApparelFirst(list);
    let primary = sorted.filter(isShoeClothingCategory);
    let more = sorted.filter((c) => !isShoeClothingCategory(c));
    let useFallbackFlat = false;
    if (primary.length === 0 && more.length > 0) {
      useFallbackFlat = true;
      primary = sorted;
      more = [];
    }

    function appendCatLink(container, c) {
      const a = document.createElement("a");
      a.className = "topbar-cats__link";
      a.href = "?category=" + encodeURIComponent(c.slug);
      a.textContent = c.name || c.slug;
      container.appendChild(a);
    }

    function sortByName(arr) {
      return [...arr].sort((a, b) =>
        String(a.name || a.slug).localeCompare(String(b.name || b.slug), undefined, {
          sensitivity: "base",
        }),
      );
    }

    const primaryRow = document.createElement("div");
    primaryRow.className = "topbar-cats__primary";

    if (useFallbackFlat) {
      for (const c of primary) {
        appendCatLink(primaryRow, c);
      }
    } else {
      const shoes = sortByName(primary.filter((c) => categoryApparelRank(c) === 0));
      const clothes = sortByName(primary.filter((c) => categoryApparelRank(c) === 1));

      function appendGroup(labelText, cats) {
        if (!cats.length) return;
        const lab = document.createElement("span");
        lab.className = "topbar-cats__group-label";
        lab.setAttribute("role", "presentation");
        lab.textContent = labelText;
        primaryRow.appendChild(lab);
        for (const c of cats) {
          appendCatLink(primaryRow, c);
        }
      }

      appendGroup("Shoes", shoes);
      appendGroup("Clothing", clothes);
    }

    if (more.length > 0) {
      const details = document.createElement("details");
      details.className = "topbar-cats__more";

      const summary = document.createElement("summary");
      summary.className = "topbar-cats__link topbar-cats__more-summary";
      summary.textContent = "More categories";

      const dropdown = document.createElement("div");
      dropdown.className = "topbar-cats__more-dropdown";
      for (const c of more) {
        appendCatLink(dropdown, c);
      }

      details.appendChild(summary);
      details.appendChild(dropdown);
      primaryRow.appendChild(details);
    }

    nav.appendChild(primaryRow);
  } catch {
    nav.innerHTML =
      '<span class="topbar-cats__fallback">Could not load categories.</span>';
  }
}

initTopbarCategories();
