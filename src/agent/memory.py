import json
import os
from datetime import datetime

MEMORY_FILE = "memory/failures.json"


def add_failure(requirement, error, analysis):

    memory_entry = {
        "requirement": requirement,
        "error": error,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    data.append(memory_entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("\n[Agent] Memory saved.")