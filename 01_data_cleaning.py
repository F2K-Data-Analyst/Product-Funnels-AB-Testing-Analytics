"""01_data_cleaning.py
Data cleaning and preparation for Product Analytics project.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean"))
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def parse_dates(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
    return df

def load_and_clean_users():
    df = pd.read_csv(DATA_DIR / "users.csv")
    df = parse_dates(df, ["created_at"])
    df["country"] = df["country"].fillna("Unknown")
    df.to_csv(CLEAN_DIR / "users_clean.csv", index=False)
    return df

def load_and_clean_sessions():
    df = pd.read_csv(DATA_DIR / "sessions.csv")
    df = parse_dates(df, ["started_at", "ended_at"])
    df["session_duration_min"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60
    df.to_csv(CLEAN_DIR / "sessions_clean.csv", index=False)
    return df

def load_and_clean_events():
    df = pd.read_csv(DATA_DIR / "events.csv")
    df = parse_dates(df, ["event_timestamp"])
    df.to_csv(CLEAN_DIR / "events_clean.csv", index=False)
    return df

def load_and_clean_purchases():
    df = pd.read_csv(DATA_DIR / "purchases.csv")
    df = parse_dates(df, ["purchased_at"])
    df.to_csv(CLEAN_DIR / "purchases_clean.csv", index=False)
    return df

def load_and_clean_error_events():
    df = pd.read_csv(DATA_DIR / "error_events.csv")
    df = parse_dates(df, ["occurred_at"])
    df.to_csv(CLEAN_DIR / "error_events_clean.csv", index=False)
    return df

if __name__ == "__main__":
    print("Cleaning users...")
    load_and_clean_users()
    print("Cleaning sessions...")
    load_and_clean_sessions()
    print("Cleaning events...")
    load_and_clean_events()
    print("Cleaning purchases...")
    load_and_clean_purchases()
    print("Cleaning error events...")
    load_and_clean_error_events()
    print("Done.")
