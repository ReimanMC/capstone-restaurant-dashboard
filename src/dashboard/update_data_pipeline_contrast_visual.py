from pathlib import Path
import py_compile
import re
import shutil
import sys

APP_PATH = Path("src/dashboard/capstone_dashboard_app.py")
BACKUP_PATH = Path("src/dashboard/capstone_dashboard_app_backup_before_pipeline_contrast_visual.py")

if not APP_PATH.exists():
    raise FileNotFoundError(f"Dashboard file not found: {APP_PATH.resolve()}")

shutil.copy2(APP_PATH, BACKUP_PATH)

text = APP_PATH.read_text(encoding="utf-8")

# ============================================================
# 1. Add data_pipeline_contrast to DATA_FILES dictionary
# ============================================================

if '"data_pipeline_contrast": DATA_DIR / "data_pipeline_contrast_summary.csv",' not in text:
    if '"data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",' in text:
        text = text.replace(
            '    "data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",',
            '    "data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",\n'
            '    "data_pipeline_contrast": DATA_DIR / "data_pipeline_contrast_summary.csv",'
        )
    elif '"data_cleaning": DATA_DIR / "data_cleaning_summary.csv",' in text:
        text = text.replace(
            '    "data_cleaning": DATA_DIR / "data_cleaning_summary.csv",',
            '    "data_cleaning": DATA_DIR / "data_cleaning_summary.csv",\n'
            '    "data_pipeline_contrast": DATA_DIR / "data_pipeline_contrast_summary.csv",'
        )
    else:
        print("Could not find where to add data_pipeline_contrast in DATA_FILES.")
        sys.exit(1)

# ============================================================
# 2. Add data_pipeline_contrast_df variable
# ============================================================

if 'data_pipeline_contrast_df = data["data_pipeline_contrast"]' not in text:
    if 'data_pipeline_evolution_df = data["data_pipeline_evolution"]' in text:
        text = text.replace(
            'data_pipeline_evolution_df = data["data_pipeline_evolution"]',
            'data_pipeline_evolution_df = data["data_pipeline_evolution"]\n'
            'data_pipeline_contrast_df = data["data_pipeline_contrast"]'
        )
    elif 'data_cleaning_df = data["data_cleaning"]' in text:
        text = text.replace(
            'data_cleaning_df = data["data_cleaning"]',
            'data_cleaning_df = data["data_cleaning"]\n'
            'data_pipeline_contrast_df = data["data_pipeline_contrast"]'
        )
    else:
        print("Could not find where to add data_pipeline_contrast_df variable.")
        sys.exit(1)

# ============================================================
# 3. Locate Data Pipeline tab block
# ============================================================

match = re.search(
    r'with tab\d+:\n    st\.subheader\("Data Pipeline"\)',
    text
)

if not match:
    print("Could not find Data Pipeline tab block.")
    sys.exit(1)

start = match.start()

next_match = re.search(
    r'\nwith tab\d+:\n',
    text[match.end():]
)

if not next_match:
    print("Could not find next tab block after Data Pipeline.")
    sys.exit(1)

end = match.end() + next_match.start()
tab_line = text[start:text.find("\n", start)]

# ============================================================
# 4. New visual Data Pipeline block
# ============================================================

new_block = f'''{tab_line}
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
            f"{{initial_records:,}}",
            f"{{initial_columns}} total columns across cleaned POS tables",
            "cyan",
        )

    with c2:
        metric_card(
            "Final Modeling Dataset",
            f"{{modeling_records:,}}",
            f"{{modeling_columns}} forecasting-ready variables",
            "green",
        )

    with c3:
        metric_card(
            "Enhanced KPI Layer",
            f"{{enhanced_records:,}}",
            f"{{enhanced_columns}} candidate engineered variables",
            "purple",
        )

    with c4:
        metric_card(
            "Final Holdout Output",
            f"{{holdout_records:,}}",
            f"{{holdout_columns}} dashboard forecast columns",
            "orange",
        )

    section_card(
        "Important Interpretation",
        "The project did not simply reduce data. It transformed detailed POS records into daily forecasting-ready datasets. The 115-column KPI layer is an expanded candidate feature layer created for experimentation, lags, rolling averages, ratios, and operational indicators. It does not mean that all 115 variables were used as final inputs in every model.",
    )

    chart_records_df = contrast_df.copy()
    chart_records_df["Records Label"] = chart_records_df["Records"].apply(
        lambda x: f"{{int(x):,}}" if pd.notna(x) else ""
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
        lambda x: f"{{int(x):,}}" if pd.notna(x) else ""
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

'''

text = text[:start] + new_block + text[end:]

# ============================================================
# 5. Save and validate
# ============================================================

APP_PATH.write_text(text, encoding="utf-8")
py_compile.compile(str(APP_PATH), doraise=True)

print("Data Pipeline contrast visualization added successfully.")
print(f"Backup created: {BACKUP_PATH}")
print("Syntax check: PASSED")
