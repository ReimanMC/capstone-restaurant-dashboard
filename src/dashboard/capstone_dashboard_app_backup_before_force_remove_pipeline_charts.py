
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Capstone Forecast Intelligence Portal", layout="wide")

st.markdown("""
<style>
.stApp {background: radial-gradient(circle at top left, #111827 0%, #070B16 45%, #020617 100%); color:#F8FAFC;}
#MainMenu, footer, header {visibility:hidden;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#111827 0%,#0F172A 100%); border-right:1px solid rgba(139,92,246,.35);}
h1,h2,h3,h4,h5,h6 {color:#F8FAFC;} p,li,span {color:#CBD5E1;}
.main-title {font-size:42px; font-weight:900; line-height:1.1; margin-bottom:6px; background:linear-gradient(90deg,#38BDF8,#8B5CF6,#F97316); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.main-subtitle {font-size:17px; color:#CBD5E1; margin-bottom:18px;}
button[data-baseweb="tab"] {background:#111827; color:#E5E7EB; border-radius:14px 14px 0 0; margin-right:8px; padding:14px 20px; border:1px solid rgba(148,163,184,.15); font-weight:700; transition:all .25s ease;}
button[data-baseweb="tab"]:hover {background:linear-gradient(90deg,rgba(139,92,246,.85),rgba(6,182,212,.85)); color:white; transform:translateY(-2px);}
button[aria-selected="true"] {background:linear-gradient(90deg,#8B5CF6,#06B6D4)!important; color:white!important; border-bottom:3px solid #F97316!important;}
.metric-card {background:linear-gradient(145deg,rgba(17,24,39,.98),rgba(30,41,59,.92)); border:1px solid rgba(148,163,184,.16); border-radius:22px; padding:22px; min-height:145px; box-shadow:0 12px 30px rgba(2,6,23,.45); transition:.25s ease; position:relative; overflow:hidden;}
.metric-card:hover {transform:translateY(-4px); box-shadow:0 0 28px rgba(6,182,212,.25); border:1px solid rgba(6,182,212,.35);}
.metric-card::before {content:""; position:absolute; top:-35px; right:-35px; width:105px; height:105px; border-radius:50%; opacity:.24;}
.metric-card.cyan::before{background:#06B6D4}.metric-card.purple::before{background:#8B5CF6}.metric-card.green::before{background:#22C55E}.metric-card.orange::before{background:#F97316}.metric-card.red::before{background:#EF4444}
.metric-label {color:#94A3B8; font-size:14px; font-weight:700; letter-spacing:.3px; text-transform:uppercase;}
.metric-value {font-size:32px; font-weight:900; margin-top:8px; margin-bottom:6px;}
.metric-note {color:#CBD5E1; font-size:14px;}
.metric-accent-cyan{color:#38BDF8}.metric-accent-purple{color:#A78BFA}.metric-accent-green{color:#22C55E}.metric-accent-orange{color:#FB923C}.metric-accent-red{color:#F87171}
.section-card {background:linear-gradient(145deg,rgba(15,23,42,.98),rgba(17,24,39,.94)); border:1px solid rgba(148,163,184,.14); border-radius:22px; padding:24px 26px; margin:14px 0 22px 0; box-shadow:0 10px 26px rgba(2,6,23,.35);}
.section-title {font-size:24px; font-weight:900; margin-bottom:8px; color:#F8FAFC;}
.section-text {color:#CBD5E1; font-size:16px; line-height:1.65;}
.insight-card {background:rgba(15,23,42,.96); border-left:5px solid #06B6D4; border-radius:18px; padding:20px; margin-bottom:16px; box-shadow:0 8px 22px rgba(2,6,23,.30);}
.insight-card.green-border{border-left-color:#22C55E}.insight-card.orange-border{border-left-color:#F97316}.insight-card.red-border{border-left-color:#EF4444}.insight-card.purple-border{border-left-color:#8B5CF6}
.insight-title {font-size:18px; font-weight:900; color:#F8FAFC; margin-bottom:6px;}
.insight-text {color:#CBD5E1; font-size:15px; line-height:1.55;}
.badge {display:inline-block; padding:6px 12px; border-radius:999px; font-size:13px; font-weight:800; margin-right:8px; margin-bottom:8px;}
.badge-cyan{background:rgba(6,182,212,.16); color:#67E8F9; border:1px solid rgba(6,182,212,.35)}.badge-purple{background:rgba(139,92,246,.16); color:#C4B5FD; border:1px solid rgba(139,92,246,.35)}.badge-green{background:rgba(34,197,94,.16); color:#86EFAC; border:1px solid rgba(34,197,94,.35)}.badge-orange{background:rgba(249,115,22,.16); color:#FDBA74; border:1px solid rgba(249,115,22,.35)}
[data-testid="stPlotlyChart"] {background:rgba(15,23,42,.58); border-radius:20px; padding:12px; border:1px solid rgba(148,163,184,.10);}
[data-testid="stDataFrame"] {border-radius:18px; overflow:hidden; border:1px solid rgba(148,163,184,.14);}
.stAlert {border-radius:18px;}
.stButton > button {background:linear-gradient(90deg,#8B5CF6,#06B6D4); color:white; border:none; border-radius:14px; padding:10px 22px; font-weight:800;}
.stButton > button:hover {background:linear-gradient(90deg,#06B6D4,#F97316); color:white;}
</style>
""", unsafe_allow_html=True)

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "dashboard"

