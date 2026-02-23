import json
import os

DOM_MEMORY_FILE = "memory/dom_snapshots.json"


def capture_dom(page, goal, error):
    """
    Capture page DOM snapshot
    """

    try:
        html = page.content()

        snapshot = {
            "goal": goal,
            "error": error,
            "html": html
        }

        if not os.path.exists(DOM_MEMORY_FILE):
            with open(DOM_MEMORY_FILE, "w") as f:
                json.dump([], f)

        with open(DOM_MEMORY_FILE, "r") as f:
            data = json.load(f)

        data.append(snapshot)

        with open(DOM_MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

        print("[DOM Memory] Snapshot saved")

    except Exception as e:
        print("[DOM Memory] Failed:", e)


def load_dom_memory():
    try:
        with open(DOM_MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []