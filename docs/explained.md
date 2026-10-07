# The project explained, from zero

This page explains the whole project in plain words: what it does, what every word means, where every number comes from, and how to talk about it in an interview. You do not need to know Power BI or DAX to read it.

[← Back to the README](../README.md)

## 1. The project in one minute

A company has a sales report in Power BI. It takes ages to open, so people stop using it and go back to Excel.

The report is slow because of how it was built. All the data sits in one very wide table, copied straight from an export: every order line carries the customer's address, the store and the full product name again. Power BI also builds hidden date tables nobody asked for, stores extra columns for small sums, and runs formulas that work through the data one row or one order at a time.

This project rebuilds that report the standard way, without changing a single number on its pages:

- the wide table becomes a **star schema**: one narrow table of sales in the middle, small lookup tables for customers, products and dates around it;
- the slow formulas become short, simple ones;
- every number on every page is worked out separately in SQL, and both reports must show exactly those numbers;
- both reports are timed the same way in Power BI Desktop, so the speed-up is measured, not guessed.

Think of a phone book. The slow report writes the customer's full address next to every single purchase. The fixed report writes each address once, in the address book, and every purchase only says "customer 947009". Less to store, less to read, and the same answer.

**Where the project stands.** The data, the SQL check numbers and both reports' build instructions are done. The two reports still have to be built in Power BI Desktop and timed. Until then this repo has no timings, and this page says so wherever a timing would go.

## 2. Words you will meet

