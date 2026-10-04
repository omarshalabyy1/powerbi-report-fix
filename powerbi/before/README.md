# The slow report (the "before" state)

This report is slow on purpose. It is built the way slow sales reports usually get built: one wide table straight from the export, Power BI's automatic date tables, calculated columns for every small sum, and measures that work row by row. It shows exactly the same numbers as the fixed report. Only the speed and the size differ, and that difference is what this project measures.

## What makes it slow and big

| Choice | Why it costs |
|---|---|
| One flat table, all 35 columns | Every customer address, birthday and product name is stored again on each of the 2.1 million order lines. Power BI stores each column separately, and long text columns with many different values take the most space. |
| Auto date/time left on | Power BI quietly builds a hidden date table for every date column (Order Date, Delivery Date, Birthday), each covering every day between the earliest and latest date. |
| Six calculated columns | `Line Amount`, `Line Cost` and `Line Margin` store a decimal for every row, values a measure could compute at query time. |
| `AVERAGEX ( VALUES ( Sales[Order Key] ), [Sales Amount] )` | Recalculates Sales Amount once per order (about 160,000 orders in 2023) instead of one division. |
| `COUNTROWS ( SUMMARIZE ( ... ) )` | Builds a table of keys just to count it, where `DISTINCTCOUNT` does it directly. |
| `IF ( [Sales Amount] = 0, ..., [Margin] / [Sales Amount] )` | Evaluates the same measure several times instead of once into a variable. |

## Build it

1. Open Power BI Desktop, new report. File > Options and settings > Options > Current File > Data Load: check **Auto date/time** is ticked (it is by default).
2. Home > Get data > Blank query > Advanced Editor, paste the query below, Done. Rename the query **Sales**, then Close & Apply. Change the path if you cloned the repo somewhere else.
3. Add the six calculated columns, then the ten measures, from [measures.dax](measures.dax), each with the format string in its comment. Select `Sales[Month]` > Column tools > Sort by column > `Month Number`. Select `Sales[Year]` > Summarization: Don't summarize.
4. View > Themes > Browse for themes > [../05-theme.json](../05-theme.json).
5. Build the two pages from [../04-pages.md](../04-pages.md), using the Sales columns below in place of the fixed report's dimension columns. Measures have the same names.
6. Check every number against [../06-checks.md](../06-checks.md).
7. File > Save as > Save as type **Power BI project files (*.pbip)** > `powerbi/before/sales-before.pbip`. If that type is missing: File > Options > Preview features > tick "Power BI Project (.pbip) save option" and restart.

| Fixed report field | Slow report field |
|---|---|
| `Date[Year]` | `Sales[Year]` |
| `Date[Month]` | `Sales[Month]` |
| `Customer[Country]` | `Sales[Country]` |
| `Product[Category]` | `Sales[Category]` |
| `Product[Subcategory]` | `Sales[Subcategory]` |
| `Product[Product Name]` | `Sales[Product Name]` |

## The query: Sales

```m
let
    Source = Csv.Document(
        File.Contents("C:\Users\DELL\GitHub\powerbi-report-fix\data\sales_flat.csv"),
        [Delimiter = ",", Columns = 35, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Types = Table.TransformColumnTypes(
        Headers,
        {
            {"Order Key", Int64.Type}, {"Line Number", Int64.Type},
            {"Order Date", type date}, {"Delivery Date", type date},
            {"Customer Key", Int64.Type}, {"Customer Name", type text}, {"Gender", type text},
            {"Birthday", type date}, {"Age", Int64.Type}, {"Occupation", type text},
            {"Company", type text}, {"Street Address", type text}, {"City", type text},
            {"State", type text}, {"Zip Code", type text}, {"Country", type text},
            {"Continent", type text}, {"Store Key", Int64.Type}, {"Store", type text},
            {"Store Country", type text}, {"Store State", type text}, {"Product Key", Int64.Type},
            {"Product Code", type text}, {"Product Name", type text}, {"Manufacturer", type text},
            {"Brand", type text}, {"Color", type text}, {"Category", type text},
            {"Subcategory", type text}, {"Quantity", Int64.Type}, {"Unit Price", type number},
            {"Net Price", type number}, {"Unit Cost", type number}, {"Currency Code", type text},
            {"Exchange Rate", type number}
        },
        "en-US"
    )
in
    Types
```
