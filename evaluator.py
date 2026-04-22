import json
import anthropic

MODEL = "claude-haiku-4-5-20251001"

def _get_client():
    return anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert evaluator for AI-generated financial advisor meeting notes.
You evaluate notes produced by an AI meeting agent (similar to Mili's Meeting Agent) against
defined quality dimensions. You are used internally by Mili's product and ML teams.

Always respond with valid JSON only. No markdown, no explanation outside the JSON."""


def _call(prompt: str) -> dict:
    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def evaluate_quality(meeting_type: str, context: str, note: str) -> dict:
    prompt = f"""Evaluate this AI-generated meeting note for quality and completeness.

MEETING TYPE: {meeting_type}

MEETING CONTEXT (what actually happened in the meeting):
{context}

AI-GENERATED NOTE:
{note}

Score these 6 dimensions. For each, return pass (true/false) and a specific reasoning sentence
referencing actual content from the note.

Return this exact JSON:
{{
  "scores": {{
    "action_items": {{"pass": bool, "reasoning": "string"}},
    "advisor_commitments": {{"pass": bool, "reasoning": "string"}},
    "client_decisions": {{"pass": bool, "reasoning": "string"}},
    "life_events": {{"pass": bool, "reasoning": "string"}},
    "factual_accuracy": {{"pass": bool, "reasoning": "string"}},
    "client_language_preserved": {{"pass": bool, "reasoning": "string"}}
  }},
  "score": int,
  "summary": "string"
}}

Dimension guidance:
- factual_accuracy: Are dates, dollar amounts, decisions, and deadlines correct? Fail if any fact is invented or wrong.
- client_language_preserved: Are client's own words about risk, goals, or concerns quoted or closely paraphrased — not reframed into advisor/financial jargon? Fail if the note substitutes technical terms for the client's actual language in ways that change nuance.

score is 0-100. Each dimension worth ~17 points (round to nearest 5).
summary is 1-2 sentences on overall quality.
Be strict on factual_accuracy. Be moderate on client_language_preserved — close paraphrase that preserves meaning is acceptable."""
    return _call(prompt)


def evaluate_compliance(meeting_type: str, context: str, note: str) -> dict:
    prompt = f"""Evaluate this AI-generated meeting note for US regulatory compliance.
Apply the standards a FINRA examiner would use under Reg BI and Rule 17a-3.

MEETING TYPE: {meeting_type}

MEETING CONTEXT (what actually happened in the meeting):
{context}

AI-GENERATED NOTE:
{note}

Score these 5 compliance dimensions. For each, return pass (true/false) and reasoning citing
the specific regulatory requirement and whether the note meets it.

Return this exact JSON:
{{
  "scores": {{
    "risk_tolerance": {{"pass": bool, "reasoning": "string", "regulation": "Reg BI"}},
    "investment_objective": {{"pass": bool, "reasoning": "string", "regulation": "Reg BI"}},
    "suitability_basis": {{"pass": bool, "reasoning": "string", "regulation": "Reg BI Best Interest"}},
    "material_changes": {{"pass": bool, "reasoning": "string", "regulation": "Rule 17a-3"}},
    "follow_up_commitments": {{"pass": bool, "reasoning": "string", "regulation": "Fiduciary Duty"}}
  }},
  "score": int,
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "summary": "string"
}}

score is 0-100. risk_level: HIGH if <=40, MEDIUM if 41-79, LOW if >=80.
Note: for Prospect/Intro calls, suitability_basis is not required — mark as pass with note.
summary is 1-2 sentences on compliance posture and regulatory exposure."""
    return _call(prompt)


def evaluate_review_decision(meeting_type: str, context: str, note: str) -> dict:
    prompt = f"""You are Mili's automated review gate. Decide whether this AI-generated meeting note
should AUTO-SYNC to the advisor's CRM, or be FLAGGED for the advisor to review first.

MEETING TYPE: {meeting_type}

MEETING CONTEXT (what actually happened in the meeting):
{context}

AI-GENERATED NOTE:
{note}

Evaluate based on: compliance completeness, accuracy of key facts, presence of client decisions,
and any fields that could cause downstream errors if synced incorrectly.

Return this exact JSON:
{{
  "decision": "AUTO-APPROVE" | "FLAG FOR REVIEW",
  "confidence": int,
  "reasons": ["string", "string"],
  "fields_to_verify": ["string"]
}}

confidence is 0-100 (how confident you are in the decision).
reasons: top 2-3 specific reasons for the decision.
fields_to_verify: specific fields the advisor should check before approving (empty list if AUTO-APPROVE).
Be decisive — lean toward FLAG FOR REVIEW if any compliance-critical field is missing."""
    return _call(prompt)
