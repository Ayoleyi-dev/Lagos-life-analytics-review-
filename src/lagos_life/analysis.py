"""Validation and descriptive summaries for manually curated public observations.

No scraping. Never infer product metrics or player-population statistics from this sample.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

VALID_VALENCES = {"positive", "negative", "mixed", "neutral"}
VALID_EVIDENCE = {"first_person_report", "secondhand_impression", "official_statement", "reported_claim"}
VALID_CONFIDENCE = {"low", "medium", "high"}
REQUIRED = {
    "observation_id", "source_id", "observed_date", "topic", "valence",
    "evidence_type", "firsthand", "paraphrase", "interpretation", "confidence",
}


class ValidationError(ValueError):
    """Raised if the research input violates data provenance rules."""


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def validate_sources(rows: list[dict[str, str]]) -> None:
    ids: set[str] = set()
    for row in rows:
        source_id = row.get("source_id", "").strip()
        if not source_id or source_id in ids:
            raise ValidationError("Source IDs must be present and unique")
        ids.add(source_id)
        if not row.get("url", "").startswith("https://"):
            raise ValidationError(f"Source {source_id} needs an https URL")


def validate_observations(
    rows: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> None:
    validate_sources(sources)
    source_ids = {row["source_id"] for row in sources}
    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        if not REQUIRED.issubset(row):
            raise ValidationError(f"CSV missing columns: {sorted(REQUIRED - set(row))}")
        oid = row["observation_id"].strip()
        if not oid or oid in seen:
            raise ValidationError(f"Duplicate/missing observation id at row {index}")
        seen.add(oid)
        if row["source_id"] not in source_ids:
            raise ValidationError(f"Unregistered source at row {index}")
        try:
            date.fromisoformat(row["observed_date"])
        except ValueError as exc:
            raise ValidationError(f"Invalid date at row {index}") from exc
        if row["valence"] not in VALID_VALENCES:
            raise ValidationError(f"Invalid valence at row {index}")
        if row["evidence_type"] not in VALID_EVIDENCE:
            raise ValidationError(f"Invalid evidence type at row {index}")
        if row["firsthand"] not in {"yes", "no"}:
            raise ValidationError(f"Invalid firsthand flag at row {index}")
        if row["confidence"] not in VALID_CONFIDENCE:
            raise ValidationError(f"Invalid confidence at row {index}")
        if not row["topic"].strip() or not row["paraphrase"].strip() or not row["interpretation"].strip():
            raise ValidationError(f"Missing topic or paraphrase at row {index}")


def summarize(rows: list[dict[str, str]]) -> dict:
    """Counts *coded observations*, not independent players or population sentiment."""
    return {
        "unit_of_analysis": "manually coded public observation",
        "sample_design": "convenience sample; no population inference",
        "n_observations": len(rows),
        "n_evidence_sources": len({r["source_id"] for r in rows}),
        "topic_counts": dict(sorted(Counter(r["topic"] for r in rows).items())),
        "valence_counts": dict(sorted(Counter(r["valence"] for r in rows).items())),
        "firsthand_count": sum(r["firsthand"] == "yes" for r in rows),
        "interpretation_warning": "Do not describe these counts as player sentiment shares or retention metrics.",
    }


def write_summary(observations: Path, sources: Path, output: Path) -> dict:
    data = read_csv(observations)
    validate_observations(data, read_csv(sources))
    summary = summarize(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary
