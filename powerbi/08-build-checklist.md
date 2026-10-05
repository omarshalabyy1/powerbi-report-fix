# 8. Build checklist

Follow it top to bottom: the slow report first, then the fixed one, then the timings. **Check** lines are the numbers you must see before moving on; if one is off, [06-checks.md](06-checks.md) has the full set. Every number here is written by the notebook.

## Before Power BI

1. In the repo folder (the demo; a client's flat export goes in `data/input/` instead of the first script):
   ```bash
   pip install -r requirements.txt
   python data/demo/prepare_data.py
   python config.py
   jupyter nbconvert --to notebook --execute --inplace analysis/analysis.ipynb
   python theme.py
   ```
   **Check:** `python config.py` prints `config and input file OK`; the notebook's first table shows <!--n:sales_rows-->2,098,633<!--/n--> sales rows and it writes `output/sales.csv`, which the fixed report reads.
2. Install DAX Studio (free, daxstudio.org).
3. Open Power BI Desktop. If File > Save as has no **Power BI project files (*.pbip)** type: File > Options and settings > Options > Preview features > tick **Power BI Project (.pbip) save option**, restart Desktop.

## The slow report (`before/`)

4. **Blank report.** File > Options and settings > Options > Current file > Data load: **Auto date/time ticked** (`before/02-model.md`).
5. **Power Query** (`before/01-power-query.md`): the `Sales` query > Close & Apply.
   **Check** (Table view, row count bottom left): Sales <!--n:sales_rows-->2,098,633<!--/n--> rows.
6. **Model** (`before/02-model.md`): the six calculated columns from the top of `before/03-measures.dax`, each with its type and format; `Month` sorted by `Month Number`; `Year` and `Month Number` set to Don't summarize.
   **Check:** Model view shows one table and no lines.
7. **Measures** (`before/03-measures.dax`): the ten measures in file order, each with the format string in its comment.
   **Check:** drop Sales Amount into a temporary card, display units None: <!--n:sales_all-->$2,127,928,962<!--/n--> (all years). Delete the card.
8. **Theme** ([05-theme.json](05-theme.json)): View > Themes > Browse for themes > pick the file.
   **Check:** the page background turns the theme's light grey-blue page colour.
9. **Page Overview** ([04-pages.md](04-pages.md)): canvas 16:9, then P1-T, P1-S1 to P1-S3, P1-V1 to P1-V9 in order, with the Sales fields from the table in `before/README.md`. Year slicer on <!--n:check_year-->2023<!--/n-->.
   **Check:** Sales Amount <!--n:sales_check-->$318,425,878<!--/n--> · Sales YoY % <!--n:yoy_check-->-28.4%<!--/n--> · Margin % <!--n:margin_check-->56.0%<!--/n--> · Orders <!--n:orders_check-->159,695<!--/n--> · Avg Order Value <!--n:aov_check-->$1,993.96<!--/n--> · Customers <!--n:customers_check-->62,337<!--/n--> · top category bar <!--n:top_category-->Computers<!--/n-->.
10. **Page Products**: copy P1-T and the three slicers to a new page (choose **Sync**), then P2-V1 and P2-V2.
    **Check:** table row 1 is rank 1, <!--n:top_product-->Adventure Works 52" LCD HDTV X590 White<!--/n-->, <!--n:top_product_sales-->$2,317,817<!--/n-->; the table has <!--n:products_check-->2,517<!--/n--> rows; matrix Total <!--n:sales_check-->$318,425,878<!--/n-->.
11. **Sync slicers** (View > Sync slicers): Year, Country and Category synced and visible on both pages. Pick the second check (`report.second_check`): Year <!--n:s_year-->2022<!--/n-->, Country <!--n:s_country-->Germany<!--/n-->, Category <!--n:s_category-->Computers<!--/n-->.
    **Check:** Sales Amount <!--n:f_sales-->$19,645,197<!--/n--> · Sales YoY % <!--n:f_yoy-->93.5%<!--/n--> · Margin % <!--n:f_margin-->56.0%<!--/n--> · Orders <!--n:f_orders-->9,854<!--/n--> · Avg Order Value <!--n:f_aov-->$1,993.63<!--/n--> · Customers <!--n:f_customers-->5,197<!--/n-->. Set the slicers back: Year <!--n:check_year-->2023<!--/n-->, Country and Category cleared.
12. **Interactions** ([07-interactions.md](07-interactions.md)): set both matrices.
    **Check:** on Overview, click the <!--n:top_category-->Computers<!--/n--> bar: Sales Amount <!--n:top_category_sales-->$113,112,204<!--/n--> · Sales YoY % <!--n:top_category_yoy-->-36.1%<!--/n--> · Margin % <!--n:top_category_margin-->56.2%<!--/n-->. Click the bar again to clear it.
13. **Save:** File > Save as > Power BI project files > `powerbi/before/sales-before.pbip`.
14. **Time it** ([../docs/measuring.md](../docs/measuring.md)): close Desktop, reopen `sales-before.pbip`, then for each page clear the cache in DAX Studio and record with Performance Analyzer. Save `before-<page>.json` for each page in `measurements.pages` (the demo: `before-overview.json`, `before-products.json`) and `before.vpax` in `data/input/`.

## The fixed report

15. **Close Desktop** (it frees the slow model's memory), then open a **blank report**. File > Options and settings > Options > Current file > Data load: **Auto date/time unticked**.
16. **Power Query** ([01-power-query.md](01-power-query.md)): `DataFolder`, `Sales Flat` (load off), `Sales`, `Customer`, `Product` > Close & Apply.
    **Check:** Sales <!--n:sales_rows-->2,098,633<!--/n--> · Customer <!--n:customers_dim-->88,063<!--/n--> · Product <!--n:products_count-->2,517<!--/n--> rows.
17. **Model** ([02-model.md](02-model.md)): the Date table, then its type, mark as date table, sort-by and formats; the column formats; the three relationships; the hidden columns.
    **Check:** Date <!--n:date_rows-->3,653<!--/n--> rows; Model view shows the star (three lines, `1` on each dimension, `*` on Sales).
18. **Measures** ([03-measures.dax](03-measures.dax)): the ten measures with their format strings and display folders.
    **Check:** temporary card with Sales Amount, display units None: <!--n:sales_all-->$2,127,928,962<!--/n-->. Delete it.
19. **Theme:** as step 8.
20. **Pages, sync slicers and interactions:** steps 9 to 12 again, with the fixed report's fields as written in `04-pages.md`.
    **Check:** the same numbers as steps 9 to 12.
21. **Save:** File > Save as > Power BI project files > `powerbi/sales-after.pbip`.
22. **Time it:** as step 14, for `sales-after.pbip`. Save `after-<page>.json` for each page and `after.vpax` in `data/input/`.

## Finish

23. **Screenshots** of the fixed report, slicers at the default and nothing clicked: Win+Shift+S around the canvas, saved as `powerbi/screenshots/overview.png` and `powerbi/screenshots/products.png`.
24. **Hand back:** commit the two `.pbip` projects, the measurement files in `data/input/` and the two screenshots. Rerun the notebook: it reads the exports (`measure.py`) and writes the before and after numbers to `output/numbers.json`; for the demo, `python data/demo/publish.py` then puts the speed-up in the README, the diagrams and the site card.
