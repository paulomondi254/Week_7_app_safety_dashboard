import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HSE Safety Dashboard", layout="wide")

# ---- Load data ----
# cached so it doesn't reload every time a filter changes
@st.cache_data
def load_data():
    df = pd.read_csv("safety_incidents_kenya.csv")
    df["incident_date"] = pd.to_datetime(df["incident_date"])
    return df

df = load_data()

st.title("HSE Safety Dashboard")
st.caption("Weekly view of site safety incidents")

# ---- Sidebar filters ----
st.sidebar.header("Filters")

sites = st.sidebar.multiselect(
    "Site / Location",
    options=sorted(df["site"].unique()),
    default=sorted(df["site"].unique())
)

types = st.sidebar.multiselect(
    "Incident Type",
    options=sorted(df["incident_type"].unique()),
    default=sorted(df["incident_type"].unique())
)

min_date = df["incident_date"].min()
max_date = df["incident_date"].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# handle case where user only picks one date
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# ---- Apply filters ----
filtered = df[
    (df["site"].isin(sites)) &
    (df["incident_type"].isin(types)) &
    (df["incident_date"] >= pd.to_datetime(start_date)) &
    (df["incident_date"] <= pd.to_datetime(end_date))
]

# ---- KPI metrics ----
total_incidents = len(filtered)
avg_severity = filtered["severity"].mean() if total_incidents > 0 else 0
critical_count = filtered["potential_sif"].sum() if total_incidents > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", total_incidents)

# color the severity metric red if it's getting high
severity_delta = "High" if avg_severity >= 2.5 else "OK"
col2.metric("Avg Severity", round(avg_severity, 2), delta=severity_delta,
            delta_color="inverse" if avg_severity >= 2.5 else "normal")

col3.metric("Critical Incidents (SIF)", int(critical_count))

# ---- Alert ----
CRITICAL_THRESHOLD = 10
if critical_count > CRITICAL_THRESHOLD:
    st.warning(f"⚠️ Critical incidents ({int(critical_count)}) exceed the threshold "
               f"of {CRITICAL_THRESHOLD}. Review high-risk sites below.")

st.divider()

# ---- Charts ----
left, right = st.columns(2)

with left:
    st.subheader("Incident Trend Over Time")
    trend = filtered.groupby(filtered["incident_date"].dt.date).size().reset_index(name="count")
    fig_trend = px.line(trend, x="incident_date", y="count", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with right:
    st.subheader("Incidents by Type")
    by_type = filtered["incident_type"].value_counts().reset_index()
    by_type.columns = ["incident_type", "count"]
    fig_bar = px.bar(by_type, x="incident_type", y="count")
    st.plotly_chart(fig_bar, use_container_width=True)

# map since we have lat/long for each site
st.subheader("Incident Locations")
if not filtered.empty:
    map_df = filtered[["latitude", "longitude", "site"]].dropna()
    st.map(map_df.rename(columns={"latitude": "lat", "longitude": "lon"}))
else:
    st.info("No data for the selected filters.")

# ---- Export ----
st.divider()
st.download_button(
    label="Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_safety_incidents.csv",
    mime="text/csv"
)
