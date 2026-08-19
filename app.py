import os
import io
import pandas as pd
import streamlit as st

from privacy_engine.process_dataframe import process_dataframe
from analytics.descriptive import descriptive_statistics
from analytics.fraud import fraud_analysis
from analytics.credit import credit_risk_analysis
from analytics.segmentation import customer_segmentation
from analytics.report_generator import generate_executive_report

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Privacy-Preserving Big Data Analytics",
    page_icon="\U0001F512",
    layout="wide",
)

os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.title("Privacy-Preserving Big Data Analytics")
st.caption(
    "Adaptive privacy protection + analytics pipeline for banking data. "
    "Raw Data -> Adaptive Privacy Engine -> Protected Dataset -> Analytics -> Dashboard."
)

# ------------------------------------------------------------------
# Data source
# ------------------------------------------------------------------
st.sidebar.header("Data Source")

data_choice = st.sidebar.radio(
    "Choose input dataset",
    ["Use bundled sample dataset", "Upload your own CSV"],
)

uploaded_file = None
if data_choice == "Upload your own CSV":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

run_button = st.sidebar.button("Run Privacy Engine + Analytics", type="primary")


@st.cache_data(show_spinner=False)
def load_bundled_data():
    return pd.read_csv("training_data.csv")


@st.cache_data(show_spinner=False)
def run_pipeline(df: pd.DataFrame):
    protected_df = process_dataframe(df)
    descriptive_results = descriptive_statistics(protected_df)
    fraud_results = fraud_analysis(protected_df)
    credit_results = credit_risk_analysis(protected_df)
    segmentation_results = customer_segmentation(protected_df)
    executive_report = generate_executive_report(
        descriptive_results, fraud_results, credit_results, segmentation_results
    )
    return {
        "protected_df": protected_df,
        "descriptive": descriptive_results,
        "fraud": fraud_results,
        "credit": credit_results,
        "segmentation": segmentation_results,
        "executive_report": executive_report,
    }


def show_kpis(kpis: dict):
    cols = st.columns(len(kpis))
    for col, (key, value) in zip(cols, kpis.items()):
        label = key.replace("_", " ").title()
        col.metric(label, value if value is not None else "N/A")


def show_charts(charts: dict):
    existing = {k: v for k, v in charts.items() if os.path.exists(v)}
    if not existing:
        st.info("No charts were generated for this dataset (required columns not present).")
        return
    cols = st.columns(2)
    for i, (name, path) in enumerate(existing.items()):
        with cols[i % 2]:
            st.image(path, caption=name.replace("_", " ").title(), use_container_width=True)


# ------------------------------------------------------------------
# Main flow
# ------------------------------------------------------------------
if run_button:
    if data_choice == "Use bundled sample dataset":
        df = load_bundled_data()
    else:
        if uploaded_file is None:
            st.warning("Please upload a CSV file first.")
            st.stop()
        df = pd.read_csv(uploaded_file)

    with st.spinner("Running adaptive privacy engine and analytics pipeline..."):
        results = run_pipeline(df)

    st.success(f"Pipeline complete — {len(df)} records processed.")

    tab_overview, tab_desc, tab_fraud, tab_credit, tab_seg, tab_data = st.tabs(
        ["Overview", "Descriptive", "Fraud", "Credit Risk", "Segmentation", "Protected Data"]
    )

    with tab_overview:
        st.subheader("Executive Summary")
        st.write(results["executive_report"])

    with tab_desc:
        st.subheader("Descriptive Analytics")
        show_kpis(results["descriptive"]["kpis"])
        show_charts(results["descriptive"]["charts"])

    with tab_fraud:
        st.subheader("Fraud Analytics")
        show_kpis(results["fraud"]["kpis"])
        show_charts(results["fraud"].get("charts", {}))

    with tab_credit:
        st.subheader("Credit Risk Analytics")
        show_kpis(results["credit"]["kpis"])
        show_charts(results["credit"].get("charts", {}))

    with tab_seg:
        st.subheader("Customer Segmentation")
        show_kpis(results["segmentation"]["kpis"])
        show_charts(results["segmentation"].get("charts", {}))

    with tab_data:
        st.subheader("Protected Dataset (post privacy engine)")
        st.dataframe(results["protected_df"].head(200), use_container_width=True)

        csv_buffer = io.StringIO()
        results["protected_df"].to_csv(csv_buffer, index=False)
        st.download_button(
            "Download protected dataset (CSV)",
            data=csv_buffer.getvalue(),
            file_name="protected_dataset.csv",
            mime="text/csv",
        )

        st.divider()
        st.caption("Optional: upload the protected dataset to AWS S3 (requires AWS secrets configured).")
        if st.button("Upload protected dataset to S3"):
            try:
                from controller.aws_manager import AWSManager

                local_path = "outputs/protected_dataset.csv"
                results["protected_df"].to_csv(local_path, index=False)

                manager = AWSManager()
                ok = manager.upload_file(local_path, "protected_dataset.csv")
                if ok:
                    st.success("Uploaded to S3 successfully.")
                else:
                    st.error("Upload failed. Check S3 credentials/bucket configuration.")
            except Exception as e:
                st.error(f"AWS upload not available: {e}")

else:
    st.info("Choose a data source in the sidebar, then click **Run Privacy Engine + Analytics** to begin.")
    st.markdown(
        """
        **Pipeline:**
        1. Raw banking dataset is loaded
        2. Adaptive Privacy Engine classifies each column (PII / sensitivity / masking strategy) and transforms it
        3. Protected dataset is analyzed for descriptive stats, fraud signals, credit risk, and customer segments
        4. Results are shown here as an executive dashboard
        """
    )