| Word | What it means here |
|---|---|
| **Power BI, Power BI Desktop** | Microsoft's tool for interactive reports. Desktop is the free Windows program where both reports are built and timed. |
| **Report, page, visual** | A report has pages; a page has visuals (cards, charts, tables). This report has 2 pages, Overview and Products, with 19 visuals in total. |
| **Card** | A visual that shows one number, like "Sales Amount $318,425,878". The Overview page has six. |
| **Slicer** | A visual that filters the page, like a drop-down list. This report has three: Year, Country and Category. |
| **Matrix** | A table visual with rows you can expand, here Category and then Subcategory. |
| **Flat table, flat export** | One wide table with everything joined on. Here `data/input/sales_flat.csv`: one row per order line, 35 columns. |
| **Order line** | One product on one order. An order for a pen and a computer has 2 order lines. "Sales rows" in the README means order lines. |
| **CSV** | Comma-separated values: a plain text file of a table, one row per line. |
| **Power Query** | The part of Power BI that loads and shapes data before the report uses it. Its code language is called **M**; the code blocks in `powerbi/01-power-query.md` are M. |
| **Staging query** | A query that loads and types the file once but is not loaded into the report itself. Here `Sales Flat`; the Sales, Customer and Product tables are built from it. |
| **DAX** | Data Analysis Expressions, the formula language of Power BI. It is used for **measures** and **calculated columns**. |
| **Measure** | A formula worked out when a visual asks for it, for the current filters. "Sales Amount" for 2023 and for Germany are the same measure with different filters. The report has ten. |
| **Calculated column** | A DAX formula that adds a column to a table and stores a value on every row. The slow report has six. The fixed report has none. |
| **Fact table** | The big table of events you add up. Here `Sales`: one row per order line, with quantity, price and cost. |
| **Dimension table** | A small lookup table that describes the facts, used to filter and group: `Customer`, `Product`, `Date`. |
| **Star schema** | One fact table in the middle with dimension tables around it, like a star. The standard shape for Power BI. See [data-model.svg](data-model.svg). |
| **Grain** | What one row of a table stands for. The grain of Sales is "one order line"; of Product, "one product". |
| **Key, PK, FK** | A key is a column that identifies something, like `Product Key` 48. A primary key (PK) is unique in its own table: Product has one row per Product Key. A foreign key (FK) in the fact points to it: many Sales rows carry Product Key 48. |
| **Relationship, 1 to \*** | The line in Power BI that links a fact column to a dimension column. "1 to \*" (one to many): one product row, many sales rows. |
| **Single filter direction** | Filters flow one way only, from the dimension to the fact. Picking "Germany" filters Sales; nothing flows back. One path for every filter, so no surprises. |
| **Auto date/time** | A Power BI setting, on by default. It quietly builds a **hidden date table** for every date column. The slow report leaves it on; the fixed report turns it off. |
| **Date table, mark as date table** | A dimension with one row per day. Marking it tells Power BI "this is the calendar", so time functions like `SAMEPERIODLASTYEAR` work. |
| **VertiPaq** | The engine inside Power BI that holds the data in memory. It stores each column separately and compresses it. A column with few different values (a year, a category) shrinks a lot; a long text column with many different values (a street address) hardly shrinks. |
| **Row by row, iterate** | A formula that walks through rows (or orders) one at a time. Functions ending in X, like `SUMX` and `AVERAGEX`, do this. |
| **Context transition** | What happens when a measure is called inside a row-by-row loop: Power BI turns the current row into a filter and works the whole measure out again. Done once per order, that is 159,695 times for 2023. |
| **Variable (`VAR`)** | A named result inside a measure. Worked out once, then reused, instead of computing the same thing twice. |
| **`DIVIDE`, `DISTINCTCOUNT`, `SAMEPERIODLASTYEAR`, `RANKX`** | DAX functions: a division that returns blank instead of an error when dividing by zero; a count of different values; the same dates one year earlier; a rank. |
| **Sales Amount, Margin, Margin %** | Sales Amount = Quantity × Net Price, summed. Margin = Sales Amount minus cost (Quantity × Unit Cost). Margin % = Margin ÷ Sales Amount. |
| **Net Price, Unit Cost** | The price per unit after discount, and what one unit cost. Both are in the export. |
| **Avg Order Value** | Sales Amount ÷ number of orders. |
| **Sales PY, Sales YoY %** | Previous year (PY): sales for the same months one year earlier. Year over year (YoY) %: how much sales changed against that, in percent. |
| **Product Rank** | A product's place by Sales Amount, 1 = best seller. |
| **Check year, second check** | The two slicer states every number is checked in: Year 2023 with nothing else picked, and Year 2022 + Germany + Computers. Both are set in `config/client.yaml`. |
| **Performance Analyzer** | A pane in Power BI Desktop that times each visual on a page and exports the result as a JSON file (JavaScript Object Notation, a text format for data). |
| **DAX Studio** | A free tool that connects to an open Power BI report. Here it clears the cache before each timing and exports the model's size. |
| **Cache, cold cache** | Power BI keeps recent results in memory, so a second look is faster. A cold cache means that memory was cleared first, so both reports start equal. |
| **`.vpax` file** | The VertiPaq Analyzer export from DAX Studio: the size of every table and column in memory. |
| **`.pbip`, `.pbix`** | A Power BI report saved as a project folder of text files (`.pbip`), or as one file (`.pbix`). The two reports here are saved as `.pbip`. |
| **SQL** | Structured Query Language, the language for asking questions of tables. The notebook uses it to work out every check number. |
| **DuckDB** | A small database engine that runs inside Python with no server. The notebook and `prepare_data.py` use it to run SQL straight on the CSV files. |
| **Python, pandas** | Python is a programming language. pandas is its library for tables; the notebook uses it to show results. |
| **Notebook** | `analysis/analysis.ipynb`, a file that mixes code, its output and notes. It is the source of every number. |
| **`config/client.yaml`** | The settings a client changes: their column names, the check year, the page names, the colours. YAML is a simple text format for settings. |
| **Theme** | A Power BI file that sets colours and fonts: `powerbi/05-theme.json`, written by `theme.py`. |
| **MB** | Megabytes. Here 1 MB = 1,000,000 bytes. |

## 3. How it works, file by file