PATHS = {
    "final": DATA_DIR / "capstone_dashboard_dataset.csv",
    "annual": DATA_DIR / "annual_sales_dashboard_dataset.csv",
    "backtest": DATA_DIR / "annual_backtesting_forecast_dataset.csv",
    "backtest_metrics": DATA_DIR / "annual_backtesting_metrics_dataset.csv",
    "scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv",
    "research_framework": DATA_DIR / "research_framework_summary.csv",
    "data_cleaning": DATA_DIR / "data_cleaning_summary.csv",
    "data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",
    "data_pipeline_contrast": DATA_DIR / "data_pipeline_contrast_summary.csv",
    "feature_engineering": DATA_DIR / "feature_engineering_summary.csv",
    "feature_selection": DATA_DIR / "feature_selection_summary.csv",
    "literature_added_value": DATA_DIR / "literature_added_value_summary.csv",
    "model_improvement": DATA_DIR / "model_improvement_evidence.csv",
    "rf_sensitivity": DATA_DIR / "rf_sensitivity_dashboard_summary.csv",
    "conformal_roadmap": DATA_DIR / "conformal_prediction_roadmap.csv",
    "operational_value": DATA_DIR / "operational_value_added_summary.csv",
}

@st.cache_data
def load_all_data():
    data = {name: pd.read_csv(path) for name, path in PATHS.items()}
    for key in ["final", "annual", "backtest"]:
        data[key]["date"] = pd.to_datetime(data[key]["date"])
    if "average_ticket" not in data["annual"].columns:
        data["annual"]["average_ticket"] = data["annual"]["net_sales"] / data["annual"]["transactions_count"]
    data["annual"]["average_ticket"] = data["annual"]["average_ticket"].fillna(0)
    data["annual"]["month"] = data["annual"]["date"].dt.to_period("M").astype(str)
    return data

data = load_all_data()
df = data["final"]
annual_df = data["annual"]
backtest_df = data["backtest"]
backtest_metrics_df = data["backtest_metrics"]
scientific_roadmap_df = data["scientific_roadmap"]
research_framework_df = data["research_framework"]
data_cleaning_df = data["data_cleaning"]
data_pipeline_evolution_df = data["data_pipeline_evolution"]
data_pipeline_contrast_df = data["data_pipeline_contrast"]
feature_engineering_df = data["feature_engineering"]
feature_selection_df = data["feature_selection"]
literature_added_value_df = data["literature_added_value"]
model_improvement_df = data["model_improvement"]
rf_sensitivity_df = data["rf_sensitivity"]
conformal_roadmap_df = data["conformal_roadmap"]
operational_value_df = data["operational_value"]

