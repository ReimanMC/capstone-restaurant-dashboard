from pathlib import Path
import py_compile
import re
import shutil
import sys

APP_PATH = Path("src/dashboard/capstone_dashboard_app.py")
BACKUP_PATH = Path("src/dashboard/capstone_dashboard_app_backup_before_quantitative_literature.py")

if not APP_PATH.exists():
    raise FileNotFoundError(f"Dashboard file not found: {APP_PATH.resolve()}")

shutil.copy2(APP_PATH, BACKUP_PATH)

text = APP_PATH.read_text(encoding="utf-8")

# ============================================================
# 1. Add required literature CSV files to DATA_FILES dictionary
# ============================================================

data_marker = '    "literature_added_value": DATA_DIR / "literature_added_value_summary.csv",'

if data_marker not in text:
    print("Could not find literature_added_value entry in DATA_FILES.")
    sys.exit(1)

missing_data_entries = []

if '"literature_implementation_results": DATA_DIR / "literature_implementation_results_matrix.csv",' not in text:
    missing_data_entries.append(
        '    "literature_implementation_results": DATA_DIR / "literature_implementation_results_matrix.csv",'
    )

if '"methodological_improvement": DATA_DIR / "methodological_improvement_summary.csv",' not in text:
    missing_data_entries.append(
        '    "methodological_improvement": DATA_DIR / "methodological_improvement_summary.csv",'
    )

if '"literature_quantitative_comparison": DATA_DIR / "literature_quantitative_comparison_summary.csv",' not in text:
    missing_data_entries.append(
        '    "literature_quantitative_comparison": DATA_DIR / "literature_quantitative_comparison_summary.csv",'
    )

if missing_data_entries:
    text = text.replace(
        data_marker,
        data_marker + "\n" + "\n".join(missing_data_entries)
    )

# ============================================================
# 2. Add dataframe variables
# ============================================================

variable_marker = 'literature_added_value_df = data["literature_added_value"]'

if variable_marker not in text:
    print("Could not find literature_added_value_df assignment.")
    sys.exit(1)

missing_variable_lines = []

if 'literature_implementation_results_df = data["literature_implementation_results"]' not in text:
    missing_variable_lines.append(
        'literature_implementation_results_df = data["literature_implementation_results"]'
    )

if 'methodological_improvement_df = data["methodological_improvement"]' not in text:
    missing_variable_lines.append(
        'methodological_improvement_df = data["methodological_improvement"]'
    )

if 'literature_quantitative_comparison_df = data["literature_quantitative_comparison"]' not in text:
    missing_variable_lines.append(
        'literature_quantitative_comparison_df = data["literature_quantitative_comparison"]'
    )

if missing_variable_lines:
    text = text.replace(
        variable_marker,
        variable_marker + "\n" + "\n".join(missing_variable_lines)
    )

# ============================================================
# 3. Locate the Literature tab block
# ============================================================

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
# 4. Replace the Literature tab content
# ============================================================

new_block = f'''{tab_line}
    st.subheader("Literature Gap & Our Contribution")

    section_card(
        "From Academic Literature to Quantitative Project Evidence",
        "This section connects the reviewed papers with our implementation. It explains what the literature proposed, what gaps remained, what we implemented, and where our results are directly better, partially comparable, or not directly comparable because the papers use different datasets, metrics, targets, and contexts.",
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        metric_card(
            "Reviewed Studies",
            "10",
            "Restaurant forecasting, POS data, ML/DL, interpretability, decision support",
            "cyan",
        )

    with l2:
        metric_card(
            "Internal Improvement",
            "22.48% → 16.20%",
            "Baseline MAPE to Hybrid SARIMAX + RF MAPE",
            "green",
        )

    with l3:
        metric_card(
            "SARIMAX Improvement",
            "18.50% → 16.20%",
            "SARIMAX Basic to Hybrid SARIMAX + RF",
            "purple",
        )

    with l4:
        metric_card(
            "Fair Comparison",
            "Context-Aware",
            "Different papers use different metrics, targets, and datasets",
            "orange",
        )

    st.subheader("Quantitative Benchmarking and Fair Comparison")

    section_card(
        "How to Interpret the Quantitative Comparison",
        "The strongest quantitative evidence is internal: the same dataset, same target, and same test window show that the Hybrid SARIMAX + Random Forest model improves over both the Seasonal Naive Baseline and SARIMAX Basic. For external papers, direct comparison is not always valid because their datasets, metrics, targets, and modeling contexts are different.",
    )

    display_dataframe(literature_quantitative_comparison_df)

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
            "Direct Quantitative Improvement",
            "Inside our own controlled experiment, the model improved from 22.48% MAPE in the Seasonal Naive Baseline to 16.20% MAPE in the Hybrid SARIMAX + Random Forest model. This is the strongest evidence because it uses the same dataset, target, and test window.",
            "green",
        )

        insight_card(
            "Interpretability and Methodology",
            "Several papers use complex ML or deep learning models. Our project keeps SARIMAX as an interpretable forecasting core and adds Random Forest as a residual correction layer only where it improves performance.",
            "purple",
        )

    with c2:
        insight_card(
            "Fairness Against Literature",
            "We do not claim to outperform all papers universally. Some papers report R², sMAPE, MSE, waste reduction, or large-chain improvement percentages. Those are not always directly comparable to our net-sales MAPE.",
            "orange",
        )

        insight_card(
            "Operational Contribution",
            "Our project goes beyond model metrics by connecting forecasts to staffing readiness, menu preparation, inventory planning, promotional timing, and an interactive dashboard accessible through a public link and QR code.",
            "cyan",
        )

    st.info(
        "Key defense message: Our results are directly better than our internal baseline and SARIMAX-only model. Against external papers, the comparison must be fair: some results are competitive, some are not directly comparable, and our main added value is the combination of interpretability, feature engineering, rolling validation, deployment, and operational decision support."
    )

'''

text = text[:start] + new_block + text[end:]

# ============================================================
# 5. Save and validate
# ============================================================

APP_PATH.write_text(text, encoding="utf-8")
py_compile.compile(str(APP_PATH), doraise=True)

print("Literature tab updated with quantitative comparison successfully.")
print(f"Backup created: {BACKUP_PATH}")
print("Syntax check: PASSED")
