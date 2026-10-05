"""Read the Power BI measurements in data/input/: Performance Analyzer exports (page and visual times) and
DAX Studio's VertiPaq Analyzer exports (model size and shape). How to take them: docs/measuring.md."""

import json
import zipfile
from datetime import datetime


def _time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def page_times(path):
    """Seconds from the first visual starting to the last one finishing, and each visual's own seconds."""
    events = json.loads(path.read_text(encoding="utf-8-sig"))["events"]
    visuals = [e for e in events if e["name"] == "Visual Container Lifecycle" and "end" in e]
    if not visuals:
        raise SystemExit(f"{path.name}: no visual timings (Start recording, Refresh visuals, Stop, then Export)")
    page = max(_time(e["end"]) for e in visuals) - min(_time(e["start"]) for e in visuals)
    each = [(e["metrics"].get("visualTitle") or e["metrics"].get("visualType", "visual"),
             (_time(e["end"]) - _time(e["start"])).total_seconds()) for e in visuals]
    return page.total_seconds(), sorted(each, key=lambda v: -v[1])


def model_stats(path):
    """Model size in memory, its columns and calculated columns, and the hidden auto date tables."""
    with zipfile.ZipFile(path) as z:
        view = json.loads(z.read("DaxVpaView.json").decode("utf-8-sig"))
    date_tables = {t["TableName"] for t in view["Tables"] if t["IsLocalDateTable"] or t["IsTemplateDateTable"]}
    columns = [c for c in view["Columns"] if c["TableName"] not in date_tables and c["ColumnType"] != "RowNumber"]
    return {
        "size_mb": sum(t["TableSize"] for t in view["Tables"]) / 1e6,
        "tables": len(view["Tables"]) - len(date_tables),
        "columns": len(columns),
        "calculated_columns": sum(c["ColumnType"] == "Calculated" for c in columns),
        "hidden_date_tables": sum(t["IsLocalDateTable"] for t in view["Tables"]),
    }


def read_measurements(cfg):
    """None until the first export is in data/input/; then every file must be there."""
    pages = cfg["measurements"]["pages"]
    names = [f"{stage}-{page}.json" for stage in ("before", "after") for page in pages] + ["before.vpax", "after.vpax"]
    missing = [n for n in names if not (cfg["input_dir"] / n).exists()]
    if len(missing) == len(names):
        return None
    if missing:
        raise SystemExit(f"data/input/ is missing {', '.join(missing)} (docs/measuring.md)")
    return {stage: {"pages": {p: page_times(cfg["input_dir"] / f"{stage}-{p}.json") for p in pages},
                    "model": model_stats(cfg["input_dir"] / f"{stage}.vpax")}
            for stage in ("before", "after")}
