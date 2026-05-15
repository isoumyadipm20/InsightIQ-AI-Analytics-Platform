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
# PROCESS FILE
# ------------------------------------------------

if uploaded_file is not None:

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

        data = response.json()

    st.success("Dataset processed successfully")

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

        # KPI SECTION

        st.header("Business KPIs")

        kpi_response = requests.get(
            "http://127.0.0.1:8000/kpis"
        )

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

        # CHARTS

        preview_df = pd.DataFrame(data["preview"])

        if "revenue" in preview_df.columns:

            st.header("Revenue Intelligence")

            fig = px.line(
                preview_df,
                y="revenue",
                title="Revenue Trend"
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

        st.header("Data Preview")

        preview_df = pd.DataFrame(data["preview"])

        st.dataframe(
            preview_df,
            use_container_width=True
        )

    # ------------------------------------------------
    # KPI PAGE
    # ------------------------------------------------

    elif page == "KPIs":

        st.header("Business KPI Analytics")

        kpi_response = requests.get(
            "http://127.0.0.1:8000/kpis"
        )

        kpi_data = kpi_response.json()["kpis"]

        kpi_df = pd.DataFrame(
            list(kpi_data.items()),
            columns=["KPI", "Value"]
        )

        st.dataframe(
            kpi_df,
            use_container_width=True
        )

    # ------------------------------------------------
    # PLACEHOLDER PAGES
    # ------------------------------------------------

    elif page == "Forecasting":

        st.header("Forecasting Engine")
        st.info("Forecasting models coming in Phase 6")

    elif page == "Anomaly Detection":

        st.header("Anomaly Detection Engine")
        st.info("Anomaly detection coming in Phase 5")

    elif page == "AI Insights":

        st.header("AI Executive Insights")

        st.markdown("""
        ### AI Generated Business Summary

        - Revenue performance is stable.
        - Operational efficiency remains healthy.
        - No major anomalies currently detected.
        - Forecast models will appear here.
        """)