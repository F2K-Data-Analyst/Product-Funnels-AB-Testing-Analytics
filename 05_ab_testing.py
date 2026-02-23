"""05_ab_testing.py
A/B testing analysis for experiment variants.
"""

import pandas as pd
from pathlib import Path
from scipy import stats

CLEAN_DIR = Path("data/clean")


def load_ab_data():
    events = pd.read_csv(CLEAN_DIR / "events_clean.csv", parse_dates=["event_timestamp"])
    purchases = pd.read_csv(CLEAN_DIR / "purchases_clean.csv", parse_dates=["purchased_at"])
    assignments = pd.read_csv("data/raw/experiment_assignments.csv", parse_dates=["assigned_at"])
    variants = pd.read_csv("data/raw/experiment_variants.csv")
    return events, purchases, assignments, variants


def compute_conversion(purchases, assignments):
    df = assignments.merge(purchases[["user_id", "purchase_id"]], on="user_id", how="left", indicator=True)
    df["converted"] = (df["_merge"] == "both").astype(int)
    conv = df.groupby("variant_id")["converted"].agg(["mean", "sum", "count"]).reset_index()
    conv.rename(columns={"mean": "conversion_rate", "sum": "conversions", "count": "users"}, inplace=True)
    return conv


def run_ab_test(conv):
    v1, v2 = conv["variant_id"].unique()
    d1 = conv.loc[conv["variant_id"] == v1].iloc[0]
    d2 = conv.loc[conv["variant_id"] == v2].iloc[0]

    conv1 = d1["conversion_rate"]
    conv2 = d2["conversion_rate"]
    n1 = d1["users"]
    n2 = d2["users"]

    successes = [d1["conversions"], d2["conversions"]]
    nobs = [n1, n2]

    stat, pval = stats.proportions_ztest(successes, nobs)
    return {
        "variant_1": int(v1),
        "variant_2": int(v2),
        "conversion_1": conv1,
        "conversion_2": conv2,
        "z_stat": stat,
        "p_value": pval
    }


if __name__ == "main__":
    events, purchases, assignments, variants = load_ab_data()
    conv = compute_conversion(purchases, assignments)
    print(conv)
    test_result = run_ab_test(conv)
    print("\nA/B test result:\n", test_result)
