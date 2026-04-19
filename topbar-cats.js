/**
 * “Categories” dropdown (MaisonLooks). Desktop: `#topbar-cats`; mobile (≤900px): `#hero-cats` under the hero CTA.
 * Same slugs as GET /public/v1/categories — paths /zh/c/{slug}.
 */
(function () {
  /** Chinese site base; category pages are /zh/c/{slug} per API handoff */
  const ML_ZH = "https://maisonlooks.com/zh";

  /** Must match the `max-width` breakpoint in `styles.css` for hero vs topbar. */
  const MQ = window.matchMedia("(max-width: 900px)");

  /** `slug` → `${ML_ZH}/c/{slug}`. "All products" → `/zh/products` (全部商品). */
  const LINKS = [
    { label: "All products", href: `${ML_ZH}/products` },
    { label: "Sneakers", slug: "sneakers" },
    { label: "Boots", slug: "boots" },
    { label: "Sandals & Slippers", slug: "sandals-slippers" },
    { label: "Loafers & Flats", slug: "loafers-flats" },
    { label: "Heels", slug: "heels" },
    { label: "Sets & Suits", slug: "sets-suits" },
    { label: "Dresses & One-piece", slug: "dresses-one-piece" },
    { label: "Outerwear", slug: "outerwear" },
    { label: "Tops", slug: "tops" },
    { label: "Bottoms", slug: "bottoms" },
    { label: "Bags & Backpacks", slug: "bags-backpacks" },
    { label: "Accessories", slug: "accessories" },
    { label: "Beauty & Fragrance", slug: "beauty-fragrance" },
    { label: "Electronics", slug: "electronics" },
  ];

  let categoriesRoot = null;

  function itemHref(item) {
    if (item.slug) return `${ML_ZH}/c/${encodeURIComponent(item.slug)}`;
    return item.href || `${ML_ZH}/products`;
  }

  function buildLink(item) {
    const a = document.createElement("a");
    a.className = "topbar-cats__link";
    a.href = itemHref(item);
    a.textContent = item.label;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    return a;
  }

  function wireDropdownDetails(details, summary) {
    summary.addEventListener(
      "click",
      (e) => {
        e.preventDefault();
        details.open = !details.open;
      },
      true,
    );
  }

  function placeOpenDropdownPanel() {
    const det = document.querySelector(
      "#topbar-cats details.topbar-cats__dropdown[open], #hero-cats details.topbar-cats__dropdown[open]",
    );
    if (!det) return;
    const summary = det.querySelector("summary");
    const panel = det.querySelector(".topbar-cats__dropdown-panel");
    if (!summary || !panel) return;
    const r = summary.getBoundingClientRect();
    const vw = window.innerWidth;
    const rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
    /** Side inset so the panel never clips off-screen (esp. when the trigger is centered and narrow). */
    const inset = 12;
    const maxPanelW = Math.min(20 * rem, Math.max(0, vw - inset * 2));
    const centerX = r.left + r.width / 2;
    let left = centerX - maxPanelW / 2;
    left = Math.max(inset, Math.min(left, vw - inset - maxPanelW));

    panel.style.setProperty("position", "fixed");
    panel.style.setProperty("z-index", "10001");
    panel.style.setProperty("top", `${Math.round(r.bottom + 6)}px`);
    panel.style.setProperty("left", `${Math.round(left)}px`);
    panel.style.setProperty("right", "auto");
    panel.style.setProperty("width", `${Math.round(maxPanelW)}px`);
    panel.style.setProperty("max-width", `${Math.round(maxPanelW)}px`);
    panel.style.setProperty("box-sizing", "border-box");
  }

  function wireDropdownPanelLayer(details, panel) {
    details.addEventListener("toggle", () => {
      if (!details.open) {
        panel.removeAttribute("style");
      } else {
        placeOpenDropdownPanel();
        requestAnimationFrame(placeOpenDropdownPanel);
      }
    });
  }

  let moveListenersBound = false;
  function bindMoveListeners() {
    if (moveListenersBound) return;
    moveListenersBound = true;
    const onMove = () => placeOpenDropdownPanel();
    window.addEventListener("resize", onMove);
    window.addEventListener("scroll", onMove, true);
  }

  function buildDropdown() {
    const details = document.createElement("details");
    details.className = "topbar-cats__dropdown";

    const summary = document.createElement("summary");
    summary.className = "topbar-cats__dropdown-summary";
    summary.textContent = "Categories";

    const panel = document.createElement("div");
    panel.className = "topbar-cats__dropdown-panel";
    LINKS.forEach((item) => {
      const a = buildLink(item);
      a.addEventListener("click", () => {
        details.open = false;
        panel.removeAttribute("style");
      });
      panel.appendChild(a);
    });

    details.appendChild(summary);
    details.appendChild(panel);

    wireDropdownDetails(details, summary);
    wireDropdownPanelLayer(details, panel);
    bindMoveListeners();

    return details;
  }

  function mountCategories() {
    const top = document.getElementById("topbar-cats");
    const hero = document.getElementById("hero-cats");
    if (!top) return;

    if (!categoriesRoot) {
      categoriesRoot = buildDropdown();
    }

    const useHero = Boolean(hero && MQ.matches);
    const target = useHero ? hero : top;
    const other = useHero ? top : hero;

    if (categoriesRoot.open) categoriesRoot.open = false;
    const panel = categoriesRoot.querySelector(".topbar-cats__dropdown-panel");
    if (panel) panel.removeAttribute("style");

    if (other) other.textContent = "";
    target.textContent = "";
    target.appendChild(categoriesRoot);
  }

  function init() {
    mountCategories();
    if (typeof MQ.addEventListener === "function") {
      MQ.addEventListener("change", mountCategories);
    } else if (typeof MQ.addListener === "function") {
      MQ.addListener(mountCategories);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
