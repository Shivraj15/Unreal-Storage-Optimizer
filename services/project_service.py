import string
import os
from core.scanner import find_ue_projects
from utils.config_loader import load_config


def get_available_drives():
    drives = []

    for letter in string.ascii_uppercase:
        path = f"{letter}:\\"
        if os.path.exists(path):
            drives.append(path)

    return drives


def scan_all_drives(progress_cb=None):
    config = load_config()

    roots = config.get("scan_directories") or get_available_drives()

    projects = []

    for i, root in enumerate(roots):
        try:
            found = find_ue_projects(root)
            projects.extend(found)
        except Exception as e:
            print(f"[SCAN ERROR] {root}: {e}")

        if progress_cb:
            progress_cb(i, len(roots), root)

    return list(set(projects))