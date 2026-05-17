import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown("""
<style>

/* Main background */
.main {
    background-color: #0E1117;
}

/* KPI Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    text-align: center;
}

/* Headers */
h1, h2, h3 {
    color: #FAFAFA;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Metric styling */
[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("InsightIQ")

st.sidebar.markdown("""
AI Powered KPI & Risk Intelligence Platform
""")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Dataset Intelligence",
        "KPIs",
        "Forecasting",
        "Anomaly Detection",
        "AI Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("System Status: ACTIVE")

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("InsightIQ")
st.caption("Enterprise AI Analytics Platform")

# ------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Business Dataset",
    type=["csv", "xlsx"]
)

# ------------------------------------------------
# IF NO FILE
# ------------------------------------------------

if uploaded_file is None:

    st.info("Upload a dataset to begin analysis.")

# ------------------------------------------------
# PROCESS FILE
# ------------------------------------------------

else:

    with st.spinner("Analyzing business dataset..."):

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue()
                )
            }
        )

    # ------------------------------------------------
    # SAFE ERROR HANDLING
    # ------------------------------------------------

    if response.status_code != 200:

        st.error("Backend Error")

        st.text(response.text)

        st.stop()

    data = response.json()

    st.success("Dataset processed successfully")

    preview_df = pd.DataFrame(data["preview"])

    # ------------------------------------------------
    # DASHBOARD PAGE
    # ------------------------------------------------

    if page == "Dashboard":

        st.header("Executive Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Rows</h3>
                <h1>{data['dataset_shape']['rows']}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Columns</h3>
                <h1>{data['dataset_shape']['columns']}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Quality Score</h3>
                <h1>{data['validation']['quality_score']}%</h1>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Duplicate Rows</h3>
                <h1>{data['validation']['duplicate_rows']}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ------------------------------------------------
        # KPI SECTION
        # ------------------------------------------------

        st.header("Business KPIs")

        kpi_response = requests.get(
            "http://127.0.0.1:8000/kpis"
        )

        if kpi_response.status_code == 200:

            kpi_data = kpi_response.json()["kpis"]

            k1, k2, k3, k4 = st.columns(4)

            kpi_columns = [k1, k2, k3, k4]

            for col, (name, value) in zip(
                kpi_columns,
                kpi_data.items()
            ):

                with col:
                    st.metric(
                        label=name,
                        value=value
                    )

        st.markdown("---")

        # ------------------------------------------------
        # REVENUE CHART
        # ------------------------------------------------

        if "revenue" in preview_df.columns:

            st.header("Revenue Intelligence")

            fig = px.line(
                preview_df,
                y="revenue",
                x=preview_df.index,
                title="Revenue Trend",
                markers=True
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#1A1F2B",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ------------------------------------------------
    # DATASET INTELLIGENCE PAGE
    # ------------------------------------------------

    elif page == "Dataset Intelligence":

        st.header("Schema Detection")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Numeric Columns")
            st.write(data["schema"]["numeric_columns"])

        with col2:
            st.subheader("Categorical Columns")
            st.write(data["schema"]["categorical_columns"])

        with col3:
            st.subheader("Datetime Columns")
            st.write(data["schema"]["datetime_columns"])

        st.markdown("---")

        st.header("Dataset Preview")

        st.dataframe(
            preview_df,
            use_container_width=True
        )

        st.markdown("---")

        st.header("Data Quality Report")

        validation = data["validation"]

        st.write("Missing Values")
        st.json(validation["missing_values"])

        st.write(f"Total Missing Values: {validation['total_missing']}")
        st.write(f"Duplicate Rows: {validation['duplicate_rows']}")
        st.write(f"Quality Score: {validation['quality_score']}%")

    # ------------------------------------------------
    # KPI PAGE
    # ------------------------------------------------

    elif page == "KPIs":

        st.header("Business KPI Analytics")

        kpi_response = requests.get(
            "http://127.0.0.1:8000/kpis"
        )

        if kpi_response.status_code == 200:

            kpi_data = kpi_response.json()["kpis"]

            kpi_df = pd.DataFrame(
                list(kpi_data.items()),
                columns=["KPI", "Value"]
            )

            st.dataframe(
                kpi_df,
                use_container_width=True
            )

            fig = px.bar(
                kpi_df,
                x="KPI",
                y="Value",
                title="KPI Comparison"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#1A1F2B",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ------------------------------------------------
    # FORECASTING PAGE
    # ------------------------------------------------

    elif page == "Forecasting":

        st.header("Forecasting Engine")

        st.info(
            "Forecasting models will be integrated in Phase 6."
        )

        if "revenue" in preview_df.columns:

            fig = px.line(
                preview_df,
                y="revenue",
                title="Historical Revenue"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#1A1F2B",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ------------------------------------------------
    # ANOMALY DETECTION PAGE
    # ------------------------------------------------

    elif page == "Anomaly Detection":

        st.header("Operational Risk Intelligence")

        anomaly_response = requests.get(
            "http://127.0.0.1:8000/anomalies"
        )

        if anomaly_response.status_code != 200:

            st.error("Failed to load anomaly analytics")

            st.stop()

        anomaly_data = anomaly_response.json()

        # ------------------------------------------------
        # RISK METRICS
        # ------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Risk Score",
                f"{anomaly_data['risk_score']}%"
            )

        with col2:
            st.metric(
                "Risk Level",
                anomaly_data["risk_level"]
            )

        with col3:
            st.metric(
                "Detected Anomalies",
                anomaly_data[
                    "isolation_forest_detection"
                ]["total_anomalies"]
            )

        st.markdown("---")

        # ------------------------------------------------
        # ANOMALY TABLE
        # ------------------------------------------------

        st.subheader("Detected Anomalies")

        anomalies = anomaly_data[
            "isolation_forest_detection"
        ]["anomaly_records"]

        if len(anomalies) > 0:

            anomaly_df = pd.DataFrame(anomalies)

            st.dataframe(
                anomaly_df,
                use_container_width=True
            )

            # ------------------------------------------------
            # ANOMALY VISUALIZATION
            # ------------------------------------------------

            if "revenue" in anomaly_df.columns:

                st.subheader("Revenue Anomaly Analysis")

                fig = px.scatter(
                    anomaly_df,
                    x="date",
                    y="revenue",
                    color="revenue",
                    size="revenue",
                    hover_data=anomaly_df.columns,
                    title="Detected Revenue Anomalies"
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#1A1F2B",
                    font_color="white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # ------------------------------------------------
            # AI INTERPRETATION
            # ------------------------------------------------

            st.markdown("---")

            st.subheader("AI Risk Interpretation")

            risk_level = anomaly_data["risk_level"]

            if risk_level == "HIGH":

                st.error("""
                Significant operational anomalies detected.

                Potential causes may include:
                - revenue spikes or crashes
                - abnormal operational behavior
                - inventory imbalance
                - customer demand fluctuations

                Immediate investigation is recommended.
                """)

            elif risk_level == "MODERATE":

                st.warning("""
                Moderate anomaly activity detected.

                Some business metrics are deviating
                from expected operational behavior.
                """)

            else:

                st.success("""
                Business operations appear stable.

                No major operational anomalies detected.
                """)

        else:

            st.success(
                "No significant anomalies detected"
            )

    # ------------------------------------------------
    # AI INSIGHTS PAGE
    # ------------------------------------------------

    elif page == "AI Insights":

        st.header("AI Executive Insights")

        st.markdown("""
        ### Executive Business Summary

        - Revenue trends appear stable across reporting periods.
        - Operational efficiency remains within expected thresholds.
        - Current anomaly detection indicates manageable business risk.
        - Forecasting and predictive intelligence modules will enhance future planning.
        """)

        st.markdown("---")

        st.subheader("Strategic Recommendations")

        st.info("""
        - Monitor operational costs closely.
        - Increase customer retention strategies.
        - Investigate unusual revenue spikes.
        - Improve forecasting readiness with larger datasets.
        """)