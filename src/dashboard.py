import streamlit as st
import pandas as pd
import plotly.express as px

def show_metric_cards(df: pd.DataFrame):
    total = len(df)
    agent_driven = int((df["dsat_type"] == "Agent-Driven DSAT").sum()) if "dsat_type" in df else 0
    non_agent = int((df["dsat_type"] == "Non-Agent-Driven DSAT").sum()) if "dsat_type" in df else 0
    needs_review = int((df["dsat_type"] == "Needs QA Validation").sum()) if "dsat_type" in df else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cases Analyzed", total)
    c2.metric("Agent-Driven", agent_driven)
    c3.metric("Non-Agent-Driven", non_agent)
    c4.metric("Needs Review", needs_review)

def show_bar_chart(df: pd.DataFrame, column: str, title: str):
    if column not in df.columns:
        st.info(f"Column not found: {column}")
        return
    data = df[column].value_counts().reset_index()
    data.columns = [column, "count"]
    fig = px.bar(data, x=column, y="count", title=title)
    st.plotly_chart(fig, use_container_width=True)

def show_dashboard(df: pd.DataFrame):
    show_metric_cards(df)
    left, right = st.columns(2)
    with left:
        show_bar_chart(df, "dsat_type", "DSAT Type Distribution")
        show_bar_chart(df, "severity", "Severity Breakdown")
    with right:
        show_bar_chart(df, "root_cause_category", "Root Cause Distribution")
        if "channel" in df.columns:
            show_bar_chart(df, "channel", "DSAT by Channel")