def format_money(value):
    return f"${value:,.0f}"

def format_money_2(value):
    return f"${value:,.2f}"

def format_number(value):
    return f"{value:,.0f}"

def metric_card(label, value, note="", color="cyan"):
    accent_class = f"metric-accent-{color}"
    st.markdown(f"""
        <div class="metric-card {color}">
            <div class="metric-label">{label}</div>
            <div class="metric-value {accent_class}">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

def section_card(title, text):
    st.markdown(f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

def insight_card(title, text, border="cyan"):
    border_class = {"green":"green-border", "orange":"orange-border", "red":"red-border", "purple":"purple-border"}.get(border, "")
    st.markdown(f"""
        <div class="insight-card {border_class}">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

def style_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",
        font=dict(color="#E5E7EB"),
        title_font=dict(color="#F8FAFC", size=20),
        legend=dict(bgcolor="rgba(15,23,42,0)", bordercolor="rgba(148,163,184,0.15)"),
        margin=dict(l=20, r=20, t=60, b=40),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.16)", zerolinecolor="rgba(148,163,184,0.25)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.16)", zerolinecolor="rgba(148,163,184,0.25)")
    return fig

def display_dataframe(df_to_show):
    st.dataframe(df_to_show, use_container_width=True, hide_index=True)

st.markdown("""
<div class="main-title">Capstone Forecast Intelligence Portal</div>
<div class="main-subtitle">
Scientific roadmap, model improvement evidence, feature engineering, literature contribution, and final manager dashboard.
</div>
<span class="badge badge-cyan">Real POS Data</span>
<span class="badge badge-purple">SARIMAX + Random Forest</span>
<span class="badge badge-green">Model Improvement Evidence</span>
<span class="badge badge-orange">Conformal Prediction Roadmap</span>
""", unsafe_allow_html=True)

st.sidebar.header("Dashboard Controls")
metric_options = {"Net Sales": "net_sales", "Transactions Count": "transactions_count", "Average Ticket": "average_ticket"}
selected_metric_label = st.sidebar.selectbox("Select Annual KPI", list(metric_options.keys()))
selected_metric = metric_options[selected_metric_label]
season_options = ["All"] + sorted(annual_df["season"].dropna().unique().tolist())
selected_season = st.sidebar.selectbox("Filter Manager KPI Cards", season_options)
st.sidebar.markdown("---")
st.sidebar.caption("This portal defends the analytical process first and shows the manager dashboard as the final business output.")

filtered_for_cards = annual_df.copy()
if selected_season != "All":
    filtered_for_cards = filtered_for_cards[filtered_for_cards["season"] == selected_season]

latest = df.iloc[-1]
total_sales = filtered_for_cards["net_sales"].sum()
avg_daily_sales = filtered_for_cards["net_sales"].mean()
total_transactions = filtered_for_cards["transactions_count"].sum()
avg_ticket = filtered_for_cards["average_ticket"].mean()
best_day = filtered_for_cards.loc[filtered_for_cards["net_sales"].idxmax()]
worst_day = filtered_for_cards.loc[filtered_for_cards["net_sales"].idxmin()]
monthly_sales_for_cards = filtered_for_cards.groupby("month", as_index=False).agg(monthly_sales=("net_sales", "sum"))
best_month = monthly_sales_for_cards.loc[monthly_sales_for_cards["monthly_sales"].idxmax()]
worst_month = monthly_sales_for_cards.loc[monthly_sales_for_cards["monthly_sales"].idxmin()]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Project Roadmap",
    "Research Framework",
    "Data Pipeline",
    "Feature Engineering",
    "Literature & Added Value",
    "Model Strategy",
    "Model Results",
    "Manager Dashboard",
    "Team & Feedback",
])

