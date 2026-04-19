---
doc: maisonlooks_public_api
audience: ai_agent
purpose: read-only product/category/outfit data for static site generation
version: v1
updated_at: 2026-04-19
---

# MaisonLooks Public API — Handoff

## Deploy (this repo)

1. Vercel → **Environment Variables**: `MATRIX_API_KEY` (Production + Preview).
2. Routes: `/api/categories`, `/api/products`, `/api/outfits` are serverless proxies; the browser never sees the key.
3. Pages: `index.html` (hero + category bar from `topbar-cats.js`: **All products** → `https://maisonlooks.com/zh/products`; other links → `https://maisonlooks.com/zh/c/{slug}`; new tab; **fill one row** then **More**; edit `LINKS`; image-only grid; scroll loads more, `limit=200`), `products.html` (full catalog UI + API-filled category dropdown, `limit=48` + Load more + `?category=`), `outfits.html` (outfits grid).

**Homepage first paint (optional):** `public/initial-products.json` is read by `products.js` before the first `/api/products` call so the grid can render without waiting on the slow round-robin. Commit a small seed or run **`npm run seed-products`** with **`SEED_API_URL`** set (e.g. `https://buysspreadsheet.com/api/products?limit=200&offset=0`) so the build can refresh the file. If `SEED_API_URL` is unset, the generator skips and leaves the existing file unchanged. Advanced: inline JSON in `window.__INITIAL_PRODUCTS__` or a `<script id="initial-products-json" type="application/json">` in HTML for zero extra request.

**Caching:** Successful JSON responses set `Cache-Control` (`s-maxage` for CDN, `max-age` for browser). Serverless handlers also keep a short in-memory TTL cache (warm instance). The static `api-parse.js` uses `fetchApiJson()` with a per-URL memory cache in the tab to avoid duplicate fetches (e.g. `products.js`).

**Do not commit API keys.** GitHub 里只保留占位说明；真实密钥只放在下面两处之一，**永远不要**写进 `docs/` 或任何会 push 的文件。

## Local (your machine only)

1. 复制 `.env.example` 为 **`.env.local`**（已在 `.gitignore` 中，不会被提交）。
2. 在 `.env.local` 里填写：`MATRIX_API_KEY=你的密钥`（从 MaisonLooks 或你本地的交接文档里复制）。
3. 本地运行 **`vercel dev`** 时，会自动读取 `.env.local`；或用  
   `MATRIX_API_KEY=... node scripts/fetch-products.mjs`.

线上仍用 Vercel 后台的环境变量，与本地 `.env.local` 相互独立。

## Auth

- Header: `X-API-Key: <your key>` (set via env `MATRIX_API_KEY` — **never commit or expose in browser**)
- Base URL: `https://api.maisonlooks.com`
- Version path: `/public/v1`
- Rate limit: 300 req/min per IP
- Constraint: **server-side / build-time only**. Do not call from browser code.

## Endpoints

### `GET /public/v1/categories`

Returns array of categories that have active products.

```ts
type PublicCategory = {
  slug: string;            // canonical id, matches main-site /c/{slug}
  name: string;
  parentSlug: string | null;
  imageUrl: string | null;
  productCount: number | null;
};
```

### `GET /public/v1/products`

Query params:

| param | required | default | max |
|---|---|---|---|
| `category` | no | — | — | filter by category slug |
| `limit` | no | 20 | 100 |
| `offset` | no | 0 | — |

Response: `{ data: PublicProduct[], meta: { total, page, limit } }`

```ts
type PublicProduct = {
  slug: string;
  title: string;
  description: string | null;
  category: string | null;
  brand: string | null;
  priceCnyRange: [number, number] | null;
  priceCny: number | null;
  priceUsdEstimate: [number, number] | null;
  images: string[];
  qcPhotoCount: number;
  hasTryOn: boolean;
  updatedAt: string;
};
```

### `GET /public/v1/products/{slug}`

Returns single `PublicProduct`. 404 if not found.

### `GET /public/v1/outfits`

Query params: `featured` (bool, default false), `limit` (default 20, max 100), `offset` (default 0), `productSlug` (string, optional).

### `GET /public/v1/outfits/{id}`

Returns single `PublicOutfit`.

## Verified curl (replace `<KEY>`)

```bash
curl -H "X-API-Key: <KEY>" \
  https://api.maisonlooks.com/public/v1/categories
```

## Slug aliases (common mistakes)

| Wrong | Correct |
|---|---|
| `shoes` | `sneakers` |
| `hoodies-sweaters` | `hoodies-sweatshirts` |
| `coats` | `outerwear` |
| `tees` | `t-shirts` |

Always validate slugs against `/public/v1/categories` before constructing product queries.

## Reference fetcher

See `scripts/fetch-products.mjs` in this repo. Run:

```bash
MATRIX_API_KEY=your_key node scripts/fetch-products.mjs
```

Writes `./data/{categories,products,outfits,_meta}.json`.

## Operational notes

- API data refreshes every ~30 min.
- On HTTP 5xx: do not break the build; reuse last successful `data/*.json`.
- Key is single-purpose; do not share or expose in client bundles.
