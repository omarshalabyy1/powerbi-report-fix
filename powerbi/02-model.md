# 2. The model: a star schema with a date table

One fact table in the middle, three dimensions around it, every relationship one-to-many with a single filter direction (from the dimension to the fact).

## Tables

| Table | Type | Grain (one row per) | Key | Rows |
|---|---|---|---|---|
| Sales | Fact | order line | none kept (Order Key + Line Number in the source; nothing needs it) | 2,098,633 |
| Customer | Dimension | customer who bought | Customer Key | 88,063 |
| Product | Dimension | product | Product Key | 2,517 |
| Date | Dimension | calendar day, 1 Jan of the first sales year to 31 Dec of the last | Date | 3,653 |

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

Then:

1. Select `Date[Date]`, Column tools > Data type: **Date**.
2. Select the Date table, Table tools > **Mark as date table** > Date column: `Date`. Power BI checks the dates are unique and have no gaps.
3. Select `Date[Month]`, Column tools > **Sort by column** > `Month Number`, so January comes first, not April.
4. Select `Date[Year]`, Column tools > Summarization: **Don't summarize**.

## Relationships

Model view: drag each fact column onto its dimension column, then double-click the line to check the settings.

| From (many) | To (one) | Cardinality | Cross-filter direction | Active |
|---|---|---|---|---|
| `Sales[Order Date]` | `Date[Date]` | Many to one (*:1) | Single | Yes |
| `Sales[Customer Key]` | `Customer[Customer Key]` | Many to one (*:1) | Single | Yes |
| `Sales[Product Key]` | `Product[Product Key]` | Many to one (*:1) | Single | Yes |

Delete any relationship Power BI created on its own that is not in this table.

## Hidden columns

Report users work with the dimensions and the measures only. In Model view, right-click > Hide in report view:

- Sales: every column (`Order Key`, `Order Date`, `Customer Key`, `Product Key`, `Quantity`, `Net Price`, `Unit Cost`). The measures stay visible.
- Customer: `Customer Key`.
- Product: `Product Key`.
- Date: `Month Number`.

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
