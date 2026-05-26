from pathlib import Path
import py_compile
import shutil
import re

app_path = Path("src/dashboard/capstone_dashboard_app.py")
backup_path = Path("src/dashboard/capstone_dashboard_app_backup_before_research_framework_v2.py")

if not app_path.exists():
    raise FileNotFoundError(f"Dashboard file not found: {app_path}")

shutil.copy2(app_path, backup_path)

text = app_path.read_text(encoding="utf-8")

# ============================================================
# 1. Add research_framework to DATA_FILES dictionary
# ============================================================

old = '    "scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv",'
new = (
    '    "scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv",\n'
    '    "research_framework": DATA_DIR / "research_framework_summary.csv",'
)

if '"research_framework": DATA_DIR / "research_framework_summary.csv",' not in text:
    if old not in text:
        raise ValueError("Could not find scientific_roadmap entry in DATA_FILES.")
    text = text.replace(old, new)

# ============================================================
# 2. Add research_framework_df variable
# ============================================================

old = 'scientific_roadmap_df = data["scientific_roadmap"]'
new = (
    'scientific_roadmap_df = data["scientific_roadmap"]\n'
    'research_framework_df = data["research_framework"]'
)

if 'research_framework_df = data["research_framework"]' not in text:
    if old not in text:
        raise ValueError("Could not find scientific_roadmap_df assignment.")
    text = text.replace(old, new)

# ============================================================
# 3. Replace tabs definition
# ============================================================

old_tabs_pattern = r'''tab1,\s*tab2,\s*tab3,\s*tab4,\s*tab5,\s*tab6,\s*tab7,\s*tab8\s*=\s*st\.tabs\(
\s*\[
\s*"Project Roadmap",
\s*"Data Pipeline",
\s*"Feature Engineering",
\s*"Literature & Added Value",
\s*"Model Strategy",
\s*"Model Results",
\s*"Manager Dashboard",
\s*"Team & Feedback",
\s*\]
\s*\)'''

new_tabs = '''tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    [
        "Project Roadmap",
        "Research Framework",
        "Data Pipeline",
        "Feature Engineering",
        "Literature & Added Value",
        "Model Strategy",
        "Model Results",
        "Manager Dashboard",
        "Team & Feedback",
    ]
)'''

if "Research Framework" not in text.split("# ============================================================")[0:]:
    text, count = re.subn(old_tabs_pattern, new_tabs, text, count=1)
    if count == 0:
        raise ValueError("Could not replace tabs definition.")
else:
    if "tab9 = st.tabs" not in text and "tab8, tab9 = st.tabs" not in text:
        text, count = re.subn(old_tabs_pattern, new_tabs, text, count=1)
        if count == 0:
            raise ValueError("Could not replace tabs definition.")

# More reliable check: if old tabs block still exists, replace it.
if '"Research Framework",' not in text:
    text, count = re.subn(old_tabs_pattern, new_tabs, text, count=1)
    if count == 0:
        raise ValueError("Could not add Research Framework tab.")

# ============================================================
# 4. Shift existing tab blocks after Project Roadmap
# ============================================================

shift_replacements = [
    ("with tab8:", "with tab9:"),
    ("with tab7:", "with tab8:"),
    ("with tab6:", "with tab7:"),
    ("with tab5:", "with tab6:"),
    ("with tab4:", "with tab5:"),
    ("with tab3:", "with tab4:"),
    ("with tab2:", "with tab3:"),
    ("# Tab 8 - Team & Feedback", "# Tab 9 - Team & Feedback"),
    ("# Tab 7 - Manager Dashboard", "# Tab 8 - Manager Dashboard"),
    ("# Tab 6 - Model Results", "# Tab 7 - Model Results"),
    ("# Tab 5 - Model Strategy", "# Tab 6 - Model Strategy"),
    ("# Tab 4 - Literature & Added Value", "# Tab 5 - Literature & Added Value"),
    ("# Tab 3 - Feature Engineering", "# Tab 4 - Feature Engineering"),
    ("# Tab 2 - Data Pipeline", "# Tab 3 - Data Pipeline"),
]

if 'with tab2:\n    st.subheader("Research Framework")' not in text:
    for old, new in shift_replacements:
        text = text.replace(old, new)

# ============================================================
# 5. Insert Research Framework tab before Data Pipeline
# ============================================================

research_tab = '''
# ============================================================
# Tab 2 - Research Framework
# ============================================================

with tab2:
    st.subheader("Research Framework")

    section_card(
        "Academic and Strategic Foundation",
        "This section integrates the core research elements of the project: problem gap, objective, research questions, data, analytical methods, findings, visual evidence, strategic implications, and future research directions.",
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
            "The framework connects the research problem, objective, questions, methods, findings, implications, limitations, and future work in one place.",
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


'''

marker = "# ============================================================\n# Tab 3 - Data Pipeline"

if 'with tab2:\n    st.subheader("Research Framework")' not in text:
    if marker not in text:
        raise ValueError("Could not find Tab 3 - Data Pipeline marker.")
    text = text.replace(marker, research_tab + marker)

# ============================================================
# 6. Update feedback sections
# ============================================================

old_feedback = 'feedback_sections = ["Project Roadmap", "Data Pipeline", "Feature Engineering", "Literature & Added Value", "Model Strategy", "Model Results", "Manager Dashboard"]'
new_feedback = 'feedback_sections = ["Project Roadmap", "Research Framework", "Data Pipeline", "Feature Engineering", "Literature & Added Value", "Model Strategy", "Model Results", "Manager Dashboard"]'

if old_feedback in text:
    text = text.replace(old_feedback, new_feedback)

# ============================================================
# 7. Save and validate
# ============================================================

app_path.write_text(text, encoding="utf-8")
py_compile.compile(str(app_path), doraise=True)

print("Research Framework tab added successfully.")
print(f"Backup created: {backup_path}")
print(f"Updated dashboard: {app_path}")
print("Syntax check: PASSED")
