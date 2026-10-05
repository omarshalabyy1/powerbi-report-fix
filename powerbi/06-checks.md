# 6. Checks: the numbers each page must show (Contoso sales)

Written by [analysis/analysis.ipynb](../analysis/analysis.ipynb) from SQL on `data/input/sales_flat.csv`; do not edit by hand. **Both reports, the slow one and the fixed one, must show exactly these numbers.** If one differs, the build has a mistake; fix it before taking any timing.

Checked cells with no sales in the selected year: 0 (months 0, months in the second check 0, subcategories 0, products sold only the year before 0). The demo's slow `Sales PY` takes the year from the rows in each cell, so it matches the fixed report only where this count is 0.

Small rounding note: a value ending in exactly .5 can round one unit differently in Power BI than in Python. Anything else is a real difference.

## Model

| Table | Rows (Table view, bottom left) |
|---|---|
| Sales (both reports) | 2,098,633 |
| Customer (fixed report) | 88,063 |
| Product (fixed report) | 2,517 |
| Date (fixed report) | 3,653 |

## Page 1: Overview, default state (Year 2023, all countries, all categories)

| Card | Shows |
|---|---|
| Sales Amount | $318,425,878 |
| Sales YoY % | -28.4% |
| Margin % | 56.0% |
| Orders | 159,695 |
| Avg Order Value | $1,993.96 |
| Customers | 62,337 |

Sales YoY % compares with Sales PY = $444,516,719 (2022).

**Sales and previous year by month** (hover a column to see both values):

| Month | Sales Amount | Sales PY |
|---|---|---|
| Jan | $34,197,837 | $36,052,336 |
| Feb | $40,800,178 | $49,140,854 |
| Mar | $22,604,720 | $29,700,003 |
| Apr | $11,939,474 | $19,221,969 |
| May | $28,979,019 | $44,587,592 |
| Jun | $27,454,645 | $46,105,321 |
| Jul | $23,332,124 | $34,978,428 |
| Aug | $24,849,603 | $35,682,325 |
| Sep | $25,110,286 | $36,801,749 |
| Oct | $25,116,723 | $36,552,588 |
| Nov | $25,131,066 | $34,153,406 |
| Dec | $28,910,204 | $41,540,147 |

**Sales by category** (bar order, top to bottom):

| Category | Sales Amount |
|---|---|
| Computers | $113,112,204 |
| Cell phones | $59,754,615 |
| Home Appliances | $54,115,079 |
| TV and Video | $41,323,827 |
| Music, Movies and Audio Books | $21,768,661 |
| Cameras and camcorders | $18,765,677 |
| Audio | $6,847,569 |
| Games and Toys | $2,738,246 |

**Sales by country** (bar order, top to bottom):

| Country | Sales Amount |
|---|---|
| United States | $156,132,838 |
| Germany | $41,279,015 |
| Canada | $37,241,921 |
| United Kingdom | $26,252,830 |
| Australia | $22,522,330 |
| Netherlands | $17,031,456 |
| France | $11,734,079 |
| Italy | $6,231,408 |

## Page 1: Overview, filtered (Year 2022, Country Germany, Category Computers)

Set these three slicers, check the cards, then set the slicers back to the default state.

| Card | Shows |
|---|---|
| Sales Amount | $19,645,197 |
| Sales YoY % | 93.5% |
| Margin % | 56.0% |
| Orders | 9,854 |
| Avg Order Value | $1,993.63 |
| Customers | 5,197 |

## Page 2: Products, default state (Year 2023)

**Products by sales:** the table has 2,517 rows (every product sold in 2023). The top 10:

| Product Rank | Product Name | Sales Amount | Sales PY | Sales YoY % | Margin % | Customers |
|---|---|---|---|---|---|---|
| 1 | Adventure Works 52" LCD HDTV X590 White | $2,317,817 | $2,712,426 | -14.5% | 64.8% | 262 |
| 2 | Adventure Works 52" LCD HDTV X590 Brown | $2,264,428 | $2,867,452 | -21.0% | 64.7% | 270 |
| 3 | Adventure Works 52" LCD HDTV X590 Silver | $2,038,838 | $3,218,644 | -36.7% | 65.0% | 228 |
| 4 | Adventure Works 52" LCD HDTV X590 Black | $1,804,751 | $3,159,420 | -42.9% | 64.3% | 207 |
| 5 | Adventure Works Desktop PC2.33 XD233 White | $1,803,958 | $3,444,403 | -47.6% | 64.8% | 621 |
| 6 | Adventure Works Desktop PC2.33 XD233 Brown | $1,775,896 | $3,110,374 | -42.9% | 64.6% | 623 |
| 7 | WWI Desktop PC2.33 X2330 Silver | $1,733,712 | $3,152,473 | -45.0% | 65.0% | 607 |
| 8 | Adventure Works Desktop PC2.33 XD233 Silver | $1,712,446 | $3,158,969 | -45.8% | 64.9% | 634 |
| 9 | WWI Desktop PC2.33 X2330 Black | $1,678,976 | $3,077,120 | -45.4% | 64.9% | 627 |
| 10 | WWI Desktop PC2.33 X2330 Brown | $1,657,784 | $3,108,136 | -46.7% | 64.8% | 615 |

**Sales by category** matrix, collapsed to Category:

| Category | Sales Amount | Sales YoY % | Margin % |
|---|---|---|---|
| Computers | $113,112,204 | -36.1% | 56.2% |
| Cell phones | $59,754,615 | -27.7% | 54.0% |
| Home Appliances | $54,115,079 | -16.4% | 55.3% |
| TV and Video | $41,323,827 | -28.1% | 56.9% |
| Music, Movies and Audio Books | $21,768,661 | -22.3% | 58.6% |
| Cameras and camcorders | $18,765,677 | -21.1% | 58.2% |
| Audio | $6,847,569 | -10.4% | 55.1% |
| Games and Toys | $2,738,246 | -13.2% | 52.0% |
| Total | $318,425,878 | -28.4% | 56.0% |
