import json
import os
import tempfile

FILE = "config/usage.json"


def track(event):
    data = {}

    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}

    data[event] = data.get(event, 0) + 1

    # Safe write
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(data, tmp, indent=4)
        temp_name = tmp.name

    os.replace(temp_name, FILE)