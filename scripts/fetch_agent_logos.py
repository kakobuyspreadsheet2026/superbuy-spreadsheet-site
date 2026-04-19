#!/usr/bin/env python3
"""Download each agent's official site icon (apple-touch-icon / high-DPI favicon / favicon.ico).

Saves under public/agent-logos/{slug}.{ext} for use next to "official site" links.
Requires network. Re-run to refresh; verify licenses/trademarks for your jurisdiction.

Usage: python3 scripts/fetch_agent_logos.py
"""

from __future__ import annotations

import re
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "public" / "agent-logos"

# Reuse canonical URLs from the site generator (single source of truth).
sys.path.insert(0, str(ROOT))
from build_agent_pages import OFFICIAL_URLS  # noqa: E402

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
TIMEOUT = 40
CTX = ssl.create_default_context()

# Simpler: find link tags and parse rel + href
LINK_ANY_RE = re.compile(r"<link\b([^>]+)>", re.I)


def _attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'{name}\s*=\s*["\']([^"\']*)["\']', attrs, re.I)
    return m.group(1).strip() if m else None


def parse_og_image(html: str, base_url: str) -> str | None:
    m = re.search(
        r'<meta\s+property\s*=\s*["\']og:image["\']\s+content\s*=\s*["\']([^"\']+)["\']',
        html,
        re.I,
    )
    if m:
        return urljoin(base_url, m.group(1).strip())
    m2 = re.search(
        r'<meta\s+content\s*=\s*["\']([^"\']+)["\']\s+property\s*=\s*["\']og:image["\']',
        html,
        re.I,
    )
    if m2:
        return urljoin(base_url, m2.group(1).strip())
    return None


def parse_icon_candidates(html: str, base_url: str) -> list[tuple[int, str]]:
    """Return (priority_score, absolute_url). Higher score = prefer for display."""
    candidates: list[tuple[int, str]] = []
    for m in LINK_ANY_RE.finditer(html):
        attrs = m.group(1)
        rel = (_attr(attrs, "rel") or "").lower()
        href = _attr(attrs, "href")
        sizes = (_attr(attrs, "sizes") or "").lower()
        if not href or "stylesheet" in rel:
            continue
        if "icon" not in rel and rel not in ("shortcut icon", "apple-touch-icon", "apple-touch-icon-precomposed"):
            continue
        abs_url = urljoin(base_url, href.strip())
        score = 0
        if "apple-touch" in rel:
            score += 500
        if "192" in sizes or "180" in sizes:
            score += 200
        if "512" in sizes or "256" in sizes:
            score += 150
        if "any" in sizes:
            score += 40
        if rel == "icon" and "mask" not in rel:
            score += 50
        if href.endswith(".svg"):
            score += 30
        if href.endswith(".png") or ".png" in href:
            score += 20
        if "32x32" in sizes or "48x48" in sizes:
            score += 10
        candidates.append((score, abs_url))
    candidates.sort(key=lambda x: -x[0])
    return candidates


def sniff_ext(data: bytes, url: str) -> str:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:4] in (b"\x00\x00\x01\x00",) or data[:4] == b"\x00\x00\x02\x00":
        return "ico"
    if data.strip().startswith(b"<svg") or b"<svg" in data[:200]:
        return "svg"
    path = urlparse(url).path.lower()
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg"):
        if path.endswith(ext):
            return ext[1:]
    return "bin"


def fetch_bytes(url: str) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=TIMEOUT, context=CTX) as r:
            if r.status != 200:
                return None
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError):
        return None


def origin_root(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}/"


def alternate_origins(url: str) -> list[str]:
    """Try www and apex variants (some CDNs only serve one)."""
    p = urlparse(url)
    roots: list[str] = [f"{p.scheme}://{p.netloc}/"]
    host = p.netloc.lower()
    if host.startswith("www."):
        apex = host[4:]
        roots.append(f"{p.scheme}://{apex}/")
    else:
        roots.append(f"{p.scheme}://www.{host}/")
    # de-dupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for r in roots:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


FALLBACK_PATHS = (
    "/favicon.ico",
    "/favicon.png",
    "/apple-touch-icon.png",
    "/apple-touch-icon-precomposed.png",
    "/static/favicon.ico",
    "/favicon.jpg",
)


def try_download_best(slug: str, candidate_urls: list[str], index_lines: list[str]) -> bool:
    for u in candidate_urls:
        data = fetch_bytes(u)
        if not data or len(data) < 32:
            continue
        ct = ""
        # Reject HTML masquerading as icon
        if data[:1] == b"<" or b"<html" in data[:500].lower():
            continue
        ext = sniff_ext(data, u)
        if ext == "bin":
            continue
        out = OUT_DIR / f"{slug}.{ext}"
        out.write_bytes(data)
        print(f"  OK -> {out.name} ({len(data)} bytes) from {u}")
        index_lines.append(f"- **{slug}**: `{out.name}` ← {u}\n")
        return True
    return False


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# Agent logos (fetched from official sites)\n", "\n"]
    for slug in sorted(OFFICIAL_URLS.keys()):
        home = OFFICIAL_URLS[slug]
        print(f"{slug}: {home}")
        html = fetch_bytes(home)
        text = ""
        if html:
            try:
                text = html.decode("utf-8", errors="ignore")
            except Exception:
                text = ""

        candidates: list[str] = []
        if text:
            for _score, icon_url in parse_icon_candidates(text, home):
                candidates.append(icon_url)
            og = parse_og_image(text, home)
            if og:
                candidates.append(og)

        for root in alternate_origins(home):
            for path in FALLBACK_PATHS:
                candidates.append(urljoin(root, path.lstrip("/")))

        saved = try_download_best(slug, candidates, index_lines)

        if not saved and text:
            # Last resort: og:image (banner; still helps recognition on tricky SPAs)
            og = parse_og_image(text, home)
            if og and og not in candidates:
                saved = try_download_best(slug, [og], index_lines)

        if not saved:
            print(f"  FAIL: no icon saved after {len(candidates)} candidate URL(s)")
            index_lines.append(f"- **{slug}**: no file saved (blocked or no icon)\n")

    readme = OUT_DIR / "README.md"
    readme.write_text("".join(index_lines), encoding="utf-8")
    print(f"\nWrote manifest {readme}")


if __name__ == "__main__":
    main()
