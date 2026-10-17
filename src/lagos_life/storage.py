"""Reproducible SQLite layer; tables preserve provenance and study limitations."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from .analysis import read_csv, validate_observations

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    access_date TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS observations (
    observation_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    observed_date TEXT NOT NULL,
    topic TEXT NOT NULL,
    valence TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    firsthand INTEGER NOT NULL CHECK(firsthand IN (0,1)),
    paraphrase TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    confidence TEXT NOT NULL
);
"""


def build_database(observations_csv: Path, sources_csv: Path, db_path: Path) -> None:
    observations = read_csv(observations_csv)
    sources = read_csv(sources_csv)
    validate_observations(observations, sources)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as con:
        con.executescript(SCHEMA)
        con.executemany(
            "INSERT INTO sources VALUES (?, ?, ?, ?, ?)",
            [(s["source_id"], s["source_type"], s["title"], s["url"], s["access_date"]) for s in sources],
        )
        con.executemany(
            "INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(o["observation_id"], o["source_id"], o["observed_date"], o["topic"],
              o["valence"], o["evidence_type"], int(o["firsthand"] == "yes"),
              o["paraphrase"], o["interpretation"], o["confidence"]) for o in observations],
        )


def topic_breakdown(db_path: Path) -> list[tuple[str, int]]:
    with sqlite3.connect(db_path) as con:
        return con.execute(
            "SELECT topic, COUNT(*) AS n FROM observations GROUP BY topic ORDER BY n DESC, topic"
        ).fetchall()
