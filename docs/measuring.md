# How the timings and sizes are measured

Both reports are measured the same way, on the same laptop, with the slicers in the default state (Year 2023, everything else unselected). Each page is timed once, from a cold cache, so neither report gets a head start from results Power BI kept in memory. Save every file in `data/input/`; the notebook reads them there (`measure.py`) and works out the before and after numbers.

Tools: Power BI Desktop (Performance Analyzer is built in) and [DAX Studio](https://daxstudio.org) (free).

## For each report: first `before/sales-before.pbip`, then `sales-after.pbip`

For a client, "before" is the client's own report as it is today: measure it this way before changing anything.

1. Close Power BI Desktop and open the report fresh. Wait until every visual has loaded.
2. Open DAX Studio > Power BI / SSDT Model > pick the open report > Connect.
3. **Page timings**, for the Overview page, then the Products page:
   1. Go to the page in Power BI.
   2. DAX Studio: Home > **Clear Cache**.
   3. Power BI: Optimize > **Performance analyzer** > Start recording > **Refresh visuals**. Wait until every visual shows a duration.
   4. Stop > **Export**, and save it in `data/input/` with the name below.
4. **Model size:** DAX Studio > Advanced > **Export Metrics**, saved in `data/input/` with the name below.

Page names come from `measurements.pages` in `config/client.yaml` (the demo: `overview`, `products`).

| File (in `data/input/`) | What it holds |
|---|---|
| `before-overview.json` | Performance Analyzer, slow report, Overview page |
| `before-products.json` | Performance Analyzer, slow report, Products page |
| `before.vpax` | VertiPaq Analyzer metrics, slow report |
| `after-overview.json` | Performance Analyzer, fixed report, Overview page |
| `after-products.json` | Performance Analyzer, fixed report, Products page |
| `after.vpax` | VertiPaq Analyzer metrics, fixed report |

## What the notebook takes from them

- **Page time:** from the first visual starting to the last visual finishing, in the page's Performance Analyzer export.
- **Visual time:** each visual's own duration in the same export.
- **Model size:** the total size of the model in memory, from the `.vpax` file.

Each page is timed in a single run, so small differences (a few tenths of a second) are within normal noise. Run the page again if a number looks odd.
