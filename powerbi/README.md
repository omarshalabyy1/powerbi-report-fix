# Power BI: build both reports

Two reports with the same two pages and the same numbers. The **slow report** (`before/`) is one flat table with the habits that make reports slow. The **fixed report** (this folder) is the same report rebuilt as a star schema with a date table and clean DAX.

## What the report answers

- How much did we sell this year, at what margin, and how does it compare with last year?
- Which months, categories and countries drive the change?
- Which products sell most, and are they growing or shrinking?

## Pages

| Page | Visuals |
|---|---|
| Overview | Year, Country and Category slicers; six cards (Sales Amount, Sales YoY %, Margin %, Orders, Avg Order Value, Customers); sales and previous year by month; sales by category; sales by country |
| Products | The same slicers, synced; a table of every product with its rank, sales, previous year, growth, margin and customers; a category and subcategory matrix |

## Files

Start with [08-build-checklist.md](08-build-checklist.md): it walks both reports click by click, from a blank report to the six timing files, with the numbers to check at each step.

| File | Slow report (`before/`) | Fixed report (this folder) |
|---|---|---|
| Power Query | [before/01-power-query.md](before/01-power-query.md): one query, all 35 columns, Auto date/time on | [01-power-query.md](01-power-query.md): parameter, staging query, Sales, Customer, Product |
| Model | [before/02-model.md](before/02-model.md): one table, six calculated columns, why each choice is slow | [02-model.md](02-model.md): Date table, formats, relationships, hidden columns, display folders, why each choice |
| DAX | [before/03-measures.dax](before/03-measures.dax): six calculated columns, ten slow measures | [03-measures.dax](03-measures.dax): ten measures, no calculated columns |
| Pages | [04-pages.md](04-pages.md) with the Sales fields from [before/README.md](before/README.md) | [04-pages.md](04-pages.md): 2 pages, 19 visuals, position, wells and format of each |
| Theme | [05-theme.json](05-theme.json) | [05-theme.json](05-theme.json): View > Themes > Browse for themes |
| Checks | [06-checks.md](06-checks.md) | [06-checks.md](06-checks.md): every number each page must show, written by the notebook |
| Interactions | [07-interactions.md](07-interactions.md) | [07-interactions.md](07-interactions.md): edit-interactions matrices, filters, nothing else |
| Build order | [08-build-checklist.md](08-build-checklist.md) | [08-build-checklist.md](08-build-checklist.md) |
| Saved as | `before/sales-before.pbip` | `sales-after.pbip` |

Screenshots of the fixed report go in `screenshots/` (`overview.png`, `products.png`); the timings in [../measurements/](../measurements/README.md).