Run in this order (the commands are in the README's "Run it" section):

| Step | File | What it does |
|---|---|---|
| 0 | `config/client.yaml`, `config.py` | Hold every setting. `config.py` reads them so no file hard-codes a value. |
| 1 | `data/demo/prepare_data.py` | Demo only. Downloads the data archive, unpacks it, and joins 4 of its tables (sales, customer, store, product) into one flat file, `data/input/sales_flat.csv`. It stops if the joined file has a different row count from the sales table, so no order line is lost. A client hands over their own export instead. |
| 2 | `python config.py` | Checks the settings and that the flat file exists and has the 11 columns mapped under `columns`. Prints `config and input file OK`. |
| 3 | `analysis/analysis.ipynb` | Reads the 11 mapped columns into DuckDB. Works out, in SQL, every number each page must show. Writes `output/sales.csv` (the 11 columns the fixed report reads), `powerbi/06-checks.md` (the numbers to check) and `output/numbers.json` (every number, for the README). |
| 4 | `theme.py` | Writes the Power BI theme from the colours in `client.yaml`. |
| 5 | `data/demo/publish.py` | Demo only. Copies the numbers from `output/numbers.json` into the README, the diagrams and the portfolio card. |
| 6 | `powerbi/08-build-checklist.md` | Click-by-click build of both reports: first the slow one (`powerbi/before/`), then the fixed one (`powerbi/`), checking the numbers from `06-checks.md` at each step. |
| 7 | `docs/measuring.md`, `measure.py` | How each report is timed, and the code that reads the timing files. After timing, rerun the notebook and `publish.py`, and the before and after numbers land in the README. Not done yet. |

The two reports read different files on purpose. The slow report reads `sales_flat.csv` as it is, all 35 columns, like a client's real slow report would. The fixed report reads `output/sales.csv`, only the 11 columns any visual needs.

### One order, traced through both reports

A real order from the flat file: order `10000`, placed on 1 Jan 2015 by customer `947009` in the United Kingdom. It has 2 order lines:

| Line | Product Key | Product Name | Category | Quantity | Net Price | Unit Cost |
|---|---|---|---|---|---|---|
| 0 | 48 | WWI 1GB Pulse Smart pen E50 Silver | Audio | 1 | 98.967 | 57.3375 |
| 1 | 460 | WWI Desktop PC1.80 E1802 White | Computers | 1 | 659.78 | 382.25 |

1. **In the flat file** each of the 2 lines has all 35 columns. The customer's name, birthday, job, company, street, city, state, zip code, country and continent, the store's name and location, and the product's code, maker, brand and colour are written on both lines. Across the whole file, every customer and product detail is repeated on every one of the 2,098,633 lines.
2. **In the slow report** the six calculated columns add six more values to each line. Line 0 gets `Line Amount` 1 × 98.967 = 98.967, `Line Cost` 57.3375, `Line Margin` 41.6295, `Year` 2015, `Month` Jan, `Month Number` 1. These are stored, on every line, in memory.
3. **In the fixed report** each line keeps 7 columns in Sales: `Order Key` 10000, `Order Date` 2015-01-01, `Customer Key` 947009, `Product Key` 48 (or 460), `Quantity` 1, `Net Price`, `Unit Cost`. "United Kingdom" is stored once, on customer 947009's row in Customer. The pen's name, Audio and Recording Pen are stored once, on product 48's row in Product. 1 Jan 2015 is one row in Date, with Year 2015, Month Number 1, Month Jan.
4. **The measures** give the same answer in both reports, for this order alone:
   - Sales Amount = 1 × 98.967 + 1 × 659.78 = 758.747
   - Total Cost = 57.3375 + 382.25 = 439.5875
   - Margin = 758.747 − 439.5875 = 319.1595, so Margin % = 319.1595 ÷ 758.747 = 42.1%
   - Orders = 1, so Avg Order Value = 758.747 ÷ 1 = 758.747

   The slow report gets Sales Amount by adding up the stored `Line Amount` column. The fixed report multiplies Quantity by Net Price at the moment a visual asks. Same number, nothing extra stored.

These per-order numbers were worked out for this page from the flat file; the notebook does not print them. The notebook prints the totals they add up to (section 4).

### The same measure, slow and fixed

Avg Order Value for 2023, on the Overview card:

- **Slow:** `AVERAGEX ( VALUES ( Sales[Order Key] ), [Sales Amount] )`. Make a list of the 159,695 orders of 2023, work out Sales Amount for each one separately, then average the 159,695 results.
- **Fixed:** `DIVIDE ( [Sales Amount], [Orders] )`. Total sales ÷ number of orders: $318,425,877.52 ÷ 159,695 = $1,993.96. One division.

Both give $1,993.96, because the average of every order's sales is always total sales ÷ number of orders. The fixed one gets there without 159,695 separate sums.

## 4. Every number, explained

The notebook ([`analysis/analysis.ipynb`](../analysis/analysis.ipynb)) prints them. The cell numbers below count from 0, the first cell. Money is in dollars ($): the measure notes in `powerbi/03-measures.dax` say US dollars.

### The headline and the fix

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **2,098,633 sales rows** | Every order line in the export. Both reports hold all of them. | Count of rows in the flat file. `prepare_data.py` also checks it equals the rows of the source sales table. | notebook cell 1 (`sales_rows`) |
| **2.1 million** | The same 2,098,633, rounded to one decimal. | 2,098,633 ÷ 1,000,000 = 2.1. | notebook cell 14 |
| **35-column flat table** | The slow report's one table: every column of the export. | Count of columns in the flat file's header. | notebook cell 1 (`flat_columns`); the list is in `prepare_data.py` |
| **7 columns** in the Sales fact | What the fixed fact keeps: Order Key, Order Date, Customer Key, Product Key, and 3 numbers (Quantity, Net Price, Unit Cost). | Counted from the `Sales` query. | `powerbi/01-power-query.md` |
| **159,695 orders in 2023** | The orders the slow Avg Order Value loops over on the default page. | Count of different order keys with an order date in 2023. | notebook cell 3 (`Orders`) |
| **ten measures** | Sales Amount, Total Cost, Margin, Margin %, Orders, Customers, Avg Order Value, Sales PY, Sales YoY %, Product Rank. | Counted in the file. | `powerbi/03-measures.dax` |
| **$318,425,878 of sales in 2023** | The Sales Amount card with Year 2023 picked. | Sum of Quantity × Net Price for order lines dated 2023, rounded to the dollar. The exact sum is $318,425,877.52. | notebook cell 3 |
| **down 28.4% on 2022** | The Sales YoY % card: 2023 against 2022. | (318,425,878 − 444,516,719) ÷ 444,516,719 = −28.4%. $444,516,719 is 2022's Sales Amount, the Sales PY. | notebook cell 3 (`Sales YoY %`, `Sales PY`) |
| **56.0% margin** | The Margin % card for 2023. | (Sales − cost) ÷ Sales, with cost = Quantity × Unit Cost. Exactly 55.96%, shown to one decimal. | notebook cell 3 |

### The results table

These shape numbers are counted from the build files of each report. Once the `.vpax` exports are in, `measure.py` reads the same counts from the real models (notebook cell 12). That has not happened yet.

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **1 table → 4** | Before: one flat table. After: Sales, Customer, Product and Date. | Counted from the queries and the Date table. | `powerbi/before/02-model.md`, `powerbi/02-model.md` |
| **41 columns** | Before: the 35 loaded columns plus the 6 calculated columns. | 35 + 6 = 41. | `powerbi/before/01-power-query.md`, `powerbi/before/03-measures.dax` |
| **17 columns** | After: Sales 7, Date 4 (Date, Year, Month Number, Month), Product 4 (key, name, category, subcategory), Customer 2 (key, country). | 7 + 4 + 4 + 2 = 17. | `powerbi/01-power-query.md`, `powerbi/02-model.md` |
| **6 → 0 calculated columns** | Line Amount, Line Cost, Line Margin, Year, Month, Month Number. The fixed report computes amounts inside the measures and takes Year and Month from the Date table. | Counted in the files. | `powerbi/before/03-measures.dax` |
| **3 → 0 hidden date tables** | Auto date/time builds one for each date column in the slow table: Order Date, Delivery Date and Birthday. The fixed report turns it off. | 3 date-typed columns in the slow query. | `powerbi/before/01-power-query.md` |
| **Numbers on the pages: identical** | Both reports must show the numbers in `06-checks.md`. | Written by the notebook from SQL. Each build step in `08-build-checklist.md` checks them. | `powerbi/06-checks.md` |

### The timings

**There are no timings in this repo yet.** The README says page load times and model size are "measured next". Notebook cell 12 prints `No measurements in data/input/ yet`. No seconds, no "times faster" and no model size in MB appear anywhere until the reports are built and timed. Nothing is hand-timed or estimated.

How they will be measured ([measuring.md](measuring.md)):

1. Same laptop, same slicers (Year 2023, nothing else), for both reports.
2. Close Power BI Desktop and open the report fresh, so nothing is left in memory from earlier.
3. For each page (Overview, then Products): DAX Studio > **Clear Cache**, then Performance Analyzer > **Refresh visuals**, then export the timings as JSON. That gives `before-overview.json`, `before-products.json`, `after-overview.json`, `after-products.json`.
4. DAX Studio > **Export Metrics** for each report: `before.vpax`, `after.vpax`.

How the numbers will be worked out (`measure.py`, then notebook cells 12 and 14):

| Number to come | How |
|---|---|
| **Page time, in seconds** | From the moment the first visual starts to the moment the last visual finishes, in that page's Performance Analyzer export. |
| **Visual time** | Each visual's own start to finish, in the same export. |
| **Times faster** | Before page time ÷ after page time. |
| **Model size, in MB** | The sizes of all tables in the `.vpax` file added up, ÷ 1,000,000. |
| **Model size down, %** | 100 × (1 − after size ÷ before size). |

Each page is timed once, so a difference of a few tenths of a second is normal noise.

### Why the fixed report should be faster

This is the reasoning the build files give. The timings above will show how much it matters on this data.

- **Less to hold in memory.** Power BI stores each column on its own and compresses it. The fixed report never loads the 24 columns no visual uses: addresses, birthdays, stores, currency. The long text it does need, like product names, is stored once per product (2,517 rows), not on 2,098,633 lines.
- **No stored sums.** The slow report's Line Amount, Line Cost and Line Margin hold a decimal on every line. Decimals with many different values compress badly. The fixed report works them out only when a visual asks.
- **No hidden tables.** With Auto date/time on, Power BI builds a date table for Birthday and Delivery Date too, though no visual uses them.
- **Less work per number.** The slow Avg Order Value works out Sales Amount once per order (159,695 times in 2023); the fixed one divides once. The slow Orders and Customers build a table of keys just to count it; `DISTINCTCOUNT` counts directly. The slow Margin % and Sales YoY % call the same measure up to three times; the fixed Sales YoY % works it out once into a variable.
- **Filters on small tables.** A slicer on Country filters an 88,063-row Customer table, and the relationship carries that filter to Sales. In the slow report the same slicer filters a text column repeated on 2,098,633 lines.

### The Data section

| Number | What it means | Where |
|---|---|---|
| **2,098,633 order lines** | As above. | notebook cell 1 |
| **875,901 orders** | Count of different order keys. An order has 2.4 lines on average (2,098,633 ÷ 875,901, worked out for this page). | notebook cell 1 (`orders`) |
| **January 2015 to April 2024** | The first and last order dates: 1 Jan 2015 and 20 Apr 2024. | notebook cell 1 (`first_order`, `last_order`) |
| **42 MB** | The size of the downloaded archive (41,740,907 bytes). | `data/demo/publish.py`, from the file's size |
| **801 MB** | The size of `sales_flat.csv` (800,946,669 bytes). | notebook cell 14 (`flat_mb`) |
| **"1M" set** | The name of the ready-made file set the archive comes from (`csv-1m.7z`). This repo does not use or measure what the "1M" counts; the flat file has 2.1 million lines. | README, Data |

### The check numbers in `powerbi/06-checks.md`

The full list is in [06-checks.md](../powerbi/06-checks.md). The ones you meet in the build checklist:

| Number | What it means | Where |
|---|---|---|
| **$2,127,928,962** | Sales Amount for all years, nothing filtered. The first check after creating the measures. | notebook cell 1 (`sales_all_years`) |
| **$1,993.96** | Avg Order Value, 2023: $318,425,877.52 ÷ 159,695. | notebook cell 3 |
| **62,337** | Different customers who bought in 2023. | notebook cell 3 |
| **$444,516,719** | Sales PY: Sales Amount in 2022. | notebook cell 3 |
| **$19,645,197 · 93.5% · 56.0% · 9,854 · $1,993.63 · 5,197** | The six cards with Year 2022, Germany and Computers picked. 93.5% = (19,645,197 − 10,153,937) ÷ 10,153,937, where $10,153,937 is the same filter in 2021. | notebook cell 4 |
| **12 monthly pairs** | Sales Amount and Sales PY per month, for the chart. | notebook cell 5 |
| **Computers $113,112,204 · −36.1% · 56.2%** | The biggest category in 2023. | notebook cells 6 and 8 |
| **2,517 products** | Rows in the Products table: every product sold in 2023. | notebook cell 7 |
| **Adventure Works 52" LCD HDTV X590 White, $2,317,817** | The best-selling product in 2023, Product Rank 1. | notebook cell 7 |
| **88,063 · 2,517 · 3,653** | Rows in Customer, Product and Date in the fixed report. | notebook cells 1 and 14 |
| **0** checked cells with no sales | See the last point below. | notebook cell 9 |

### The diagrams

| Number | Where you see it | What it means |
|---|---|---|
| **01 to 05** | how-it-works.svg | The five steps: measure, model, DAX, check, hand over. |
| **1 to 4** | data-flow.svg | The four stages: flatten, compute, write, Power BI. |
| **4 CSV files** | data-flow.svg | The 4 source tables `prepare_data.py` joins: sales, customer, store, product. |
| **2,098,633 rows, 35 columns, 801 MB** | data-flow.svg, data-model.svg, header.svg | The flat file, as above. |
| **11 mapped columns** | data-flow.svg | The columns listed under `columns` in `config/client.yaml`. The notebook reads only these. |
| **2,098,633 rows, 11 columns** | data-flow.svg | `output/sales.csv`: the same lines, the 11 columns only. |
| **6, 3** | data-flow.svg, before-after.svg | Calculated columns and hidden date tables in the slow report. |
| **88,063 rows** | data-flow.svg, data-model.svg | Customer: one row per customer who bought. |
| **2,517 rows** | data-flow.svg, data-model.svg | Product: one row per product. |
| **3,653 days** | data-flow.svg, data-model.svg | Date: every day from 1 Jan 2015 to 31 Dec 2024 (10 years, 3 of them leap years: 3,650 + 3). |
| **41 → 17 columns** | data-model.svg, before-after.svg | As in the results table. |
| **35 + 6 calculated** | data-model.svg, before-after.svg | The 41 before columns. |
| **7 columns** | before-after.svg | The Sales fact after the fix. |
| **2.1 million** | before-after.svg | Order lines, rounded. |
| **1 and \*** | data-model.svg, before-after.svg | One dimension row to many Sales rows. |

### Things that can look wrong but are not

- **The fixed Sales Amount also uses `SUMX`, a row-by-row function.** It multiplies two columns of the same table on each row, which Power BI handles in one fast pass. The slow pattern is a loop that calls a whole measure again for every order.
- **88,063 customers, but the source customer table has 104,990.** The Customer table is built from the sales export, so it only holds customers who bought something. (104,990 is the row count of the source file, counted for this page.)
- **The Date table runs to 31 Dec 2024, but the last order is 20 Apr 2024.** A date table must cover whole years with no gaps, so that previous-year logic works.
- **Margin % is 56.0% in both checks.** A coincidence at one decimal: exactly 55.96% for 2023 and 55.98% for Germany Computers 2022 (worked out for this page).
- **2,517 products in the table and 2,517 products in total.** Every product was sold in 2023, so the Products page lists all of them.
- **The export has a currency code and an exchange rate on each line** (the first line says GBP and 0.64155). No number in this project uses them.
- **The slow Sales PY only works if each cell has sales in the selected year.** It takes the year from the rows it can see. Notebook cell 9 counts the checked cells with no sales (months, subcategories, products sold only the year before): 0, so both reports match here. For a client this count is checked again.
- **A value ending in exactly .5 can round one unit differently** in Power BI and in Python. `06-checks.md` notes it. Anything else is a real mistake.

## 5. What the results mean for the business

- **A report people open again.** The point of the fix is speed, so people stop exporting to Excel. How much faster is still to be measured; until then, the README shows the shape of the change and no speed claim.
- **Nobody has to re-learn the numbers.** Every card, chart and table must show what it showed before, checked against SQL. If the numbers moved, people would stop trusting the faster report too.
- **A model the next person can read.** Four named tables, ten measures in display folders, no hidden tables and no stored helper columns. Changing a measure means changing one formula.
- **The same method works on a client's report.** Their export goes in `data/input/`, their column names go in `client.yaml`, and their own report is timed before anything changes.

What the demo numbers say about sales (the data is generated, see Data in the README, so this is practice, not a real business):

- **2023 sales fell 28.4%** against 2022: $318,425,878 against $444,516,719 (cell 3). Every month of 2023 is below the same month of 2022 (cell 5), and every category is down, from −10.4% for Audio to −36.1% for Computers (cell 8).
- **Margin held at 56.0%** of sales in 2023 (cell 3), even as sales fell.
- **Computers is the biggest category**, $113,112,204 in 2023 (cell 6), 35.5% of sales (worked out for this page).
- **The United States is about half of 2023 sales**: $156,132,838, 49.0% (cell 6; the share is worked out for this page).
- **Germany Computers went the other way in 2022**: up 93.5% on 2021 (cell 4).

## 6. Interview questions you can expect

**Explain the project in 30 seconds.**
A sales report on 2.1 million order lines was too slow, so people went back to Excel. It was built the usual slow way: one 35-column table, hidden date tables, six calculated columns and row-by-row DAX. I rebuilt it as a star schema with a marked date table and simple measures: 41 columns down to 17, no calculated columns, no hidden date tables. Every number on both reports is checked against SQL, and both are timed the same way in Power BI Desktop, from a cold cache.

**Why is a star schema faster than one flat table?**
Power BI stores each column on its own and compresses it. In a flat table every product name and address is repeated on every line, and columns nobody uses are loaded anyway. In a star, the fact keeps only keys and numbers, which compress well, and each name is stored once in a small dimension. A slicer filters a small table and the relationship carries the filter to the fact.

**Why turn off Auto date/time?**
It builds a hidden date table for every date column, here 3, including Birthday and Delivery Date that no visual uses. One marked Date table serves every visual and lets `SAMEPERIODLASTYEAR` work.

**Why no calculated columns?**
A calculated column stores a value on every row, here 2.1 million decimals per column. A measure works the same value out only when a visual needs it, for the rows in the filter. Line Amount becomes `SUMX ( Sales, Sales[Quantity] * Sales[Net Price] )` inside Sales Amount.

**`AVERAGEX ( VALUES ( Sales[Order Key] ), [Sales Amount] )` and `DIVIDE ( [Sales Amount], [Orders] )` give the same number. Why is one slower?**
The first works out Sales Amount once per order, 159,695 times for 2023, through context transition. The second does one division. The average of each order's sales is always total sales ÷ number of orders, so the answer is the same: $1,993.96.

**Why `DISTINCTCOUNT` and not `COUNTROWS ( SUMMARIZE ( ... ) )`?**
`SUMMARIZE` builds a whole table of keys just to count its rows. `DISTINCTCOUNT` counts the different values directly. Same answer: 159,695 orders, 62,337 customers in 2023.

**How do you prove the numbers did not change?**
The notebook works out every number each page must show in plain SQL, straight from the export, and writes them to `06-checks.md`. Both reports must show those numbers, in two slicer states: Year 2023 alone, and Year 2022 + Germany + Computers. A filtered check matters because a bug in filter logic can hide at the grand total.

**How do you measure speed fairly?**
Same laptop, same slicers, report opened fresh, cache cleared in DAX Studio before each page, Performance Analyzer timing every visual. Page time runs from the first visual starting to the last one finishing. Model size comes from DAX Studio's `.vpax` export. Each page is timed once, so I treat a few tenths of a second as noise.

**Why build the star in Power Query and not in a database?**
The client only has the flat export, so the star is rebuilt from it inside Power BI: one staging query reads the file once, and Sales, Customer and Product are built from it. With a client database, the same tables could be views there instead.

**How would you do this for a client?**
Measure their report first, as it is, with the same method. Put their export in `data/input/`, map their column names in `config/client.yaml`, run the notebook for the check numbers, rebuild with the checklist, then measure again. No code changes.

## 7. Limits, in plain words

- No timings yet. The reports still have to be built and timed in Power BI Desktop, so the speed-up and the model size are not known. The README will show them only once they are measured.
- Until both reports are built, "every number unchanged" is what the numbers must match, proven in SQL. The match inside Power BI is checked during the build.
- Each page is timed once, on one laptop. Small differences are noise.
- The data is generated (see Data in the README), so the sales trends do not describe a real company.
- The slow report's previous-year measure only matches where every checked cell has sales in the selected year. That count is 0 here; a client's data must be checked again.
- The Customer table only knows customers who bought and their country, because it is built from the sales export.
