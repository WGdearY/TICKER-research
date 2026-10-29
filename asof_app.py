"""
asof_app.py — Lab 17: Point-in-Time Audit (FRED-style rates app)
FIN 43900 — AI in Finance, Fall 2026 | Week 10 (Thursday)
Author: Will Gao (gao713@purdue.edu)

Data from FRED and ALFRED, Federal Reserve Bank of St. Louis;
built with AI help, a learning demonstration, not investment advice.

Run:  streamlit run asof_app.py
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import StringIO
import urllib.request


# ---------------------------------------------------------------------------
# DATA DOWNLOAD FUNCTIONS (cached)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fred(series_id: str, start_date: str) -> pd.DataFrame:
    """Download current-vintage data from FRED's public CSV endpoint."""
    url = (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}&cosd={start_date}"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"FRED download failed for {series_id}: {e}")

    df = pd.read_csv(StringIO(raw))
    col = [c for c in df.columns if c != "DATE"][0]
    df.rename(columns={"DATE": "date", col: "value"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df.dropna(subset=["value"], inplace=True)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_alfred(series_id: str, vintage_date: str, start_date: str) -> pd.DataFrame:
    """Download as-known-on data from ALFRED's public CSV endpoint."""
    url = (
        f"https://alfred.stlouisfed.org/graph/alfredgraph.csv"
        f"?id={series_id}&vintage_date={vintage_date}&cosd={start_date}"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"ALFRED download failed for {series_id}: {e}")

    df = pd.read_csv(StringIO(raw))
    col = [c for c in df.columns if c != "DATE"][0]
    df.rename(columns={"DATE": "date", col: "value"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df.dropna(subset=["value"], inplace=True)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# SERIES CATALOG
# ---------------------------------------------------------------------------

DEFAULT_SERIES = {
    "BAA":          "Moody's Baa corporate bond yield",
    "FEDFUNDS":     "Federal funds rate",
    "DGS10":        "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


# ---------------------------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Point-in-Time Rate Audit", layout="wide")
st.title("Point-in-Time Rate Audit")
st.caption(
    "Data from [FRED](https://fred.stlouisfed.org) and "
    "[ALFRED](https://alfred.stlouisfed.org), Federal Reserve Bank of St. Louis, "
    f"downloaded {date.today().isoformat()}; built with AI help, a learning "
    "demonstration, not investment advice."
)

# ---- Sidebar ----
st.sidebar.header("Controls")

selected = st.sidebar.multiselect(
    "Series",
    options=list(DEFAULT_SERIES.keys()),
    default=list(DEFAULT_SERIES.keys()),
    format_func=lambda s: f"{s} — {DEFAULT_SERIES[s]}",
)

extra_id = st.sidebar.text_input("Add another FRED series ID", "").strip().upper()
if extra_id and extra_id not in selected:
    selected.append(extra_id)

start_date = st.sidebar.date_input("Start date", date(2020, 1, 1))
asof_date = st.sidebar.date_input("As known on", date.today())

start_str = start_date.isoformat()
asof_str = asof_date.isoformat()

# ---- Fetch & display ----
summary_rows = []

for sid in selected:
    label = DEFAULT_SERIES.get(sid, sid)
    try:
        df_today = fetch_fred(sid, start_str)
        df_asof = fetch_alfred(sid, asof_str, start_str)
    except RuntimeError as e:
        st.error(str(e))
        continue

    # --- Chart: today's values ---
    st.subheader(f"{sid} — {label}")
    chart_df = df_today.set_index("date")[["value"]].rename(columns={"value": sid})
    st.line_chart(chart_df)

    # --- As-known-on info ---
    if df_asof.empty:
        st.info(f"No ALFRED data for {sid} on {asof_str}.")
        continue

    last_asof_date = df_asof["date"].max()
    last_asof_val  = df_asof.loc[df_asof["date"] == last_asof_date, "value"].iloc[0]

    last_today_date = df_today["date"].max()
    last_today_val  = df_today.loc[df_today["date"] == last_today_date, "value"].iloc[0]

    # Count of values in today's data AFTER the last date known then
    after_count = int((df_today["date"] > last_asof_date).sum())

    # Count of revised values: same dates, different values
    merged = df_asof.merge(df_today, on="date", suffixes=("_asof", "_today"))
    revised_count = int((merged["value_asof"] != merged["value_today"]).sum())

    st.caption(
        f"Last date known on {asof_str}: **{last_asof_date.strftime('%Y-%m-%d')}** "
        f"= **{last_asof_val}**"
    )

    fred_link = f"https://fred.stlouisfed.org/series/{sid}"

    summary_rows.append({
        "Series": f"[{sid}]({fred_link})",
        "Last date (as known)": last_asof_date.strftime("%Y-%m-%d"),
        "Value (as known)": last_asof_val,
        "Last date (today)": last_today_date.strftime("%Y-%m-%d"),
        "Value (today)": last_today_val,
        "New values after known": after_count,
        "Revised since": revised_count,
    })

# ---- Summary table ----
if summary_rows:
    st.markdown("---")
    st.subheader("Summary: Today vs. As Known On")
    st.markdown(pd.DataFrame(summary_rows).to_markdown(index=False))
