# Lagos Life | Player Intelligence & Growth Analytics

**Independent product analytics case study, not affiliated with or commissioned by Lagos Life or Vatar.**

> **Data integrity:** This project separates manually curated public commentary from a **fully synthetic** player-event simulation. It does **not** have access to player accounts, private telemetry, chats, game APIs, revenue, DAU, churn or Vatar dashboards. Do not interpret the toy retention metrics or tiny public source counts as actual game statistics.

## Why this project exists
Lagos Life is a browser-based social world inspired by Lagos. This portfolio project asks how product teams could turn public feedback and privacy-appropriate internal event instrumentation into evidence-backed improvements in gameplay pacing, engagement and product development. The product identity was verified against [Vatar's site](https://vatar.com/) linking to [lagoslife.app](https://lagoslife.app/).

## Phase 1 deliverables
- **Traceable public feedback dataset:** six hand-coded, paraphrased observations from one public [r/Nigeria thread](https://www.reddit.com/r/Nigeria/comments/1wzdj0o/lagos_life/), with dates, evidence type and confidence.
- **Reproducible Python + SQLite pipeline:** validates source IDs, dates, labels, uniqueness and provenance, then creates queryable summaries.
- **Interactive Streamlit dashboard:** observation topics, labelled qualitative findings, and click-through source evidence.
- **Separate synthetic gameplay lab:** deterministic 250-player scenario with correctly eligible D1/D7 cohorts. No production numbers claimed.
- **Product research brief:** several falsifiable hypotheses, suggested experiments and metrics the actual operator would need to evaluate.
- **Privacy-first event schema and automated tests:** consent-appropriate telemetry proposal; no user accounts or private chats collected.

## Quickstart
Requires Python 3.11+.

```bash
git clone https://github.com/Ayoleyi-dev/Lagos-life-analytics-review-.git
cd Lagos-life-analytics-review-
git checkout development
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/quickstart.py
python -m unittest discover -s tests -v
streamlit run dashboard/app.py
```

`quickstart.py` uses only Python standard-library dependencies, so it and the unit tests run without installing Streamlit. Generated outputs are in ignored `outputs/`.

## Repository map
```
├── data/public/                 # Annotated, short public-source paraphrases + registry
├── src/lagos_life/              # Validation, SQLite storage, synthetic cohort lab
├── dashboard/app.py             # Public and synthetic views separated by tabs
├── scripts/quickstart.py        # Reproduce tables, SQLite DB, and sample outputs
├── docs/                        # Research design, hypotheses, schema, dictionary
├── tests/                       # Built-in unittest suite
└── .github/workflows/tests.yml  # Automated quality checks
```

## Initial, limited research signals
A small public discussion contains an account of slow-feeling gameplay timing (OBS-003), a report of boredom (OBS-006), and praise of visible developer updates (OBS-004/005). These **are leads for further study, not an estimate of the proportion of players experiencing those issues**. See [research protocol](docs/research_protocol.md) and [hypothesis brief](docs/product_hypotheses.md).

## What this project does NOT do
- Scrape X/Twitter or bypass access restrictions. X [prohibits scraping without written consent](https://x.com/en/tos); future API integration would require approved access.
- Scrape Lagos Life's authenticated or private endpoints, player presence, DMs, payment details, personal identifiers or private comments.
- Treat `lagoslife.com.ng` or other same-name websites as the operator of Vatar's `lagoslife.app` product without independent verification.
- Present social-media comments as representative user sentiment, or fictional metrics as real business results.
- Claim a deployed dashboard: the app source is included and locally runnable; deployment comes after review.

## Next milestones
1. Expand the research sample across independently verified, permitted sources and add time-stamped evidence review.
2. Double-code a labelled sample and measure inter-annotator agreement.
3. Add an approved social/API ingestion source if permitted; retain platform links over bulk user-generated text.
4. Publish a Streamlit demo and a polished, concise product-intelligence memo.
5. Send a speculative application for a paid remote data/product analytics role with a truthful portfolio link.

**Maintainer:** [Ayoleyi-dev](https://github.com/Ayoleyi-dev) · [Portfolio](https://ayoleyi-portfolio.vercel.app/)