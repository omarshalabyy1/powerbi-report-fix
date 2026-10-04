# 4. Pages and visuals

Two pages, the same in the slow report and the fixed report, so the timings compare like for like. Fields are written for the fixed report; the slow report uses the matching Sales column (the mapping is in [before/README.md](before/README.md)). Measures have the same names in both.

Canvas: View > Page view > Fit to page; Format page > Canvas settings > 16:9 (1280 × 720). Positions are in pixels: Format visual > General > Properties > Size and Position.

Everything not listed is left at the default: default tooltips, no drill-through, no bookmarks, default interactions (clicking a bar cross-highlights the other visuals).

## Page 1: Overview

Rename the page **Overview**.

| # | Visual | X | Y | W | H | Fields | Settings |
|---|---|---|---|---|---|---|---|
| 1 | Text box | 20 | 10 | 600 | 50 | "Sales overview" | Font 20, bold |
| 2 | Slicer | 700 | 10 | 180 | 60 | `Date[Year]` | Style Dropdown; Selection: Single select on; select **2023** |
| 3 | Slicer | 890 | 10 | 180 | 60 | `Customer[Country]` | Style Dropdown; multi-select; nothing selected |
| 4 | Slicer | 1080 | 10 | 180 | 60 | `Product[Category]` | Style Dropdown; multi-select; nothing selected |
| 5 | Card | 20 | 80 | 200 | 100 | Sales Amount | Callout value display units: **None** |
| 6 | Card | 230 | 80 | 200 | 100 | Sales YoY % | Display units None |
| 7 | Card | 440 | 80 | 200 | 100 | Margin % | Display units None |
| 8 | Card | 650 | 80 | 200 | 100 | Orders | Display units None |
| 9 | Card | 860 | 80 | 200 | 100 | Avg Order Value | Display units None |
| 10 | Card | 1070 | 80 | 190 | 100 | Customers | Display units None |
| 11 | Line and clustered column chart | 20 | 200 | 820 | 500 | X-axis `Date[Month]`; Column y-axis Sales Amount; Line y-axis Sales PY | Title "Sales and previous year by month"; sort by Month ascending (it follows Month Number) |
| 12 | Clustered bar chart | 850 | 200 | 410 | 245 | Y-axis `Product[Category]`; X-axis Sales Amount | Title "Sales by category"; sort by Sales Amount descending; data labels on, display units Millions |
| 13 | Clustered bar chart | 850 | 455 | 410 | 245 | Y-axis `Customer[Country]`; X-axis Sales Amount | Title "Sales by country"; sort by Sales Amount descending; data labels on, display units Millions |

## Page 2: Products

Rename the page **Products**. Copy the title text box and the three slicers from page 1 (Ctrl+C, Ctrl+V) and choose **Sync** when Power BI asks, then change the title.

| # | Visual | X | Y | W | H | Fields | Settings |
|---|---|---|---|---|---|---|---|
| 1 | Text box | 20 | 10 | 600 | 50 | "Products" | Font 20, bold |
| 2 to 4 | Slicers | as page 1 | | | | Year, Country, Category | Synced with page 1 |
| 5 | Table | 20 | 80 | 760 | 620 | `Product[Product Name]`, Sales Amount, Sales PY, Sales YoY %, Margin %, Customers, Product Rank | Title "Products by sales"; sort by Sales Amount descending; Totals **off**; Cell elements: Data bars on Sales Amount; Font colour on Sales YoY % by rules: below 0 red `#DC2626`, 0 and above green `#16A34A` |
| 6 | Matrix | 790 | 80 | 470 | 620 | Rows `Product[Category]`, then `Product[Subcategory]`; Values Sales Amount, Sales YoY %, Margin % | Title "Sales by category"; Row subtotals on; Grand total on; sort by Sales Amount descending; expand to Category level only (collapsed) |

## Sync slicers

View > Sync slicers. For each of Year, Country and Category: both **Sync** and **Visible** ticked on Overview and Products. Picking 2022 on one page then shows 2022 on the other.

## Before you take screenshots or timings

Set the slicers back to the default: Year 2023, Country and Category with nothing selected. The numbers in [06-checks.md](06-checks.md) are for this state.
