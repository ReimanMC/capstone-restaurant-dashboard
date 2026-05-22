from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Capstone Forecast Dashboard",
    layout="wide",
)


REPO_ROOT = Path(__file__).resolve().parents[2]

FINAL_FORECAST_PATH = REPO_ROOT / "data" / "dashboard" / "capstone_dashboard_dataset.csv"
ANNUAL_PATH = REPO_ROOT / "data" / "dashboard" / "annual_sales_dashboard_dataset.csv"
BACKTEST_PATH = REPO_ROOT / "data" / "dashboard" / "annual_backtesting_forecast_dataset.csv"
BACKTEST_METRICS_PATH = REPO_ROOT / "data" / "dashboard" / "annual_backtesting_metrics_dataset.csv"


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
        annual_df["average_ticket"] = annual_df["net_sales"] / annual_df["transactions_count"]

    annual_df["month"] = annual_df["date"].dt.to_period("M").astype(str)

    return final_df, annual_df, backtest_df, backtest_metrics_df


df, annual_df, backtest_df, backtest_metrics_df = load_data()


st.title("Restaurant Forecast Decision Platform")
st.markdown("Forecasting + KPI Engine + Operational Intelligence")


# ============================================================
# Sidebar controls
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

filtered_for_cards = annual_df.copy()

if selected_season != "All":
    filtered_for_cards = filtered_for_cards[
        filtered_for_cards["season"] == selected_season
    ]


# ============================================================
# Executive KPI cards
# ============================================================

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


c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Avg Daily Sales", f"${avg_daily_sales:,.0f}")
c3.metric("Total Transactions", f"{total_transactions:,.0f}")
c4.metric("Avg Ticket", f"${avg_ticket:,.2f}")

c5, c6, c7, c8 = st.columns(4)

c5.metric("Latest Predicted Sales", f"${latest['hybrid_forecast']:,.0f}")
c6.metric("Latest Forecast Accuracy", f"{latest['hybrid_forecast_accuracy']:.1f}%")
c7.metric("Latest Predicted Transactions", f"{latest['predicted_transactions_count']:.0f}")
c8.metric("Latest Predicted Avg Ticket", f"${latest['predicted_average_ticket']:.2f}")

c9, c10, c11, c12 = st.columns(4)

c9.metric(
    "Best Sales Day",
    best_day["date"].strftime("%Y-%m-%d"),
    f"${best_day['net_sales']:,.0f}",
)

c10.metric(
    "Worst Sales Day",
    worst_day["date"].strftime("%Y-%m-%d"),
    f"${worst_day['net_sales']:,.0f}",
)

c11.metric(
    "Best Sales Month",
    best_month["month"],
    f"${best_month['monthly_sales']:,.0f}",
)

c12.metric(
    "Worst Sales Month",
    worst_month["month"],
    f"${worst_month['monthly_sales']:,.0f}",
)

st.divider()


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Annual Behavior",
        "Seasonal Behavior",
        "Annual Backtesting Forecast",
        "Final Holdout Forecast",
        "KPI Engine",
        "Model & Insights",
    ]
)


# ============================================================
# Tab 1 - Annual Behavior
# ============================================================

