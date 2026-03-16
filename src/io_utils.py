from __future__ import annotations
from pathlib import Path
import pandas as pd

from .config import COLUMN_ALIASES

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # standardize column labels (keep original for mapping, but normalize safely)
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]

    rename_map = {}
    for c in df.columns:
        key = c.replace("_", "").lower()  # <-- critical fix
        if key in COLUMN_ALIASES:
            rename_map[c] = COLUMN_ALIASES[key]

    df = df.rename(columns=rename_map)
    df.columns = [c.lower() for c in df.columns]
    return df

def read_csv_safe(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_columns(df)

def save_parquet(df: pd.DataFrame, path: Path) -> None:
    df.to_parquet(path, index=False)

def save_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)