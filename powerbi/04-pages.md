# 4. Pages and visuals

Two pages, the same in the slow report and the fixed report, so the timings compare like for like. Fields are written for the fixed report; the slow report uses the matching Sales column (the mapping is in [before/README.md](before/README.md)). Measures have the same names in both.

Canvas: Format page > Canvas settings > Type 16:9 (1280 × 720); View > Page view > Fit to page. Positions are in pixels: Format visual > General > Properties > Size and Position. Build the visuals in the order listed.

Colours are named by theme slot from [05-theme.json](05-theme.json) (Theme colour 1 = first `dataColors` entry, and so on), never typed by hand. Number formats come from the measures ([03-measures.dax](03-measures.dax)); no visual overrides them, except the display units noted below. Every visual keeps the default tooltip (its own fields); there are no tooltip fields, tooltip pages, drill-through pages, bookmarks or buttons. Interactions are in [07-interactions.md](07-interactions.md).

## Page 1: Overview

Rename the page **Overview** (double-click the tab).

| ID | Visual | X | Y | W | H | Fields (well: field) | Format |
|---|---|---|---|---|---|---|---|
| P1-T | Text box | 20 | 10 | 600 | 50 | Text: "Sales overview" | Segoe UI Semibold, 20, colour: Theme colour 2 (navy) |
| P1-S1 | Slicer | 700 | 10 | 180 | 60 | Field: `Date[Year]` | Slicer settings > Style: **Dropdown**; Selection: **Single select** on; select **<!--n:check_year-->2023<!--/n-->** (`report.check_year`). Header on |
| P1-S2 | Slicer | 890 | 10 | 180 | 60 | Field: `Customer[Country]` | Style: Dropdown; Single select off (Ctrl+click picks several); "Select all" option off; nothing selected. Header on |
| P1-S3 | Slicer | 1080 | 10 | 180 | 60 | Field: `Product[Category]` | As P1-S2 |
| P1-V1 | Card | 20 | 80 | 200 | 100 | Fields: Sales Amount | Callout value: display units **None**; Category label on (shows the measure name); Title off |
| P1-V2 | Card | 230 | 80 | 200 | 100 | Fields: Sales YoY % | As P1-V1 |
| P1-V3 | Card | 440 | 80 | 200 | 100 | Fields: Margin % | As P1-V1 |
| P1-V4 | Card | 650 | 80 | 200 | 100 | Fields: Orders | As P1-V1 |
| P1-V5 | Card | 860 | 80 | 200 | 100 | Fields: Avg Order Value | As P1-V1 |
| P1-V6 | Card | 1070 | 80 | 190 | 100 | Fields: Customers | As P1-V1 |
| P1-V7 | Line and clustered column chart | 20 | 200 | 820 | 500 | X-axis: `Date[Month]` · Column y-axis: Sales Amount · Line y-axis: Sales PY · Column legend: empty · Tooltips: empty | Title on: "Sales and previous year by month"; Legend on, position Top; Data labels off; Y-axis display units Millions; Sort axis: Month, ascending (follows Month Number) |
| P1-V8 | Clustered bar chart | 850 | 200 | 410 | 245 | Y-axis: `Product[Category]` · X-axis: Sales Amount · Legend: empty · Tooltips: empty | Title on: "Sales by category"; Data labels on, display units Millions, 2 decimal places; Legend off; Sort axis: Sales Amount, descending |
| P1-V9 | Clustered bar chart | 850 | 455 | 410 | 245 | Y-axis: `Customer[Country]` · X-axis: Sales Amount · Legend: empty · Tooltips: empty | Title on: "Sales by country"; otherwise as P1-V8 |

13 visuals: a text box, 3 slicers, 6 cards, 3 charts.

## Page 2: Products

Add a page (+ at the bottom) and rename it **Products**. Copy P1-T and the three slicers from page 1 (Ctrl+C, then Ctrl+V on page 2) and choose **Sync** when Power BI asks; they keep their positions. Change the title text.

| ID | Visual | X | Y | W | H | Fields (well: field) | Format |
|---|---|---|---|---|---|---|---|
| P2-T | Text box | 20 | 10 | 600 | 50 | Text: "Products" | As P1-T |
| P2-S1 to P2-S3 | Slicers | as P1-S1 to P1-S3 | | | | Year, Country, Category | Synced with page 1 |
| P2-V1 | Table | 20 | 80 | 760 | 620 | Columns, in this order: `Product[Product Name]`, Sales Amount, Sales PY, Sales YoY %, Margin %, Customers, Product Rank | Title on: "Products by sales"; Totals **off**; Sort: Sales Amount, descending; Cell elements: **Data bars** on Sales Amount (positive bar: Theme colour 1); **Font colour** on Sales YoY % by rules: if value is less than 0 then the theme's `bad` colour (Custom colour, value from `05-theme.json`), if value is greater than or equal to 0 then Theme colour 1 |
| P2-V2 | Matrix | 790 | 80 | 470 | 620 | Rows: `Product[Category]`, then `Product[Subcategory]` · Columns: empty · Values: Sales Amount, Sales YoY %, Margin % | Title on: "Sales by category"; Layout: Stepped; Row subtotals on; Grand total on; Sort: Sales Amount, descending; leave it collapsed to Category |

6 visuals: a text box, 3 slicers, a table, a matrix. 19 visuals in the report.

## Sync slicers

View > Sync slicers. For each of Year, Country and Category: **Sync** and **Visible** ticked on Overview and Products. Picking a year on one page then shows it on the other.

## Before you take screenshots or timings

Set the slicers back to the default: Year <!--n:check_year-->2023<!--/n-->, Country and Category with nothing selected, nothing clicked. The numbers in [06-checks.md](06-checks.md) are for this state.
