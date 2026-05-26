from pathlib import Path
import py_compile
import shutil
import sys

app_path = Path("src/dashboard/capstone_dashboard_app.py")
backup_path = Path("src/dashboard/capstone_dashboard_app_backup_before_research_framework_final.py")

if not app_path.exists():
    raise FileNotFoundError(f"Dashboard file not found: {app_path.resolve()}")

shutil.copy2(app_path, backup_path)

text = app_path.read_text(encoding="utf-8")

required_markers = [
    "Capstone Forecast Intelligence Portal",
    '"scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv"',
    'scientific_roadmap_df = data["scientific_roadmap"]',
    'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([',
    'with tab2:',
    'st.subheader("Data Pipeline")',
]

missing = [m for m in required_markers if m not in text]
if missing:
    print("This dashboard file does not match the expected Scientific Roadmap version.")
    print("Missing markers:")
    for m in missing:
        print(f"- {m}")
    sys.exit(1)

if '"Research Framework",' in text and 'research_framework_df = data["research_framework"]' in text:
    print("Research Framework already appears to be added. No changes needed.")
    py_compile.compile(str(app_path), doraise=True)
    print("Syntax check: PASSED")
    sys.exit(0)

text = text.replace(
    '    "scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv",',
    '    "scientific_roadmap": DATA_DIR / "scientific_roadmap_summary.csv",\n'
    '    "research_framework": DATA_DIR / "research_framework_summary.csv",'
)

text = text.replace(
    'scientific_roadmap_df = data["scientific_roadmap"]',
    'scientific_roadmap_df = data["scientific_roadmap"]\n'
    'research_framework_df = data["research_framework"]'
)

old_tabs = """tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Project Roadmap",
    "Data Pipeline",
    "Feature Engineering",
    "Literature & Added Value",
    "Model Strategy",
    "Model Results",
    "Manager Dashboard",
    "Team & Feedback",
])"""

new_tabs = """tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Project Roadmap",
    "Research Framework",
    "Data Pipeline",
    "Feature Engineering",
    "Literature & Added Value",
    "Model Strategy",
    "Model Results",
    "Manager Dashboard",
    "Team & Feedback",
])"""

if old_tabs not in text:
    print("Could not find the exact tabs block.")
    print("No changes were saved.")
    sys.exit(1)

text = text.replace(old_tabs, new_tabs)

shift_pairs = [
    ("with tab8:", "with tab9:"),
    ("with tab7:", "with tab8:"),
    ("with tab6:", "with tab7:"),
    ("with tab5:", "with tab6:"),
    ("with tab4:", "with tab5:"),
    ("with tab3:", "with tab4:"),
    ("with tab2:", "with tab3:"),
]

for old, new in shift_pairs:
    text = text.replace(old, new)

research_framework_block = """
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


"""

marker = 'with tab3:\n    st.subheader("Data Pipeline")'

if marker not in text:
    print("Could not find the shifted Data Pipeline block.")
    print("No changes were saved.")
    sys.exit(1)

text = text.replace(marker, research_framework_block + marker)

text = text.replace(
    'feedback_sections = ["Project Roadmap", "Data Pipeline", "Feature Engineering", "Literature & Added Value", "Model Strategy", "Model Results", "Manager Dashboard"]',
    'feedback_sections = ["Project Roadmap", "Research Framework", "Data Pipeline", "Feature Engineering", "Literature & Added Value", "Model Strategy", "Model Results", "Manager Dashboard"]'
)

app_path.write_text(text, encoding="utf-8")
py_compile.compile(str(app_path), doraise=True)

print("Research Framework tab added successfully.")
print(f"Backup created: {backup_path}")
print(f"Updated dashboard: {app_path}")
print("Syntax check: PASSED")
