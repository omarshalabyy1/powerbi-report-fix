"""Demo only: write the demo's numbers (output/numbers.json, written by the notebook) into the README, the diagrams,
the slow report's build pack and the portfolio site's card. A client copy does not run this.

Run: python data/demo/publish.py   (after the notebook)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[2]
CARD = ROOT.parent / "portfolio" / "content" / "projects" / "powerbi-report-fix.en.md"
numbers = json.loads((ROOT / "output" / "numbers.json").read_text(encoding="utf-8"))
rows = numbers["sales_rows"]
numbers["archive_mb"] = f"{(ROOT / 'data' / 'demo' / 'csv-1m.7z').stat().st_size / 1e6:,.0f} MB"

if "slowest_before" in numbers:  # the Power BI measurements are in
    before, after, down = numbers["slowest_before"], numbers["slowest_after"], numbers["size_down"]
    numbers["headline"] = f"{rows} sales rows: slowest page from {before} to {after}, model size down {down}, every number unchanged."
    numbers["headline_short"] = f"Slowest page from {before} to {after}, with the same numbers."
    numbers["card_title"] = f"A Power BI report taken from {before} to {after}, with the same numbers"
    numbers["card_result"] = f"{rows} sales rows: slowest page from {before} to {after}, model size down {down}."
    pages = numbers["pages"].split(",")
    table = ["| | Before | After | Change |", "|---|---|---|---|"]
    table += [f"| {p.capitalize()} page | {numbers[p + '_before']} | {numbers[p + '_after']} | {numbers[p + '_change']} |" for p in pages]
    table.append(f"| Model in memory | {numbers['size_before']} | {numbers['size_after']} | down {down} |")
    numbers["timings"] = ("\n\n" + "\n".join(table) + "\n\nEach page timed once in Power BI Desktop with Performance Analyzer "
                          "from a cold cache, model size from DAX Studio's VertiPaq Analyzer "
                          "([method](docs/measuring.md)).\n\n")
else:
    numbers["headline"] = f"{rows} sales rows: a {numbers['flat_columns']}-column flat table rebuilt as a star schema, every number unchanged."
    numbers["headline_short"] = f"{rows} sales rows, the same numbers before and after."
    numbers["card_title"] = "Rebuilding a slow sales report without changing a single number"
    numbers["card_result"] = (f"{rows} sales rows: one {numbers['flat_columns']}-column table rebuilt as a star schema "
                              "of 4 tables, every number matched against SQL before and after.")


def fill(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--n:(\w+)-->(.*?)<!--/n-->",
                  lambda m: f"<!--n:{m[1]}-->{numbers.get(m[1], m[2])}<!--/n-->", text, flags=re.S)
    path.write_text(text, encoding="utf-8")


for name in ["README.md", "docs/header.svg", "docs/before-after.svg",
             "powerbi/before/README.md", "powerbi/before/01-power-query.md", "powerbi/before/02-model.md"]:
    fill(ROOT / name)

if CARD.exists():  # Omar's portfolio checkout, next to this repo
    text = CARD.read_text(encoding="utf-8")
    text = re.sub(r'^title: ".*"$', f'title: "{numbers["card_title"]}"', text, flags=re.M)
    text = re.sub(r'^result: ".*"$', f'result: "{numbers["card_result"]}"', text, flags=re.M)
    CARD.write_text(text, encoding="utf-8")
    fill(CARD)
print("wrote the demo numbers:", numbers["headline"])
