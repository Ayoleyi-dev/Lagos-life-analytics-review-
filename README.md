
# Lagos Life: Player Intelligence & Growth Analytics
 
*An independent product analytics case study. Not affiliated with, commissioned by, or endorsed by Lagos Life or Vatar.*
 
> **Read this first:** this repo contains two things only: a small set of public comments I curated by hand, and a player simulation that is **100% synthetic**. I have no access to Lagos Life's player accounts, telemetry, chats, revenue, DAU, churn, or Vatar's dashboards. None of the numbers here describe the real game.
 
## What this is
 
[Lagos Life](https://lagoslife.app/) is a browser-based social world inspired by Lagos, built by [Vatar](https://vatar.com/) (Vatar's site links to lagoslife.app, which is how I confirmed the product identity).
 
I wanted to know: how could a product team turn public feedback, plus privacy-respecting event tracking, into concrete decisions about pacing and engagement? So I built that workflow end to end on a small sample. **The method is the point here, not the findings.**
 
## What's in the repo
 
- **A public feedback dataset.** 14 hand-coded, paraphrased observations from four public sources (three Reddit discussions and one guest review). The first source is [this r/Nigeria thread](https://www.reddit.com/r/Nigeria/comments/1wzdj0o/lagos_life/). Every observation has a date, an evidence type, and a confidence rating so you can trace it back.
- **A Python + SQLite pipeline.** It checks source IDs, dates, labels, uniqueness, and provenance, then builds queryable summary tables.
- **A Streamlit dashboard.** Separate tabs for public observations, the synthetic lab, and product decisions, with click-through to the source evidence.
- **A synthetic gameplay lab.** A deterministic 250-player scenario with properly eligible D1/D7 cohorts. It exists to show how the analysis would work, not to claim anything about real retention.
- **A product research brief.** Testable hypotheses, suggested experiments, and the metrics the real operator would need to check them. See the [Phase 2 brief](docs/phase2_brief.md), the [hypothesis brief](docs/product_hypotheses.md), and the [trust-and-safety context](docs/trust_safety_watch.md).
- **A privacy-first event schema and automated tests.** A consent-friendly telemetry proposal. No user accounts, no private chats.
## What the public comments suggest
 
A few early leads, nothing more. One commenter described gameplay timing as slow (OBS-003), another said they got bored (OBS-006), and two others praised how visible the developers' updates were (OBS-004, OBS-005).
 
With 14 observations from four sources, this is **not** a measure of how many players feel any of this. Treat these as questions worth testing, not conclusions. The [research protocol](docs/research_protocol.md) explains how I coded and checked them.
 
## Run it yourself
 
Needs Python 3.11+.
 
```bash
git clone https://github.com/Ayoleyi-dev/Lagos-life-analytics-review-.git
cd Lagos-life-analytics-review-
git checkout development
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/quickstart.py
python -m unittest discover -s tests -v
streamlit run dashboard/app.py
```
 
`quickstart.py` and the tests only use the Python standard library, so you can run them without installing Streamlit. Outputs land in `outputs/` (git-ignored).
 
The dashboard isn't deployed yet. For now it runs locally.
 
## What I deliberately didn't do
- **Scrape X/Twitter.** Since Its [terms](https://x.com/en/tos) prohibit scraping without written consent. If I am to add it later, it will be through approved API access.
- **Touch anything private.** No authenticated or private Lagos Life endpoints, player presence, DMs, payment details, personal identifiers, or private comments.
- **Assume same-name sites are the same product.** `lagoslife.com.ng` and similar sites aren't treated as Vatar's product without independent verification.
- **Pass off comments as "player sentiment" or fake metrics as business results.**
## Repo map
 
```
├── data/public/                 # Short paraphrased public observations + source registry
├── src/lagos_life/              # Validation, SQLite storage, synthetic cohort lab
├── dashboard/app.py             # Public and synthetic views, split by tabs
├── scripts/quickstart.py        # Rebuilds tables, the SQLite DB, and sample outputs
├── docs/                        # Research design, hypotheses, schema, data dictionary
├── tests/                       # Built-in unittest suite
└── .github/workflows/tests.yml  # Automated checks
```
 
 
**Maintainer:** [Ayoleyi-dev](https://github.com/Ayoleyi-dev) · [Portfolio](https://ayoleyi-portfolio.vercel.app/)