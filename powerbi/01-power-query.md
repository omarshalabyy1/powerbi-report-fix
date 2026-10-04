# 1. Power Query: the flat file split into a star

The fixed report reads the same file as the slow one, `data/sales_flat.csv` (run `python prepare_data.py` first). Power Query reads it once into a staging query, then three queries take only the columns they need: the Sales fact and the Customer and Product dimensions. The Date table is added in DAX in [02-model.md](02-model.md).

**Before you load anything:** File > Options and settings > Options > Current File > Data Load > untick **Auto date/time**. Do it first, so Power BI never builds its hidden date tables.

For each query below: Home > Get data > Blank query, then Home > Advanced Editor, select everything, paste the code, Done. Rename the query (right-click > Rename) to the name in the heading.

| Query | Load to report? | What it is |
|---|---|---|
| `DataFolder` | No (parameter) | The folder that holds `sales_flat.csv` |
| `Sales Flat` | **No** (staging) | The 11 columns the report uses, typed |
| `Sales` | Yes | Fact table: one row per order line, keys and numbers only |
| `Customer` | Yes | One row per customer |
| `Product` | Yes | One row per product |

To stop a query loading: right-click it > untick **Enable load**.

## DataFolder

Change the path if you cloned the repo somewhere else. Keep the backslash at the end.

```m
"C:\Users\DELL\GitHub\powerbi-report-fix\data\" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
```

## Sales Flat (staging, Enable load off)

Applied steps: Source (read the CSV as UTF-8), Headers (first row becomes headers), KeepColumns (drop the 24 columns no visual uses: addresses, birthdays, store, currency and so on), Types (set each column's type with the en-US culture, so the dots in the prices read as decimals on any Windows locale).

```m
let
    Source = Csv.Document(
        File.Contents(DataFolder & "sales_flat.csv"),
        [Delimiter = ",", Columns = 35, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    KeepColumns = Table.SelectColumns(
        Headers,
        {"Order Key", "Order Date", "Customer Key", "Country", "Product Key", "Product Name",
         "Category", "Subcategory", "Quantity", "Net Price", "Unit Cost"}
    ),
    Types = Table.TransformColumnTypes(
        KeepColumns,
        {
            {"Order Key", Int64.Type},
            {"Order Date", type date},
            {"Customer Key", Int64.Type},
            {"Country", type text},
            {"Product Key", Int64.Type},
            {"Product Name", type text},
            {"Category", type text},
            {"Subcategory", type text},
            {"Quantity", Int64.Type},
            {"Net Price", type number},
            {"Unit Cost", type number}
        },
        "en-US"
    )
in
    Types
```

## Sales (loaded)

Applied steps: Source (the staging query), Fact (keep the keys and the three numbers). The text columns move to the dimensions, so each product name is stored once instead of on every order line.

```m
let
    Source = #"Sales Flat",
    Fact = Table.SelectColumns(
        Source,
        {"Order Key", "Order Date", "Customer Key", "Product Key", "Quantity", "Net Price", "Unit Cost"}
    )
in
    Fact
```

Column types: Order Key, Customer Key, Product Key and Quantity whole number; Order Date date; Net Price and Unit Cost decimal number.

## Customer (loaded)

Applied steps: Source, Columns (key and country), Distinct (one row per customer key).

```m
let
    Source = #"Sales Flat",
    Columns = Table.SelectColumns(Source, {"Customer Key", "Country"}),
    Distinct = Table.Distinct(Columns, {"Customer Key"})
in
    Distinct
```

Column types: Customer Key whole number; Country text.

## Product (loaded)

Applied steps: Source, Columns (key, name, category, subcategory), Distinct (one row per product key).

```m
let
    Source = #"Sales Flat",
    Columns = Table.SelectColumns(Source, {"Product Key", "Product Name", "Category", "Subcategory"}),
    Distinct = Table.Distinct(Columns, {"Product Key"})
in
    Distinct
```

Column types: Product Key whole number; Product Name, Category and Subcategory text.

Then Home > Close & Apply. The first refresh reads the 800 MB file once per loaded query, so it takes a few minutes.

**Check after loading** (Table view, row count at the bottom left): Sales 2,098,633 rows, Customer 88,063, Product 2,517.
