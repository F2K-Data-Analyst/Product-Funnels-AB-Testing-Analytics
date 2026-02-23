"""03_eda_analysis.py
Exploratory Data Analysis (EDA) for Product Analytics dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CLEAN_DIR = Path("data/clean")


def load_data():
    users = pd.read_csv(CLEAN_DIR / "users_clean.csv", parse_dates=["created_at"])
    sessions = pd.read_csv(CLEAN_DIR / "sessions_clean.csv", parse_dates=["started_at", "ended_at"])
    events = pd.read_csv(CLEAN_DIR / "events_clean.csv", parse_dates=["event_timestamp"])
    purchases = pd.read_csv(CLEAN_DIR / "purchases_clean.csv", parse_dates=["purchased_at"])
    return users, sessions, events, purchases


def plot_dau(events):
    events["date"] = events["event_timestamp"].dt.date
    dau = events.groupby("date")["user_id"].nunique()
    plt.figure()
    dau.plot(kind="bar")
    plt.title("Daily Active Users (DAU)")
    plt.xlabel("Date")
    plt.ylabel("Unique Users")
    plt.tight_layout()
    plt.show()


def country_distribution(users):
    country_counts = users["country"].value_counts()
    print("\nUsers by country:\n", country_counts)


def events_by_type(events):
    print("\nTop events:\n", events["event_name"].value_counts())


if __name__ == "__main__":
    users, sessions, events, purchases = load_data()
    country_distribution(users)
    events_by_type(events)
    plot_dau(events)