with tab1:
    st.subheader("Project Roadmap")
    section_card(
        "From Raw Restaurant Data to Operational Decision Support",
        "This roadmap shows the complete analytical journey: raw POS data and external weather variables were cleaned, engineered, modeled, validated, and translated into a manager-facing dashboard.",
    )
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        metric_card("Data Sources", "POS + Weather", "Square POS and external Niagara weather signals", "cyan")
    with r2:
        metric_card("Modeling Scope", "Twisted Bar", "Primary MVP because it has the most complete dataset", "purple")
    with r3:
        metric_card("Best MAPE", "16.20%", "Hybrid SARIMAX + RF Lag Residual", "green")
    with r4:
        metric_card("Next Method", "Conformal", "Prediction intervals for uncertainty-aware planning", "orange")
    st.subheader("Scientific Roadmap Summary")
    display_dataframe(scientific_roadmap_df)
    st.subheader("How to Read This Portal")
    c1, c2, c3 = st.columns(3)
    with c1:
        insight_card("First", "Review the data pipeline and feature engineering strategy to understand how the data was prepared and transformed.", "cyan")
    with c2:
        insight_card("Second", "Review model strategy and model results to understand why the Hybrid SARIMAX + RF approach improved performance.", "purple")
    with c3:
        insight_card("Finally", "Use the manager dashboard as the business-facing output for restaurant planning and operational interpretation.", "green")


