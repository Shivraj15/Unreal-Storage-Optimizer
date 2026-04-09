import os
from utils.config_loader import load_config


def find_ue_projects(root, max_depth=5):
    config = load_config()
    ignore_dirs = set(p.lower() for p in config.get("exclude_patterns", []))

    projects = []

    root = os.path.abspath(root)

    for dirpath, dirnames, filenames in os.walk(root):

        # 🔥 Skip heavy/ignored directories early
        if any(skip in dirpath.lower() for skip in ignore_dirs):
            dirnames[:] = []
            continue

        # Apply ignore filters
        dirnames[:] = [d for d in dirnames if d.lower() not in ignore_dirs]

        # Depth control
        try:
            rel = os.path.relpath(dirpath, root)
            depth = rel.count(os.sep)
        except Exception:
            depth = 0

        if depth > max_depth:
            dirnames[:] = []
            continue

        # Detect UE project
        if any(f.endswith(".uproject") for f in filenames):
            if os.path.isdir(os.path.join(dirpath, "Content")):
                projects.append(dirpath)

    return projects