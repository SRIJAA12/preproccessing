# Prepayment Control & Portfolio Retention
### Idea Olympics 2026 — Team: Portfolio Protectors

> **"வரும்முன் காப்போம்"** — Prevention is better than cure.

---

## Overview

A Streamlit prototype demonstrating a **business process simulator** for proactive prepayment control. The application identifies early warning signals and guides the RM through structured retention conversations — before the customer reaches closure intent.

---

## Quick Start

```bash
cd prepayment_demo
pip install -r requirements.txt
streamlit run app.py
```

---

## Screens

| Screen | Description |
|--------|-------------|
| **Home — Prepayment Snapshot** | Company KPI cards (YTD Rs.1,727 Cr, 158% of budget), Tamil tagline, workflow diagram |
| **Early Warning List** | Filterable table of ~25 synthetic customers with colour-coded risk rows |
| **Customer Retention Action** | Per-customer profile, trigger analysis, category-specific action panels, action recording |
| **Management Summary** | KPI cards, 5 Plotly charts, branch-wise periodical review table |

---

## Demo Customers

| Customer | Branch | Outstanding | Scenario |
|----------|--------|-------------|----------|
| **Arun Kumar** | Madurai | Rs.38 L | Balance Transfer — bureau alert + foreclosure enquiry + competitor quote |
| **Meena R** | Sivakasi | Rs.25 L | Own Funds — partial prepayment simulation (Rs.15 L retained) |
| **Suresh P** | Chennai | Rs.32 L | Service Issue — documentation delay, resolved via escalation |

---

## File Structure

```
prepayment_demo/
├── app.py              # Main Streamlit application (all screens)
├── data/
│   └── customers.csv   # Synthetic customer dataset (~25 customers)
├── requirements.txt    # streamlit, pandas, plotly
└── README.md           # This file
```

---

## Technology

- **Python** + **Streamlit** — UI and navigation
- **Pandas** — Data handling
- **Plotly** — Interactive charts
- **Rule-based logic** — Simple trigger rules for risk assignment
- **CSV** — Synthetic customer data (no database required)

---

## Important Notes

- This is a **business process simulator**, not an AI prediction product.
- No machine learning, model training, or external APIs are used.
- No login, cloud services, or real customer data.
- Investment options shown are for workflow demonstration only and must follow company policy.

---

*Demo duration: 3–5 minutes | Idea Olympics 2026*
