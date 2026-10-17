"""Run: python scripts/quickstart.py"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lagos_life.analysis import write_summary  # noqa: E402
from lagos_life.simulation import retention, simulate_sessions  # noqa: E402
from lagos_life.storage import build_database, topic_breakdown  # noqa: E402

out = ROOT / "outputs"
summary = write_summary(
    ROOT / "data/public/research_observations.csv",
    ROOT / "data/public/source_registry.csv",
    out / "public_observation_summary.json",
)
build_database(
    ROOT / "data/public/research_observations.csv",
    ROOT / "data/public/source_registry.csv",
    out / "public_research.sqlite3",
)
print("SQL topic breakdown:", topic_breakdown(out / "public_research.sqlite3"))
rows = simulate_sessions()
out.mkdir(exist_ok=True)
with (out / "synthetic_sessions.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
metrics = {"D1": retention(rows, 1), "D7": retention(rows, 7)}
(out / "synthetic_retention.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
print("PUBLIC OBSERVATIONS — not a representative sample:", json.dumps(summary, indent=2))
print("SYNTHETIC SIMULATION — not real Lagos Life activity:", json.dumps(metrics, indent=2))
