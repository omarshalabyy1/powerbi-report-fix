# The slow report (the "before" state)

This report is slow on purpose. It is built the way slow sales reports usually get built: one wide table straight from the export, Power BI's automatic date tables, calculated columns for every small sum, and measures that work row by row. It shows exactly the same numbers as the fixed report. Only the speed and the size differ, and that difference is what this project measures.

## What makes it slow and big

| Choice | Why it costs |
|---|---|
| One flat table, all <!--n:flat_columns-->35<!--/n--> columns | Every customer address, birthday and product name is stored again on each of the <!--n:rows_million-->2.1 million<!--/n--> order lines. Power BI stores each column separately, and long text columns with many different values take the most space. |
| Auto date/time left on | Power BI quietly builds a hidden date table for every date column (Order Date, Delivery Date, Birthday), each covering every day between the earliest and latest date. |
| Six calculated columns | `Line Amount`, `Line Cost` and `Line Margin` store a decimal for every row, values a measure could compute at query time. |
| `AVERAGEX ( VALUES ( Sales[Order Key] ), [Sales Amount] )` | Recalculates Sales Amount once per order (<!--n:orders_2023-->159,695<!--/n--> orders in 2023) instead of one division. |
| `COUNTROWS ( SUMMARIZE ( ... ) )` | Builds a table of keys just to count it, where `DISTINCTCOUNT` does it directly. |
| `IF ( [Sales Amount] = 0, ..., [Margin] / [Sales Amount] )` | Evaluates the same measure several times instead of once into a variable. |

## Files, in build order

| File | Contents |
|---|---|
| [01-power-query.md](01-power-query.md) | Auto date/time left on, and the one query with all 35 columns |
| [02-model.md](02-model.md) | The one table, the calculated columns' types and formats, sort-by, and why each choice is slow |
| [03-measures.dax](03-measures.dax) | Six calculated columns and the ten slow measures |
| [../05-theme.json](../05-theme.json) | The same theme as the fixed report |
| [../04-pages.md](../04-pages.md) | The same two pages, with the Sales fields below in place of the dimension fields |
| [../07-interactions.md](../07-interactions.md) | The same interactions |
| [../06-checks.md](../06-checks.md) | The same numbers |

The full click-by-click order, with the numbers to check at each step, is [../08-build-checklist.md](../08-build-checklist.md). Save as **Power BI project files (*.pbip)** at `powerbi/before/sales-before.pbip`.

## Fields on the pages

`04-pages.md` and `07-interactions.md` name the fixed report's fields. In this report use:

| Fixed report field | Slow report field |
|---|---|
| `Date[Year]` | `Sales[Year]` |
| `Date[Month]` | `Sales[Month]` |
| `Customer[Country]` | `Sales[Country]` |
| `Product[Category]` | `Sales[Category]` |
| `Product[Subcategory]` | `Sales[Subcategory]` |
| `Product[Product Name]` | `Sales[Product Name]` |
