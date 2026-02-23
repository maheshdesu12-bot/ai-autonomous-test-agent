import os
import time
from pathlib import Path
from datetime import datetime


REPORT_DIR = Path("reports")
SCREENSHOT_DIR = REPORT_DIR / "screenshots"
REPORT_FILE = REPORT_DIR / "report.html"


# -----------------------------
# Ensure directories exist
# -----------------------------

def ensure_dirs():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Save screenshot
# -----------------------------

def save_screenshot(page, test_name: str, status: str) -> str | None:

    try:

        ensure_dirs()

        ts = int(time.time())

        safe_name = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in test_name.lower()
        )

        filename = f"{safe_name}_{status}_{ts}.png"

        path = SCREENSHOT_DIR / filename

        page.screenshot(
            path=str(path),
            full_page=True
        )

        print(f"[Screenshot] Saved: {path}")

        return str(path)

    except Exception as e:

        print("[Screenshot] Failed:", e)

        return None


# -----------------------------
# Generate HTML report
# -----------------------------

def generate_html_report(results: dict, out_path: str | None = None) -> str:

    ensure_dirs()

    output = Path(out_path) if out_path else REPORT_FILE

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = len(results)
    passed = sum(1 for r in results.values() if r.get("status") == "passed")
    failed = sum(1 for r in results.values() if r.get("status") == "failed")

    rows = []

    for name, r in results.items():

        status = r.get("status", "unknown")
        error = r.get("error", "")
        screenshot = r.get("screenshot")

        # status color
        if status == "passed":
            color = "#28a745"
        elif status == "failed":
            color = "#dc3545"
        else:
            color = "#ffc107"

        screenshot_link = ""

        if screenshot and os.path.exists(screenshot):

            rel = os.path.relpath(
                screenshot,
                start=output.parent
            )

            screenshot_link = f'<a href="{rel}">View</a>'

        rows.append(f"""
        <tr>
            <td>{name}</td>
            <td style="color:{color}; font-weight:bold;">
                {status}
            </td>
            <td>{error}</td>
            <td>{screenshot_link}</td>
        </tr>
        """)

    html = f"""
<html>

<head>

<title>AI Autonomous Test Report</title>

<style>

body {{
    font-family: Arial;
    padding: 20px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
}}

th {{
    background-color: #f4f4f4;
}}

.summary {{
    margin-bottom: 20px;
    padding: 10px;
    background: #f9f9f9;
}}

</style>

</head>

<body>

<h2>AI Autonomous Test Agent Report</h2>

<div class="summary">

<b>Execution Time:</b> {timestamp} <br>
<b>Total Tests:</b> {total} <br>
<b>Passed:</b> <span style="color:green;">{passed}</span> <br>
<b>Failed:</b> <span style="color:red;">{failed}</span>

</div>

<table>

<tr>
<th>Test</th>
<th>Status</th>
<th>Error</th>
<th>Screenshot</th>
</tr>

{''.join(rows)}

</table>

</body>

</html>
"""

    output.write_text(html, encoding="utf-8")

    print("[Reporter] HTML report generated:", output)

    return str(output)