with tab2:
    st.subheader("Research Framework")

    section_card(
        "Academic and Strategic Foundation",
        "This section integrates the core research elements of the project: problem gap, objective, research questions, data, analytical methods, key findings, visual evidence, strategic implications, limitations, and future research directions.",
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        metric_card(
            "Research Focus",
            "Forecasting",
            "Short-term restaurant demand",
            "cyan",
        )

    with f2:
        metric_card(
            "Main Dataset",
            "Twisted Bar",
            "Complete MVP data source",
            "purple",
        )

    with f3:
        metric_card(
            "Best Model",
            "Hybrid",
            "SARIMAX + Random Forest",
            "green",
        )

    with f4:
        metric_card(
            "Next Method",
            "Conformal",
            "Prediction intervals",
            "orange",
        )

    st.subheader("Research Framework Summary")
    display_dataframe(research_framework_df)

    st.subheader("How This Supports the Project Defense")

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_card(
            "Academic Alignment",
            "The framework connects the research problem, objective, questions, analytical methods, findings, strategic implications, limitations, and future work in one place.",
            "cyan",
        )

    with c2:
        insight_card(
            "Team Guidance",
            "This section helps all team members explain the project consistently during the final presentation or poster session.",
            "purple",
        )

    with c3:
        insight_card(
            "Evaluator Clarity",
            "Visitors can quickly understand what was studied, how it was analyzed, what was found, and why it matters.",
            "green",
        )


with tab3:
    st.subheader("Data Pipeline")

    section_card(
        "From High-Volume POS Data to Forecast-Ready Datasets",
        "This section shows the transformation from detailed POS operational records into daily forecasting, validation, and dashboard-ready datasets. The goal is to make the cleaning and modeling pipeline visually clear: we started with high-volume transaction, item, order, and section data, then built cleaner daily analytical layers for forecasting.",
    )

    st.subheader("Before → After Dataset Transformation")

    contrast_df = data_pipeline_contrast_df.copy()

    contrast_df["Records"] = pd.to_numeric(contrast_df["Records"], errors="coerce")
    contrast_df["Columns / Features"] = pd.to_numeric(
        contrast_df["Columns / Features"],
        errors="coerce",
    )

    initial_records = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Initial Cleaned POS Tables",
            "Records",
        ].iloc[0]
    )

    initial_columns = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Initial Cleaned POS Tables",
            "Columns / Features",
        ].iloc[0]
    )

    modeling_records = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Final Modeling Dataset",
            "Records",
        ].iloc[0]
    )

    modeling_columns = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Final Modeling Dataset",
            "Columns / Features",
        ].iloc[0]
    )

    enhanced_records = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Enhanced KPI Feature Layer",
            "Records",
        ].iloc[0]
    )

    enhanced_columns = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Enhanced KPI Feature Layer",
            "Columns / Features",
        ].iloc[0]
    )

    holdout_records = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Final Holdout Dashboard Dataset",
            "Records",
        ].iloc[0]
    )

    holdout_columns = int(
        contrast_df.loc[
            contrast_df["Dataset Stage"] == "Final Holdout Dashboard Dataset",
            "Columns / Features",
        ].iloc[0]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Initial Cleaned POS",
            f"{initial_records:,}",
            f"{initial_columns} total columns across cleaned POS tables",
            "cyan",
        )

    with c2:
        metric_card(
            "Final Modeling Dataset",
            f"{modeling_records:,}",
            f"{modeling_columns} forecasting-ready variables",
            "green",
        )

    with c3:
        metric_card(
            "Enhanced KPI Layer",
            f"{enhanced_records:,}",
            f"{enhanced_columns} candidate engineered variables",
            "purple",
        )

    with c4:
        metric_card(
            "Final Holdout Output",
            f"{holdout_records:,}",
            f"{holdout_columns} dashboard forecast columns",
            "orange",
        )

    section_card(
        "Important Interpretation",
        "The project did not simply reduce data. It transformed detailed POS records into daily forecasting-ready datasets. The 115-column KPI layer is an expanded candidate feature layer created for experimentation, lags, rolling averages, ratios, and operational indicators. It does not mean that all 115 variables were used as final inputs in every model.",
    )

    chart_records_df = contrast_df.copy()
    chart_records_df["Records Label"] = chart_records_df["Records"].apply(
        lambda x: f"{int(x):,}" if pd.notna(x) else ""
    )

    records_fig = px.bar(
        chart_records_df,
        x="Dataset Stage",
        y="Records",
        text="Records Label",
        title="Records by Dataset Stage",
        color="Dataset Stage",
        color_discrete_sequence=[
            "#38BDF8",
            "#8B5CF6",
            "#22C55E",
            "#F97316",
            "#EF4444",
            "#14B8A6",
        ],
    )
    records_fig.update_xaxes(tickangle=-25)
    records_fig.update_traces(textposition="outside")
    records_fig = style_plotly(records_fig)
    st.plotly_chart(records_fig, use_container_width=True)

    chart_columns_df = contrast_df.copy()
    chart_columns_df["Columns Label"] = chart_columns_df["Columns / Features"].apply(
        lambda x: f"{int(x):,}" if pd.notna(x) else ""
    )

    columns_fig = px.bar(
        chart_columns_df,
        x="Dataset Stage",
        y="Columns / Features",
        text="Columns Label",
        title="Columns / Candidate Features by Dataset Stage",
        color="Dataset Stage",
        color_discrete_sequence=[
            "#F97316",
            "#38BDF8",
            "#22C55E",
            "#8B5CF6",
            "#EF4444",
            "#14B8A6",
        ],
    )
    columns_fig.update_xaxes(tickangle=-25)
    columns_fig.update_traces(textposition="outside")
    columns_fig = style_plotly(columns_fig)
    st.plotly_chart(columns_fig, use_container_width=True)

    st.subheader("Dataset Transformation Summary")
    display_dataframe(contrast_df)

    st.subheader("Detailed Data Pipeline Evolution")
    if "data_pipeline_evolution_df" in globals():
        display_dataframe(data_pipeline_evolution_df)

    st.subheader("Data Cleaning and Quality Decisions")
    display_dataframe(data_cleaning_df)

    st.subheader("How the Data Pipeline Supports Forecasting")

    p1, p2, p3 = st.columns(3)

    with p1:
        insight_card(
            "Raw POS to Clean Layers",
            "Transaction, item, order, and section files were cleaned and standardized to validate sales, refunds, tips, discounts, and operational behavior.",
            "cyan",
        )

    with p2:
        insight_card(
            "Daily Modeling Structure",
            "The modeling dataset converts granular POS activity into daily restaurant-level demand observations enriched with calendar, weather, holiday, event, and seasonality variables.",
            "green",
        )

    with p3:
        insight_card(
            "Forecast and Dashboard Outputs",
            "The final datasets separate model evaluation, annual rolling validation, and manager-facing visual outputs to avoid mixing raw data, candidate features, and final forecast results.",
            "purple",
        )


