import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lagos_life.analysis import read_csv, validate_observations  # noqa: E402
from lagos_life.evidence import audit_evidence  # noqa: E402

class EvidenceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = read_csv(ROOT / 'data/public/source_registry.csv')
        cls.rows = read_csv(ROOT / 'data/public/research_observations.csv')

    def test_updated_research_data_valid(self):
        validate_observations(self.rows, self.sources)

    def test_four_research_sources_not_eight_registry_entries(self):
        audit = audit_evidence(self.rows, self.sources)
        self.assertEqual(audit['distinct_source_documents'], 4)
        self.assertEqual(audit['observations'], 14)

    def test_depth_hypothesis_triangles_without_claiming_population(self):
        audit = audit_evidence(self.rows, self.sources)
        depth = next(r for r in audit['topics'] if r['topic'] == 'engagement_depth')
        self.assertEqual(depth['independent_source_documents'], 3)
        self.assertEqual(depth['firsthand_source_documents'], 3)
        self.assertNotIn('estimated_player_sentiment', audit)

    def test_repetition_within_one_thread_does_not_inflate_source_count(self):
        x = list(self.rows) + [dict(self.rows[0], observation_id='OBS-FAKE')]
        report = audit_evidence(x, self.sources)
        topic = next(y for y in report['topics'] if y['topic']=='gameplay')
        self.assertEqual(topic['independent_source_documents'], 1)
        self.assertEqual(topic['observation_count'], 2)

    def test_ignores_registered_policy_sources_without_observations(self):
        audit = audit_evidence(self.rows, self.sources)
        self.assertNotIn('official', audit['source_documents_by_type'])

if __name__ == '__main__':
    unittest.main()
