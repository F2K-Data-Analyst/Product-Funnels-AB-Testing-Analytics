from __future__ import annotations
import pandas as pd
from .config import get_paths
from .io_utils import ensure_dir, save_csv

def run_eda(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    P = get_paths()
    ensure_dir(P.data_processed)

    out: dict[str, pd.DataFrame] = {}
    users = dfs.get("users", pd.DataFrame())
    sessions = dfs.get("sessions", pd.DataFrame())
    purchases = dfs.get("purchases", pd.DataFrame())

    if not users.empty and "country" in users.columns:
        df = users["country"].value_counts(dropna=False).reset_index()
        df.columns = ["country", "users"]
        out["users_by_country"] = df

    if not users.empty and "device" in users.columns:
        df = users["device"].value_counts(dropna=False).reset_index()
        df.columns = ["device", "users"]
        out["users_by_device"] = df

    if not users.empty and "acquisition_channel" in users.columns:
        df = users["acquisition_channel"].value_counts(dropna=False).reset_index()
        df.columns = ["acquisition_channel", "users"]
        out["users_by_acquisition_channel"] = df

    if not sessions.empty and "user_id" in sessions.columns:
        s_per_user = sessions.groupby("user_id").size().rename("sessions").reset_index()
        desc = s_per_user["sessions"].describe().to_frame().reset_index()
        desc.columns = ["metric", "value"]
        out["sessions_per_user_desc"] = desc

    if not purchases.empty and "revenue_amount" in purchases.columns:
        rev = purchases["revenue_amount"].dropna()
        desc = rev.describe().to_frame().reset_index()
        desc.columns = ["metric", "value"]
        out["revenue_amount_desc"] = desc

        if "user_id" in purchases.columns:
            rpu = purchases.groupby("user_id")["revenue_amount"].sum().rename("revenue_per_user").reset_index()
            rpu_desc = rpu["revenue_per_user"].describe().to_frame().reset_index()
            rpu_desc.columns = ["metric", "value"]
            out["revenue_per_user_desc"] = rpu_desc

    for name, df in out.items():
        save_csv(df, P.data_processed / f"02_eda_{name}.csv")

    return out