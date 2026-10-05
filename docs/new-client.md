# New client

This repo is a GitHub template for offering 14, "Power BI report fix". A new client gets a **private** repo from it (Use this template > Create a new repository > Private); client data never goes into this public repo. What changes per client is `config/client.yaml` and the files in `data/input/`. There is no secret, so there is no `.env`, and no Docker.

The client's deliverable is **their** report, made fast with the same numbers. So the template is the method and the measuring kit: it measures their report before and after, proves every number still matches, and carries the worked pattern of the fix (the demo's slow report and its rebuild). Rebuilding their own model and measures is custom work, priced by the size of the report.

## Done in the template

What the client gets with no work. Hours are an estimate of building each part from scratch.

| # | Part | Estimate (hours) |
|---|---|---|
| A | Client settings: `config/client.yaml`, `config.py` (`load_config()`, `check_inputs()`, a one-line stop for every bad key, file or column), the Power BI theme written from the config (`theme.py`) | 1.5 |
| B | The measuring kit: the method (`docs/measuring.md`: cold cache, one Performance Analyzer export per page, a VertiPaq Analyzer export per report) and `measure.py` (page and visual seconds, model size, columns, calculated columns, hidden date tables), read by the notebook | 3 |
| C | The check numbers: the notebook maps the client's headers to standard names, computes every card, chart and table with SQL for the check year and a second filtered state, counts the cells the slow pattern could get wrong, and writes `powerbi/06-checks.md`, `output/sales.csv` and `output/numbers.json` | 3 |
| D | The fix pattern: what makes reports slow and why (`powerbi/before/`), the star built in Power Query, the date table, relationships and formats, 10 measures in their slow and fixed versions (`powerbi/01` to `03`) | 4 |
| E | Power BI build pack: 2 pages with 19 visuals, interactions, a 24-step checklist whose check numbers the notebook writes (`powerbi/04`, `07`, `08`) | 3 |
| F | README with its diagrams, and the input guide (`data/input/README.md`) | 2 |
| | **Total** | **16.5** |

## Configure

Per client. Hours are an estimate for a small report (one fact table, 2 or 3 pages) and a large one (8 to 10 pages).

| File | Key or step | Example (the drill below) | Small | Large |
|---|---|---|---|---|
| `config/client.yaml` | `client.name`, `client.currency`, `inputs.flat`, `columns` (11 headers), `report.check_year`, `report.second_check`, `report.title`, `report.colours` | `"EGP "`, `Qty`, `2025`, `Egypt` / `TV` | 0.5 | 0.5 |
| `data/input/` | the flat export of their fact table; `python config.py` until it prints OK | `nile_sales.csv` | 0.5 | 1 |
| `measurements.pages`, `docs/measuring.md` | measure **their** report before any change: one export per page, cold cache, and `before.vpax` | `[summary]` | 0.5 | 2 |
| notebook, `theme.py` | run them; read the checks and the empty-cell count with the client | | 0.5 | 0.5 |
| `data/input/` | measure the fixed report the same way (`after-<page>.json`, `after.vpax`), rerun the notebook | | 0.5 | 1.5 |
| | **Total** | | **2.5** | **5.5** |

## Custom

Rebuilding the client's own model and measures, which the template cannot do for them. Hours are estimates.

| Work | Small | Large |
|---|---|---|
| Read their model and find what makes it slow: the biggest columns in VertiPaq Analyzer, the slowest visuals, server timings in DAX Studio | 1.5 | 4 |
| Rebuild the model: Power Query to a star, a marked date table, relationships, unused columns removed | 3 | 8 |
| Rewrite the slow measures, keeping every name the visuals use | 3 | 12 |
| Re-point the visuals, interactions and any row-level security | 1.5 | 6 |
| Prove the same numbers: their pages against the notebook's checks, adding SQL for measures the template does not have | 1 | 3 |
| The handover note: every change, with the before and after timings | 1 | 2 |
| **Total** | **11** | **35** |

## Share already done (estimate)

Template hours ÷ (template + configure + custom) hours:

| Offering 14, Power BI report fix | Arithmetic | Share already done |
|---|---|---|
| A small report (one fact table, about 15 measures, 2 or 3 pages) | 16.5 ÷ (16.5 + 2.5 + 11) = 16.5 ÷ 30 | **55%** (55.0%) |
| A large report (2 or 3 fact tables, 60+ measures, 8 to 10 pages, row-level security) | 16.5 ÷ (16.5 + 5.5 + 35) = 16.5 ÷ 57 | **29%** (28.9%) |

