# 1. Power Query (slow report): one query, every column

**Before you load anything:** File > Options and settings > Options > Current File > Data Load: check **Auto date/time** is ticked (it is by default for a new file). Leaving it on is part of the slow build.

Home > Get data > Blank query > Home > Advanced Editor, select everything, paste the code, Done. Rename the query **Sales** (right-click > Rename). Change the path if you cloned the repo somewhere else.

| Query | Load to report? | What it is |
|---|---|---|
| `Sales` | Yes | The whole export: all 35 columns, one row per order line |

Applied steps: Source (read the CSV as UTF-8), Headers (first row becomes headers), Types (every column typed with the en-US culture, so the dots in the prices read as decimals on any Windows locale). No column is removed: that is the slow part.

```m
let
    Source = Csv.Document(
        File.Contents("C:\Users\you\GitHub\powerbi-report-fix\data\input\sales_flat.csv"),
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

Then Home > Close & Apply.

**Check after loading** (Table view, row count at the bottom left): Sales <!--n:sales_rows-->2,098,633<!--/n--> rows.
