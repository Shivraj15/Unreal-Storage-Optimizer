import json
import os

_config_cache = None

DEFAULT_CONFIG = {
    "scan_directories": [],
    "exclude_patterns": [],
    "safe_mode": True,
    "log_enabled": True,
    "default_preset": "Balanced",
    "max_threads": 8
}


def get_base_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_config_path():
    return os.path.join(get_base_path(), "config", "settings.json")


def load_config(force_reload=False):
    global _config_cache

    if _config_cache and not force_reload:
        return _config_cache

    path = get_config_path()

    if not os.path.exists(path):
        _config_cache = DEFAULT_CONFIG.copy()
        return _config_cache

    try:
        with open(path, "r") as f:
            data = json.load(f)

        config = DEFAULT_CONFIG.copy()
        config.update(data)

        _config_cache = config
        return config

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        _config_cache = DEFAULT_CONFIG.copy()
        return _config_cache