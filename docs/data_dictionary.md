# Data dictionary and provenance

## Source registry
`data/public/source_registry.csv`: `source_id` unique reference, `source_type`, `title`, `url`, `published_or_updated` (can be blank), `access_date`, and `usage_notes`.

## Research observations
`data/public/research_observations.csv`: `observation_id` primary key, `source_id` foreign key, `observed_date`, `topic`, human-coded `valence`, `evidence_type`, `firsthand` yes/no, editorial `paraphrase`, cautious `interpretation`, and `confidence` (classification confidence only).

**Denominator:** observations, not unique players. Source links point to entire Reddit discussion, not individual comment permalinks — a current traceability limitation.

## Ignored outputs
- `public_research.sqlite3`: relational mirror, enforced source foreign keys.
- `public_observation_summary.json`: counts of annotated observations.
- `synthetic_sessions.csv`: fully fictional records marked `SYNTHETIC_SIMULATION`.
- `synthetic_retention.json`: toy D1 and D7 metrics calculated from fabricated events.

No private game data, social-account identity, live-user activity or revenue measurements are included.
