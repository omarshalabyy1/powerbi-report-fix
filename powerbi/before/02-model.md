# 2. The model (slow report): one flat table

Each choice below is the usual one in slow reports, and the reason it costs speed or size.

## Table

| Table | Type | Grain (one row per) | Key | Rows |
|---|---|---|---|---|
| Sales | One flat table, everything in it | order line | none | <!--n:sales_rows-->2,098,633<!--/n--> |

| Choice | Why it is slow or big |
|---|---|
| All 35 columns loaded | Every customer address, birthday and product name is stored again for every order line. Power BI stores each column separately; long text columns with many different values take the most memory. |
| No relationships, no dimensions | Every filter and every sum runs on the one wide table. |
| Auto date/time on | Power BI builds a hidden date table for each date column (Order Date, Delivery Date, Birthday), each covering every day between that column's first and last date. |
| No date table | Previous-year logic has to be written by hand on a Year column (see `Sales PY` in `03-measures.dax`). |

## Calculated columns

Table tools > New column, paste each from the top of [03-measures.dax](03-measures.dax), then set the type and format in Column tools.

| Column | Data type | Format | Why it costs |
|---|---|---|---|
| `Line Amount` | Decimal number | `\$#,0.00` | Stores a decimal for every row; a measure can compute it when asked. |
| `Line Cost` | Decimal number | `\$#,0.00` | Same. |
| `Line Margin` | Decimal number | `\$#,0.00` | Same, built on the two above. |
| `Year` | Whole number | `0` (no thousands separator) | Stands in for a date table. |
| `Month` | Text | none | Stands in for a date table. Sort by `Month Number`. |
| `Month Number` | Whole number | `0` | Sort key for `Month`. |

## Column settings

| Setting | Columns |
|---|---|
| Sort by column | `Sales[Month]` sorted by `Sales[Month Number]` (so Jan comes first, not Apr) |
| Summarization: Don't summarize | `Sales[Year]`, `Sales[Month Number]` |
| Hidden columns | None. Slow reports usually leave every column visible. |
| Display folders | None. The ten measures sit loose on the Sales table. |
| Loaded columns' formats | Leave Power BI's defaults. |

## Check

- Model view shows one table, Sales, with no lines.
- File > Options > Current File > Data Load: **Auto date/time** is ticked.