with tab1:
    st.subheader("Annual Restaurant Behavior")

    st.caption(
        "This section shows the real historical behavior of the restaurant "
        "from January 2025 to April 2026."
    )

    annual_fig = px.line(
        annual_df,
        x="date",
        y=selected_metric,
        title=f"Continuous Annual Trend: {selected_metric_label}",
    )

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
    )

    monthly_fig.update_xaxes(tickangle=-45)

    st.plotly_chart(
        monthly_fig,
        use_container_width=True,
    )

    st.dataframe(
        monthly_df.rename(
            columns={
                "month": "Month",
                "net_sales": "Monthly Net Sales",
                "transactions_count": "Monthly Transactions",
                "average_ticket": "Monthly Avg Ticket",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Tab 2 - Seasonal Behavior
# ============================================================

with tab2:
    st.subheader("Seasonal Behavior Analysis")

    st.caption(
        "This section compares the restaurant performance by season using business KPIs only."
    )

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
        )

        st.plotly_chart(
            season_sales_fig,
            use_container_width=True,
        )

    with s2:
        season_transactions_fig = px.bar(
            seasonal_summary,
            x="season",
            y="avg_transactions",
            title="Average Transactions by Season",
        )

        st.plotly_chart(
            season_transactions_fig,
            use_container_width=True,
        )

    season_ticket_fig = px.bar(
        seasonal_summary,
        x="season",
        y="avg_ticket",
        title="Average Ticket by Season",
    )

    st.plotly_chart(
        season_ticket_fig,
        use_container_width=True,
    )

    st.dataframe(
        seasonal_summary.rename(
            columns={
                "season": "Season",
                "total_sales": "Total Sales",
                "avg_daily_sales": "Avg Daily Sales",
                "total_transactions": "Total Transactions",
                "avg_transactions": "Avg Transactions",
                "avg_ticket": "Avg Ticket",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Tab 3 - Annual Backtesting Forecast
# ============================================================

with tab3:
    st.subheader("Annual Backtesting Forecast")

    st.info(
        "This is not an invented full-year forecast. It is a rolling backtesting forecast: "
        "each validation month was predicted using only previous historical data. "
        "Rolling validation starts in October 2025 because sufficient historical data is required "
        "before forecasting evaluation can begin."
    )

    annual_backtest_fig = px.line(
        backtest_df,
        x="date",
        y=[
            "actual_net_sales",
            "annual_backtest_forecast",
        ],
        title="Actual Net Sales vs Annual Backtested Forecast",
    )

    st.plotly_chart(
        annual_backtest_fig,
        use_container_width=True,
    )

    backtest_error_fig = px.bar(
        backtest_df,
        x="date",
        y="forecast_error",
        color="validation_month",
        title="Annual Backtesting Forecast Error",
    )

    st.plotly_chart(
        backtest_error_fig,
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
        "the explanatory performance for that monthly validation window."
    )

    st.dataframe(
        clean_metrics,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Tab 4 - Final Holdout Forecast
# ============================================================

with tab4:
    st.subheader("Final 30-Day Holdout Forecast")

    st.info(
        "This section shows the final 30-day holdout window used for the strongest model comparison. "
        "It should not be interpreted as a full-year forecast."
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
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True,
    )

    accuracy_fig = px.line(
        df,
        x="date",
        y="hybrid_forecast_accuracy",
        title="Hybrid Forecast Accuracy Trend",
    )

    st.plotly_chart(
        accuracy_fig,
        use_container_width=True,
    )


# ============================================================
# Tab 5 - KPI Engine
# ============================================================

with tab5:
    st.subheader("KPI Forecast Engine")

    st.info(
        "The KPI forecast engine currently evaluates the final 30-day holdout window. "
        "Annual KPI behavior is shown in the Annual Behavior tab, while KPI forecasting performance "
        "is shown here for the final evaluated period."
    )

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

    st.subheader("Monthly KPI Forecast Summary")

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
        )

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
        )

        st.plotly_chart(
            monthly_ticket_fig,
            use_container_width=True,
        )

    monthly_kpi_sales_fig = px.bar(
        kpi_monthly,
        x="month",
        y=[
            "actual_kpi_net_sales",
            "predicted_kpi_net_sales",
        ],
        title="Monthly Actual vs Predicted KPI-Based Net Sales",
        barmode="group",
    )

    st.plotly_chart(
        monthly_kpi_sales_fig,
        use_container_width=True,
    )

    st.dataframe(
        kpi_monthly.rename(
            columns={
                "month": "Month",
                "actual_transactions_count": "Actual Transactions",
                "predicted_transactions_count": "Predicted Transactions",
                "actual_average_ticket": "Actual Avg Ticket",
                "predicted_average_ticket": "Predicted Avg Ticket",
                "actual_kpi_net_sales": "Actual KPI Net Sales",
                "predicted_kpi_net_sales": "Predicted KPI Net Sales",
            }
        ).round(2),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Tab 6 - Model & Insights
# ============================================================

with tab6:
    st.subheader("Model Performance Summary")

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

    st.subheader("Operational Intelligence Findings")

    findings = pd.DataFrame(
        [
            [
                "Hybrid model improved sales forecasting",
                "MAPE reduced from 22.48% to 16.20%",
                "Better forecast quality for planning",
                "Use hybrid model as main sales forecast engine",
            ],
            [
                "January 2026 instability detected",
                "Monthly rolling validation showed 107.14% MAPE",
                "Winter demand behaves differently",
                "Develop winter-aware forecasting improvements",
            ],
            [
                "Cold and snow affect demand",
                "January had higher cold and snow exposure than March",
                "Weather conditions influence customer traffic",
                "Expand weather-adjusted operational planning",
            ],
            [
                "RF tree sensitivity validated",
                "100, 300, and 500 trees showed similar performance",
                "300 trees balances accuracy and speed",
                "Standardize Random Forest using 300 trees",
            ],
            [
                "KPI engine is operational",
                "Transactions, Average Ticket, and KPI sales were predicted",
                "Management can monitor demand drivers",
                "Integrate KPI engine into final dashboard",
            ],
        ],
        columns=[
            "Finding",
            "Evidence",
            "Business Meaning",
            "Next Action",
        ],
    )

    st.dataframe(
        findings,
        use_container_width=True,
        hide_index=True,
    )