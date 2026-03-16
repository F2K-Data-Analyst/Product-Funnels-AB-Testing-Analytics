from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from .config import get_paths
from .io_utils import ensure_dir

def make_charts(
    funnel_counts: pd.DataFrame,
    conversion_df: pd.DataFrame,
    variant_summary: pd.DataFrame
) -> dict[str, str]:
    P = get_paths()
    ensure_dir(P.reports_figures)

    outputs: dict[str, str] = {}

    # Funnel users bar chart
    if funnel_counts is not None and not funnel_counts.empty:
        plt.figure()
        plt.bar(funnel_counts["step"].astype(str), funnel_counts["users"])
        plt.title("Funnel Users by Step")
        plt.xlabel("Step")
        plt.ylabel("Unique Users")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = P.reports_figures / "funnel_users_by_step.png"
        plt.savefig(path)
        plt.close()
        outputs["funnel_users_by_step"] = str(path)

    # Conversion from start (line)
    if conversion_df is not None and not conversion_df.empty and "conversion_from_start" in conversion_df.columns:
        plt.figure()
        plt.plot(conversion_df["step"].astype(str), conversion_df["conversion_from_start"])
        plt.title("Funnel Conversion from Start")
        plt.xlabel("Step")
        plt.ylabel("Conversion Rate")
        plt.ylim(0, 1)  # <-- helps readability
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = P.reports_figures / "funnel_conversion_from_start.png"
        plt.savefig(path)
        plt.close()
        outputs["funnel_conversion_from_start"] = str(path)

    # Variant conversion bar chart
    if variant_summary is not None and not variant_summary.empty and "conversion_rate" in variant_summary.columns:
        plt.figure()
        plt.bar(variant_summary["variant"].astype(str), variant_summary["conversion_rate"])
        plt.title("Conversion Rate by Variant")
        plt.xlabel("Variant")
        plt.ylabel("Conversion Rate")
        plt.ylim(0, 1)  # <-- helps readability
        plt.tight_layout()
        path = P.reports_figures / "ab_conversion_by_variant.png"
        plt.savefig(path)
        plt.close()
        outputs["ab_conversion_by_variant"] = str(path)

    return outputs