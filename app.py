import streamlit as st
import pandas as pd

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = pd.read_csv("analytics.csv")

# --------------------------------------------------
# Data Transformations
# --------------------------------------------------

df["SessionsPerUser"] = (
    df["Sessions"] / df["Users"]
)

# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("🚀 Data Armada Analytics Command Center")

st.markdown("""
This dashboard demonstrates a basic analytics and ETL workflow.

Data Source → Transformation → KPI Calculation →
Visualization → Business Insights

Built using Python, Pandas, and Streamlit.
""")

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------

total_users = df["Users"].sum()

total_sessions = df["Sessions"].sum()

avg_sessions_per_user = round(
    df["SessionsPerUser"].mean(),
    2
)

source_summary = (
    df.groupby("Source")
      .agg({"Users": "sum"})
)

state_summary = (
    df.groupby("State")
      .agg({"Users": "sum"})
)

device_summary = (
    df.groupby("Device")
      .agg({"Users": "sum"})
)

top_source = source_summary["Users"].idxmax()

top_state = state_summary["Users"].idxmax()

top_device = device_summary["Users"].idxmax()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Users", total_users)

with col2:
    st.metric("Total Sessions", total_sessions)

with col3:
    st.metric("Avg Sessions/User", avg_sessions_per_user)

with col4:
    st.metric("Top Source", top_source)

with col5:
    st.metric("Top State", top_state)

with col6:
    st.metric("Top Device", top_device)

# --------------------------------------------------
# Filters
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_device = st.sidebar.selectbox(
    "Device",
    ["All"] + list(df["Device"].unique())
)

selected_state = st.sidebar.selectbox(
    "State",
    ["All"] + list(df["State"].unique())
)

filtered_df = df.copy()

if selected_device != "All":
    filtered_df = filtered_df[
        filtered_df["Device"] == selected_device
    ]

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["State"] == selected_state
    ]

# --------------------------------------------------
# User Traffic By Source
# --------------------------------------------------

st.subheader("Users By Traffic Source")

source_chart = (
    filtered_df.groupby("Source")
               .agg({"Users": "sum"})
               .sort_values(
                    by="Users",
                    ascending=False
               )
)

st.bar_chart(source_chart)

# --------------------------------------------------
# Users By State
# --------------------------------------------------

st.subheader("Users By State")

state_chart = (
    filtered_df.groupby("State")
               .agg({"Users": "sum"})
               .sort_values(
                    by="Users",
                    ascending=False
               )
)

st.bar_chart(state_chart)

# --------------------------------------------------
# Users By Device
# --------------------------------------------------

st.subheader("Users By Device")

device_chart = (
    filtered_df.groupby("Device")
               .agg({"Users": "sum"})
               .sort_values(
                    by="Users",
                    ascending=False
               )
)

st.bar_chart(device_chart)

# --------------------------------------------------
# Users Over Time
# --------------------------------------------------

st.subheader("Users Over Time")

time_chart = (
    filtered_df.groupby("Date")
               .agg({"Users": "sum"})
)

st.line_chart(time_chart)

# --------------------------------------------------
# Raw Dataset
# --------------------------------------------------

st.subheader("Underlying Dataset")

st.dataframe(filtered_df)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "Built by Isaiah Acker | Python • Pandas • Streamlit"
)