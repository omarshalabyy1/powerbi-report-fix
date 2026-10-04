# 7. Interactions and filters

The same in both reports. Timings are taken with nothing clicked, so these settings do not change the measurement.

## Edit interactions

On each page: select the **source** visual > **Format > Edit interactions** > on every other visual click the icon in the table (**Filter** = funnel, **None** = circle with a line). Click **Edit interactions** again to finish. Visual IDs are from [04-pages.md](04-pages.md).

Why Filter, not Highlight: the cards and percentages must recompute for the selection; a highlight would leave them at the page total.

Why None on the slicers: a click on a chart should not change what the slicer lists offer.

### Page 1: Overview

| Source ↓ / Target → | V1 to V6 cards | V7 Month chart | V8 Category bars | V9 Country bars | S1 to S3 slicers |
|---|---|---|---|---|---|
| P1-V7 month chart (click a month) | Filter | — | Filter | Filter | None |
| P1-V8 category bars (click a bar) | Filter | Filter | — | Filter | None |
| P1-V9 country bars (click a bar) | Filter | Filter | Filter | — | None |

The cards are not sources: clicking a card does nothing.

### Page 2: Products

| Source ↓ / Target → | V1 Table | V2 Matrix | S1 to S3 slicers |
|---|---|---|---|
| P2-V1 table (click a product) | — | Filter | None |
| P2-V2 matrix (click a category or subcategory) | Filter | — | None |

The slicers (P1-S1 to S3, P2-S1 to S3) and the text boxes keep the defaults: each slicer filters every visual on its page and is synced across both pages; the text boxes have no data.

## Filters

| Level | Filter |
|---|---|
| Report (all pages) | None |
| Page | None on both pages |
| Visual | None |

## Not used

- **Drill-through pages:** none. The Products page already lists every product.
- **Bookmarks and buttons:** none. Move between pages with the page tabs.
- **Tooltip pages:** none. Every visual keeps the default tooltip (its own fields).
