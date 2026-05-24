from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Restaurant Forecast Intelligence Platform",
    layout="wide",
)


# ============================================================
# Premium Dark Theme CSS
# ============================================================

st.markdown(
    """
<style>

/* ---------- Main App ---------- */
.stApp {
    background: radial-gradient(circle at top left, #111827 0%, #070B16 45%, #020617 100%);
    color: #F8FAFC;
}

/* ---------- Hide Streamlit Decoration ---------- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0F172A 100%);
    border-right: 1px solid rgba(139, 92, 246, 0.35);
}

/* ---------- Global Text ---------- */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC;
}

p, li, span {
    color: #CBD5E1;
}

/* ---------- Header ---------- */
.main-title {
    font-size: 44px;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 6px;
    background: linear-gradient(90deg, #38BDF8, #8B5CF6, #F97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-subtitle {
    font-size: 17px;
    color: #CBD5E1;
    margin-bottom: 18px;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    background: #111827;
    color: #E5E7EB;
    border-radius: 14px 14px 0px 0px;
    margin-right: 8px;
    padding: 14px 20px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    font-weight: 700;
    transition: all 0.25s ease;
}

button[data-baseweb="tab"]:hover {
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.85), rgba(6, 182, 212, 0.85));
    color: white;
    transform: translateY(-2px);
}

button[aria-selected="true"] {
    background: linear-gradient(90deg, #8B5CF6, #06B6D4) !important;
    color: white !important;
    border-bottom: 3px solid #F97316 !important;
}

/* ---------- KPI Cards ---------- */
.metric-card {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.98), rgba(30, 41, 59, 0.92));
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 22px;
    padding: 22px;
    min-height: 150px;
    box-shadow: 0 12px 30px rgba(2, 6, 23, 0.45);
    transition: 0.25s ease;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 28px rgba(6, 182, 212, 0.25);
    border: 1px solid rgba(6, 182, 212, 0.35);
}

.metric-card::before {
    content: "";
    position: absolute;
    top: -35px;
    right: -35px;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    opacity: 0.24;
}

.metric-card.cyan::before { background: #06B6D4; }
.metric-card.purple::before { background: #8B5CF6; }
.metric-card.green::before { background: #22C55E; }
.metric-card.orange::before { background: #F97316; }
.metric-card.red::before { background: #EF4444; }

.metric-label {
    color: #94A3B8;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.metric-value {
    font-size: 34px;
    font-weight: 900;
    margin-top: 8px;
    margin-bottom: 6px;
}

.metric-note {
    color: #CBD5E1;
    font-size: 14px;
}

.metric-accent-cyan { color: #38BDF8; }
.metric-accent-purple { color: #A78BFA; }
.metric-accent-green { color: #22C55E; }
.metric-accent-orange { color: #FB923C; }
.metric-accent-red { color: #F87171; }

/* ---------- Section Cards ---------- */
.section-card {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.98), rgba(17, 24, 39, 0.94));
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 22px;
    padding: 24px 26px;
    margin: 14px 0 22px 0;
    box-shadow: 0 10px 26px rgba(2, 6, 23, 0.35);
}

.section-title {
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 8px;
    color: #F8FAFC;
}

.section-text {
    color: #CBD5E1;
    font-size: 16px;
    line-height: 1.65;
}

/* ---------- Insight Cards ---------- */
.insight-card {
    background: rgba(15, 23, 42, 0.96);
    border-left: 5px solid #06B6D4;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 22px rgba(2, 6, 23, 0.30);
}

.insight-card.green-border { border-left-color: #22C55E; }
.insight-card.orange-border { border-left-color: #F97316; }
.insight-card.red-border { border-left-color: #EF4444; }
.insight-card.purple-border { border-left-color: #8B5CF6; }

.insight-title {
    font-size: 18px;
    font-weight: 900;
    color: #F8FAFC;
    margin-bottom: 6px;
}

.insight-text {
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.55;
}

/* ---------- Badges ---------- */
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-right: 8px;
    margin-bottom: 8px;
}

.badge-cyan {
    background: rgba(6, 182, 212, 0.16);
    color: #67E8F9;
    border: 1px solid rgba(6, 182, 212, 0.35);
}

.badge-purple {
    background: rgba(139, 92, 246, 0.16);
    color: #C4B5FD;
    border: 1px solid rgba(139, 92, 246, 0.35);
}

.badge-green {
    background: rgba(34, 197, 94, 0.16);
    color: #86EFAC;
    border: 1px solid rgba(34, 197, 94, 0.35);
}

.badge-orange {
    background: rgba(249, 115, 22, 0.16);
    color: #FDBA74;
    border: 1px solid rgba(249, 115, 22, 0.35);
}

/* ---------- Charts and Tables ---------- */
[data-testid="stPlotlyChart"] {
    background: rgba(15, 23, 42, 0.58);
    border-radius: 20px;
    padding: 12px;
    border: 1px solid rgba(148, 163, 184, 0.10);
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.14);
}

.stAlert {
    border-radius: 18px;
}

.stButton > button {
    background: linear-gradient(90deg, #8B5CF6, #06B6D4);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 10px 22px;
    font-weight: 800;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #06B6D4, #F97316);
    color: white;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# File Paths
# ============================================================

REPO_ROOT = Path(__file__).resolve().parents[2]

FINAL_FORECAST_PATH = REPO_ROOT / "data" / "dashboard" / "capstone_dashboard_dataset.csv"
ANNUAL_PATH = REPO_ROOT / "data" / "dashboard" / "annual_sales_dashboard_dataset.csv"
BACKTEST_PATH = REPO_ROOT / "data" / "dashboard" / "annual_backtesting_forecast_dataset.csv"
BACKTEST_METRICS_PATH = REPO_ROOT / "data" / "dashboard" / "annual_backtesting_metrics_dataset.csv"


# ============================================================
# Data Loading
# ============================================================

@st.cache_data
def load_data():
    final_df = pd.read_csv(FINAL_FORECAST_PATH)
    annual_df = pd.read_csv(ANNUAL_PATH)
    backtest_df = pd.read_csv(BACKTEST_PATH)
    backtest_metrics_df = pd.read_csv(BACKTEST_METRICS_PATH)

    final_df["date"] = pd.to_datetime(final_df["date"])
    annual_df["date"] = pd.to_datetime(annual_df["date"])
    backtest_df["date"] = pd.to_datetime(backtest_df["date"])

    if "average_ticket" not in annual_df.columns:
        annual_df["average_ticket"] = (
            annual_df["net_sales"] / annual_df["transactions_count"]
        )

    annual_df["average_ticket"] = annual_df["average_ticket"].fillna(0)
    annual_df["month"] = annual_df["date"].dt.to_period("M").astype(str)

    return final_df, annual_df, backtest_df, backtest_metrics_df


df, annual_df, backtest_df, backtest_metrics_df = load_data()


# ============================================================
# Helper Functions
# ============================================================

def format_money(value):
    return f"${value:,.0f}"


def format_money_2(value):
    return f"${value:,.2f}"


def format_number(value):
    return f"{value:,.0f}"


def metric_card(label, value, note="", color="cyan"):
    accent_class = f"metric-accent-{color}"

    st.markdown(
        f"""
        <div class="metric-card {color}">
            <div class="metric-label">{label}</div>
            <div class="metric-value {accent_class}">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title, text):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title, text, border="cyan"):
    border_class = ""

    if border == "green":
        border_class = "green-border"
    elif border == "orange":
        border_class = "orange-border"
    elif border == "red":
        border_class = "red-border"
    elif border == "purple":
        border_class = "purple-border"

    st.markdown(
        f"""
        <div class="insight-card {border_class}">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",
        font=dict(color="#E5E7EB"),
        title_font=dict(color="#F8FAFC", size=20),
        legend=dict(
            bgcolor="rgba(15,23,42,0)",
            bordercolor="rgba(148,163,184,0.15)",
        ),
        margin=dict(l=20, r=20, t=60, b=40),
    )

    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.16)",
        zerolinecolor="rgba(148,163,184,0.25)",
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.16)",
        zerolinecolor="rgba(148,163,184,0.25)",
    )

    return fig


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="main-title">Restaurant Forecast Intelligence Platform</div>
    <div class="main-subtitle">
        Short-Term Demand Forecasting + KPI Engine + Operational Intelligence using real POS data from Twisted Bar.
    </div>
    <span class="badge badge-cyan">Real POS Data</span>
    <span class="badge badge-purple">SARIMAX + Random Forest</span>
    <span class="badge badge-green">Rolling Backtesting</span>
    <span class="badge badge-orange">Executive Decision Support</span>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar Controls
# ============================================================

st.sidebar.header("Dashboard Controls")

metric_options = {
    "Net Sales": "net_sales",
    "Transactions Count": "transactions_count",
    "Average Ticket": "average_ticket",
}

selected_metric_label = st.sidebar.selectbox(
    "Select Annual KPI",
    list(metric_options.keys()),
)

selected_metric = metric_options[selected_metric_label]

season_options = ["All"] + sorted(annual_df["season"].dropna().unique().tolist())

selected_season = st.sidebar.selectbox(
    "Filter KPI Cards",
    season_options,
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "This dashboard is designed as an executive analytics layer for the Capstone project."
)


# ============================================================
# Main Metrics Preparation
# ============================================================

filtered_for_cards = annual_df.copy()

if selected_season != "All":
    filtered_for_cards = filtered_for_cards[
        filtered_for_cards["season"] == selected_season
    ]

latest = df.iloc[-1]

total_sales = filtered_for_cards["net_sales"].sum()
avg_daily_sales = filtered_for_cards["net_sales"].mean()
total_transactions = filtered_for_cards["transactions_count"].sum()
avg_transactions = filtered_for_cards["transactions_count"].mean()
avg_ticket = filtered_for_cards["average_ticket"].mean()

best_day = filtered_for_cards.loc[filtered_for_cards["net_sales"].idxmax()]
worst_day = filtered_for_cards.loc[filtered_for_cards["net_sales"].idxmin()]

monthly_sales_for_cards = (
    filtered_for_cards
    .groupby("month", as_index=False)
    .agg(monthly_sales=("net_sales", "sum"))
)

best_month = monthly_sales_for_cards.loc[
    monthly_sales_for_cards["monthly_sales"].idxmax()
]

worst_month = monthly_sales_for_cards.loc[
    monthly_sales_for_cards["monthly_sales"].idxmin()
]


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Executive Dashboard",
        "Forecast Models",
        "Operational Intelligence",
        "Project Overview",
        "Methodology",
        "Limitations & Future Work",
        "Team",
        "Visitor Feedback",
    ]
)


# ============================================================
# Tab 1 - Executive Dashboard
# ============================================================

with tab1:
    st.subheader("Executive Dashboard")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        metric_card(
            "Total Sales",
            format_money(total_sales),
            "Historical net sales for selected scope",
            "cyan",
        )

    with k2:
        metric_card(
            "Avg Daily Sales",
            format_money(avg_daily_sales),
            "Average daily demand level",
            "purple",
        )

    with k3:
        metric_card(
            "Total Transactions",
            format_number(total_transactions),
            "Customer/order activity volume",
            "green",
        )

    with k4:
        metric_card(
            "Avg Ticket",
            format_money_2(avg_ticket),
            "Average revenue per transaction",
            "orange",
        )

    k5, k6, k7, k8 = st.columns(4)

    with k5:
        metric_card(
            "Latest Predicted Sales",
            format_money(latest["hybrid_forecast"]),
            "Hybrid forecast for latest evaluated date",
            "cyan",
        )

    with k6:
        metric_card(
            "Latest Forecast Accuracy",
            f"{latest['hybrid_forecast_accuracy']:.1f}%",
            "Final holdout accuracy point",
            "green",
        )

    with k7:
        metric_card(
            "Predicted Transactions",
            f"{latest['predicted_transactions_count']:.0f}",
            "KPI forecast engine output",
            "purple",
        )

    with k8:
        metric_card(
            "Predicted Avg Ticket",
            format_money_2(latest["predicted_average_ticket"]),
            "Revenue-per-transaction forecast",
            "orange",
        )

    k9, k10, k11, k12 = st.columns(4)

    with k9:
        metric_card(
            "Best Sales Day",
            best_day["date"].strftime("%Y-%m-%d"),
            format_money(best_day["net_sales"]),
            "green",
        )

    with k10:
        metric_card(
            "Lowest Sales Day",
            worst_day["date"].strftime("%Y-%m-%d"),
            format_money(worst_day["net_sales"]),
            "red",
        )

    with k11:
        metric_card(
            "Best Sales Month",
            best_month["month"],
            format_money(best_month["monthly_sales"]),
            "cyan",
        )

    with k12:
        metric_card(
            "Lowest Sales Month",
            worst_month["month"],
            format_money(worst_month["monthly_sales"]),
            "orange",
        )

    st.divider()

    st.subheader("Annual Restaurant Behavior")

    annual_fig = px.line(
        annual_df,
        x="date",
        y=selected_metric,
        title=f"Continuous Annual Trend: {selected_metric_label}",
        color_discrete_sequence=["#38BDF8"],
    )

    annual_fig = style_plotly(annual_fig)

    st.plotly_chart(
        annual_fig,
        use_container_width=True,
    )

    monthly_df = (
        annual_df
        .groupby("month", as_index=False)
        .agg(
            net_sales=("net_sales", "sum"),
            transactions_count=("transactions_count", "sum"),
            average_ticket=("average_ticket", "mean"),
        )
    )

    monthly_fig = px.bar(
        monthly_df,
        x="month",
        y=selected_metric,
        title=f"Monthly Aggregated View: {selected_metric_label}",
        color_discrete_sequence=["#8B5CF6"],
    )

    monthly_fig.update_xaxes(tickangle=-45)
    monthly_fig = style_plotly(monthly_fig)

    st.plotly_chart(
        monthly_fig,
        use_container_width=True,
    )

    st.subheader("Seasonal Business Summary")

    seasonal_summary = (
        annual_df.groupby("season", as_index=False)
        .agg(
            total_sales=("net_sales", "sum"),
            avg_daily_sales=("net_sales", "mean"),
            total_transactions=("transactions_count", "sum"),
            avg_transactions=("transactions_count", "mean"),
            avg_ticket=("average_ticket", "mean"),
        )
    )

    s1, s2 = st.columns(2)

    with s1:
        season_sales_fig = px.bar(
            seasonal_summary,
            x="season",
            y="total_sales",
            title="Total Sales by Season",
            color="season",
            color_discrete_sequence=["#06B6D4", "#8B5CF6", "#22C55E", "#F97316"],
        )

        season_sales_fig = style_plotly(season_sales_fig)

        st.plotly_chart(
            season_sales_fig,
            use_container_width=True,
        )

    with s2:
        season_ticket_fig = px.bar(
            seasonal_summary,
            x="season",
            y="avg_ticket",
            title="Average Ticket by Season",
            color="season",
            color_discrete_sequence=["#F97316", "#06B6D4", "#22C55E", "#8B5CF6"],
        )

        season_ticket_fig = style_plotly(season_ticket_fig)

        st.plotly_chart(
            season_ticket_fig,
            use_container_width=True,
        )


# ============================================================
# Tab 2 - Forecast Models
# ============================================================

with tab2:
    st.subheader("Forecast Models")

    section_card(
        "Transparent Forecasting Strategy",
        "This section separates model comparison, rolling backtesting, and final holdout evaluation. "
        "The annual forecast shown here is based on rolling backtesting, not an invented future forecast. "
        "Each validation month is predicted using only previous historical data.",
    )

    model_summary = pd.DataFrame(
        [
            ["Seasonal Naive Baseline", "Net Sales", "22.48%", "77.52%", "Baseline"],
            ["SARIMAX Basic", "Net Sales", "18.50%", "81.50%", "Improved"],
            ["Hybrid SARIMAX + RF Residual", "Net Sales", "16.20%", "83.80%", "Best Sales Forecast Model"],
            ["RF Transactions Forecast", "Transactions Count", "20.20%", "79.80%", "KPI Engine"],
            ["RF Average Ticket Forecast", "Average Ticket", "10.40%", "89.60%", "Best KPI Prediction"],
            ["KPI-Based Net Sales Forecast", "Net Sales", "20.99%", "79.01%", "Explainable KPI Model"],
        ],
        columns=[
            "Model",
            "Target",
            "MAPE",
            "Approx. Accuracy",
            "Status",
        ],
    )

    st.dataframe(
        model_summary,
        use_container_width=True,
        hide_index=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_card(
            "SARIMAX",
            "Captures time-series behavior, seasonality, and temporal structure. It is interpretable and aligned with short-term forecasting.",
            "cyan",
        )

    with c2:
        insight_card(
            "Random Forest",
            "Captures nonlinear operational patterns and residual behavior that may not be fully explained by a statistical model.",
            "purple",
        )

    with c3:
        insight_card(
            "Hybrid Model",
            "Combines SARIMAX structure with Random Forest residual learning, improving forecasting quality while preserving operational interpretation.",
            "green",
        )

    st.subheader("Annual Backtesting Forecast")

    annual_backtest_fig = px.line(
        backtest_df,
        x="date",
        y=[
            "actual_net_sales",
            "annual_backtest_forecast",
        ],
        title="Actual Net Sales vs Annual Backtested Forecast",
        color_discrete_sequence=["#38BDF8", "#F97316"],
    )

    annual_backtest_fig = style_plotly(annual_backtest_fig)

    st.plotly_chart(
        annual_backtest_fig,
        use_container_width=True,
    )

    clean_metrics = backtest_metrics_df.rename(
        columns={
            "validation_month": "Validation Month",
            "records": "Records",
            "mae": "MAE",
            "rmse": "RMSE",
            "mape": "MAPE",
            "approx_accuracy": "Approx. Accuracy",
            "r2": "R²",
        }
    )

    clean_metrics["MAPE"] = clean_metrics["MAPE"].round(2)
    clean_metrics["Approx. Accuracy"] = clean_metrics["Approx. Accuracy"].round(2)
    clean_metrics["MAE"] = clean_metrics["MAE"].round(2)
    clean_metrics["RMSE"] = clean_metrics["RMSE"].round(2)
    clean_metrics["R²"] = clean_metrics["R²"].round(3)

    st.subheader("Monthly Backtesting Metrics")

    st.caption(
        "Each row represents one validation month. MAE and RMSE are dollar-based error metrics, "
        "MAPE is percentage error, Approx. Accuracy is calculated as 100 - MAPE, and R² shows "
        "monthly explanatory performance."
    )

    st.dataframe(
        clean_metrics,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Final 30-Day Holdout Forecast")

    section_card(
        "Final Holdout Evaluation",
        "This section shows the final 30-day holdout window used for model comparison. "
        "It should not be interpreted as a full-year forecast.",
    )

    forecast_fig = px.line(
        df,
        x="date",
        y=[
            "actual_net_sales",
            "sarimax_forecast",
            "hybrid_forecast",
        ],
        title="Actual vs Forecast - Final Holdout Window",
        color_discrete_sequence=["#38BDF8", "#8B5CF6", "#F97316"],
    )

    forecast_fig = style_plotly(forecast_fig)

    st.plotly_chart(
        forecast_fig,
        use_container_width=True,
    )


# ============================================================
# Tab 3 - Operational Intelligence
# ============================================================

with tab3:
    st.subheader("Operational Intelligence")

    section_card(
        "From Prediction to Decision Support",
        "This section translates forecasting results into practical restaurant planning insights. "
        "The current version focuses on demand forecasting, KPI interpretation, and prescriptive planning logic.",
    )

    r1, r2 = st.columns(2)

    with r1:
        insight_card(
            "High-Demand Planning",
            "When forecasted demand increases significantly, the restaurant should prepare additional staff coverage and inventory readiness.",
            "green",
        )

        insight_card(
            "Winter Volatility",
            "January 2026 showed unstable forecasting behavior. Conservative planning is recommended during winter periods.",
            "orange",
        )

        insight_card(
            "Weekend Demand Signal",
            "Friday to Sunday should be prioritized for staffing and preparation planning due to stronger operational demand.",
            "cyan",
        )

    with r2:
        insight_card(
            "Average Ticket Stability",
            "Average ticket forecasting performed strongly and can be used as a revenue-per-transaction planning indicator.",
            "purple",
        )

        insight_card(
            "Forecast Risk Awareness",
            "Avoid using a single 30-day result as the only decision input. Rolling validation gives a more reliable view of model stability.",
            "orange",
        )

        insight_card(
            "Future Labor KPI Layer",
            "Once payroll data is available, the platform should include Labor Cost %, Sales per Labor Dollar, and Profit After Labor.",
            "red",
        )

    st.subheader("KPI Forecast Engine")

    kpi_monthly = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(
            actual_transactions_count=("actual_transactions_count", "sum"),
            predicted_transactions_count=("predicted_transactions_count", "sum"),
            actual_average_ticket=("actual_average_ticket", "mean"),
            predicted_average_ticket=("predicted_average_ticket", "mean"),
            actual_kpi_net_sales=("actual_kpi_net_sales", "sum"),
            predicted_kpi_net_sales=("predicted_kpi_net_sales", "sum"),
        )
    )

    k1, k2 = st.columns(2)

    with k1:
        monthly_transactions_fig = px.bar(
            kpi_monthly,
            x="month",
            y=[
                "actual_transactions_count",
                "predicted_transactions_count",
            ],
            title="Monthly Actual vs Predicted Transactions",
            barmode="group",
            color_discrete_sequence=["#38BDF8", "#8B5CF6"],
        )

        monthly_transactions_fig = style_plotly(monthly_transactions_fig)

        st.plotly_chart(
            monthly_transactions_fig,
            use_container_width=True,
        )

    with k2:
        monthly_ticket_fig = px.bar(
            kpi_monthly,
            x="month",
            y=[
                "actual_average_ticket",
                "predicted_average_ticket",
            ],
            title="Monthly Actual vs Predicted Average Ticket",
            barmode="group",
            color_discrete_sequence=["#22C55E", "#F97316"],
        )

        monthly_ticket_fig = style_plotly(monthly_ticket_fig)

        st.plotly_chart(
            monthly_ticket_fig,
            use_container_width=True,
        )


# ============================================================
# Tab 4 - Project Overview
# ============================================================

with tab4:
    st.subheader("Project Overview")

    p1, p2 = st.columns(2)

    with p1:
        section_card(
            "Problem Gap",
            "Restaurant POS systems such as Square, Toast, and similar platforms are strong at recording "
            "transactions, orders, payments, and historical reports. However, they provide limited predictive "
            "support for short-term operational planning.",
        )

        section_card(
            "Project Objective",
            "The objective of this Capstone project is to analyze demand patterns and evaluate short-term "
            "forecasting approaches using real POS data from Twisted Bar, with the purpose of supporting "
            "practical operational planning.",
        )

    with p2:
        section_card(
            "Current MVP Scope",
            "The original group proposal considered Twisted Bar and Chile & Agave. The current dashboard "
            "focuses on Twisted Bar because this location has the most complete dataset for full-year analysis. "
            "Chile & Agave remains a future extension because its currently available dataset covers only a partial operational window.",
        )

        section_card(
            "Proposed Solution",
            "The project delivers a Restaurant Forecast Intelligence Platform that combines historical POS analytics, "
            "short-term demand forecasting, rolling backtesting validation, KPI forecasting, model comparison, "
            "operational recommendations, and a deployed interactive dashboard.",
        )

    section_card(
        "Business Value",
        "The dashboard supports more proactive decision-making by helping restaurant stakeholders understand demand behavior, "
        "model reliability, seasonal patterns, and planning opportunities for staffing, menu preparation, and promotional timing.",
    )


# ============================================================
# Tab 5 - Methodology
# ============================================================

with tab5:
    st.subheader("Methodology")

    methodology = pd.DataFrame(
        [
            ["1", "Data Collection", "Real POS data exported from restaurant operations"],
            ["2", "Data Cleaning", "Standardization, missing value checks, and validation"],
            ["3", "Exploratory Data Analysis", "Temporal, seasonal, and operational demand patterns"],
            ["4", "Feature Engineering", "Calendar, lag, rolling, seasonality, and operational indicators"],
            ["5", "Forecast Modeling", "Baseline, SARIMAX, Random Forest, and Hybrid model testing"],
            ["6", "Model Evaluation", "MAE, RMSE, MAPE, R², holdout testing, and rolling validation"],
            ["7", "Decision Support", "Dashboard, KPI interpretation, and operational recommendations"],
        ],
        columns=[
            "Step",
            "Phase",
            "Description",
        ],
    )

    st.dataframe(
        methodology,
        use_container_width=True,
        hide_index=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        insight_card(
            "Analytics Pipeline",
            "POS Data → Cleaning → EDA → Feature Engineering → Forecast Models → Validation → Recommendations → Dashboard",
            "cyan",
        )

    with m2:
        insight_card(
            "Validation Strategy",
            "The project uses final 30-day holdout validation and rolling monthly backtesting to avoid overclaiming model performance.",
            "green",
        )

    with m3:
        insight_card(
            "Evaluation Metrics",
            "Forecast performance is evaluated using MAE, RMSE, MAPE, Approx. Accuracy, and R².",
            "purple",
        )


# ============================================================
# Tab 6 - Limitations & Future Work
# ============================================================

with tab6:
    st.subheader("Limitations & Future Work")

    limitations = pd.DataFrame(
        [
            [
                "Single-location MVP",
                "The deployed dashboard currently focuses on Twisted Bar because it has the most complete dataset.",
                "Extend the platform to Chile & Agave once a full-year dataset is available.",
            ],
            [
                "Labor cost KPI not yet integrated",
                "Payroll and staff cost data are not currently included in the dashboard.",
                "Add Labor Cost %, Sales per Labor Dollar, and Profit After Labor once reliable payroll data is available.",
            ],
            [
                "KPI forecast limited to final evaluation period",
                "The current KPI forecast engine evaluates the final holdout window.",
                "Develop annual KPI backtesting and future KPI forecasting.",
            ],
            [
                "External variables",
                "Weather and event signals were explored, but not all external drivers are fully optimized.",
                "Expand weather, holidays, events, and promotion variables.",
            ],
            [
                "Prescriptive analytics layer",
                "Current recommendations are rule-based and interpretation-driven.",
                "Build a stronger recommendation engine for staffing, inventory, and promotion planning.",
            ],
        ],
        columns=[
            "Limitation",
            "Current Status",
            "Future Improvement",
        ],
    )

    st.dataframe(
        limitations,
        use_container_width=True,
        hide_index=True,
    )

    insight_card(
        "Important Academic Positioning",
        "These limitations are not weaknesses of the project; they demonstrate transparency and define a realistic roadmap for turning the Capstone into a scalable restaurant analytics platform.",
        "green",
    )


# ============================================================
# Tab 7 - Team
# ============================================================

with tab7:
    st.subheader("Team")

    team = pd.DataFrame(
        [
            ["Jessica Orijuela", "Data analysis, documentation, and project support"],
            ["Jhonyfren Moncada Corro", "Data preparation, analysis support, and presentation support"],
            ["María Carolina Aguilar", "Business interpretation, reporting, and research support"],
            ["Sergio Manrique", "Project support, validation, and documentation"],
            ["Reiman Muñoz Chara", "Forecasting engine, KPI dashboard, deployment, and analytics integration"],
        ],
        columns=[
            "Team Member",
            "Contribution",
        ],
    )

    st.dataframe(
        team,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Team contribution descriptions can be adjusted before the final presentation based on the group's official role distribution."
    )


# ============================================================
# Tab 8 - Visitor Feedback
# ============================================================

with tab8:
    st.subheader("Visitor Feedback")

    section_card(
        "Help Us Evaluate the Dashboard",
        "We would like to collect feedback from visitors, classmates, instructors, and stakeholders. "
        "Please rate each section from 1 to 5 stars and leave one general comment at the end. "
        "In the next iteration, this section can be connected to Google Forms or Microsoft Forms so responses are stored automatically.",
    )

    st.markdown("### Rate Each Section")

    executive_rating = st.radio(
        "Executive Dashboard",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="executive_rating"
    )

    forecast_rating = st.radio(
        "Forecast Models",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="forecast_rating"
    )

    operational_rating = st.radio(
        "Operational Intelligence",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="operational_rating"
    )

    overview_rating = st.radio(
        "Project Overview",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="overview_rating"
    )

    methodology_rating = st.radio(
        "Methodology",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="methodology_rating"
    )

    limitations_rating = st.radio(
        "Limitations & Future Work",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="limitations_rating"
    )

    team_rating = st.radio(
        "Team",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True,
        key="team_rating"
    )

    st.markdown("### Suggestions or Comments")

    comments = st.text_area(
        "Write your general feedback here",
        placeholder="Write your suggestions, comments, or recommendations here...",
        height=150,
    )

    if st.button("Submit Feedback"):
        feedback_summary = pd.DataFrame(
            {
                "Section": [
                    "Executive Dashboard",
                    "Forecast Models",
                    "Operational Intelligence",
                    "Project Overview",
                    "Methodology",
                    "Limitations & Future Work",
                    "Team",
                ],
                "Rating": [
                    executive_rating,
                    forecast_rating,
                    operational_rating,
                    overview_rating,
                    methodology_rating,
                    limitations_rating,
                    team_rating,
                ],
            }
        )

        st.success("Thank you for your feedback.")

        st.markdown("#### Feedback Summary")
        st.dataframe(feedback_summary, use_container_width=True, hide_index=True)

        if comments.strip():
            st.markdown("#### Visitor Comments")
            st.write(comments)

    st.info(
        "For the final poster version, this feedback tab can later be connected to Google Forms, Microsoft Forms, or a database so all visitor responses are stored automatically."
    )