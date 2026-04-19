/**
 * Fills the teal category bar: show as many links as fit on one row, then fold the rest under "More".
 * Links open MaisonLooks (same slugs as GET /public/v1/categories — main site path /zh/c/{slug}).
 */
(function () {
  /** Chinese site base; category pages are /zh/c/{slug} per API handoff */
  const ML_ZH = "https://maisonlooks.com/zh";

  /** `slug` → `${ML_ZH}/c/{slug}`. "All products" → `/zh/search` (full catalog), not `/zh/` (marketing home). */
  const LINKS = [
    { label: "All products", href: `${ML_ZH}/search` },
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

  function itemHref(item) {
    if (item.slug) return `${ML_ZH}/c/${encodeURIComponent(item.slug)}`;
    return item.href || `${ML_ZH}/search`;
  }

  let debounceTimer;
  let measureHost;

  function contentWidth(el) {
    if (!el) return 0;
    const st = getComputedStyle(el);
    return el.clientWidth - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight);
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

  function measureWidths(nav) {
    if (measureHost && measureHost.parentNode) measureHost.parentNode.removeChild(measureHost);
    measureHost = document.createElement("div");
    measureHost.className = "topbar-cats topbar-cats--measure";
    measureHost.setAttribute("aria-hidden", "true");
    measureHost.style.cssText =
      "position:absolute;left:0;top:0;visibility:hidden;pointer-events:none;z-index:-1;width:max-content;";
    const line = document.createElement("div");
    line.className = "topbar-cats__line";
    LINKS.forEach((item) => line.appendChild(buildLink(item)));
    measureHost.appendChild(line);
    nav.appendChild(measureHost);

    const cs = getComputedStyle(line);
    const gapRaw =
      cs.columnGap && cs.columnGap !== "normal" ? cs.columnGap : cs.gap && cs.gap !== "normal" ? cs.gap : "0";
    const gapPx = parseFloat(gapRaw) || 0;
    const widths = [...line.querySelectorAll("a")].map((a) => a.getBoundingClientRect().width);

    const moreLine = document.createElement("div");
    moreLine.className = "topbar-cats__line";
    const det = document.createElement("details");
    det.className = "topbar-cats__more";
    const sum = document.createElement("summary");
    sum.className = "topbar-cats__link topbar-cats__more-summary";
    sum.textContent = "More";
    det.appendChild(sum);
    moreLine.appendChild(det);
    measureHost.appendChild(moreLine);
    const moreW = det.getBoundingClientRect().width;

    nav.removeChild(measureHost);
    measureHost = null;

    return { widths, gapPx, moreW };
  }

  /** prefix[k] = width of first k links including gaps between them */
  function prefixSums(widths, gapPx) {
    const p = [0];
    for (let i = 0; i < widths.length; i++) {
      p.push(p[p.length - 1] + (i > 0 ? gapPx : 0) + widths[i]);
    }
    return p;
  }

  function maxFit(prefix, lineW, moreW, gapPx) {
    const n = LINKS.length;
    let best = 1;
    for (let k = n; k >= 1; k--) {
      const needMore = k < n;
      const total = prefix[k] + (needMore ? gapPx + moreW : 0);
      if (total <= lineW + 2) {
        best = k;
        break;
      }
    }
    return best;
  }

  function render() {
    const nav = document.getElementById("topbar-cats");
    const lineEl = document.getElementById("topbar-cats-line");
    if (!nav || !lineEl) return;

    const lineW = contentWidth(nav);
    if (lineW < 40) return;

    const { widths, gapPx, moreW } = measureWidths(nav);
    const prefix = prefixSums(widths, gapPx);
    const k = maxFit(prefix, lineW, moreW, gapPx);

    lineEl.innerHTML = "";

    for (let i = 0; i < k; i++) {
      lineEl.appendChild(buildLink(LINKS[i]));
    }

    if (k < LINKS.length) {
      const details = document.createElement("details");
      details.className = "topbar-cats__more";
      const summary = document.createElement("summary");
      summary.className = "topbar-cats__link topbar-cats__more-summary";
      summary.textContent = "More";
      const panel = document.createElement("div");
      panel.className = "topbar-cats__more-panel";
      for (let j = k; j < LINKS.length; j++) {
        panel.appendChild(buildLink(LINKS[j]));
      }
      details.appendChild(summary);
      details.appendChild(panel);
      lineEl.appendChild(details);
    }
  }

  function debouncedRender() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => requestAnimationFrame(render), 80);
  }

  function init() {
    render();
    const nav = document.getElementById("topbar-cats");
    if (!nav) return;
    if (typeof ResizeObserver !== "undefined") {
      const ro = new ResizeObserver(debouncedRender);
      ro.observe(nav);
    } else {
      window.addEventListener("resize", debouncedRender);
    }
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(debouncedRender);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
