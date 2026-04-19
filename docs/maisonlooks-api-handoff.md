---
doc: maisonlooks_public_api
audience: ai_agent
purpose: read-only product/category/outfit data for static site generation
version: v1
updated_at: 2026-04-19
---

# MaisonLooks Public API — Handoff

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
