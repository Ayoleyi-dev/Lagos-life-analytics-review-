"""Source-aware research audit, never population sentiment inference."""
from __future__ import annotations
from collections import Counter, defaultdict

RESEARCH_SOURCE_TYPES = {"community", "editorial_review"}


def audit_evidence(observations: list[dict], sources: list[dict]) -> dict:
    """Count observations and independent *source documents*, not unique players."""
    source_types = {s["source_id"]: s["source_type"] for s in sources}
    topic_sources: dict[str, set[str]] = defaultdict(set)
    topic_firsthand_sources: dict[str, set[str]] = defaultdict(set)
    by_source = Counter()
    for o in observations:
        if source_types.get(o["source_id"]) not in RESEARCH_SOURCE_TYPES:
            continue
        topic_sources[o["topic"]].add(o["source_id"])
        by_source[o["source_id"]] += 1
        if o["firsthand"] == "yes":
            topic_firsthand_sources[o["topic"]].add(o["source_id"])
    return {
        "data_class": "CURATED_PUBLIC_COMMENTARY",
        "observations": sum(by_source.values()),
        "distinct_source_documents": len(by_source),
        "source_documents_by_type": dict(sorted(Counter(source_types[k] for k in by_source).items())),
        "observations_per_source": dict(sorted(by_source.items())),
        "topics": [
            {"topic": topic, "observation_count": sum(o["topic"] == topic for o in observations
               if o["source_id"] in by_source),
             "independent_source_documents": len(ids),
             "firsthand_source_documents": len(topic_firsthand_sources[topic]),
             "source_ids": sorted(ids)}
            for topic, ids in sorted(topic_sources.items())
        ],
        "limitations": [
            "Non-random, manually selected material. No inference to all Lagos Life players.",
            "Multiple comments in one thread are not independent sources; one reviewer contributes one document.",
            "A source mentioning a topic does not establish the topic's prevalence, severity or causal impact.",
            "No internal telemetry, user identities, survey denominators, revenue or retention data.",
        ],
    }
