#!/usr/bin/env python3
"""Generate agent landing pages (Kakobuy-style length, unique copy per agent). Does not overwrite kakobuy.html.

SEO wording: each page should target that agent’s own “{Name} spreadsheet” phrasing (see agent_copy_pools.py)—not “kakobuy spreadsheet” on every platform’s page.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import json

import agent_copy_pools as acp

ROOT = Path(__file__).resolve().parent

# Icons live in public/agent-logos/ (see scripts/fetch_agent_logos.py). HTML uses public/agent-logos/… so paths match the repo.
LOGO_DIR = ROOT / "public" / "agent-logos"
_LOGO_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg")


def agent_logo_relpath(slug: str) -> str | None:
    """Return root-relative URL; files live under public/agent-logos/ (see fetch_agent_logos.py)."""
    for ext in _LOGO_EXTS:
        p = LOGO_DIR / f"{slug}{ext}"
        if p.is_file():
            return f"public/agent-logos/{slug}{ext}"
    return None


def agent_official_btn_content(host_label: str, slug: str) -> str:
    """Primary CTA label: optional brand icon + ‘Open hostname’."""
    label = f"Open {host_label}"
    rel = agent_logo_relpath(slug)
    if not rel:
        return label
    img = (
        f'<img class="agent-landing__official-logo" src="{rel}" width="28" height="28" alt="" '
        'decoding="async" loading="lazy" />'
    )
    return f'{img}<span class="agent-landing__official-btn-text">{label}</span>'


def agent_cta_logo_img(slug: str) -> str:
    """Smaller icon before the footer ‘{Name} official’ link."""
    rel = agent_logo_relpath(slug)
    if not rel:
        return ""
    return (
        f'<img class="agent-landing__cta-logo" src="{rel}" width="22" height="22" alt="" '
        'decoding="async" loading="lazy" />'
    )


# Primary homepages found via public search / live checks (Apr 2026). Verify periodically.
OFFICIAL_URLS: dict[str, str] = {
    "kakobuy": "https://kakobuy.com/",
    "litbuy": "https://litbuy.com/",
    "oopbuy": "https://oopbuy.com/",
    "sugargoo": "https://www.sugargoo.com/",
    "acbuy": "https://acbuy.com/",
    "superbuy": "https://www.superbuy.com/",
    "cssbuy": "https://www.cssbuy.com/",
    "lovegobuy": "https://www.lovegobuy.com/",
    "cnfans": "https://cnfans.com/",
    "hipobuy": "https://hipobuy.com/",
    "mulebuy": "https://mulebuy.com/",
    "ponybuy": "https://ponybuy.cc/",
    "allchinabuy": "https://www.allchinabuy.com/",
    "hoobuy": "https://hoobuy.com/",
    "basetao": "https://basetao.com/",
    "kameymall": "https://www.kameymall.com/",
    "eastmallbuy": "https://www.eastmallbuy.com/",
    "hubbuycn": "https://www.hubbuycn.com/",
    "joyagoo": "https://joyagoo.com/",
    "orientdig": "https://orientdig.com/",
    "loongbuy": "https://loongbuy.com/",
    "itaobuy": "https://itaobuys.com/",
    "cnshopper": "https://cnshopper.com/",
    "usfans": "https://usfans.com/",
    "gtbuy": "https://www.gtbuy.com/",
    "fishgoo": "https://www.fishgoo.com/",
}


def official_host_label(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc or url

# Order matches nav: priority agents first, then the rest (same as current site).
AGENTS: list[tuple[str, str]] = [
    ("kakobuy", "Kakobuy"),
    ("litbuy", "Litbuy"),
    ("oopbuy", "Oopbuy"),
    ("sugargoo", "Sugargoo"),
    ("acbuy", "ACBuy"),
    ("superbuy", "Superbuy"),
    ("cssbuy", "Cssbuy"),
    ("lovegobuy", "LoveGoBuy"),
    ("cnfans", "CnFans"),
    ("hipobuy", "Hipobuy"),
    ("mulebuy", "MuleBuy"),
    ("ponybuy", "PonyBuy"),
    ("allchinabuy", "AllChinaBuy"),
    ("hoobuy", "HooBuy"),
    ("basetao", "BaseTao"),
    ("kameymall", "KameyMall"),
    ("eastmallbuy", "EastMallBuy"),
    ("hubbuycn", "HubbuyCN"),
    ("joyagoo", "JoyaGoo"),
    ("orientdig", "OrientDig"),
    ("loongbuy", "LoongBuy"),
    ("itaobuy", "iTaoBuy"),
    ("cnshopper", "CnShopper"),
    ("usfans", "USFans"),
    ("gtbuy", "GTBuy"),
    ("fishgoo", "Fishgoo"),
]


def nav_block(current: str) -> str:
    lines = []
    for slug, name in AGENTS:
        cur = ' aria-current="page"' if slug == current else ""
        lines.append(f'              <a class="topbar-agent__link" href="/{slug}"{cur}>{name}</a>')
    return (
        '            <div class="topbar-agent__panel topbar-agent__panel--agents">\n'
        + "\n".join(lines)
        + "\n            </div>"
    )


def faq_json_ld(
    slug: str,
    name: str,
    official_url: str,
    host_label: str,
    faq_dl_plain: str,
    faq_vs_plain: str,
    faq_year_plain: str,
    year: str,
) -> str:
    q1_text = json.dumps(acp.faq_spreadsheet_jsonld_plain(slug, name), ensure_ascii=False)
    q_dl = json.dumps(faq_dl_plain, ensure_ascii=False)
    q_vs = json.dumps(faq_vs_plain, ensure_ascii=False)
    q_year = json.dumps(faq_year_plain, ensure_ascii=False)
    return f"""    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "What is a {name} spreadsheet?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": {q1_text}
            }}
          }},
          {{
            "@type": "Question",
            "name": "Is this page run by {name}?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "No. The best spreadsheet is independent. Logins, payments, warehouse QC, and shipping are always handled on your chosen agent platform—not on this discovery site."
            }}
          }},
          {{
            "@type": "Question",
            "name": "How is this different from Google Sheets or Excel?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Sheets go stale when sellers change links or stock. Here you scroll a web grid, search by keyword or image, and open current listings on MaisonLooks in a new tab."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Does browsing here cost money?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Using this discovery site is free. You only pay when you place an order, top up a balance, or ship a parcel on your shopping agent."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Where do I log in to {name}?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "On {name}'s own site at {official_url} (bookmark {host_label} from sources you trust). This discovery page is not their checkout."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Where do shipping calculators and tracking live?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Inside your agent account. This site does not show freight quotes or parcel tracking because it is not the logistics provider."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Are there guides for other agents?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Yes. Open the Agent menu—each platform has its own guide page on this site, all powered by the same discovery catalog."
            }}
          }},
          {{
            "@type": "Question",
            "name": "When should I use image search instead of keyword search?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Use keyword search when you know a brand, model name, or distinct token. Use image search when you only have a photo or screenshot and do not know how the listing is titled."
            }}
          }},
          {{
            "@type": "Question",
            "name": "What if a listing is out of stock after I find it?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Sellers restock, delist, or rotate batches. Re-search on the home grid, try image search again, or look for an updated link in communities—this site cannot reserve inventory."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Does The best spreadsheet ship to my country?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "No. This site is discovery only with no warehouse. International forwarding is arranged through your shopping agent after you place an order there."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Can I download a {name} spreadsheet file here?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": {q_dl}
            }}
          }},
          {{
            "@type": "Question",
            "name": "How is a shared {name} spreadsheet different from this page?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": {q_vs}
            }}
          }},
          {{
            "@type": "Question",
            "name": "Is there a single best {name} spreadsheet in {year}?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": {q_year}
            }}
          }}
        ]
      }}
    </script>"""


def page_html(slug: str, name: str) -> str:
    official_url = OFFICIAL_URLS[slug]
    host_label = official_host_label(official_url)
    year = acp.CONTENT_YEAR
    official_btn_inner = agent_official_btn_content(host_label, slug)
    cta_logo_html = agent_cta_logo_img(slug)

    lead = acp.format_lead(slug, name, host_label, official_url)
    intro2 = acp.pick_variant(slug, "intro2", acp.INTRO2)
    intro_ss = acp.intro_agent_spreadsheet_paragraph(slug, name)

    stat_a, stat_b, stat_c = acp.pick_variant(slug, "stats", acp.STATS)
    h2_catalog = acp.pick_variant(slug, "h2cat", acp.H2_CATALOG)
    h2_why = acp.pick_variant(slug, "h2why", acp.H2_WHY)
    h2_inside = acp.pick_variant(slug, "h2in", acp.H2_WHATS_INSIDE)
    h2_read = acp.pick_variant(slug, "h2read", acp.H2_READ_LISTING)
    h2_img = acp.pick_variant(slug, "h2img", acp.H2_IMAGE)
    h2_mist = acp.pick_variant(slug, "h2mist", acp.H2_MISTAKES)
    h2_customs = acp.pick_variant(slug, "h2cust", acp.H2_CUSTOMS)
    h2_when_not = acp.pick_variant(slug, "h2when", acp.H2_WHEN_NOT)
    steps_h2 = acp.pick_variant(slug, "h2steps", acp.STEPS_LEAD_INS).format(name=name)

    catalog_angle = acp.pick_variant(slug, "cata", acp.CATALOG_A)
    catalog_angle2 = acp.pick_variant(slug, "catb", acp.CATALOG_B)

    compare_rows = acp.pick_variant(slug, "compare", acp.COMPARE_TABLES)
    compare_tbody = ""
    for topic, left, right in compare_rows:
        t_cell = topic.format(name=name) if "{name}" in topic else topic
        l_cell = left.format(name=name) if "{name}" in left else left
        r_cell = right.format(name=name) if "{name}" in right else right
        compare_tbody += (
            "              <tr>\n"
            f"                <td>{t_cell}</td>\n"
            f"                <td>{l_cell}</td>\n"
            f"                <td>{r_cell}</td>\n"
            "              </tr>\n"
        )

    h3a, h3b, h3c = acp.pick_variant(slug, "feat_h3", acp.FEATURE_H3_SETS)
    h3a = h3a.format(name=name)
    h3b = h3b.format(name=name)
    h3c = h3c.format(name=name)

    feat1 = acp.pick_variant(slug, "feat1", acp.FEAT1_POOL)
    feat2 = acp.pick_variant(slug, "feat2", acp.FEAT2_POOL)
    feat3 = acp.pick_variant(slug, "feat3", acp.FEAT3_POOL).format(name=name)

    inside_bullets = acp.pick_variant(slug, "inside", acp.WHATS_INSIDE_BULLETS)
    inside_li = "\n".join(
        f"          <li>{b.format(name=name)}</li>" for b in inside_bullets
    )

    cat_intro = acp.pick_variant(slug, "catintro", acp.CATEGORY_INTROS)

    step_lines = acp.pick_variant(slug, "steps", acp.STEP_POOLS)
    steps_ol = ""
    for line in step_lines:
        steps_ol += f"          <li>\n            {line.format(name=name, host_label=host_label, official_url=official_url)}\n          </li>\n"

    checklist_rows = acp.pick_variant(slug, "check", acp.CHECKLIST)
    checklist_li = "\n".join(
        f'          <li>{row[0]}</li>' for row in checklist_rows
    )

    customs_p = acp.pick_variant(slug, "customs", acp.CUSTOMS_P).format(name=name)

    mistake_lines = acp.pick_variant(slug, "mistakes", acp.MISTAKE_SETS)
    mistake_li = "\n".join(
        f"          <li>{m.format(name=name, host_label=host_label)}</li>" for m in mistake_lines
    )

    what_is = acp.pick_variant(slug, "whatis", acp.WHAT_IS_POOL).format(name=name)
    weidian = acp.pick_variant(slug, "weidian", acp.WEIDIAN_POOL).format(name=name)
    timeline = acp.pick_variant(slug, "timeline", acp.TIMELINE_POOL).format(name=name)
    haul = acp.pick_variant(slug, "haul", acp.HAUL_POOL).format(name=name)
    when_not = acp.pick_variant(slug, "whennot", acp.WHEN_NOT_POOL).format(name=name)
    glossary_agent = acp.pick_variant(slug, "gloss_agent", acp.GLOSSARY_AGENT_POOL).format(name=name)
    svc_fee = acp.pick_variant(slug, "svc_fee", acp.SVC_FEE_POOL).format(name=name)
    read_listing = acp.pick_variant(slug, "readlist", acp.READ_LISTING_POOL)
    img_search = acp.pick_variant(slug, "imgsearch", acp.IMG_SEARCH_POOL)

    faq_ss_html = acp.faq_spreadsheet_meaning(slug, name)

    page_title = escape(
        acp.pick_variant(slug, "pgtitle", acp.META_PAGE_TITLES).format(
            name=name, host_label=host_label, official_url=official_url, year=year
        )
    )
    meta_desc = escape(
        acp.pick_variant(slug, "metades", acp.META_DESCRIPTIONS).format(
            name=name, host_label=host_label, official_url=official_url, year=year
        )
    )
    meta_keywords = escape(acp.meta_keywords_content(name, host_label, slug, year))
    h1_text = escape(acp.pick_variant(slug, "h1seo", acp.H1_TITLES).format(name=name, year=year))

    faq_dl_plain = acp.pick_variant(slug, "faq_dl", acp.FAQ_LONGTAIL_DOWNLOAD).format(name=name)
    faq_vs_plain = acp.pick_variant(slug, "faq_vs", acp.FAQ_LONGTAIL_VS_SITE).format(name=name)
    faq_year_plain = acp.pick_variant(slug, "faq_year", acp.FAQ_BEST_YEAR).format(
        name=name, year=year, host_label=host_label
    )
    faq_dl_html = escape(faq_dl_plain)
    faq_vs_html = escape(faq_vs_plain)
    faq_year_html = escape(faq_year_plain)

    h2_gwhat = escape(acp.pick_variant(slug, "h2gwhat", acp.H2_GUIDE_WHAT).format(name=name, year=year))
    p_gwhat = escape(acp.pick_variant(slug, "pgwhat", acp.P_GUIDE_WHAT).format(name=name, year=year, host_label=host_label))
    h2_wf = escape(
        acp.pick_variant(slug, "h2wf", acp.H2_WORKFLOW).format(
            name=name, year=year, host_label=host_label
        )
    )
    p_wf = escape(acp.pick_variant(slug, "pwf", acp.P_WORKFLOW).format(name=name, year=year, host_label=host_label))
    h2_qc = escape(acp.pick_variant(slug, "h2qc", acp.H2_QC_BATCH).format(name=name, year=year))
    p_qc = escape(acp.pick_variant(slug, "pqc", acp.P_QC_BATCH).format(name=name, year=year, host_label=host_label))
    h2_sets = escape(acp.pick_variant(slug, "h2sets", acp.H2_SETS_COORD).format(name=name, year=year))
    p_sets = escape(acp.pick_variant(slug, "psets", acp.P_SETS_COORD).format(name=name, year=year, host_label=host_label))

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="theme-color" content="#e9eff8" />
    <link rel="icon" href="/favicon.png" type="image/png" />
    <link rel="apple-touch-icon" href="/favicon.png" />
    <meta name="description" content="{meta_desc}" />
    <meta name="keywords" content="{meta_keywords}" />
    <title>{page_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="styles.css" />
{faq_json_ld(slug, name, official_url, host_label, faq_dl_plain, faq_vs_plain, faq_year_plain, year)}
  </head>
  <body class="page-products page-agent">
    <header class="site-header">
      <div class="topbar">
        <a class="topbar__logo" href="/">The best spreadsheet</a>
        <nav class="topbar__nav topbar__nav--compact" aria-label="Primary">
          <a class="topbar__link" href="/">Home</a>
          <details class="topbar-agent">
            <summary class="topbar-agent__summary">Agent</summary>
{nav_block(slug)}
          </details>
          <a class="topbar__link" href="/outfits">Outfits</a>
        </nav>
      </div>
    </header>

    <main class="products-main agent-landing" id="main">
      <article class="agent-landing__article">
        <h1>{h1_text}</h1>
        <p class="agent-landing__lead">
          {lead}
        </p>
        <p>
          {intro2}
        </p>
        <p>
          {intro_ss}
        </p>

        <ul class="agent-landing__stats" aria-label="Highlights">
          <li>{stat_a}</li>
          <li>{stat_b}</li>
          <li>{stat_c}</li>
        </ul>

        <div class="agent-landing__official">
          <p class="agent-landing__official-text">
            {name} official entry
            <span>Log in, paste links, warehouse QC &amp; shipping—on {name}’s own site. Always confirm <strong>{host_label}</strong> in your address bar; ignore look-alike domains.</span>
          </p>
          <div class="agent-landing__official-cta">
            <a
              class="agent-landing__official-btn"
              href="{official_url}"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Open {name} official site ({host_label})"
              >{official_btn_inner}</a
            >
            <a class="topbar__link" href="/">Browse discovery grid first</a>
          </div>
        </div>

        <h2>{h2_gwhat}</h2>
        <p>
          {p_gwhat}
        </p>

        <h2>{h2_wf}</h2>
        <p>
          {p_wf}
        </p>

        <h2>{h2_qc}</h2>
        <p>
          {p_qc}
        </p>

        <h2>{h2_sets}</h2>
        <p>
          {p_sets}
        </p>

        <h2>{h2_catalog}</h2>
        <p>
          {catalog_angle}
        </p>
        <p>
          {catalog_angle2}
        </p>

        <h3>Community spreadsheet vs this browser (at a glance)</h3>
        <div class="agent-landing__table-wrap">
          <table class="agent-landing__compare">
            <thead>
              <tr>
                <th scope="col">Topic</th>
                <th scope="col">Typical shared sheet</th>
                <th scope="col">The best spreadsheet (this site)</th>
              </tr>
            </thead>
            <tbody>
{compare_tbody}            </tbody>
          </table>
        </div>

        <h2>{h2_why}</h2>
        <div class="agent-landing__feature-grid">
          <section class="agent-landing__feature">
            <h3>{h3a}</h3>
            <p>
              {feat1}
            </p>
          </section>
          <section class="agent-landing__feature">
            <h3>{h3b}</h3>
            <p>
              {feat2} Combine with the <a href="/outfits">Outfits</a> lane when you want coordinated ideas instead of a lone SKU.
            </p>
          </section>
          <section class="agent-landing__feature">
            <h3>{h3c}</h3>
            <p>
              {feat3}
            </p>
          </section>
        </div>

        <h2>{h2_inside}</h2>
        <ul>
{inside_li}
        </ul>

        <h2>Browse by category (MaisonLooks)</h2>
        <p>
          {cat_intro}
        </p>
        <div class="agent-landing__cat-grid">
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/products" target="_blank" rel="noopener noreferrer">All products</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/sneakers" target="_blank" rel="noopener noreferrer">Sneakers</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/outerwear" target="_blank" rel="noopener noreferrer">Outerwear</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/tops" target="_blank" rel="noopener noreferrer">Tops</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/bottoms" target="_blank" rel="noopener noreferrer">Bottoms</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/bags-backpacks" target="_blank" rel="noopener noreferrer">Bags</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/accessories" target="_blank" rel="noopener noreferrer">Accessories</a>
          <a class="agent-landing__cat-btn" href="https://maisonlooks.com/zh/c/electronics" target="_blank" rel="noopener noreferrer">Electronics</a>
        </div>
        <p class="agent-landing__topic-cluster">
          More on this site: <a href="/">spreadsheet home</a>,
          <a href="/products">all products</a>, and
          <a href="/outfits">Outfits</a> (coordinated looks)—browse here, then checkout on
          <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a>.
        </p>

        <h2>What is {name} (the short version)</h2>
        <p>
          {what_is}
        </p>

        <h2>{steps_h2}</h2>
        <ol class="agent-landing__steps">
{steps_ol}        </ol>

        <h2>What to double-check before you pay</h2>
        <ul class="agent-landing__checklist">
{checklist_li}
        </ul>

        <div class="agent-landing__callout">
          <strong>Safety tip.</strong> Phishing loves agent keywords. Bookmark <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a> from a source you trust; never trust a “shortcut” spreadsheet that asks for passwords.
        </div>

        <h2>Weidian, Taobao, 1688 &amp; Yupoo-style research</h2>
        <p>
          {weidian}
        </p>

        <h3>Quick glossary</h3>
        <dl class="agent-landing__glossary">
          <dt>Agent</dt>
          <dd>{glossary_agent}</dd>
          <dt>QC</dt>
          <dd>Warehouse photos before you approve international shipping—not the seller’s marketing render.</dd>
          <dt>W2C / finds</dt>
          <dd>Discovery slang for hunting a link before anyone commits cash.</dd>
          <dt>Haul</dt>
          <dd>A parcel plan; use the grid to decide what belongs together before you ship.</dd>
          <dt>Domestic leg</dt>
          <dd>Seller → agent warehouse; fast until factories or holidays interfere.</dd>
          <dt>Service fee</dt>
          <dd>{svc_fee}</dd>
          <dt>Consolidation</dt>
          <dd>Merging warehouse items to tame volumetric shipping—handled inside your agent UI.</dd>
          <dt>Rehearsal / packing</dt>
          <dd>Optional pre-weigh/pack to estimate freight—names differ by platform.</dd>
        </dl>

        <h2>{h2_read}</h2>
        <p>
          {read_listing}
        </p>

        <h2>{h2_img}</h2>
        <p>
          {img_search}
        </p>

        <div class="agent-landing__callout agent-landing__callout--info">
          <strong>Tip.</strong> Keep <a href="/">the spreadsheet home</a> open for discovery and <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a> logged in for submissions—two-pane discipline beats losing tabs to Discord chaos.
        </div>

        <h2>{h2_mist}</h2>
        <ul class="agent-landing__checklist">
{mistake_li}
        </ul>

        <h2>Rough timeline (order → door)</h2>
        <p>
          Expect <strong>order → domestic transit → warehouse → QC → outbound → customs → delivery</strong>, with seasonal spikes. {timeline}
        </p>

        <h2>{h2_customs}</h2>
        <p>
          {customs_p}
        </p>

        <h2>Building a haul without a tab for every SKU</h2>
        <p>
          {haul}
        </p>

        <h2>{h2_when_not}</h2>
        <p>
          {when_not}
        </p>

        <h2>FAQ</h2>
        <dl class="agent-landing__faq">
          <dt>What is a {name} spreadsheet?</dt>
          <dd>
            {faq_ss_html}
          </dd>
          <dt>Is this run by {name}?</dt>
          <dd>
            No. Money, passwords, and parcel data stay on <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a>—bookmark it from sources you trust.
          </dd>
          <dt>How is this different from Google Sheets or Excel?</dt>
          <dd>
            Files freeze; listings move. Here the UI stays wired to current pages instead of static rows.
          </dd>
          <dt>Does browsing here cost money?</dt>
          <dd>
            No. You pay when you order through your agent—not for scrolling this guide.
          </dd>
          <dt>Where is the official {name} website?</dt>
          <dd>
            Primary site: <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a>. If the hostname differs by even one character, stop and re-verify—typosquatting is routine.
          </dd>
          <dt>Where do shipping calculators and tracking live?</dt>
          <dd>
            Inside {name} after you log in. We do not mirror freight quotes or tracking IDs.
          </dd>
          <dt>Do you have guides for other agents?</dt>
          <dd>
            Yes—open the Agent menu; each platform has its own page on this site with the same discovery backbone.
          </dd>
          <dt>When should I use image search instead of keyword search?</dt>
          <dd>
            Keywords when you can name things; images when you cannot.
          </dd>
          <dt>What if a listing is out of stock after I find it?</dt>
          <dd>
            Sellers rotate stock constantly. Re-run search, try image lookup again, or ask your community for a refreshed link.
          </dd>
          <dt>Does The best spreadsheet ship to my country?</dt>
          <dd>
            No—we are discovery only. {name} or another agent handles international forwarding after you purchase there.
          </dd>
          <dt>Can I download a {name} spreadsheet file here?</dt>
          <dd>
            {faq_dl_html}
          </dd>
          <dt>How is a shared {name} spreadsheet different from this page?</dt>
          <dd>
            {faq_vs_html}
          </dd>
          <dt>Is there a single best {name} spreadsheet in {year}?</dt>
          <dd>
            {faq_year_html}
          </dd>
        </dl>

        <div class="agent-landing__cta">
          <a class="hero__title-btn" href="/">Open the spreadsheet home</a>
          <a
            class="topbar__link agent-landing__cta-kb"
            href="{official_url}"
            target="_blank"
            rel="noopener noreferrer"
            >{cta_logo_html}{name} official ({host_label})</a
          >
          <a class="topbar__link" href="/products">All products</a>
          <a class="topbar__link" href="https://maisonlooks.com/zh" target="_blank" rel="noopener noreferrer">MaisonLooks</a>
        </div>

        <p class="agent-landing__more-agents">
          Every agent in the <strong>Agent</strong> menu above has a dedicated guide page powered by the same catalog.
        </p>

        <h2>About this page</h2>
        <p>
          <strong>The best spreadsheet</strong> is independent editorial and discovery. It is not affiliated with {name} or MaisonLooks beyond linking to public pages. We do not sell goods, run warehouses, or process agent payments—for purchases and shipping, use <a href="{official_url}" target="_blank" rel="noopener noreferrer">{host_label}</a> and the marketplace’s own terms.
        </p>

        <p class="agent-landing__note">
          “{name}” is a third-party trademark. This content is general information only and does not imply endorsement. Prices, availability, and policies change—confirm on live listings and inside your agent before you pay.
        </p>
      </article>
    </main>
  </body>
</html>
"""


def inject_nav(path: Path, current_slug: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_nav = nav_block(current_slug)
    text2, n = re.subn(
        r'\n\s*<div class="topbar-agent__panel topbar-agent__panel--agents">[\s\S]*?</div>\s*(?=\s*</details>)',
        "\n" + new_nav,
        text,
        count=1,
    )
    if n != 1:
        raise RuntimeError(f"Nav replace failed in {path} (matches={n})")
    path.write_text(text2, encoding="utf-8")


def main() -> None:
    for slug, name in AGENTS:
        if slug == "kakobuy":
            continue
        out = ROOT / f"{slug}.html"
        out.write_text(page_html(slug, name), encoding="utf-8")
        print("wrote", out.name)

    # No agent landing is "current" on home / products / outfits; Kakobuy guide highlights Kakobuy.
    none_slug = "__n__"
    for fname, cur in [
        ("index.html", none_slug),
        ("products.html", none_slug),
        ("outfits.html", none_slug),
        ("kakobuy.html", "kakobuy"),
    ]:
        inject_nav(ROOT / fname, cur)


if __name__ == "__main__":
    main()
