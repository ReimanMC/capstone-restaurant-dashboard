from pathlib import Path
import py_compile
import shutil

app_path = Path("src/dashboard/capstone_dashboard_app.py")
backup_path = Path("src/dashboard/capstone_dashboard_app_backup_before_research_framework.py")

if not app_path.exists():
    raise FileNotFoundError(f"Dashboard file not found: {app_path}")

# Backup before editing
shutil.copy2(app_path, backup_path)

text = app_path.read_text(encoding="utf-8")

# ------------------------------------------------------------
# 1. Add research framework file path
# ------------------------------------------------------------

old = 'SCIENTIFIC_ROADMAP_PATH = DATA_DIR / "scientific_roadmap_summary.csv"\n'
new = (
    'SCIENTIFIC_ROADMAP_PATH = DATA_DIR / "scientific_roadmap_summary.csv"\n'
    'RESEARCH_FRAMEWORK_PATH = DATA_DIR / "research_framework_summary.csv"\n'
)

if new not in text:
    if old not in text:
        raise ValueError("Could not find SCIENTIFIC_ROADMAP_PATH section.")
    text = text.replace(old, new)

# ------------------------------------------------------------
# 2. Load research framework CSV
# ------------------------------------------------------------

old = '    scientific_roadmap_df = load_csv(SCIENTIFIC_ROADMAP_PATH)\n'
new = (
    '    scientific_roadmap_df = load_csv(SCIENTIFIC_ROADMAP_PATH)\n'
    '    research_framework_df = load_csv(RESEARCH_FRAMEWORK_PATH)\n'
)

if new not in text:
    if old not in text:
        raise ValueError("Could not find scientific_roadmap_df load section.")
    text = text.replace(old, new)

# ------------------------------------------------------------
# 3. Add to data dictionary
# ------------------------------------------------------------

old = '        "scientific_roadmap": scientific_roadmap_df,\n'
new = (
    '        "scientific_roadmap": scientific_roadmap_df,\n'
    '        "research_framework": research_framework_df,\n'
)

if new not in text:
    if old not in text:
        raise ValueError("Could not find scientific_roadmap dictionary section.")
    text = text.replace(old, new)

# ------------------------------------------------------------
# 4. Assign variable after loading
# ------------------------------------------------------------

old = 'scientific_roadmap_df = data["scientific_roadmap"]\n'
new = (
    'scientific_roadmap_df = data["scientific_roadmap"]\n'
    'research_framework_df = data["research_framework"]\n'
)

if new not in text:
    if old not in text:
        raise ValueError("Could not find scientific_roadmap assignment section.")
    text = text.replace(old, new)

# ------------------------------------------------------------
# 5. Replace tabs structure
# ------------------------------------------------------------

old_tabs = '''tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Project Roadmap",
        "Data Pipeline",
        "Feature Engineering",
        "Literature & Added Value",
        "Model Strategy",
        "Model Results",
        "Manager Dashboard",
        "Team & Feedback",
    ]
)
'''

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
)
'''

if new_tabs not in text:
    if old_tabs not in text:
        raise ValueError("Could not find original tabs block.")
    text = text.replace(old_tabs, new_tabs)

# ------------------------------------------------------------
# 6. Shift existing tab references after Project Roadmap
# ------------------------------------------------------------

replacements = [
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

for old, new in replacements:
    text = text.replace(old, new)

# ------------------------------------------------------------
# 7. Insert new Research Framework tab before Data Pipeline
# ------------------------------------------------------------

research_tab = '''
# ============================================================
# Tab 2 - Research Framework
# ============================================================

with tab2:
    st.subheader("Research Framework")

    section_card(
        "Academic and Strategic Foundation",
        "This section integrates the core research elements of the project: problem gap, objective, research questions, data, methods, findings, visual evidence, strategic implications, and future research directions.",
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        metric_card(
            "Research Focus",
            "Demand Forecasting",
            "Short-term restaurant operations",
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
            "The framework connects the research problem, objective, questions, methods, findings, and future work in one place.",
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

if "with tab2:\n    st.subheader(\"Research Framework\")" not in text:
    if marker not in text:
        raise ValueError("Could not find Data Pipeline marker to insert Research Framework tab.")
    text = text.replace(marker, research_tab + marker)

# ------------------------------------------------------------
# 8. Write and compile
# ------------------------------------------------------------

app_path.write_text(text, encoding="utf-8")
py_compile.compile(str(app_path), doraise=True)

print("Research Framework tab added successfully.")
print(f"Backup created: {backup_path}")
print(f"Updated dashboard: {app_path}")
print("Syntax check: PASSED")
