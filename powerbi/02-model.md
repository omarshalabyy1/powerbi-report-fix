# 2. The model: a star schema with a date table

One fact table in the middle, three dimensions around it, every relationship one-to-many with a single filter direction (from the dimension to the fact).

## Tables

| Table | Type | Grain (one row per) | Key | Rows |
|---|---|---|---|---|
| Sales | Fact | order line | none kept (Order Key + Line Number in the source; nothing needs it) | <!--n:sales_rows-->2,098,633<!--/n--> |
| Customer | Dimension | customer who bought | Customer Key | <!--n:customers_dim-->88,063<!--/n--> |
| Product | Dimension | product | Product Key | <!--n:products_count-->2,517<!--/n--> |
| Date | Dimension | calendar day, 1 Jan of the first sales year to 31 Dec of the last | Date | <!--n:date_rows-->3,653<!--/n--> |

| Choice | Why |
|---|---|
| Fact keeps only keys and numbers (7 columns) | Narrow whole-number and decimal columns compress well; each name is stored once, in its dimension. |
| Dimensions built from the flat file | The client only has the export; the star is rebuilt from it in Power Query. |
| Auto date/time off | No hidden date tables; one Date table serves every visual. |
| No calculated columns | Amounts are computed by the measures when asked, so nothing extra is stored per row. |

## The Date table

Modeling > New table, paste:

```dax
Date =
VAR FirstYear = YEAR ( MIN ( Sales[Order Date] ) )
VAR LastYear = YEAR ( MAX ( Sales[Order Date] ) )
RETURN
    ADDCOLUMNS (
        CALENDAR ( DATE ( FirstYear, 1, 1 ), DATE ( LastYear, 12, 31 ) ),
        "Year", YEAR ( [Date] ),
        "Month Number", MONTH ( [Date] ),
        "Month", FORMAT ( [Date], "mmm" )
    )
```

Why: `SAMEPERIODLASTYEAR` needs every day of every year in one marked table; the years follow the data, so a refresh with new years extends it.

Then:

1. Select `Date[Date]`, Column tools > Data type: **Date**.
2. Select the Date table, Table tools > **Mark as date table** > Date column: `Date`. Power BI checks the dates are unique and have no gaps.
3. Select `Date[Month]`, Column tools > **Sort by column** > `Month Number`, so January comes first, not April.
4. Select `Date[Year]`, Column tools > Summarization: **Don't summarize**.

## Column formats

Column tools > Format, for each column:

| Column | Data type | Format | Why |
|---|---|---|---|
| `Date[Date]` | Date | `yyyy-mm-dd` | Date only, no time, so it matches `Sales[Order Date]` |
| `Date[Year]` | Whole number | `0` | The slicer shows a year without a thousands separator |
| `Date[Month Number]` | Whole number | `0` | Sort key only (hidden) |
| `Date[Month]` | Text | none | Jan to Dec, sorted by Month Number |
| `Sales[Order Date]` | Date | `yyyy-mm-dd` | Hidden; joins to `Date[Date]` |
| `Sales[Order Key]`, `Sales[Customer Key]`, `Sales[Product Key]`, `Customer[Customer Key]`, `Product[Product Key]` | Whole number | `0` | Keys, hidden |
| `Sales[Quantity]` | Whole number | `#,0` | Hidden; used by the measures |
| `Sales[Net Price]`, `Sales[Unit Cost]` | Decimal number | `client.currency` + `#,0.00` | Hidden; used by the measures |

## Relationships

Model view: drag each fact column onto its dimension column, then double-click the line to check the settings.

| From (many) | To (one) | Cardinality | Cross-filter direction | Active |
|---|---|---|---|---|
| `Sales[Order Date]` | `Date[Date]` | Many to one (*:1) | Single | Yes |
| `Sales[Customer Key]` | `Customer[Customer Key]` | Many to one (*:1) | Single | Yes |
| `Sales[Product Key]` | `Product[Product Key]` | Many to one (*:1) | Single | Yes |

Why single direction: filters flow from each dimension to the fact only, so there is one path for every filter and no ambiguity.

Delete any relationship Power BI created on its own that is not in this table.

## Hidden columns

Report users work with the dimensions and the measures only. In Model view, right-click > Hide in report view:

- Sales: every column (`Order Key`, `Order Date`, `Customer Key`, `Product Key`, `Quantity`, `Net Price`, `Unit Cost`). The measures stay visible.
- Customer: `Customer Key`.
- Product: `Product Key`.
- Date: `Month Number`.

Why: nobody can drag a key into a visual and sum it by mistake.

## Measures and display folders

Create the measures from [03-measures.dax](03-measures.dax) on the Sales table. In Model view, select each measure and set **Display folder** in Properties:

| Display folder | Measures |
|---|---|
| Sales | Sales Amount, Total Cost, Margin, Margin % |
| Orders and customers | Orders, Customers, Avg Order Value |
| Time | Sales PY, Sales YoY % |
| Rank | Product Rank |

## Check

- Model view shows a star: Sales in the middle, Date, Customer and Product around it, three lines, each with `1` on the dimension side and `*` on Sales.
- File > Options > Current File > Data Load: **Auto date/time** is unticked.
