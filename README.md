# Mili — Meeting Note Eval Tool

An internal evaluation framework for AI-generated financial advisor meeting notes. Scores notes across three dimensions before they sync to a CRM — surfacing gaps before they become compliance incidents.

---

## What it does

Mili's Meeting Agent auto-generates structured notes from advisor-client meetings in real time. This tool evaluates the quality of those notes systematically, across:

| Tab | What's evaluated |
|-----|-----------------|
| **Quality** | Action items, advisor commitments, client decisions, life events, factual accuracy, client language preservation |
| **Compliance (Reg BI)** | Risk tolerance, investment objective, suitability basis, material changes, follow-up commitments |
| **Review Decision** | Auto-approve to CRM, or flag for advisor review — with specific fields to verify |

Each dimension returns a pass/fail verdict with field-level reasoning, so ML engineers and PMs can pinpoint exactly where note quality degrades — not just that it did.

---

## Why this exists

Mili is ranked the most accurate AI note-taker for wealth advisors. Maintaining that standard at scale requires systematic measurement.

This eval framework makes quality visible and actionable across three real use cases:

1. **Pre-deployment regression testing** — run on historical notes before shipping a new model or prompt change
2. **Online monitoring** — sample production notes weekly to detect failure patterns by meeting type
3. **Real-time gating** — run before CRM sync; flag low-confidence notes for advisor review

---

## Running locally

```bash
git clone https://github.com/YOUR_USERNAME/mili-eval
cd mili-eval
pip install -r requirements.txt
```

Add your API key:

```bash
# Create .streamlit/secrets.toml
echo 'ANTHROPIC_API_KEY = "sk-ant-..."' > .streamlit/secrets.toml
```

Run:

```bash
streamlit run app.py
```

---

## Deploying to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select repo, set main file to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Deploy

---

## Project structure

```
app.py          # Streamlit UI — sidebar, 3 scored tabs
evaluator.py    # Evaluation logic — structured prompts + JSON parsing
samples.py      # Synthetic meeting samples (3 types × good/bad note versions)
requirements.txt
```

---

## Sample meetings included

| Meeting type | Why it's included |
|---|---|
| Annual Review | Complex, high compliance stakes — full Reg BI documentation required |
| Prospect / Intro Call | Simpler discovery meeting — fewer compliance fields, relationship-building focus |
| Portfolio Rebalancing | Suitability-critical — every trade recommendation needs a documented basis |

Each sample has a **complete note** and a **degraded note** — toggle between them to see scores change visibly across all three tabs.

---
