from pathlib import Path
import py_compile
import re
import shutil
import sys

app_path = Path("src/dashboard/capstone_dashboard_app.py")
backup_path = Path("src/dashboard/capstone_dashboard_app_backup_before_data_pipeline_evolution.py")

if not app_path.exists():
    raise FileNotFoundError(f"Dashboard file not found: {app_path}")

shutil.copy2(app_path, backup_path)

text = app_path.read_text(encoding="utf-8")

# ============================================================
# 1. Add data_pipeline_evolution file to DATA_FILES dictionary
# ============================================================

if '"data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",' not in text:
    if '"data_cleaning": DATA_DIR / "data_cleaning_summary.csv",' in text:
        text = text.replace(
            '    "data_cleaning": DATA_DIR / "data_cleaning_summary.csv",',
            '    "data_cleaning": DATA_DIR / "data_cleaning_summary.csv",\n'
            '    "data_pipeline_evolution": DATA_DIR / "data_pipeline_evolution_summary.csv",'
        )
    else:
        print("Could not find data_cleaning entry in DATA_FILES.")
        sys.exit(1)

# ============================================================
# 2. Add data_pipeline_evolution_df variable
# ============================================================

if 'data_pipeline_evolution_df = data["data_pipeline_evolution"]' not in text:
    if 'data_cleaning_df = data["data_cleaning"]' in text:
        text = text.replace(
            'data_cleaning_df = data["data_cleaning"]',
            'data_cleaning_df = data["data_cleaning"]\n'
            'data_pipeline_evolution_df = data["data_pipeline_evolution"]'
        )
    else:
        print("Could not find data_cleaning_df assignment.")
        sys.exit(1)

# ============================================================
# 3. Find Data Pipeline tab block
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
    print("Could not find the next tab after Data Pipeline.")
    sys.exit(1)

end = match.end() + next_match.start()

tab_line = text[start:text.find("\n", start)]

new_data_pipeline_block = f'''{tab_line}
    st.subheader("Data Pipeline")

    section_card(
        "From Raw POS Data to Dashboard-Ready Forecasting Datasets",
        "This section shows how the original restaurant POS exports and external weather data were transformed into clean, daily, model-ready, and dashboard-ready datasets. The goal is to make the data preparation process transparent and avoid confusion between candidate engineered variables and final selected model features.",
    )

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        metric_card(
            "Clean Transactions",
            "39,505",
            "Transaction-level POS records after cleaning",
            "cyan",
        )

    with d2:
        metric_card(
            "Clean Items",
            "138,093",
            "Item-level sales records after cleaning",
            "purple",
        )

    with d3:
        metric_card(
            "Modeling Dataset",
            "474 x 50",
            "Daily POS + calendar + weather + event variables",
            "green",
        )

    with d4:
        metric_card(
            "Enhanced KPI Layer",
            "474 x 115",
            "Candidate engineered variables, not all final model features",
            "orange",
        )

    st.subheader("Data Pipeline Evolution")
    display_dataframe(data_pipeline_evolution_df)

    st.subheader("Data Cleaning and Quality Decisions")
    display_dataframe(data_cleaning_df)

    st.subheader("Key Clarification About the 115 Columns")

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_card(
            "Raw POS Granularity",
            "The original POS exports contained transaction-level, item-level, order-level, and section-level data. These were useful for audit, validation, and business understanding.",
            "cyan",
        )

    with c2:
        insight_card(
            "Modeling Dataset",
            "The main modeling dataset contains 474 daily records and 50 columns after integrating POS, calendar, holiday, weather, event, and seasonality variables.",
            "green",
        )

    with c3:
        insight_card(
            "Enhanced KPI Layer",
            "The 115-column KPI dataset is an expanded candidate feature layer with lags, rolling averages, ratios, and operational indicators. It does not mean all 115 columns were used as final features in every model.",
            "orange",
        )

    st.subheader("Pipeline Interpretation")

    p1, p2 = st.columns(2)

    with p1:
        insight_card(
            "POS Data Preparation",
            "Sales, transactions, refunds, discounts, tips, orders, items, and sections were cleaned and consolidated to move from raw operational records to daily restaurant-level demand data.",
            "purple",
        )

    with p2:
        insight_card(
            "External Weather Integration",
            "Weather data was aligned by date and transformed into daily exposure indicators such as cold hours, hot hours, rain hours, snow hours, fog hours, and haze/smoke hours.",
            "cyan",
        )

'''

text = text[:start] + new_data_pipeline_block + text[end:]

# ============================================================
# 4. Save and validate
# ============================================================

app_path.write_text(text, encoding="utf-8")
py_compile.compile(str(app_path), doraise=True)

print("Data Pipeline tab updated successfully.")
print(f"Backup created: {backup_path}")
print("Syntax check: PASSED")
