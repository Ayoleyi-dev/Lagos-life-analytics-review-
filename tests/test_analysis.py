import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lagos_life.analysis import ValidationError, read_csv, summarize, validate_observations  # noqa: E402
from lagos_life.simulation import retention, simulate_sessions  # noqa: E402


class PublicResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = read_csv(ROOT / "data/public/source_registry.csv")
        cls.obs = read_csv(ROOT / "data/public/research_observations.csv")

    def test_seed_passes_provenance_validation(self):
        validate_observations(self.obs, self.sources)

    def test_duplicate_id_is_rejected(self):
        rows = copy.deepcopy(self.obs)
        rows[1]["observation_id"] = rows[0]["observation_id"]
        with self.assertRaises(ValidationError):
            validate_observations(rows, self.sources)

    def test_unknown_source_is_rejected(self):
        rows = copy.deepcopy(self.obs)
        rows[0]["source_id"] = "UNVERIFIED"
        with self.assertRaises(ValidationError):
            validate_observations(rows, self.sources)

    def test_bad_label_is_rejected(self):
        rows = copy.deepcopy(self.obs)
        rows[0]["valence"] = "super_positive"
        with self.assertRaises(ValidationError):
            validate_observations(rows, self.sources)

    def test_summary_denominator_is_observations(self):
        summary = summarize(self.obs)
        self.assertEqual(summary["n_observations"], len(self.obs))
        self.assertEqual(sum(summary["topic_counts"].values()), len(self.obs))
        self.assertEqual(summary["n_evidence_sources"], 4)


class SyntheticSimulationTests(unittest.TestCase):
    def test_seed_is_reproducible(self):
        self.assertEqual(simulate_sessions(20, 11), simulate_sessions(20, 11))

    def test_each_player_has_a_day_zero_session(self):
        events = simulate_sessions(23, 99)
        self.assertEqual(sum(e["day_since_signup"] == 0 for e in events), 23)
        self.assertTrue(all(e["data_class"] == "SYNTHETIC_SIMULATION" for e in events))

    def test_retention_is_bounded(self):
        events = simulate_sessions(70)
        for day in (1, 7):
            r = retention(events, day)
            self.assertLessEqual(r["retained_players"], r["eligible_players"])
            self.assertGreaterEqual(r["retention_rate"], 0)
            self.assertLessEqual(r["retention_rate"], 1)

    def test_zero_players_rejected(self):
        with self.assertRaises(ValueError):
            simulate_sessions(0)

    def test_ineligible_cohort_excluded(self):
        events = [
            {"synthetic_user_id": "P1", "signup_date": "2026-10-10", "session_date": "2026-10-10", "day_since_signup": 0},
            {"synthetic_user_id": "P2", "signup_date": "2026-10-01", "session_date": "2026-10-10", "day_since_signup": 9},
            {"synthetic_user_id": "P2", "signup_date": "2026-10-01", "session_date": "2026-10-01", "day_since_signup": 0},
        ]
        r = retention(events, 7)
        self.assertEqual(r["eligible_players"], 1)
        self.assertEqual(r["retained_players"], 0)


class SQLTests(unittest.TestCase):
    def test_sqlite_provenance_and_counts(self):
        import sqlite3
        import tempfile
        from lagos_life.storage import build_database, topic_breakdown
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "research.sqlite3"
            build_database(ROOT / "data/public/research_observations.csv", ROOT / "data/public/source_registry.csv", p)
            self.assertEqual(sum(count for _, count in topic_breakdown(p)), 14)
            with sqlite3.connect(p) as con:
                n = con.execute("SELECT COUNT(*) FROM observations o JOIN sources s ON o.source_id=s.source_id").fetchone()[0]
            self.assertEqual(n, 14)


if __name__ == "__main__":
    unittest.main()
