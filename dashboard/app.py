"""Run at repository root: streamlit run dashboard/app.py."""
from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lagos_life.analysis import read_csv, summarize, validate_observations  # noqa: E402
from lagos_life.evidence import audit_evidence  # noqa: E402
from lagos_life.simulation import simulate_sessions, retention  # noqa: E402

st.set_page_config(page_title="Lagos Life | Independent Product Intelligence", page_icon="📊", layout="wide")
st.title("Lagos Life | Player Intelligence Lab")
st.caption("Independent and unaffiliated research prototype · 17 October 2026 · Not official Vatar analytics")
st.warning("PUBLIC FEEDBACK ≠ PLAYER POPULATION. Synthetic gameplay is a demonstration, not real Lagos Life telemetry.")

sources = read_csv(ROOT / "data/public/source_registry.csv")
observations = read_csv(ROOT / "data/public/research_observations.csv")
validate_observations(observations, sources)
summary = summarize(observations)
audit = audit_evidence(observations, sources)
feedback_tab, product_tab, demo_tab, method_tab = st.tabs(["Public evidence", "Product decisions", "Synthetic retention lab", "Methods & limitations"])

with feedback_tab:
    st.subheader("Small, hand-curated public feedback sample — not a survey")
    a, b, c = st.columns(3)
    a.metric("Coded observations", summary["n_observations"])
    b.metric("Distinct source documents", audit["distinct_source_documents"])
    c.metric("First-person reports", summary["firsthand_count"])
    st.caption("14 observations across 3 public discussion threads and 1 guest review. Not independent players, and not representative sentiment percentages.")
    df = pd.DataFrame(observations)
    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.bar(df.groupby("topic").size().reset_index(name="observations"),
            x="topic", y="observations", title="Topics appearing in the coded sample"), use_container_width=True)
    with right:
        st.plotly_chart(px.bar(df.groupby("valence").size().reset_index(name="observations"),
            x="valence", y="observations", title="Human-coded valence (sample only)"), use_container_width=True)
    st.subheader("Traceable research observations")
    select = st.selectbox("Filter by topic", ["All topics"] + sorted(df.topic.unique().tolist()))
    displayed = df if select == "All topics" else df[df.topic == select]
    registry = {s["source_id"]: s for s in sources}
    for item in displayed.to_dict("records"):
        with st.expander(f"{item['observation_id']} · {item['topic'].replace('_', ' ').title()} · {item['valence']}"):
            st.write(item["paraphrase"])
            st.caption(f"Interpretation: {item['interpretation']}")
            st.caption(f"Evidence: {item['evidence_type']}; firsthand: {item['firsthand']}; coder confidence: {item['confidence']}")
            st.link_button("Open source discussion", registry[item["source_id"]]["url"])
    st.info("The source links open discussions or articles, not guaranteed comment-level permalinks. Multiple remarks may belong to one reviewer or one thread. Do not claim population sentiment, churn, user totals or causality.")

with product_tab:
    st.subheader("Source-aware product hypotheses")
    st.caption("A topic appearing in several source documents merits investigation but does not measure prevalence.")
    topic_data = pd.DataFrame(audit["topics"])
    st.dataframe(topic_data, hide_index=True, use_container_width=True)
    st.plotly_chart(px.bar(topic_data, x="topic", y="independent_source_documents", title="Distinct source documents mentioning a topic"), use_container_width=True)
    st.markdown("""
    | Hypothesis | Validation idea | Internal success metrics required |
    |---|---|---|
    | Repeat-play depth may need strengthening | Try optional progression quests with a holdout | Eligible D1/D7, quest completion, frustration feedback |
    | Social currency transfers may need clearer guidance | Test optional transfer explanations or safeguards | Support tickets, mis-sends, opted-in feedback |
    | Nigerian cultural specificity supports appeal | Test themed onboarding guidance | First-session completion and satisfaction |
    | Open social spaces require trust and safety safeguards | Review reporting workflow with the operator | Case resolution time, repeat incidents |

    These are testable proposals, not effects observed in actual company telemetry.
    See `docs/phase2_brief.md` and `docs/trust_safety_watch.md` for the research context.
    """)


with demo_tab:
    st.subheader("Synthetic scenario testing — no real game telemetry")
    st.caption("Deterministic simulated cohorts let us demonstrate event tracking and retention calculations without access to Vatar's databases.")
    n = st.slider("Fictional players", min_value=50, max_value=1000, step=50, value=250)
    simulated = simulate_sessions(n_players=n, seed=42)
    d1, d7 = retention(simulated, 1), retention(simulated, 7)
    x, y, z = st.columns(3)
    x.metric("Synthetic D1", f"{d1['retention_rate']:.1%}")
    y.metric("Synthetic D7", f"{d7['retention_rate']:.1%}")
    z.metric("Generated player sessions", f"{len(simulated):,}")
    daily = pd.DataFrame(simulated).groupby("session_date")["synthetic_user_id"].nunique().reset_index(name="fictional_active_users")
    st.plotly_chart(px.line(daily, x="session_date", y="fictional_active_users", markers=True,
        title="Hypothetical daily active players — simulated only"), use_container_width=True)
    st.dataframe(pd.DataFrame([d1, d7]), hide_index=True, use_container_width=True)
    st.error("These values must never be presented as Lagos Life DAU, D1, D7, actual player behaviour or commercial performance.")

with method_tab:
    st.markdown("""
    ### Research design
    - Official game: [lagoslife.app](https://lagoslife.app/) · company: [Vatar](https://vatar.com/)
    - Fourteen manually paraphrased observations were curated from three public Reddit discussions and one guest review.
    - Observations are not a random sample; multiple comments in one thread and paragraphs in a review are not independent participants. No usernames or private messages are stored.
    - Every observation has an ID, date, source reference, topic, valence, evidence type, first-person flag and confidence.
    - This project does not scrape X, access private game endpoints, or collect players' personal data.
    - Suggested product experiments are hypotheses requiring Vatar's internal and consent-appropriate metrics to validate.
    - Synthetic model parameters are fabricated to exercise analytics software, not fitted to game data.
    See `docs/research_protocol.md`, `docs/product_hypotheses.md` and `docs/event_instrumentation.md` in the repository.
    """)
    st.subheader("Source register")
    st.dataframe(pd.DataFrame(sources)[["source_id", "source_type", "title", "url", "access_date"]], hide_index=True)
