from __future__ import annotations
import pandas as pd
from .config import get_paths
from .io_utils import ensure_dir, save_csv

def compute_conversion(funnel_counts: pd.DataFrame) -> pd.DataFrame:
    P = get_paths()
    ensure_dir(P.data_processed)

    df = funnel_counts.copy()
    if df.empty or "users" not in df.columns:
        return df

    df["users"] = pd.to_numeric(df["users"], errors="coerce").fillna(0).astype(int)
    first = int(df["users"].iloc[0]) if len(df) else 0

    df["conversion_from_start"] = (df["users"] / first) if first > 0 else 0.0
    df["step_to_step_conversion"] = df["users"] / df["users"].shift(1)
    df.loc[df["users"].shift(1) == 0, "step_to_step_conversion"] = 0.0

    df["drop_off_rate"] = 1 - df["step_to_step_conversion"]
    df.loc[df["users"].shift(1) == 0, "drop_off_rate"] = 0.0

    save_csv(df, P.data_processed / "04_funnel_conversion_rates.csv")
    return df