The bigger the report, the more of the work is rebuilding it by hand, so the share falls.

## Steps

1. Create the private repo from the template and clone it.
2. Put the client's flat export in `data/input/` ([columns and examples](../data/input/README.md)); CSV files there are ignored by git.
3. Edit `config/client.yaml`: the file name, the 11 headers, the check year and a second filtered state, the title and colours.
4. `pip install -r requirements.txt`, then `python config.py`. It stops with one line if a key, the file or a column is wrong; fix and run again.
5. Measure their report as it is ([method](measuring.md)): `before-<page>.json` per page and `before.vpax`, in `data/input/`. Set `measurements.pages` to their page names.
6. Run the notebook (`jupyter nbconvert --to notebook --execute --inplace analysis/analysis.ipynb`) and `python theme.py`. Read `powerbi/06-checks.md` with the client: these are the numbers the fixed report must keep.
7. Rebuild their report following the pattern in `powerbi/` (custom), check every page against `06-checks.md`, measure it (`after-<page>.json`, `after.vpax`) and rerun the notebook: `output/numbers.json` holds the before and after timings and sizes for the handover note.

Do not run `data/demo/` scripts for a client: they download the demo data and write the demo's numbers into this README and the portfolio site's card.

## Second-client drill (2026-10-05)

The acceptance test: a fresh clone of the repo (no `data/input/` CSV, no `output/`), a made-up second client, a run from scratch.

**Client B (drill):** "Nile Electronics", currency `"EGP "`, title "Nile report fix", teal colours (`#0F766E` main, `#B91C1C` danger, page `#F0FDFA`), `check_year: 2025`, second check 2024 / Egypt / TV, one report page (`summary`).

- Its own file name (`nile_sales.csv`) and headers (`OrderNo`, `Date`, `CustID`, `Market`, `SKU`, `Item`, `Dept`, `Sub Dept`, `Qty`, `Price`, `Cost`), and an extra column first (`Channel`).
- 10 lines over 2023 to 2025: an order with two lines, a customer with two orders, two countries, a product sold in July of the previous year only (an empty month in the check year), two products tied on sales.
- Measurement files in the real formats: Performance Analyzer exports with a byte-order mark, and `.vpax` files with `DaxVpaView.json` (two hidden date tables, a template date table, row-number and calculated columns before; a calculated Date table after).

| What | Demo | Client B (drill) |
|---|---|---|
| Rows, orders, customers, products | 2,098,633, 875,901, 88,063, 2,517 | 10, 9, 5, 4 |
| Check year: Sales, YoY, margin | 2023: $318,425,878, -28.4%, 56.0% | 2025: EGP 2,300, 2.7%, 40.4% |
| Orders, average order, customers | 159,695, $1,993.96, 62,337 | 4, EGP 575.00, 3 |
| Second check: Sales, YoY | 2022 / Germany / Computers: $19,645,197, 93.5% | 2024 / Egypt / TV: EGP 1,900, 375.0% |
| Top product, top category | Adventure Works 52" LCD HDTV X590 White $2,317,817; Computers | Smart TV 55 EGP 1,000; TV EGP 1,900, 0.0%, 42.1% |
| Months by Sales and PY | 12 months | Jan 700 / 900, Feb 700 / 120, Mar 900 / 1,000, Jul blank / 220 |
| Product rank ties | none in the top 10 | Phone X and Phone Y both rank 3 |
| Checked cells with no sales in the check year | 0 | 19 (months 9, second-check months 10) |
| Slowest page, model size | not measured yet | 4.2 s to 0.9 s (4.7× faster); 53 MB to 9 MB (down 83%) |
| Columns, calculated columns, hidden date tables | not measured yet | before 14, 2, 2; after 13, 0, 0 |
| Power BI theme | "Power BI report fix", `#2563EB` | "Nile report fix", `#0F766E`, danger `#B91C1C`, page `#F0FDFA` |
| Notebook | 0 errors | 0 errors; checks titled Nile Electronics, amounts in EGP, the checklist set to 2025 |

