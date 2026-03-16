from __future__ import annotations
import pandas as pd
from .config import get_paths
from .io_utils import ensure_dir, save_csv

DEFAULT_FUNNEL_STEPS = ["product_view", "add_to_cart", "checkout", "purchase"]

def _get_steps_from_tables(dfs: dict[str, pd.DataFrame]) -> list[str]:
    steps_df = dfs.get("funnel_steps", pd.DataFrame())
    if steps_df.empty:
        return DEFAULT_FUNNEL_STEPS

    if "event_name" in steps_df.columns:
        if "step_number" in steps_df.columns:
            steps_df = steps_df.sort_values("step_number")
        return steps_df["event_name"].dropna().astype(str).tolist()

    # If your funnel_steps table uses different column names, fallback:
    for alt in ["step", "step_name", "event", "name"]:
        if alt in steps_df.columns:
            return steps_df[alt].dropna().astype(str).tolist()

    return DEFAULT_FUNNEL_STEPS

def build_funnel(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    P = get_paths()
    ensure_dir(P.data_processed)

    sessions = dfs.get("sessions", pd.DataFrame()).copy()
    steps = _get_steps_from_tables(dfs)

    if sessions.empty:
        out = {"funnel_counts": pd.DataFrame({"step": steps, "users": [0]*len(steps)}), "funnel_user_level": pd.DataFrame()}
        save_csv(out["funnel_counts"], P.data_processed / "03_funnel_counts.csv")
        return out

    if "user_id" not in sessions.columns or "event_name" not in sessions.columns:
        # Diagnostic output to help you map correct columns
        diag = pd.DataFrame({"sessions_columns": list(sessions.columns)})
        save_csv(diag, P.data_processed / "03_funnel_sessions_columns_debug.csv")
        out = {"funnel_counts": pd.DataFrame({"step": steps, "users": [0]*len(steps)}), "funnel_user_level": pd.DataFrame()}
        save_csv(out["funnel_counts"], P.data_processed / "03_funnel_counts.csv")
        return out

    sessions = sessions.dropna(subset=["user_id", "event_name"])
    sessions["event_name"] = sessions["event_name"].astype(str)

    user_level = pd.DataFrame({"user_id": sessions["user_id"].unique()})
    for step in steps:
        reached = sessions.loc[sessions["event_name"] == step, "user_id"].unique()
        user_level[f"reached_{step}"] = user_level["user_id"].isin(reached)

    funnel_counts = pd.DataFrame({
        "step": steps,
        "users": [int(user_level[f"reached_{s}"].sum()) for s in steps]
    })

    save_csv(user_level, P.data_processed / "03_funnel_user_level.csv")
    save_csv(funnel_counts, P.data_processed / "03_funnel_counts.csv")
    return {"funnel_counts": funnel_counts, "funnel_user_level": user_level}