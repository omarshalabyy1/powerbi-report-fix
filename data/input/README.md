# Input files

What the client hands over, in this folder. CSV files here are ignored by git; the measurement exports are small and are committed with the project.

`python config.py` (and the notebook's first cell) checks the flat export before anything is computed and stops with one line naming the file and the problem. The notebook stops with one line if a measurement file is missing once the first one is in.

## 1. The flat export of the fact table (`inputs.flat`)

One CSV (UTF-8, comma-separated, a header row), one row per order line: the export the client's slow report reads, or the same rows pulled from its source. Each header the code reads is set under `columns` in `config/client.yaml` (standard name: the client's header). Extra columns are ignored; only the mapped ones are read. Dates are read as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`; decimals use a dot.

| Standard column | Type | Demo header | Demo example |
|---|---|---|---|
| order_key | whole number, the same on every line of one order | Order Key | 10000 |
| order_date | date | Order Date | 2015-01-01 |
| customer_key | whole number | Customer Key | 947009 |
| country | text, the customer's country | Country | United Kingdom |
| product_key | whole number | Product Key | 48 |
| product_name | text, one name per product key | Product Name | WWI 1GB Pulse Smart pen E50 Silver |
| category | text | Category | Audio |
| subcategory | text | Subcategory | Recording Pen |
| quantity | whole number | Quantity | 1 |
| net_price | number, the price per unit after discount | Net Price | 98.967 |
| unit_cost | number, the cost per unit | Unit Cost | 57.3375 |

The demo's file is made by `python data/demo/prepare_data.py` (2.1 million lines, about 800 MB, 35 columns); it is not committed.

The three keys are whole numbers in the fixed report's Power Query (`powerbi/01-power-query.md`); text keys work in the notebook, and the three key types change to `type text` there.

## 2. The client's report

Their `.pbix`, or their `.pbip` folder, as it is today. No code reads it: it is the report that gets measured, then rebuilt. Keep it out of the public template; in the client's private repo it can sit next to this folder.

## 3. The measurements (docs/measuring.md)

Taken in Power BI Desktop, one Performance Analyzer export per page in `measurements.pages` and one VertiPaq Analyzer export per report:

| File | What it is | Read by |
|---|---|---|
| `before-<page>.json` | Performance Analyzer export of one page of the client's report, before any change | `measure.py`: page and visual seconds |
| `before.vpax` | DAX Studio > Advanced > Export Metrics on the client's report | `measure.py`: model size, columns, calculated columns, hidden date tables |
| `after-<page>.json`, `after.vpax` | The same, on the fixed report | `measure.py` |

The notebook shows nothing until the first of these files is here; after that, every one must be.
