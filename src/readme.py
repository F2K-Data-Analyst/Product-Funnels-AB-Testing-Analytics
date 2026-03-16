from __future__ import annotations
import pandas as pd
from .config import get_paths

def write_readme(conversion_df: pd.DataFrame, variant_summary: pd.DataFrame, stats_df: pd.DataFrame) -> str:
    P = get_paths()

    funnel_note = ""
    if conversion_df is not None and not conversion_df.empty and "users" in conversion_df.columns:
        funnel_note = f"Top-of-funnel users: **{int(conversion_df['users'].iloc[0])}**"

    ab_note = ""
    if variant_summary is not None and not variant_summary.empty and "conversion_rate" in variant_summary.columns:
        best = variant_summary.sort_values("conversion_rate", ascending=False).head(1).iloc[0]
        ab_note = f"Best variant by conversion: **{best['variant']}** (CR: **{float(best['conversion_rate']):.2%}**)"

    stats_note = ""
    if stats_df is not None and not stats_df.empty and "p_value" in stats_df.columns:
        row = stats_df.iloc[0]
        stats_note = f"p-value: **{float(row['p_value']):.4f}**, uplift (B − A): **{float(row.get('uplift_B_minus_A', 0.0)):.2%}**"

    readme = f"""# Product Funnels & A/B Testing Analytics

## Executive Summary
This project analyzes user behavior, funnel progression, and A/B testing outcomes using product analytics data. It identifies key drop-off points, compares experiment variants, and provides actionable product recommendations.

## Business Problem
Where do users drop off in the purchase journey, and does a UI experiment (A vs B) improve conversion or revenue?

## Dataset
CSV tables include: users, sessions/events, purchases, funnels/funnel_steps, experiments, experiment_variants, experiment_assignments, and supporting reference tables.

## Methodology
1. Data Load & Cleaning  
2. Exploratory Data Analysis  
3. Funnel Construction  
4. Conversion Rates  
5. Variant Comparison  
6. Statistical Testing  
7. Business Insights  
8. Visualizations  
9. Documentation (README)

## Key Results (From This Run)
- {funnel_note}
- {ab_note}
- {stats_note}

## Visualizations
![Funnel Users](reports/figures/funnel_users_by_step.png)  
![Funnel Conversion](reports/figures/funnel_conversion_from_start.png)  
![A/B Conversion](reports/figures/ab_conversion_by_variant.png)

## How to Run
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.run_all