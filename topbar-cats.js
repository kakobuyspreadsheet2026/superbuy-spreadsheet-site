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

  /** iOS Safari: `position:fixed` inside `<details>` / under `.hero` can paint below composited layers; host on `body` while open. */
  const PANEL_Z = "2147483000";

  function placeOpenDropdownPanel() {
    const det = document.querySelector(
      "#topbar-cats details.topbar-cats__dropdown[open], #hero-cats details.topbar-cats__dropdown[open]",
    );
    if (!det) return;
    const summary = det.querySelector("summary");
    /** After `portalPanelToBodyIfHero`, the panel is no longer under `det` — still the only `.topbar-cats__dropdown-panel` on the page. */
    const panel =
      det.querySelector(".topbar-cats__dropdown-panel") ||
      document.querySelector(".topbar-cats__dropdown-panel");
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

    /**
     * When the panel is under `document.body`, stylesheet `top: calc(100% + …)` + `position:absolute`
     * resolves `%` against the wrong containing block on WebKit → ~100vh → menu jumps to viewport bottom.
     * `!important` beats that rule so fixed coordinates always apply.
     */
    const imp = "important";
    const topPx = Math.round(r.bottom + 6);
    panel.style.setProperty("position", "fixed", imp);
    panel.style.setProperty("z-index", PANEL_Z, imp);
    panel.style.setProperty("top", `${topPx}px`, imp);
    panel.style.setProperty("left", `${Math.round(left)}px`, imp);
    panel.style.setProperty("right", "auto", imp);
    panel.style.setProperty("bottom", "auto", imp);
    panel.style.setProperty("width", `${Math.round(maxPanelW)}px`, imp);
    panel.style.setProperty("max-width", `${Math.round(maxPanelW)}px`, imp);
    panel.style.setProperty("box-sizing", "border-box", imp);
    panel.style.setProperty("-webkit-transform", "translateZ(0)", imp);
    panel.style.setProperty("transform", "translateZ(0)", imp);
  }

  function restorePanelIntoDetails(details, panel) {
    if (!panel || !details) return;
    if (panel.parentNode === document.body) {
      details.appendChild(panel);
    }
  }

  function portalPanelToBodyIfHero(details, panel) {
    const hero = document.getElementById("hero-cats");
    if (!hero || !hero.contains(details) || !MQ.matches) return;
    if (panel.parentNode === document.body) return;
    document.body.appendChild(panel);
  }

  function wireDropdownPanelLayer(details, panel) {
    details.addEventListener("toggle", () => {
      if (!details.open) {
        panel.removeAttribute("style");
        restorePanelIntoDetails(details, panel);
      } else {
        /* Position while panel is still inside `details`, then move to body (iOS) — keeps first paint valid. */
        placeOpenDropdownPanel();
        portalPanelToBodyIfHero(details, panel);
        placeOpenDropdownPanel();
        requestAnimationFrame(() => {
          placeOpenDropdownPanel();
          requestAnimationFrame(() => {
            placeOpenDropdownPanel();
            setTimeout(placeOpenDropdownPanel, 0);
            setTimeout(placeOpenDropdownPanel, 50);
          });
        });
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
    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", onMove);
      window.visualViewport.addEventListener("scroll", onMove);
    }
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
        restorePanelIntoDetails(details, panel);
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

    const panel = categoriesRoot.querySelector(".topbar-cats__dropdown-panel");
    if (panel && panel.parentNode === document.body) {
      categoriesRoot.appendChild(panel);
    }

    const useHero = Boolean(hero && MQ.matches);
    const target = useHero ? hero : top;
    const other = useHero ? top : hero;

    if (categoriesRoot.open) categoriesRoot.open = false;
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
