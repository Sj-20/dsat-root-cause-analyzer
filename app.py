import os
import pandas as pd
import streamlit as st

from src.preprocessing import read_input_file
from src.dsat_analyzer import analyze_dataframe, build_executive_summary
from src.dashboard import show_dashboard
from src.report_generator import to_excel_bytes
from src.evaluation import evaluate_predictions

st.set_page_config(
    page_title="DSAT Root Cause Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GenAI-Powered DSAT Root Cause Analyzer")
st.caption("Privacy-safe customer dissatisfaction classification, coaching insights, and RCA dashboard.")

with st.sidebar:
    st.header("Settings")

    provider = st.selectbox(
        "Analysis mode",
        ["Rule-based demo", "OpenAI"],
        help="Rule-based demo works without API keys. OpenAI mode uses your secret API key."
    )

    model = st.text_input("OpenAI model", value="gpt-4o-mini")

    api_key = ""
    if provider == "OpenAI":
        api_key = st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") else ""
        api_key = st.text_input(
            "OpenAI API key",
            value=api_key,
            type="password",
            help="For Streamlit Cloud, add OPENAI_API_KEY in app Secrets instead of hardcoding it."
        )

    max_rows = st.slider(
        "Rows to analyze",
        min_value=5,
        max_value=200,
        value=50,
        step=5,
        help="Keep this low when using paid APIs to control cost."
    )

st.info(
    "This app includes a rule-based demo mode so it can run on Streamlit Cloud without paid API keys. "
    "For a true GenAI version, select OpenAI mode and add your API key in Streamlit secrets."
)

sample_path = "data/synthetic_dsat_cases.csv"

uploaded_file = st.file_uploader("Upload DSAT cases CSV or Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    df = read_input_file(uploaded_file)
else:
    st.write("Using bundled synthetic dataset for demo.")
    df = pd.read_csv(sample_path)

st.subheader("Input Data Preview")
st.dataframe(df.head(10), use_container_width=True)

candidate_text_cols = [
    c for c in df.columns
    if any(keyword in c.lower() for keyword in ["comment", "transcript", "notes", "summary", "message", "text"])
]

default_cols = [c for c in candidate_text_cols if c in df.columns]
if not default_cols:
    default_cols = list(df.select_dtypes(include=["object"]).columns[:3])

text_columns = st.multiselect(
    "Select text columns to analyze",
    options=list(df.columns),
    default=default_cols,
    help="Select columns such as transcript, survey comment, QA notes, and case summary."
)

if st.button("Run DSAT Analysis", type="primary"):
    with st.spinner("Analyzing DSAT cases..."):
        result_df = analyze_dataframe(
            df=df,
            text_columns=text_columns,
            provider=provider,
            api_key=api_key,
            model=model,
            max_rows=max_rows,
        )
        st.session_state["result_df"] = result_df

if "result_df" in st.session_state:
    result_df = st.session_state["result_df"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Analyzed Cases",
        "Dashboard",
        "Coaching Insights",
        "Evaluation",
        "Download"
    ])

    with tab1:
        st.subheader("Analyzed DSAT Cases")
        st.dataframe(result_df, use_container_width=True)

    with tab2:
        st.subheader("RCA Dashboard")
        show_dashboard(result_df)

    with tab3:
        st.subheader("Coaching Insights")
        agent_cases = result_df[result_df["dsat_type"] == "Agent-Driven DSAT"]
        if len(agent_cases) == 0:
            st.success("No agent-driven cases detected in the analyzed sample.")
        else:
            st.write("Top coaching recommendations:")
            coaching = agent_cases["coaching_recommendation"].value_counts().reset_index()
            coaching.columns = ["Coaching Recommendation", "Count"]
            st.dataframe(coaching, use_container_width=True)

            if "agent_name" in result_df.columns:
                st.write("Agent-driven cases by agent:")
                by_agent = agent_cases["agent_name"].value_counts().reset_index()
                by_agent.columns = ["Agent", "Agent-Driven DSAT Count"]
                st.dataframe(by_agent, use_container_width=True)

    with tab4:
        st.subheader("Evaluation")
        if "human_label" in result_df.columns:
            eval_result = evaluate_predictions(result_df, actual_col="human_label", pred_col="dsat_type")
            if "error" in eval_result:
                st.warning(eval_result["error"])
            else:
                st.metric("Human-AI Agreement / Accuracy", f"{eval_result['accuracy']:.2%}")
                st.write("Classification report:")
                st.dataframe(pd.DataFrame(eval_result["classification_report"]).T, use_container_width=True)
        else:
            st.info("Add a human_label column to evaluate model/classifier performance.")

    with tab5:
        st.subheader("Download Reports")
        summary_text = build_executive_summary(result_df)
        st.text_area("Executive Summary", value=summary_text, height=180)

        csv_bytes = result_df.to_csv(index=False).encode("utf-8")
        excel_bytes = to_excel_bytes(result_df, summary_text=summary_text)

        st.download_button(
            "Download analyzed cases CSV",
            data=csv_bytes,
            file_name="analyzed_dsat_cases.csv",
            mime="text/csv"
        )

        st.download_button(
            "Download DSAT RCA report Excel",
            data=excel_bytes,
            file_name="dsat_rca_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
