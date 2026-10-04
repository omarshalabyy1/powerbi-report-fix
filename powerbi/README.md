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

## Order

Run `python prepare_data.py` once first: it writes `data/sales_flat.csv`, the file both reports read.

**Slow report:** follow [before/README.md](before/README.md), then check it against [06-checks.md](06-checks.md).

**Fixed report:**

1. [01-power-query.md](01-power-query.md): untick Auto date/time, then the parameter, the staging query and the three tables.
2. [02-model.md](02-model.md): the Date table, the relationships, hidden columns and display folders.
3. [03-measures.dax](03-measures.dax): the ten measures with their formats.
4. [05-theme.json](05-theme.json): View > Themes > Browse for themes.
5. [04-pages.md](04-pages.md): the two pages, visual by visual.
6. [06-checks.md](06-checks.md): every card, chart and table against the notebook's numbers.
7. File > Save as > Power BI project files > `powerbi/sales-after.pbip`.
8. Screenshot each page (View > Fit to page, then Win+Shift+S around the canvas) into `screenshots/overview.png` and `screenshots/products.png`, with the slicers in the default state.

Then measure both reports: [../measurements/README.md](../measurements/README.md).