with tab4:
    st.subheader("Feature Engineering")
    section_card(
        "Feature Engineering Strategy",
        "Features were not selected blindly. They were engineered based on restaurant operations, time-series forecasting principles, weather exposure, seasonal demand behavior, and KPI interpretation.",
    )
    st.subheader("Features Created and Used")
    display_dataframe(feature_engineering_df)
    st.subheader("Features Excluded or Controlled")
    display_dataframe(feature_selection_df)
    st.subheader("Why Feature Engineering Matters")
    c1, c2, c3 = st.columns(3)
    with c1:
        insight_card("Operational Logic", "Restaurant demand changes by day of week, weekend, season, weather, events, and recent demand behavior.", "green")
    with c2:
        insight_card("Leakage Prevention", "Identifiers and future target-derived values were excluded from forecasting to avoid unrealistic model performance.", "red")
    with c3:
        insight_card("Predictive Structure", "Lag and rolling features help models learn recent demand patterns while reducing short-term volatility.", "purple")

with tab5:
    st.subheader("Literature Gap & Our Added Value")
    section_card(
        "From Literature to Implementation",
        "The project does not only replicate academic literature. It operationalizes restaurant analytics, demand forecasting, and AI concepts using real POS data, model comparison, rolling validation, and an interactive decision-support dashboard.",
    )
    display_dataframe(literature_added_value_df)
    st.subheader("Scientific Contribution")
    c1, c2 = st.columns(2)
    with c1:
        insight_card("What the Literature Provides", "The papers support the importance of restaurant analytics, hospitality big data, AI adoption, and short-term demand forecasting.", "cyan")
        insight_card("Remaining Gap", "Many studies remain conceptual, focus on large chains, or do not provide a manager-facing operational dashboard.", "orange")
    with c2:
        insight_card("Our Added Value", "We implemented the ideas with real POS data from Twisted Bar, engineered restaurant-specific features, compared models, validated performance, and deployed a QR-accessible dashboard.", "green")
        insight_card("Business Translation", "The project connects forecast outputs to staffing readiness, menu preparation, promotional timing, and risk-aware restaurant planning.", "purple")

with tab6:
    st.subheader("Model Strategy")
    section_card(
        "Why These Models Were Selected",
        "The modeling strategy starts with a simple benchmark, then adds statistical time-series structure, external variables, machine learning, hybrid residual correction, and finally a roadmap for conformal prediction intervals.",
    )
    s1, s2, s3 = st.columns(3)
    with s1:
        insight_card("Baseline", "The Seasonal Naive model establishes a minimum benchmark using same-week historical behavior.", "cyan")
    with s2:
        insight_card("SARIMAX", "SARIMAX was selected because restaurant demand has temporal, weekly, and seasonal behavior. The weekly seasonal component uses a period of 7 days.", "purple")
    with s3:
        insight_card("Hybrid SARIMAX + RF", "The hybrid model combines SARIMAX temporal structure with Random Forest residual correction to capture nonlinear patterns.", "green")
    st.subheader("Key Parameter Strategy")
    parameter_strategy = pd.DataFrame([
        ["SARIMAX Basic", "order=(1,1,1), seasonal_order=(1,0,1,7)", "Captures trend, differencing, moving average behavior, and weekly restaurant seasonality."],
        ["SARIMAX External", "Calendar, weather, holiday, and event exogenous variables", "Tests whether external operational signals improve forecasting."],
        ["Random Forest Residual", "n_estimators=300, max_features=sqrt, min_samples_leaf=3", "Learns nonlinear residual patterns after SARIMAX forecast."],
        ["RF Sensitivity", "100, 300, and 500 trees", "Tests whether increasing the number of trees improves stability or accuracy."],
        ["Conformal Prediction", "Future lower and upper prediction bounds", "Adds uncertainty-aware planning beyond a single point forecast."],
    ], columns=["Model / Method", "Key Parameters", "Why It Matters"])
    display_dataframe(parameter_strategy)
    st.subheader("Conformal Prediction Roadmap")
    display_dataframe(conformal_roadmap_df)

