from __future__ import annotations
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats as scipy_stats
from .config import get_paths
from .io_utils import ensure_dir, save_csv

def _diff_ci(p1: float, n1: int, p2: float, n2: int, alpha: float = 0.05):
    diff = p2 - p1
    if n1 <= 0 or n2 <= 0:
        return diff, np.nan, np.nan
    se = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
    z = scipy_stats.norm.ppf(1 - alpha/2)
    return diff, diff - z*se, diff + z*se

def run_stats(ab_user_level: pd.DataFrame) -> pd.DataFrame:
    P = get_paths()
    ensure_dir(P.data_processed)

    if ab_user_level.empty or "variant" not in ab_user_level.columns:
        out = pd.DataFrame([{"note": "Missing AB user-level data or 'variant' column."}])
        save_csv(out, P.data_processed / "06_ab_stats_results.csv")
        return out

    variants = list(ab_user_level["variant"].dropna().unique())
    if len(variants) != 2:
        out = pd.DataFrame([{"note": f"Expected 2 variants, found {len(variants)}: {variants}"}])
        save_csv(out, P.data_processed / "06_ab_stats_results.csv")
        return out

    A, B = variants[0], variants[1]
    gA = ab_user_level[ab_user_level["variant"] == A]
    gB = ab_user_level[ab_user_level["variant"] == B]

    sA = int(gA["purchased"].sum())
    nA = int(gA["user_id"].nunique())
    sB = int(gB["purchased"].sum())
    nB = int(gB["user_id"].nunique())

    pA = sA / nA if nA else 0.0
    pB = sB / nB if nB else 0.0

    z_stat, pval = proportions_ztest(count=np.array([sA, sB]), nobs=np.array([nA, nB]))
    diff, lo, hi = _diff_ci(pA, nA, pB, nB)

    revenue_test = {}
    if "revenue" in ab_user_level.columns and ab_user_level["revenue"].notna().any():
        rA = gA["revenue"].fillna(0.0).astype(float)
        rB = gB["revenue"].fillna(0.0).astype(float)
        t_stat, t_p = scipy_stats.ttest_ind(rA, rB, equal_var=False)
        revenue_test = {"rev_mean_A": float(rA.mean()), "rev_mean_B": float(rB.mean()), "rev_t_stat": float(t_stat), "rev_p_value": float(t_p)}
    else:
        revenue_test = {"rev_note": "Revenue column missing or all null; skipped revenue test."}

    out = pd.DataFrame([{
        "variant_A": A,
        "variant_B": B,
        "users_A": nA,
        "users_B": nB,
        "purchasers_A": sA,
        "purchasers_B": sB,
        "conversion_A": pA,
        "conversion_B": pB,
        "uplift_B_minus_A": (pB - pA),
        "z_stat": float(z_stat),
        "p_value": float(pval),
        "diff_ci_low": float(lo) if lo == lo else np.nan,
        "diff_ci_high": float(hi) if hi == hi else np.nan,
        **revenue_test
    }])

    save_csv(out, P.data_processed / "06_ab_stats_results.csv")
    return out