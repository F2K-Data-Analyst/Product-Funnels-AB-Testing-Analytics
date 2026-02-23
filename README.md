# Product Funnels & A/B Testing Analytics

## Executive Summary
This project analyzes user behavior, funnel progression, and A/B testing outcomes using simulated product analytics data (20,000 users and 150,000+ events). The analysis identifies key funnel drop-offs and evaluates whether an experiment (Variant A vs Variant B) improves conversion and revenue.

---

## Business Context
The business operates a digital product platform with a multi-step purchase journey. Understanding where users drop off and which design changes improve conversions is critical for increasing revenue and improving the user experience.

---

## Dataset Overview
The dataset includes the following CSV tables:

- `users.csv` — user attributes (country, device, acquisition_channel, sign_up_date)
- `sessions.csv` — product/session event data (user_id, event_name, timestamp, etc.)
- `purchases.csv` — transactions/revenue (user_id, purchase_timestamp, revenue_amount, etc.)
- `funnels.csv`, `funnel_steps.csv` — funnel definitions and step mapping
- `experiments.csv`, `experiment_variants.csv`, `experiment_assignments.csv` — A/B test setup
- `devices.csv`, `error_events.csv` — supporting reference + friction signals (optional)

---

## Methodology (Steps 1–8)
1. **Data Load & Cleaning**: standardized schemas, parsed timestamps, removed duplicates, validated joins  
2. **EDA**: user distribution by country/device/channel, sessions per user, revenue distribution  
3. **Funnel Construction**: built a user-level funnel reach table and funnel step counts  
4. **Conversion Rates**: calculated conversion from start, step-to-step conversion, and drop-off rates  
5. **Variant Comparison**: compared conversion and revenue metrics by experiment variant  
6. **Statistical Testing**: two-proportion z-test for conversion + confidence intervals (and revenue test when available)  
7. **Business Insights**: summarized key opportunities and recommendations  
8. **Visualizations**: saved funnel + A/B charts into `reports/figures/`

---

## Key Results
- **Largest funnel drop-off step:** [fill in step] — drop-off ≈ [fill in %]
- **Winning variant (conversion):** [fill in variant] — conversion ≈ [fill in %]
- **Uplift (B − A):** [fill in uplift %]
- **p-value:** [fill in p-value]
- **Decision:** [Statistically significant / Not significant → next steps]

---

## Visualizations
![Funnel Users](reports/figures/funnel_users_by_step.png)
![Funnel Conversion](reports/figures/funnel_conversion_from_start.png)
![A/B Conversion](reports/figures/ab_conversion_by_variant.png)

---

## How to Run (VS Code / Windows)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.run_all