with tab7:
    st.subheader("Model Results and Improvement Evidence")
    section_card(
        "What Improved and Why",
        "The model improved by moving from a simple historical benchmark to SARIMAX time-series modeling and then to a Hybrid SARIMAX + Random Forest approach that corrects nonlinear residual patterns.",
    )
    clean_model_improvement = model_improvement_df.copy()
    for col in ["MAE", "RMSE", "MAPE"]:
        if col in clean_model_improvement.columns:
            clean_model_improvement[col] = pd.to_numeric(clean_model_improvement[col], errors="coerce").round(2)
    display_dataframe(clean_model_improvement)
    plot_df = clean_model_improvement.dropna(subset=["MAPE"]).copy()
    if not plot_df.empty:
        improvement_fig = px.bar(
            plot_df,
            x="Model",
            y="MAPE",
            color="Model",
            title="Model Improvement Evidence - MAPE Comparison",
            color_discrete_sequence=["#38BDF8", "#8B5CF6", "#22C55E", "#F97316", "#EF4444"],
        )
        improvement_fig.update_xaxes(tickangle=-25)
        improvement_fig = style_plotly(improvement_fig)
        st.plotly_chart(improvement_fig, use_container_width=True)
    st.subheader("Random Forest Sensitivity Analysis: 100 / 300 / 500 Trees")
    rf_clean = rf_sensitivity_df.copy()
    for col in ["MAE", "RMSE", "MAPE", "Approx. Accuracy", "R²"]:
        if col in rf_clean.columns:
            rf_clean[col] = pd.to_numeric(rf_clean[col], errors="coerce").round(2)
    display_dataframe(rf_clean)
    if "Trees" in rf_sensitivity_df.columns and "MAPE" in rf_sensitivity_df.columns:
        rf_fig = px.line(
            rf_sensitivity_df,
            x="Trees",
            y="MAPE",
            color="Target",
            markers=True,
            title="Random Forest Tree Sensitivity - MAPE by Number of Trees",
            color_discrete_sequence=["#38BDF8", "#F97316", "#22C55E"],
        )
        rf_fig = style_plotly(rf_fig)
        st.plotly_chart(rf_fig, use_container_width=True)
    st.subheader("Annual Rolling Backtesting")
    annual_backtest_fig = px.line(
        backtest_df,
        x="date",
        y=["actual_net_sales", "annual_backtest_forecast"],
        title="Actual Net Sales vs Annual Backtested Forecast",
        color_discrete_sequence=["#38BDF8", "#F97316"],
    )
    annual_backtest_fig = style_plotly(annual_backtest_fig)
    st.plotly_chart(annual_backtest_fig, use_container_width=True)
    st.subheader("Monthly Backtesting Metrics")
    backtest_metrics_clean = backtest_metrics_df.copy()
    for col in ["mae", "rmse", "mape", "approx_accuracy", "r2"]:
        if col in backtest_metrics_clean.columns:
            backtest_metrics_clean[col] = backtest_metrics_clean[col].round(2)
    display_dataframe(backtest_metrics_clean)

