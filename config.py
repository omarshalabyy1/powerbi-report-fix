"""The one place client values come from: config/client.yaml. `python config.py` checks the input file."""

from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).parent
STANDARD = ["order_key", "order_date", "customer_key", "country", "product_key", "product_name",
            "category", "subcategory", "quantity", "net_price", "unit_cost"]
# The column names the fixed report reads from output/sales.csv (powerbi/01-power-query.md).
REPORT_COLUMNS = {
    "order_key": "Order Key", "order_date": "Order Date", "customer_key": "Customer Key", "country": "Country",
    "product_key": "Product Key", "product_name": "Product Name", "category": "Category",
    "subcategory": "Subcategory", "quantity": "Quantity", "net_price": "Net Price", "unit_cost": "Unit Cost",
}
REQUIRED = (
    ["client.name", "client.currency", "inputs.flat"]
    + [f"columns.{c}" for c in STANDARD]
    + ["measurements.pages", "report.title", "report.check_year", "report.date_start", "report.date_end",
       "report.second_check.year", "report.second_check.country", "report.second_check.category",
       "report.colours.data", "report.colours.text", "report.colours.muted",
       "report.colours.page", "report.colours.line", "report.colours.danger"]
)


def load_config():
    try:
        cfg = yaml.safe_load((ROOT / "config" / "client.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        line = error.problem_mark.line + 1 if getattr(error, "problem_mark", None) else "?"
        raise SystemExit(f"config/client.yaml is not valid YAML near line {line} (quote a value with # or :)")
    for key in REQUIRED:
        node = cfg
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                raise SystemExit(f"config/client.yaml is missing {key}")
            node = node[part]
    cfg["input_dir"] = ROOT / "data" / "input"
    cfg["output_dir"] = ROOT / "output"
    return cfg


def check_inputs(cfg):
    """Stop with one line if the flat export is missing or lacks a mapped column."""
    path = cfg["input_dir"] / cfg["inputs"]["flat"]
    if not path.exists():
        raise SystemExit(f"missing data/input/{path.name} (inputs.flat in config/client.yaml)")
    header = duckdb.sql(f"SELECT * FROM read_csv('{path.as_posix()}') LIMIT 0").columns
    missing = [c for c in cfg["columns"].values() if c not in header]
    if missing:
        raise SystemExit(f"data/input/{path.name}: missing column(s): {', '.join(missing)}")


if __name__ == "__main__":
    check_inputs(load_config())
    print("config and input file OK")