**By hand:** 2025 lines 500 + 2 × 100 + 500 + 200 + 900 = 2,300; cost 300 + 120 + 300 + 150 + 500 = 1,370, margin 930 ÷ 2,300 = 40.4%; orders 1, 2, 3, 4 = 4, so 575.00 each; customers 1, 2, 3. 2024: 2 × 450 + 120 + 1,000 + 220 = 2,240, so (2,300 − 2,240) ÷ 2,240 = 2.7%. Second check, 2024 Egypt TV: 900 + 1,000 = 1,900, cost 600 + 500, margin 800 ÷ 1,900 = 42.1%, against 2023 Egypt TV 400: +375.0%; orders 5 and 7, so 950.00. Products: Smart TV 55 500 + 500 = 1,000 (rank 1), OLED TV 65 900 (2), Phone X 2 × 100 = 200 and Phone Y 200 (both 3). Before page: first visual starts at 0.000 s, last ends at 4.200 s; after: 0.000 to 0.900 s; 4.2 ÷ 0.9 = 4.7. Model: 50 + 2 + 1 + 0.0005 = 53.0 MB against 8 + 0.4 + 0.6 = 9.0 MB, 1 − 9 ÷ 53 = 83%; columns 12 data + 2 calculated = 14 (the date tables' and row-number columns left out) against 7 + 3 + 3 = 13. Every output number matched.

`data/demo/publish.py` run on the drill copy (with a stand-in archive) wrote the timed headline, "10 sales rows: slowest page from 4.2 s to 0.9 s, model size down 83%", and the timings table into the README; with no portfolio checkout next to the copy, it left the site's card alone.

**Clear failures**, one line each, run on the Client B copy:

```
config/client.yaml is missing report.check_year
config/client.yaml is not valid YAML near line 2 (quote a value with # or :)
missing data/input/nile_sales.csv (inputs.flat in config/client.yaml)
data/input/nile_sales.csv: missing column(s): Qty
report.second_check matches no rows in data/input/nile_sales.csv
report.check_year matches no rows in data/input/nile_sales.csv
data/input/ is missing after-summary.json (docs/measuring.md)
```

The first four come from `python config.py` (and the notebook's first cell); the last three from the notebook. A fresh clone with the demo config and no export stops with `missing data/input/sales_flat.csv (inputs.flat in config/client.yaml)`.

**Nothing hard-coded:** this search over `config.py`, `measure.py`, `theme.py`, the notebook's code cells, `powerbi/03-measures.dax` and the M and DAX code in `powerbi/01-power-query.md` and `powerbi/02-model.md` finds nothing (the same search finds 13 lines in `config/client.yaml`):

```
Contoso|sales_flat|csv-1m|\b2021\b|\b2022\b|\b2023\b|\b2024\b|Germany|Computers|#[0-9A-Fa-f]{6}|[\\][$]#|\bUSD\b|Power BI report fix|C:[\\]Users
```

These keep the demo's values on purpose: the README and the diagrams in `docs/`, `docs/measuring.md`, `powerbi/04-pages.md`, `06-checks.md` and `08-build-checklist.md` (they describe the demo run, and the notebook rewrites their numbers for a client), `powerbi/before/` (see the gaps), and `data/demo/`.

**Nothing broke:** the demo rerun through the template code gives the same numbers as before: `powerbi/06-checks.md` changed only in its heading and two lines of wording, and the README and the site's card kept every number.

## Gaps against the template standard

- **`powerbi/before/` keeps the demo's headers and file path.** It builds the demo's slow report on purpose; a client's slow report is their own file, measured as it is. It is exempt like `data/demo/`, which the standard does not list.
- **The star's table and key names are not in `client.yaml`.** Nothing could read them: Power Query M and DAX cannot read the YAML. The fixed report reads `output/sales.csv` under the standard names, so the pattern works for any client; renaming the tables to a client's own names is part of rebuilding their model (custom).
- **The checks cover the template's 10 measures.** A client's report with other measures needs their SQL added to the notebook (custom, "Prove the same numbers").
- **The parsers were tested against one real Performance Analyzer export** (a public sample from a 2020 Power BI talk: 23 visuals, a 34.5 s page) and against `.vpax` files built from SQLBI's documented format (`DaxVpaView.json`, its `Tables` and `Columns`). Check the first real DAX Studio export against what the notebook reports.
- **The empty-cell count** proves the demo's slow previous-year measure safe; a client's slow logic is their own, so for them it is a warning to read, not a proof.
- **Dates other than `YYYY-MM-DD`, Excel exports, or text keys** need a small change (the read in the notebook, or `type text` for the keys in `powerbi/01-power-query.md`).
