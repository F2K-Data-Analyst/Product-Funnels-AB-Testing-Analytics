from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    project_root: Path
    data_raw: Path
    data_processed: Path
    reports_figures: Path
    reports_summary: Path

def get_paths() -> Paths:
    root = Path(__file__).resolve().parents[1]
    return Paths(
        project_root=root,
        data_raw=root / "data" / "raw",
        data_processed=root / "data" / "processed",
        reports_figures=root / "reports" / "figures",
        reports_summary=root / "reports" / "summary",
    )

RAW_FILES = {
    "users": "users.csv",
    "sessions": "sessions.csv",
    "purchases": "purchases.csv",
    "products": "products.csv",
    "funnels": "funnels.csv",
    "funnel_steps": "funnel_steps.csv",
    "experiments": "experiments.csv",
    "experiment_variants": "experiment_variants.csv",
    "experiment_assignments": "experiment_assignments.csv",
    "devices": "devices.csv",
    "error_events": "error_events.csv",
}

# IMPORTANT: keys should be lowercase + underscoreless
COLUMN_ALIASES = {
    # identifiers
    "userid": "user_id",
    "sessionid": "session_id",
    "purchaseid": "purchase_id",
    "productid": "product_id",
    "eventid": "event_id",
    "experimentid": "experiment_id",

    # timestamps
    "time": "timestamp",
    "datetime": "timestamp",
    "eventtime": "timestamp",
    "eventtimestamp": "timestamp",
    "sessionstarttime": "session_start",
    "sessionendtime": "session_end",
    "purchasetimestamp": "purchase_timestamp",
    "assignmenttimestamp": "assignment_timestamp",

    # event name
    "event": "event_name",
    "eventname": "event_name",
    "name": "event_name",

    # variant
    "variant": "variant_name",
    "variantid": "variant_id",

    # revenue
    "amount": "revenue_amount",
    "revenue": "revenue_amount",
    "revenueamount": "revenue_amount",
    "price": "revenue_amount",
}
# %%
