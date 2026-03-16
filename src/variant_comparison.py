from __future__ import annotations
import pandas as pd
import numpy as np
from .config import get_paths
from .io_utils import ensure_dir, save_csv

def compare_variants(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    P = get_paths()
    ensure_dir(P.data_processed)

    assignments = dfs.get("experiment_assignments", pd.DataFrame()).copy()
    purchases = dfs.get("purchases", pd.DataFrame()).copy()

    if assignments.empty or "user_id" not in assignments.columns:
        out = pd.DataFrame()
        save_csv(out, P.data_processed / "05_variant_summary.csv")
        return out

    variant_col = None
    for c in ["variant_id", "variant_name", "variant"]:
        if c in assignments.columns:
            variant_col = c
            break

    if variant_col is None:
        diag = pd.DataFrame({"assignments_columns": list(assignments.columns)})
        save_csv(diag, P.data_processed / "05_assignments_columns_debug.csv")
        out = pd.DataFrame()
        save_csv(out, P.data_processed / "05_variant_summary.csv")
        return out

    if not purchases.empty and "user_id" in purchases.columns:
        purchase_user = purchases.groupby("user_id").size().rename("purchase_count").reset_index()
        if "revenue_amount" in purchases.columns:
            rpu = purchases.groupby("user_id")["revenue_amount"].sum().rename("revenue").reset_index()
            purchase_user = purchase_user.merge(rpu, on="user_id", how="left")
        else:
            purchase_user["revenue"] = np.nan
    else:
        purchase_user = pd.DataFrame({"user_id": assignments["user_id"].unique(), "purchase_count": 0, "revenue": np.nan})

    ab = assignments[["user_id", variant_col]].drop_duplicates().merge(purchase_user, on="user_id", how="left")
    ab["purchase_count"] = ab["purchase_count"].fillna(0).astype(int)
    ab["purchased"] = (ab["purchase_count"] > 0).astype(int)

    summary = ab.groupby(variant_col).agg(
        users=("user_id", "nunique"),
        purchasers=("purchased", "sum"),
        conversion_rate=("purchased", "mean"),
        avg_revenue_per_user=("revenue", "mean"),
        total_revenue=("revenue", "sum"),
    ).reset_index().rename(columns={variant_col: "variant"})

    save_csv(summary, P.data_processed / "05_variant_summary.csv")
    save_csv(ab.rename(columns={variant_col: "variant"}), P.data_processed / "05_ab_user_level.csv")
    return summary