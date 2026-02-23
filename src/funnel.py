#%%
import pandas as pd
# %%
def build_funnel(events_df, funnel_steps):
    """
    Build user-level funnel completion table.
    Returns boolean DataFrame (user_id x funnel_step).
    """
    
    # Filter only relevant steps once
    filtered = events_df[events_df["event_name"].isin(funnel_steps)]
    
    # Create pivot table
    funnel_df = (
        filtered
        .assign(completed=True)
        .pivot_table(
            index="user_id",
            columns="event_name",
            values="completed",
            aggfunc="any",
            fill_value=False
        )
    )
    # Ensure all funnel steps appear (even if missing in data)
    for step in funnel_steps:
        if step not in funnel_df.columns:
            funnel_df[step] = False

    return funnel_df[funnel_steps]
# %%
def funnel_conversion(funnel_df):
    total_users = len(funnel_df)
    
    results = []
    for step in funnel_df.columns:
        completed = funnel_df[step].sum()
        conversion_rate = completed / total_users
        results.append((step, completed, conversion_rate))
    
    return pd.DataFrame(results, columns=["step", "users", "conversion_rate"])
# %%
