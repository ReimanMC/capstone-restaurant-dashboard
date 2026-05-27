from pathlib import Path
import py_compile
import re
import shutil
import sys

APP_PATH = Path("src/dashboard/capstone_dashboard_app.py")
BACKUP_PATH = Path("src/dashboard/capstone_dashboard_app_backup_before_literature_matrix.py")

if not APP_PATH.exists():
    raise FileNotFoundError(f"Dashboard file not found: {APP_PATH.resolve()}")

shutil.copy2(APP_PATH, BACKUP_PATH)

text = APP_PATH.read_text(encoding="utf-8")

# ============================================================
# 1. Add new literature tables to DATA_FILES dictionary
# ============================================================

if '"literature_implementation_results": DATA_DIR / "literature_implementation_results_matrix.csv",' not in text:
    marker = '    "literature_added_value": DATA_DIR / "literature_added_value_summary.csv",'
    if marker not in text:
        print("Could not find literature_added_value entry in DATA_FILES.")
        sys.exit(1)

    text = text.replace(
        marker,
        marker + '\n'
        '    "literature_implementation_results": DATA_DIR / "literature_implementation_results_matrix.csv",\n'
        '    "methodological_improvement": DATA_DIR / "methodological_improvement_summary.csv",'
    )

# ============================================================
# 2. Add dataframe variables after literature_added_value_df
# ============================================================

if 'literature_implementation_results_df = data["literature_implementation_results"]' not in text:
    marker = 'literature_added_value_df = data["literature_added_value"]'
    if marker not in text:
        print("Could not find literature_added_value_df assignment.")
        sys.exit(1)

    text = text.replace(
        marker,
        marker + '\n'
        'literature_implementation_results_df = data["literature_implementation_results"]\n'
        'methodological_improvement_df = data["methodological_improvement"]'
    )

# ============================================================
# 3. Locate Literature tab block
# ============================================================

match = re.search(
    r'with tab\d+:\n    st\.subheader\("Literature Gap & Our Added Value"\)',
    text
)

if not match:
    match = re.search(
        r'with tab\d+:\n    st\.subheader\("Literature.*?"\)',
        text
    )

if not match:
    print("Could not find the Literature tab block.")
    sys.exit(1)

start = match.start()

next_match = re.search(
    r'\nwith tab\d+:\n',
    text[match.end():]
)

if not next_match:
    print("Could not find the next tab after Literature.")
    sys.exit(1)

end = match.end() + next_match.start()
tab_line = text[start:text.find("\n", start)]

# ============================================================
# 4. Replace Literature tab content
# ============================================================

new_block = f'''{tab_line}
    st.subheader("Literature Gap & Our Contribution")

    section_card(
        "From Academic Literature to Project Implementation",
        "This section explains how the reviewed papers informed the project, what gaps remained in the literature, and how our implementation improved the methodology, model evaluation, interpretability, operational decision support, and deployment.",
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        metric_card(
            "Reviewed Studies",
            "10",
            "Restaurant forecasting, POS data, ML/DL, SARIMAX-related gaps",
            "cyan",
        )

    with l2:
        metric_card(
            "Main Gap",
            "Decision Support",
            "Many studies focus on accuracy more than operational use",
            "purple",
        )

    with l3:
        metric_card(
            "Our Best Result",
            "16.20% MAPE",
            "Hybrid SARIMAX + RF",
            "green",
        )

    with l4:
        metric_card(
            "Next Improvement",
            "Conformal",
            "Prediction intervals for uncertainty-aware planning",
            "orange",
        )

    st.subheader("Methodological Improvement Summary")
    display_dataframe(methodological_improvement_df)

    st.subheader("Literature-to-Implementation and Results Matrix")
    display_dataframe(literature_implementation_results_df)

    st.subheader("Previous Literature Gap Summary")
    display_dataframe(literature_added_value_df)

    st.subheader("How Our Project Improves the Literature")

    c1, c2 = st.columns(2)

    with c1:
        insight_card(
            "Methodological Improvement",
            "The literature supports restaurant demand forecasting, POS data, feature engineering, weather and holiday variables, and ML benchmarking. Our project integrates those ideas into a full pipeline: data cleaning, daily aggregation, feature engineering, model comparison, rolling validation, and deployment.",
            "cyan",
        )

        insight_card(
            "Interpretability Improvement",
            "Several papers use advanced machine learning or deep learning models that may be difficult for managers to understand. Our approach keeps SARIMAX as an interpretable forecasting core and uses Random Forest as a residual correction layer.",
            "purple",
        )

    with c2:
        insight_card(
            "Empirical Improvement",
            "Our model comparison shows measurable improvement: the baseline MAPE was 22.48%, SARIMAX Basic reached 18.50%, and the Hybrid SARIMAX + Random Forest model improved to 16.20%.",
            "green",
        )

        insight_card(
            "Operational Improvement",
            "Many studies stop at forecasting metrics. Our project translates predictions into a manager-facing dashboard for staffing readiness, menu preparation, inventory planning, promotional timing, and operational risk interpretation.",
            "orange",
        )

    st.info(
        "This section is designed to answer the professor's question: what did the papers propose, what gap remained, what did we implement, and what evidence shows that our project improved the methodology and results?"
    )

'''

text = text[:start] + new_block + text[end:]

# ============================================================
# 5. Save and validate
# ============================================================

APP_PATH.write_text(text, encoding="utf-8")
py_compile.compile(str(APP_PATH), doraise=True)

print("Literature Gap & Contribution tab updated successfully.")
print(f"Backup created: {BACKUP_PATH}")
print("Syntax check: PASSED")
