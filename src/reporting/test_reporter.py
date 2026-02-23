import json
from datetime import datetime


REPORT_FILE = "reports/test_report.json"


def save_test_report(agent_name, result):

    report = {
        "agent": agent_name,
        "timestamp": datetime.utcnow().isoformat(),
        "result": result
    }

    try:
        with open(REPORT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(report)

    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("[Report] Test report saved")