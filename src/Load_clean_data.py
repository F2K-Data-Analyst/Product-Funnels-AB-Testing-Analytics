from __future__ import annotations
import pandas as pd
from .config import get_paths, RAW_FILES
from .io_utils import ensure_dir, read_csv_safe, save_parquet, save_csv

def _parse_datetime_if_exists(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def _dedupe(df: pd.DataFrame, key_cols: list[str] | None = None) -> pd.DataFrame:
    df = df.copy()
    before = len(df)
    if key_cols and all(c in df.columns for c in key_cols):
        df = df.drop_duplicates(subset=key_cols)
    else:
        df = df.drop_duplicates()
    df.attrs["deduped_rows"] = before - len(df)
    return df

def load_and_clean_all() -> dict[str, pd.DataFrame]:
    P = get_paths()
    ensure_dir(P.data_processed)

    dfs: dict[str, pd.DataFrame] = {}
    for name, fname in RAW_FILES.items():
        fpath = P.data_raw / fname
        if fpath.exists():
            dfs[name] = read_csv_safe(fpath)
        else:
            dfs[name] = pd.DataFrame()

    if not dfs["users"].empty:
        dfs["users"] = _parse_datetime_if_exists(dfs["users"], ["sign_up_date"])
        dfs["users"] = _dedupe(dfs["users"], ["user_id"])

    if not dfs["sessions"].empty:
        dfs["sessions"] = _parse_datetime_if_exists(dfs["sessions"], ["session_start", "session_end", "timestamp"])
        dfs["sessions"] = _dedupe(dfs["sessions"], ["session_id"])

    if not dfs["purchases"].empty:
        dfs["purchases"] = _parse_datetime_if_exists(dfs["purchases"], ["purchase_timestamp", "timestamp"])
        if "revenue_amount" in dfs["purchases"].columns:
            dfs["purchases"]["revenue_amount"] = pd.to_numeric(dfs["purchases"]["revenue_amount"], errors="coerce")
        dfs["purchases"] = _dedupe(dfs["purchases"], ["purchase_id"])

    if not dfs["experiment_assignments"].empty:
        dfs["experiment_assignments"] = _parse_datetime_if_exists(
            dfs["experiment_assignments"], ["assignment_timestamp", "timestamp"]
        )
        if "experiment_id" in dfs["experiment_assignments"].columns:
            dfs["experiment_assignments"] = _dedupe(dfs["experiment_assignments"], ["user_id", "experiment_id"])
        else:
            dfs["experiment_assignments"] = _dedupe(dfs["experiment_assignments"], ["user_id"])

    report_rows = []
    for name, df in dfs.items():
        if df.empty:
            report_rows.append({"table": name, "rows": 0, "cols": 0, "notes": "missing or empty"})
        else:
            notes = []
            if "deduped_rows" in getattr(df, "attrs", {}):
                notes.append(f"deduped={df.attrs['deduped_rows']}")
            report_rows.append({"table": name, "rows": len(df), "cols": df.shape[1], "notes": "; ".join(notes)})

    report = pd.DataFrame(report_rows).sort_values("table")

    for name, df in dfs.items():
        if not df.empty:
            save_parquet(df, P.data_processed / f"{name}_clean.parquet")

    save_csv(report, P.data_processed / "01_load_clean_report.csv")
    return dfs