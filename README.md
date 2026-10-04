<p align="center">
  <img width="100%" src="docs/header.svg" alt="Power BI report fix: a slow sales report rebuilt as a star schema with clean DAX, with the same numbers.">
</p>

# Power BI report fix

**<!--n:sales_rows-->2,098,633<!--/n--> sales rows: slowest page from <!--n:slowest_before-->[X]<!--/n--> to <!--n:slowest_after-->[Y]<!--/n--> seconds, model size down <!--n:size_down-->[Z]<!--/n-->%, every number unchanged.**

## The problem

The sales report takes ages to open, so people stop using it and go back to Excel. Nobody trusts a number they can't get quickly, and nobody wants to touch a model they can't read.

Slow reports usually get that way for the same reasons: one wide table pulled straight from an export, Power BI's automatic date tables left on, calculated columns for every small sum, and measures that work row by row. The slow report here is built exactly that way on purpose (`powerbi/before/`), on <!--n:rows_million-->2.1 million<!--/n--> order lines, so the fix can be measured.

## The fix

<p align="center">
  <img width="100%" src="docs/how-it-works.svg" alt="How it works: 01 Measure, 02 Model, 03 DAX, 04 Check, 05 Hand over.">
</p>

<p align="center">
  <img width="100%" src="docs/before-after.svg" alt="Before: one flat table with hidden date tables and row-by-row DAX. After: a star schema with a date table and simple DAX. Same numbers.">
</p>

- **Model.** The <!--n:flat_columns-->35<!--/n-->-column flat table becomes a star: a Sales fact that keeps only keys and numbers (7 columns), and Customer, Product and Date dimensions around it. Each product name is now stored once, not on every order line. Auto date/time is off, and one marked Date table drives all time logic.
- **DAX.** No calculated columns: amounts are computed inside the measures. `Avg Order Value` is one division instead of a loop over <!--n:orders_2023-->159,695<!--/n--> orders in 2023; counts use `DISTINCTCOUNT` instead of building a table to count it; `Sales PY` uses `SAMEPERIODLASTYEAR` on the date table; results that are used twice are kept in variables. All ten measures are in [`powerbi/03-measures.dax`](powerbi/03-measures.dax), next to the slow versions in [`powerbi/before/measures.dax`](powerbi/before/measures.dax).
- **Check.** Every card, chart and table is compared with numbers computed in SQL straight from the source ([`powerbi/06-checks.md`](powerbi/06-checks.md)). Both reports show the same numbers, for example <!--n:sales_2023-->$318,425,878<!--/n--> of sales in 2023, down <!--n:yoy_2023-->28.4%<!--/n--> on 2022, at a <!--n:margin_2023-->56.0%<!--/n--> margin.

## The result

| | Before | After | Change |
|---|---|---|---|
| Slowest page | <!--n:slowest_before-->[X]<!--/n--> s | <!--n:slowest_after-->[Y]<!--/n--> s | <!--n:slowest_change-->[ ]<!--/n--> |
| Overview page | <!--n:overview_before-->[ ]<!--/n--> s | <!--n:overview_after-->[ ]<!--/n--> s | <!--n:overview_change-->[ ]<!--/n--> |
| Products page | <!--n:products_before-->[ ]<!--/n--> s | <!--n:products_after-->[ ]<!--/n--> s | <!--n:products_change-->[ ]<!--/n--> |
| Model in memory | <!--n:size_before-->[A]<!--/n--> MB | <!--n:size_after-->[B]<!--/n--> MB | down <!--n:size_down-->[Z]<!--/n-->% |
| Columns in the model | 41 (35 + 6 calculated) | 17 (Sales 7, Date 4, Product 4, Customer 2) | |
| Hidden date tables | 3 | 0 | |
| Numbers on the pages | | | identical |

Timed in Power BI Desktop with Performance Analyzer from a cold cache, model size from DAX Studio's VertiPaq Analyzer. The method is in [`measurements/README.md`](measurements/README.md), and every number in this table is worked out in [`analysis/analysis.ipynb`](analysis/analysis.ipynb) from the raw exports in `measurements/`.

## Screenshots

Added once the reports are built.

## Run it

```bash
pip install -r requirements.txt
python prepare_data.py
```

`prepare_data.py` downloads the data (<!--n:archive_mb-->42 MB<!--/n-->), unpacks it and writes `data/sales_flat.csv` (<!--n:rows_million-->2.1 million<!--/n--> rows, <!--n:flat_mb-->801 MB<!--/n-->), the one file both reports read. Then:

1. Build the slow report from [`powerbi/before/README.md`](powerbi/before/README.md) and the fixed one from [`powerbi/README.md`](powerbi/README.md), both in Power BI Desktop, checking each against [`powerbi/06-checks.md`](powerbi/06-checks.md).
2. Measure both with [`measurements/README.md`](measurements/README.md).
3. Rerun the notebook to recompute every number: `jupyter nbconvert --to notebook --execute --inplace analysis/analysis.ipynb`.

## Data

Contoso sales data made with SQLBI's [Contoso Data Generator V2](https://github.com/sql-bi/Contoso-Data-Generator-V2) (the ready-made 1M set, MIT licence): generated, not real, with <!--n:sales_rows-->2,098,633<!--/n--> order lines from <!--n:orders-->875,901<!--/n--> orders between <!--n:first_month-->January 2015<!--/n--> and <!--n:last_month-->April 2024<!--/n-->. `prepare_data.py` joins its sales, customer, product and store tables into the one flat export the slow report is built on.
