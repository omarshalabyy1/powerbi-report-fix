"""Demo only: download the Contoso sales data and write data/input/sales_flat.csv, the flat export the demo's
slow report reads and the notebook checks. A client hands over their own export instead (data/input/README.md).

Run: python data/demo/prepare_data.py   (about a minute; skips the download if the archive is already there)
"""
from pathlib import Path
import urllib.request

import duckdb
import py7zr

URL = "https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data-2024/csv-1m.7z"
DEMO = Path(__file__).parent
ARCHIVE = DEMO / "csv-1m.7z"
RAW = DEMO / "raw"
FLAT = DEMO.parent / "input" / "sales_flat.csv"

# One row per order line with every customer, store and product column joined on:
# the wide export slow reports are usually built on.
FLAT_SQL = f"""
SELECT
    s.OrderKey        AS "Order Key",
    s.LineNumber      AS "Line Number",
    s.OrderDate       AS "Order Date",
    s.DeliveryDate    AS "Delivery Date",
    s.CustomerKey     AS "Customer Key",
    c.GivenName || ' ' || c.Surname AS "Customer Name",
    c.Gender          AS "Gender",
    c.Birthday        AS "Birthday",
    c.Age             AS "Age",
    c.Occupation      AS "Occupation",
    c.Company         AS "Company",
    c.StreetAddress   AS "Street Address",
    c.City            AS "City",
    c.StateFull       AS "State",
    c.ZipCode         AS "Zip Code",
    c.CountryFull     AS "Country",
    c.Continent       AS "Continent",
    s.StoreKey        AS "Store Key",
    st.Description    AS "Store",
    st.CountryName    AS "Store Country",
    st.State          AS "Store State",
    s.ProductKey      AS "Product Key",
    p.ProductCode     AS "Product Code",
    p.ProductName     AS "Product Name",
    p.Manufacturer    AS "Manufacturer",
    p.Brand           AS "Brand",
    p.Color           AS "Color",
    trim(p.CategoryName)    AS "Category",
    trim(p.SubCategoryName) AS "Subcategory",
    s.Quantity        AS "Quantity",
    s.UnitPrice       AS "Unit Price",
    s.NetPrice        AS "Net Price",
    s.UnitCost        AS "Unit Cost",
    s.CurrencyCode    AS "Currency Code",
    s.ExchangeRate    AS "Exchange Rate"
FROM '{RAW / "sales.csv"}' s
JOIN '{RAW / "customer.csv"}' c USING (CustomerKey)
JOIN '{RAW / "store.csv"}' st USING (StoreKey)
JOIN (SELECT * FROM read_csv('{RAW / "product.csv"}', types = {{'ProductCode': 'VARCHAR'}})) p USING (ProductKey)
ORDER BY s.OrderKey, s.LineNumber
"""

if not ARCHIVE.exists():
    print("Downloading", URL)
    urllib.request.urlretrieve(URL, ARCHIVE)

if not (RAW / "sales.csv").exists():
    print("Extracting", ARCHIVE.name)
    with py7zr.SevenZipFile(ARCHIVE) as z:
        z.extractall(RAW)

sales_rows = duckdb.sql(f"SELECT count(*) FROM '{RAW / 'sales.csv'}'").fetchone()[0]
duckdb.sql(f"COPY ({FLAT_SQL}) TO '{FLAT}' (HEADER, DELIMITER ',')")
flat_rows = duckdb.sql(f"SELECT count(*) FROM '{FLAT}'").fetchone()[0]

# Every sales row must survive the joins, or the reports would not match the source.
assert flat_rows == sales_rows, f"flat file has {flat_rows:,} rows, sales has {sales_rows:,}"
print(f"Wrote data/input/{FLAT.name} ({flat_rows:,} rows, {FLAT.stat().st_size / 1e6:,.0f} MB)")
