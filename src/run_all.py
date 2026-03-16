from __future__ import annotations
import pandas as pd
from .config import get_paths
from .io_utils import ensure_dir
from .Load_clean_data import load_and_clean_all
from .Exploratory_Data_Analysis import run_eda
from .funnel import build_funnel
from .conversion import compute_conversion
from .variant_comparison import compare_variants
from .stats import run_stats
from .insights import write_insights
from .charts import make_charts
from .readme import write_readme

def main():
    P = get_paths()
    ensure_dir(P.data_processed)
    ensure_dir(P.reports_figures)
    ensure_dir(P.reports_summary)

    dfs = load_and_clean_all()
    run_eda(dfs)

    funnel_out = build_funnel(dfs)
    funnel_counts = funnel_out["funnel_counts"]

    conversion_df = compute_conversion(funnel_counts)
    variant_summary = compare_variants(dfs)

    ab_user_level_path = P.data_processed / "05_ab_user_level.csv"
    ab_user_level = pd.read_csv(ab_user_level_path) if ab_user_level_path.exists() else pd.DataFrame()

    stats_df = run_stats(ab_user_level)

    write_insights(conversion_df, variant_summary, stats_df)
    make_charts(funnel_counts, conversion_df, variant_summary)
    write_readme(conversion_df, variant_summary, stats_df)

    print("✅ Pipeline complete.")
    print("Check outputs in:")
    print("- data/processed/")
    print("- reports/figures/")
    print("- reports/summary/")
    print("- README.md")

if __name__ == "__main__":
    main()