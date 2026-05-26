from pathlib import Path
import py_compile
import shutil
import sys

app_path = Path("src/dashboard/capstone_dashboard_app.py")
backup_path = Path("src/dashboard/capstone_dashboard_app_backup_before_force_remove_pipeline_charts.py")

shutil.copy2(app_path, backup_path)

text = app_path.read_text(encoding="utf-8")

start_marker = '    chart_records_df = contrast_df.copy()\n'
end_marker = '    st.subheader("Dataset Transformation Summary")\n'

if start_marker not in text:
    print("Chart block was not found. The code may already be clean.")
    py_compile.compile(str(app_path), doraise=True)
    print("Syntax check: PASSED")
    sys.exit(0)

start = text.find(start_marker)
end = text.find(end_marker, start)

if end == -1:
    raise ValueError("Could not find the end marker for the chart block.")

text = text[:start] + text[end:]

app_path.write_text(text, encoding="utf-8")
py_compile.compile(str(app_path), doraise=True)

print("Pipeline charts were removed successfully.")
print(f"Backup created: {backup_path}")
print("Syntax check: PASSED")
