"""
Synthetic meeting samples for the Mili eval prototype.
Each sample has a 'good' note (complete, compliant) and a 'bad' note (missing fields).
These simulate what Mili's Meeting Agent would produce — good vs. degraded output.
"""

SAMPLES = {
    "Annual Review": {
        "description": "Complex year-end portfolio review. High compliance stakes — Reg BI requires full suitability documentation.",
        "context": """
Meeting Type: Annual Review
Client: Robert & Linda Chen, married, ages 58 & 55
Advisor: Sarah Mitchell, CFP
Duration: 52 minutes
Platform: Zoom
Date: April 18, 2025

Key topics discussed:
- Robert planning to retire in 4 years (age 62). Linda continuing to work.
- Portfolio currently 70/30 equity/bond. Client expressed concern about sequence-of-returns risk.
- Robert said: "I can't afford to lose more than 20% — that would really stress us out."
- Linda mentioned her mother recently moved into assisted living — may affect estate plan.
- Advisor recommended shifting to 60/40 over next 12 months given retirement horizon.
- Discussed Roth conversion strategy — convert $50K this year while Robert still in lower bracket.
- Robert asked about long-term care insurance. Advisor said she'd research options and follow up.
- Action: Advisor to send revised IPS draft within 2 weeks.
- Action: Client to confirm beneficiary designations on all accounts by May 15.
- Next meeting: July 2025 for mid-year check-in.
        """,
        "good_note": """
Meeting Summary — Annual Review
Date: April 18, 2025 | Client: Robert & Linda Chen | Advisor: Sarah Mitchell, CFP

MEETING OVERVIEW
Annual portfolio review focused on retirement readiness and near-term allocation shift.

CLIENT SITUATION UPDATE
- Robert targeting retirement at age 62 (4 years). Linda continuing to work.
- Linda's mother recently moved to assisted living — estate planning implications flagged for follow-up.

RISK PROFILE & SUITABILITY
- Risk Tolerance: Moderate-conservative. Client explicitly stated maximum acceptable loss of 20%.
- Investment Objective: Capital preservation with moderate growth as primary goal entering retirement window.
- Suitability Basis: Current 70/30 allocation no longer optimal given 4-year retirement horizon and stated sequence-of-returns concern. Shift to 60/40 is consistent with client's risk tolerance and time horizon.

RECOMMENDATIONS & DECISIONS
- Agreed to rebalance portfolio from 70/30 to 60/40 equity/bond allocation over next 12 months.
- Roth conversion of $50,000 approved for 2025 tax year while Robert remains in lower bracket.
- Long-term care insurance review deferred pending advisor research.

ACTION ITEMS
- [ ] Sarah Mitchell: Send revised Investment Policy Statement draft (due: May 2, 2025)
- [ ] Sarah Mitchell: Research long-term care insurance options for clients aged 58–62 (due: May 15, 2025)
- [ ] Robert & Linda Chen: Confirm beneficiary designations on all accounts (due: May 15, 2025)

NEXT STEPS
Mid-year check-in scheduled for July 2025.
        """,
        "bad_note": """
Meeting Notes — Chen Annual Review
April 18, 2025

Met with Robert and Linda Chen for their annual review. Discussed the portfolio and made some changes.

Robert is thinking about retiring soon and they're concerned about market risk. We talked about adjusting the allocation and doing a Roth conversion this year.

Linda mentioned something about her mother.

Sarah will send some documents and the clients need to update their accounts.

Follow up in July.
        """,
    },

    "Prospect / Intro Call": {
        "description": "First meeting with a potential new client. Fewer compliance requirements but relationship-building and discovery are critical.",
        "context": """
Meeting Type: Prospect / Intro Call
Prospect: James Okafor, age 41, software engineer at Series B startup
Advisor: David Patel, CFP
Duration: 28 minutes
Platform: Phone call
Date: April 15, 2025

Key topics discussed:
- James has ~$420K in 401(k) from previous employer, wants to roll over.
- Has significant equity compensation (ISOs) — unsure of tax implications on exercise.
- Currently no financial advisor. Found David through LinkedIn.
- Primary goal: build wealth for early retirement by age 55.
- James mentioned his wife is pregnant with their first child — planning to review life insurance.
- Risk appetite: "I'm okay with volatility — I'm a long-term investor."
- Concerns: doesn't want to be sold products, wants fee-only advice.
- Advisor confirmed fee-only model, explained fiduciary duty.
- Next step: James to send 401(k) statements; David to prepare a proposal.
        """,
        "good_note": """
Meeting Summary — Prospect / Intro Call
Date: April 15, 2025 | Prospect: James Okafor | Advisor: David Patel, CFP

PROSPECT PROFILE
- Age 41, software engineer at a Series B startup
- Discovered advisor via LinkedIn; no existing financial advisor relationship

FINANCIAL SITUATION
- 401(k) rollover: ~$420,000 from previous employer, seeking guidance on rollover options
- Equity compensation: Holds ISOs, has questions about tax implications on exercise
- Currently unadvised; managing own finances

GOALS & TIMELINE
- Primary goal: Financial independence / early retirement by age 55 (14-year horizon)
- Life events: Wife is pregnant with first child — life insurance review flagged as near-term priority

RISK & INVESTMENT PROFILE
- Risk tolerance: High. Client self-described as "long-term investor, comfortable with volatility."
- Preference: Fee-only, fiduciary advice. Explicitly does not want product sales.

NEXT STEPS
- [ ] James Okafor: Send 401(k) statements from prior employer (no hard deadline set)
- [ ] David Patel: Prepare personalized proposal covering rollover options, ISO tax strategy, and life insurance framing (due before next call)
- Schedule follow-up call to review proposal
        """,
        "bad_note": """
Call Notes — James Okafor
April 15, 2025

Spoke with James, a software engineer. He has a 401k he wants to roll over and some stock options.

He wants to retire early and is interested in our services. He prefers fee-only advice.

James will send his statements. David will send a proposal.
        """,
    },

    "Portfolio Rebalancing": {
        "description": "Triggered rebalancing after equity run-up. Suitability documentation is critical — any trade recommendation must be justified against client's risk profile.",
        "context": """
Meeting Type: Portfolio Rebalancing Discussion
Client: Patricia Nguyen, age 67, retired
Advisor: Mark Torres, CFP
Duration: 20 minutes
Platform: Phone call
Date: April 17, 2025

Key topics discussed:
- Portfolio has drifted to 78% equity after Q1 market rally. Target allocation is 55/45.
- Patricia confirmed she does not need portfolio income for at least 3 years (pension + Social Security covers expenses).
- Advisor proposed selling $85,000 in large-cap growth funds and buying intermediate-term bond funds.
- Patricia asked if this was a good time to sell given recent gains.
- Advisor explained tax implications: $85K sale triggers ~$12K in long-term capital gains tax.
- Patricia approved the rebalance after understanding tax impact.
- No changes to risk profile — still moderate-conservative per IPS.
- Advisor will place trades by end of week.
- No change to beneficiary designations discussed.
        """,
        "good_note": """
Meeting Summary — Portfolio Rebalancing
Date: April 17, 2025 | Client: Patricia Nguyen | Advisor: Mark Torres, CFP

REBALANCING RATIONALE
Portfolio drifted to 78% equity following Q1 market rally, exceeding target allocation of 55/45 (equity/bond) by 23 percentage points. Rebalancing required to bring portfolio back in line with IPS.

SUITABILITY CONFIRMATION
- Risk Tolerance: Moderate-conservative (unchanged from IPS dated January 2025)
- Investment Objective: Capital preservation with income — confirmed still appropriate
- Income Need: Client confirmed no portfolio withdrawals needed for minimum 3 years (pension + Social Security fully covers living expenses)
- Suitability Basis: Rebalance from 78% to 55% equity is consistent with client's risk profile, time horizon, and liquidity needs. No change to IPS required.

TRADE RECOMMENDATION
- Sell: $85,000 in large-cap growth funds
- Buy: $85,000 in intermediate-term bond funds
- Tax Impact: Disclosed — approximately $12,000 in long-term capital gains liability. Client acknowledged and approved.

CLIENT DECISION
Patricia Nguyen approved rebalancing trade after advisor explained tax implications. Verbal consent obtained on call.

ACTION ITEMS
- [ ] Mark Torres: Execute rebalance trades by April 21, 2025 (end of week)
- [ ] Mark Torres: Send trade confirmation summary to client after execution

NO CHANGES
- Beneficiary designations: Not discussed, no changes
- Risk profile: Unchanged
        """,
        "bad_note": """
Rebalancing Call Notes
April 17, 2025 — Patricia Nguyen

Portfolio was out of balance so we discussed rebalancing. Patricia agreed to sell some equity funds and buy bonds. There will be some capital gains taxes.

Mark will place the trades this week.
        """,
    },
}
