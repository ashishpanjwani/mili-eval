import os
import streamlit as st
from samples import SAMPLES
from evaluator import evaluate_quality, evaluate_compliance, evaluate_review_decision

# Streamlit Cloud stores secrets in st.secrets; locally use the env var directly
if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

st.set_page_config(page_title="Mili Note Evaluator", page_icon="🏦", layout="wide")

st.title("Mili — Meeting Note Eval Tool")
st.caption(
    "Internal prototype · LLM-as-judge framework for evaluating AI-generated meeting notes "
    "across quality, compliance (Reg BI / FINRA), and sync readiness."
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Meeting Setup")
    meeting_type = st.selectbox("Meeting type", list(SAMPLES.keys()))
    note_version = st.radio(
        "Note version",
        ["Good note (complete)", "Bad note (degraded)"],
        help="Toggle between a complete note and a degraded note to see scores change.",
    )
    st.caption(SAMPLES[meeting_type]["description"])
    st.divider()
    st.markdown("**How this works**")
    st.markdown(
        "1. Select a meeting type and note version\n"
        "2. Click **Run Eval** to score with Claude\n"
        "3. Scores update across all three tabs\n\n"
        "_In production, Mili runs this eval on every generated note before CRM sync._"
    )
    run = st.button("Run Eval", type="primary", use_container_width=True)

sample = SAMPLES[meeting_type]
context = sample["context"]
note = sample["good_note"] if "Good" in note_version else sample["bad_note"]

# ── Note preview ──────────────────────────────────────────────────────────────
with st.expander("View selected note", expanded=False):
    st.code(note, language=None)

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_badge(score: int) -> str:
    color = "green" if score >= 80 else ("orange" if score >= 50 else "red")
    return f":{color}[**{score}/100**]"

def pass_fail(passed: bool) -> str:
    return ":white_check_mark: Pass" if passed else ":x: Fail"

def risk_badge(level: str) -> str:
    colors = {"LOW": "green", "MEDIUM": "orange", "HIGH": "red"}
    return f":{colors.get(level, 'gray')}[**{level} RISK**]"

# ── Results ───────────────────────────────────────────────────────────────────
if run:
    with st.spinner("Scoring with Claude (LLM-as-judge)…"):
        q = evaluate_quality(meeting_type, context, note)
        c = evaluate_compliance(meeting_type, context, note)
        r = evaluate_review_decision(meeting_type, context, note)

    tab1, tab2, tab3 = st.tabs(["Quality", "Compliance (Reg BI)", "Review Decision"])

    # ── Tab 1: Quality ────────────────────────────────────────────────────────
    with tab1:
        col_score, col_summary = st.columns([1, 3])
        with col_score:
            st.metric("Quality Score", f"{q['score']}/100")
        with col_summary:
            st.info(q["summary"])

        st.subheader("Field-level scores")
        labels = {
            "action_items": "Action Items",
            "advisor_commitments": "Advisor Commitments",
            "client_decisions": "Client Decisions",
            "life_events": "Life Events Captured",
            "factual_accuracy": "Factual Accuracy",
            "client_language_preserved": "Client Language Preserved",
        }
        for key, label in labels.items():
            s = q["scores"][key]
            with st.container(border=True):
                cols = st.columns([2, 1, 5])
                cols[0].markdown(f"**{label}**")
                cols[1].markdown(pass_fail(s["pass"]))
                cols[2].caption(s["reasoning"])

    # ── Tab 2: Compliance ─────────────────────────────────────────────────────
    with tab2:
        col_score, col_risk, col_summary = st.columns([1, 1, 3])
        with col_score:
            st.metric("Compliance Score", f"{c['score']}/100")
        with col_risk:
            st.markdown(f"**Risk Level**  \n{risk_badge(c['risk_level'])}")
        with col_summary:
            st.info(c["summary"])

        st.subheader("Regulatory field checks")
        reg_labels = {
            "risk_tolerance": "Risk Tolerance",
            "investment_objective": "Investment Objective",
            "suitability_basis": "Suitability Basis",
            "material_changes": "Material Changes",
            "follow_up_commitments": "Follow-up Commitments",
        }
        for key, label in reg_labels.items():
            s = c["scores"][key]
            with st.container(border=True):
                cols = st.columns([2, 1, 1, 4])
                cols[0].markdown(f"**{label}**")
                cols[1].markdown(pass_fail(s["pass"]))
                cols[2].caption(s.get("regulation", ""))
                cols[3].caption(s["reasoning"])

    # ── Tab 3: Review Decision ────────────────────────────────────────────────
    with tab3:
        decision = r["decision"]
        is_approve = decision == "AUTO-APPROVE"
        decision_color = "green" if is_approve else "red"

        st.markdown(f"## :{decision_color}[{decision}]")
        st.metric("Confidence", f"{r['confidence']}/100")

        st.subheader("Reasons")
        for reason in r["reasons"]:
            st.markdown(f"- {reason}")

        if r["fields_to_verify"]:
            st.subheader("Fields for advisor to verify before approving")
            for field in r["fields_to_verify"]:
                st.markdown(f"- {field}")
        else:
            st.success("No fields require manual verification — safe to auto-sync.")

else:
    st.info("Select a meeting type and note version in the sidebar, then click **Run Eval**.")
