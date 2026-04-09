from concurrent.futures import ThreadPoolExecutor
import os

from utils.file_utils import get_dir_size
from utils.config_loader import load_config
from core.rules import PRESETS


def get_project_targets(project_path, preset_name):
    preset = PRESETS[preset_name]
    targets = []

    def add(path):
        if os.path.exists(path):
            targets.append(path)

    if preset.get("DerivedDataCache"):
        add(os.path.join(project_path, "DerivedDataCache"))

    if preset.get("Intermediate"):
        add(os.path.join(project_path, "Intermediate"))

    if preset.get("Binaries"):
        add(os.path.join(project_path, "Binaries"))

    # Saved
    saved = os.path.join(project_path, "Saved")
    if os.path.exists(saved):
        if preset["Saved"] == "full":
            add(saved)
        else:
            for sub in preset["Saved"]:
                add(os.path.join(saved, sub))

    # Plugins
    if preset.get("Plugins"):
        plugins = os.path.join(project_path, "Plugins")
        if os.path.exists(plugins):
            for root, dirs, _ in os.walk(plugins):
                for d in dirs:
                    if d in ["Intermediate", "Binaries"]:
                        targets.append(os.path.join(root, d))

    return list(set(targets))


def analyze_project(project_path, preset_name="Balanced"):
    config = load_config()
    max_threads = config.get("max_threads", 8)

    targets = get_project_targets(project_path, preset_name)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        sizes = list(executor.map(get_dir_size, targets))

    breakdown = list(zip(targets, sizes))
    total = sum(sizes)

    return breakdown, total