from __future__ import annotations
import pandas as pd
from .config import get_paths
from .io_utils import ensure_dir

def write_insights(conversion_df: pd.DataFrame, variant_summary: pd.DataFrame, stats_df: pd.DataFrame) -> str:
    P = get_paths()
    ensure_dir(P.reports_summary)

    lines: list[str] = []
    lines.append("# Insights & Recommendations\n")

    if conversion_df is not None and not conversion_df.empty and "drop_off_rate" in conversion_df.columns and len(conversion_df) > 1:
        worst = conversion_df.iloc[1:].sort_values("drop_off_rate", ascending=False).head(1)
        if not worst.empty:
            step = worst["step"].iloc[0]
            drop = float(worst["drop_off_rate"].iloc[0])
            lines.append("## Funnel Insights\n")
            lines.append(f"- **Largest drop-off step:** `{step}` with drop-off rate ≈ **{drop:.1%}**.\n")

    if variant_summary is not None and not variant_summary.empty and "conversion_rate" in variant_summary.columns:
        best = variant_summary.sort_values("conversion_rate", ascending=False).head(1)
        if not best.empty:
            v = best["variant"].iloc[0]
            cr = float(best["conversion_rate"].iloc[0])
            lines.append("## Experiment Snapshot\n")
            lines.append(f"- **Top variant by conversion:** `{v}` with conversion rate ≈ **{cr:.2%}**.\n")

    if stats_df is not None and not stats_df.empty and "p_value" in stats_df.columns:
        row = stats_df.iloc[0]
        p = float(row["p_value"])
        uplift = float(row.get("uplift_B_minus_A", 0.0))
        lines.append("## Statistical Conclusion\n")
        lines.append(f"- **Uplift (B − A):** **{uplift:.2%}**\n")
        lines.append(f"- **p-value:** **{p:.4f}**\n")
        lines.append("- Result is **statistically significant** at α=0.05.\n" if p < 0.05 else "- Result is **not statistically significant** at α=0.05.\n")

    lines.append("## Recommendations\n")
    lines.append("- Fix the highest drop-off step (UX, clarity, speed, form friction).\n")
    lines.append("- Segment by device/country/channel to find the strongest opportunities.\n")
    lines.append("- If experiment is significant, ship winner and monitor post-release metrics.\n")

    out_path = P.reports_summary / "insights.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return str(out_path)