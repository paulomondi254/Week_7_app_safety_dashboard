"""
Safety Command Center Dashboard - Smart Column Detection
Auto-detects date, site, shift, type, and location columns.
Fully compatible with your safety_incidents.csv structure.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Safety Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- SMART DATA LOADING (CACHED) --------------------
@st.cache_data(ttl=3600)
def load_data():
    """
    Loads HSE incident data from data/safety_incidents.csv.
    Automatically detects:
    - Date column (any column that parses as datetime)
    - Time column (combines with date if found)
    - Site/Location column
    - Shift column
    - Incident Type column
    - Latitude & Longitude columns
    """
    file_path = "data/safety_incidents.csv"
    
    if not os.path.exists(file_path):
        st.warning(f"File '{file_path}' not found. Using synthetic data for demo.")
        return generate_synthetic_data()
    
    # Try to read with auto-delimiter detection
    try:
        # Detect delimiter
        with open(file_path, 'r') as f:
            first_line = f.readline()
        if '\t' in first_line:
            delimiter = '\t'
        elif ';' in first_line:
            delimiter = ';'
        else:
            delimiter = ','
        
        df = pd.read_csv(file_path, delimiter=delimiter)
    except Exception as e:
        st.error(f"Error reading CSV: {e}. Using synthetic data.")
        return generate_synthetic_data()
    
    # ---------- AUTO-DETECT DATE COLUMN ----------
    date_col = None
    for col in df.columns:
        try:
            # Check if at least 50% of values can be parsed as dates
            parsed = pd.to_datetime(df[col], errors='coerce')
            if parsed.notna().sum() > len(df) * 0.5:
                date_col = col
                break
        except:
            continue
    
    if date_col is None:
        st.error("Could not auto-detect a date column. Please ensure your CSV has a date field.")
        st.stop()
    
    # Rename to 'date' and parse
    df.rename(columns={date_col: 'date'}, inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # ---------- AUTO-DETECT TIME COLUMN & COMBINE ----------
    time_col = None
    for col in df.columns:
        if 'time' in col.lower() or 'hour' in col.lower():
            # Check if it looks like time strings
            sample = df[col].dropna().astype(str).iloc[0] if len(df) > 0 else ''
            if ':' in sample or sample.isdigit():
                time_col = col
                break
    
    if time_col:
        # Combine date and time
        df['datetime'] = pd.to_datetime(
            df['date'].dt.date.astype(str) + ' ' + df[time_col].astype(str),
            errors='coerce'
        )
        # Use the combined datetime as the primary date column
        df['date'] = df['datetime']
        df.drop(columns=['datetime'], inplace=True)
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['date'])
    
    # ---------- AUTO-DETECT SITE/LOCATION ----------
    site_aliases = ['site', 'location', 'plant', 'depot', 'facility']
    site_col = None
    for col in df.columns:
        if col.lower() in site_aliases:
            site_col = col
            break
    if site_col:
        df.rename(columns={site_col: 'site'}, inplace=True)
    else:
        # If no site column, create a default
        df['site'] = 'Unknown'
    
    # ---------- AUTO-DETECT SHIFT ----------
    shift_aliases = ['shift', 'period', 'crew']
    shift_col = None
    for col in df.columns:
        if col.lower() in shift_aliases:
            shift_col = col
            break
    if shift_col:
        df.rename(columns={shift_col: 'shift'}, inplace=True)
    else:
        df['shift'] = 'Unknown'
    
    # ---------- AUTO-DETECT INCIDENT TYPE ----------
    type_aliases = ['type', 'incident_type', 'category', 'hazard']
    type_col = None
    for col in df.columns:
        if col.lower() in type_aliases:
            type_col = col
            break
    if type_col:
        df.rename(columns={type_col: 'type'}, inplace=True)
    else:
        df['type'] = 'Unspecified'
    
    # ---------- ENSURE REQUIRED COLUMNS ----------
    # Severity
    if 'severity' not in df.columns:
        # Try to find numeric column with max 5
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64'] and df[col].max() <= 10:
                df.rename(columns={col: 'severity'}, inplace=True)
                break
        else:
            df['severity'] = 1  # fallback
    
    # Injuries
    if 'injuries' not in df.columns:
        if 'injury_outcome' in df.columns:
            # Map text to numeric (simplified)
            df['injuries'] = df['injury_outcome'].apply(
                lambda x: 1 if isinstance(x, str) and 'medical' in x.lower() else 0
            )
        else:
            df['injuries'] = 0
    
    # Latitude / Longitude
    lat_col = None
    lon_col = None
    for col in df.columns:
        if 'lat' in col.lower():
            lat_col = col
        if 'lon' in col.lower() or 'long' in col.lower():
            lon_col = col
    if lat_col and lon_col:
        df.rename(columns={lat_col: 'latitude', lon_col: 'longitude'}, inplace=True)
    else:
        # Create placeholder coordinates if missing
        df['latitude'] = 0.0
        df['longitude'] = 0.0
    
    # ---------- DERIVE ADDITIONAL FIELDS ----------
    if 'is_critical' not in df.columns and 'severity' in df.columns:
        df['is_critical'] = df['severity'] >= 4
    df['weekday'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    
    # Ensure incident_id exists for row identification
    if 'incident_id' not in df.columns and 'description' in df.columns:
        df.rename(columns={'description': 'incident_id'}, inplace=True)
    elif 'incident_id' not in df.columns:
        df['incident_id'] = [f'INC-{i:04d}' for i in range(1, len(df)+1)]
    
    return df

# -------------------- SYNTHETIC FALLBACK --------------------
def generate_synthetic_data():
    """Generate synthetic safety data for demo when CSV is missing."""
    np.random.seed(42)
    n = 500
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    dates = pd.date_range(start=start_date, end=end_date, periods=n)

    sites = ['Houston Refinery', 'Gulf Platform Alpha', 'Baton Rouge Plant',
             'Dallas Terminal', 'Corpus Christi Port']
    types = ['Slip/Trip/Fall', 'Equipment Failure', 'Chemical Exposure',
             'Fire/Explosion', 'Vehicle Collision', 'Pressure Release']

    df = pd.DataFrame({
        'incident_id': [f'INC-{i:04d}' for i in range(1, n+1)],
        'date': dates,
        'site': np.random.choice(sites, n, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        'type': np.random.choice(types, n, p=[0.25, 0.2, 0.15, 0.1, 0.2, 0.1]),
        'severity': np.random.choice([1,2,3,4,5], n, p=[0.4,0.3,0.15,0.1,0.05]),
        'shift': np.random.choice(['Day','Night','Swing'], n, p=[0.5,0.3,0.2]),
        'injuries': np.random.choice([0,1,2,3], n, p=[0.6,0.25,0.1,0.05]),
        'near_miss': np.random.choice([0,1], n, p=[0.7,0.3]),
        'latitude': np.random.uniform(25, 48, n),
        'longitude': np.random.uniform(-125, -65, n)
    })
    df['is_critical'] = df['severity'] >= 4
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['weekday'] = df['date'].dt.day_name()
    return df

# -------------------- FILTERING LOGIC --------------------
def apply_filters(df, site, start_date, end_date, types, shift):
    """Apply sidebar filters and return filtered DataFrame."""
    filtered = df.copy()
    if site != 'All':
        filtered = filtered[filtered['site'] == site]
    filtered = filtered[(filtered['date'].dt.date >= start_date) &
                        (filtered['date'].dt.date <= end_date)]
    if types != ['All'] and 'All' not in types:
        filtered = filtered[filtered['type'].isin(types)]
    if shift != 'All':
        filtered = filtered[filtered['shift'] == shift]
    return filtered

# -------------------- KPI CALCULATIONS --------------------
def compute_kpis(df):
    """Return dictionary of key metrics."""
    critical_val = int(df['is_critical'].sum()) if 'is_critical' in df else 0
    avg_sev = float(df['severity'].mean()) if len(df) > 0 and 'severity' in df else 0.0
    injuries_val = int(df['injuries'].sum()) if 'injuries' in df else 0
    return {
        'total': int(len(df)),
        'critical': critical_val,
        'avg_severity': avg_sev,
        'injuries': injuries_val
    }

# -------------------- CHART BUILDERS --------------------
def build_trend_chart(df):
    if df.empty:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    trend = df.groupby('date').agg(
        total=('incident_id','count'),
        critical=('is_critical','sum')
    ).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend['date'], y=trend['total'],
                             mode='lines+markers', name='Total Incidents',
                             line=dict(color='#1f77b4')))
    fig.add_trace(go.Bar(x=trend['date'], y=trend['critical'],
                         name='Critical (Sev 4+)', marker_color='#d62728',
                         yaxis='y2', opacity=0.6))
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'),
                      hovermode='x unified', height=350)
    return fig

def build_type_chart(df):
    if df.empty:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    counts = df['type'].value_counts().reset_index()
    counts.columns = ['type', 'count']
    severity = df.groupby('type')['severity'].mean().reset_index()
    merged = counts.merge(severity, on='type')
    fig = px.bar(merged, x='count', y='type', color='severity',
                 color_continuous_scale='RdYlGn_r', orientation='h',
                 text='count', height=350)
    fig.update_traces(textposition='outside')
    return fig

def build_heatmap(df):
    if df.empty:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    heat = df.pivot_table(index='shift', columns='weekday',
                          values='incident_id', aggfunc='count', fill_value=0)
    weekday_order = ['Monday','Tuesday','Wednesday','Thursday',
                     'Friday','Saturday','Sunday']
    heat = heat.reindex(columns=weekday_order, fill_value=0)
    fig = px.imshow(heat, text_auto=True, color_continuous_scale='Reds',
                    height=350)
    fig.update_layout(xaxis_title='Weekday', yaxis_title='Shift')
    return fig

def build_site_pie(df):
    if df.empty:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    counts = df['site'].value_counts().reset_index()
    counts.columns = ['site', 'count']
    if len(counts) > 5:
        top = counts.head(5)
        others = pd.DataFrame({'site': ['Others'],
                               'count': [counts['count'].iloc[5:].sum()]})
        counts = pd.concat([top, others], ignore_index=True)
    fig = px.pie(counts, values='count', names='site', hole=0.3, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def build_map(df):
    """Scatter mapbox showing incident density by location."""
    if df.empty or df['latitude'].nunique() < 2:
        return go.Figure().add_annotation(text="Not enough location data", showarrow=False)
    
    # Aggregate by location for density
    map_data = df.groupby(['latitude', 'longitude', 'site']).size().reset_index(name='count')
    
    fig = px.scatter_mapbox(
        map_data,
        lat='latitude',
        lon='longitude',
        size='count',
        color='count',
        color_continuous_scale='Reds',
        hover_name='site',
        hover_data={'count': True},
        zoom=3,
        height=400,
        title='Incident Density by Location'
    )
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig

# -------------------- MAIN APP --------------------
def main():
    df = load_data()

    # -------------------- SIDEBAR --------------------
    st.sidebar.title("🔍 Safety Filters")
    sites = ['All'] + sorted(df['site'].unique().tolist())
    selected_site = st.sidebar.selectbox("📍 Site/Location", sites)

    min_date, max_date = df['date'].min().date(), df['date'].max().date()
    start_date = st.sidebar.date_input("Start Date", min_date,
                                       min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date,
                                     min_value=min_date, max_value=max_date)

    types = ['All'] + sorted(df['type'].unique().tolist())
    selected_types = st.sidebar.multiselect("⚠️ Incident Type", types, default=['All'])

    shifts = ['All'] + sorted(df['shift'].unique().tolist())
    selected_shift = st.sidebar.selectbox("🕒 Shift", shifts)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🚨 Alert Threshold")
    critical_threshold = st.sidebar.number_input("Critical Incident Threshold",
                                                 min_value=1, max_value=50, value=5)

    # Apply filters
    filtered = apply_filters(df, selected_site, start_date, end_date,
                             selected_types, selected_shift)

    # -------------------- KPIs --------------------
    st.title("🛡️ Safety Command Center")
    kpis = compute_kpis(filtered)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Incidents", kpis['total'])
    with col2:
        st.metric("🚨 Critical (Sev 4+)", kpis['critical'],
                  delta=f"{kpis['critical'] - critical_threshold}" if kpis['critical'] > 0 else None,
                  delta_color="inverse")
    with col3:
        st.metric("⚡ Avg Severity", f"{kpis['avg_severity']:.2f}/5")
    with col4:
        st.metric("👥 Total Injuries", kpis['injuries'])

    # -------------------- ALERTING --------------------
    if kpis['critical'] >= critical_threshold:
        st.warning(f"⚠️ **HIGH ALERT**: {kpis['critical']} critical incidents (threshold {critical_threshold}+). Immediate review!")
    elif kpis['critical'] >= 0.6 * critical_threshold:
        st.info(f"ℹ️ **Watch**: {kpis['critical']} critical incidents – monitor closely.")
    else:
        st.success(f"✅ Critical incidents: {kpis['critical']} – below threshold.")

    st.markdown("---")

    # -------------------- CHARTS (3 rows now) --------------------
    if filtered.empty:
        st.info("ℹ️ No incidents match your filters. Try adjusting the criteria.")
    else:
        # Row 1: Trend + Type
        left, right = st.columns(2)
        with left:
            st.subheader("📈 Incident Trend")
            st.plotly_chart(build_trend_chart(filtered), use_container_width=True)
        with right:
            st.subheader("📊 Breakdown by Type")
            st.plotly_chart(build_type_chart(filtered), use_container_width=True)

        # Row 2: Heatmap + Site Pie
        left2, right2 = st.columns(2)
        with left2:
            st.subheader("🗺️ Heatmap: Shift vs Weekday")
            st.plotly_chart(build_heatmap(filtered), use_container_width=True)
        with right2:
            st.subheader("🏢 Incidents by Site")
            st.plotly_chart(build_site_pie(filtered), use_container_width=True)

        # Row 3: Map (NEW – uses latitude/longitude)
        st.subheader("📍 Incident Density Map")
        st.plotly_chart(build_map(filtered), use_container_width=True)

    # -------------------- DATA TABLE & EXPORT --------------------
    st.subheader("📋 Detailed Data")
    # Select columns that exist
    display_cols = ['incident_id','date','site','type','severity','shift']
    for col in ['injuries','near_miss','latitude','longitude','risk_score']:
        if col in filtered.columns:
            display_cols.append(col)
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols],
                 use_container_width=True, hide_index=True, height=300)

    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv,
                       file_name=f"safety_data_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime='text/csv')

    st.caption(f"*Showing {len(filtered)} of {len(df)} total incidents. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