with tab8:
    st.subheader("Manager Dashboard")
    section_card(
        "Business-Facing Output",
        "After completing the analytical pipeline, the results are translated into this dashboard for restaurant managers and owners. The purpose is to support staffing, menu preparation, promotional timing, and operational readiness.",
    )
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metric_card("Total Sales", format_money(total_sales), "Historical net sales for selected scope", "cyan")
    with k2:
        metric_card("Avg Daily Sales", format_money(avg_daily_sales), "Average daily demand level", "purple")
    with k3:
        metric_card("Total Transactions", format_number(total_transactions), "Customer/order activity volume", "green")
    with k4:
        metric_card("Avg Ticket", format_money_2(avg_ticket), "Average revenue per transaction", "orange")
    k5, k6, k7, k8 = st.columns(4)
    with k5:
        metric_card("Latest Predicted Sales", format_money(latest["hybrid_forecast"]), "Hybrid forecast for latest evaluated date", "cyan")
    with k6:
        metric_card("Latest Forecast Accuracy", f"{latest['hybrid_forecast_accuracy']:.1f}%", "Final holdout accuracy point", "green")
    with k7:
        metric_card("Best Sales Month", best_month["month"], format_money(best_month["monthly_sales"]), "purple")
    with k8:
        metric_card("Lowest Sales Month", worst_month["month"], format_money(worst_month["monthly_sales"]), "orange")
    st.subheader("Annual Restaurant Behavior")
    annual_fig = px.line(annual_df, x="date", y=selected_metric, title=f"Continuous Annual Trend: {selected_metric_label}", color_discrete_sequence=["#38BDF8"])
    annual_fig = style_plotly(annual_fig)
    st.plotly_chart(annual_fig, use_container_width=True)
    monthly_df = annual_df.groupby("month", as_index=False).agg(net_sales=("net_sales", "sum"), transactions_count=("transactions_count", "sum"), average_ticket=("average_ticket", "mean"))
    monthly_fig = px.bar(monthly_df, x="month", y=selected_metric, title=f"Monthly Aggregated View: {selected_metric_label}", color_discrete_sequence=["#8B5CF6"])
    monthly_fig.update_xaxes(tickangle=-45)
    monthly_fig = style_plotly(monthly_fig)
    st.plotly_chart(monthly_fig, use_container_width=True)
    st.subheader("Final Holdout Forecast")
    forecast_fig = px.line(df, x="date", y=["actual_net_sales", "sarimax_forecast", "hybrid_forecast"], title="Actual vs Forecast - Final Holdout Window", color_discrete_sequence=["#38BDF8", "#8B5CF6", "#F97316"])
    forecast_fig = style_plotly(forecast_fig)
    st.plotly_chart(forecast_fig, use_container_width=True)
    st.subheader("Operational Value Added")
    display_dataframe(operational_value_df)

with tab9:
    st.subheader("Team")
    team = pd.DataFrame([
        ["Jessica Orijuela", "Data analysis, documentation, and project support"],
        ["Jhonyfren Moncada Corro", "Data preparation, analysis support, and presentation support"],
        ["María Carolina Aguilar", "Business interpretation, reporting, and research support"],
        ["Sergio Manrique", "Project support, validation, and documentation"],
        ["Reiman Muñoz Chara", "Forecasting engine, KPI dashboard, deployment, and analytics integration"],
    ], columns=["Team Member", "Contribution"])
    display_dataframe(team)
    st.caption("Team contribution descriptions can be adjusted before the final presentation based on the group's official role distribution.")
    st.divider()
    st.subheader("Visitor Feedback")
    section_card(
        "Help Us Evaluate the Portal",
        "Please rate each section from 1 to 5 stars and leave one general comment at the end. In the final version, this can be connected to Google Forms so each response is stored automatically.",
    )
    feedback_sections = ["Project Roadmap", "Research Framework", "Data Pipeline", "Feature Engineering", "Literature & Added Value", "Model Strategy", "Model Results", "Manager Dashboard"]
    ratings = {}
    for section in feedback_sections:
        ratings[section] = st.radio(section, ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True, key=f"rating_{section}")
    comments = st.text_area("Suggestions or Comments", placeholder="Write your suggestions, comments, or recommendations here...", height=150)
    if st.button("Submit Feedback"):
        feedback_summary = pd.DataFrame({"Section": list(ratings.keys()), "Rating": list(ratings.values())})
        st.success("Thank you for your feedback.")
        st.markdown("#### Feedback Summary")
        display_dataframe(feedback_summary)
        if comments.strip():
            st.markdown("#### Visitor Comments")
            st.write(comments)
    st.info("For the final poster version, we can connect this tab to Google Forms or Microsoft Forms so every visitor response is stored permanently.")
