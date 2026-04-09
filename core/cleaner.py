import shutil
import os

from utils.config_loader import load_config
from utils.file_utils import get_dir_size


def safe_delete(path, safe_mode=True):
    try:
        if safe_mode:
            if not os.path.exists(path):
                return False, "Path not found"

        shutil.rmtree(path)
        return True, None

    except Exception as e:
        return False, str(e)


def execute_cleanup(targets, progress_cb=None):
    """
    targets = [(path, size)]
    """

    config = load_config()
    safe_mode = config.get("safe_mode", True)

    total_freed = 0

    for i, (path, size) in enumerate(targets):

        # Fix: compute size if missing (global cache case)
        if size == 0 or size is None:
            try:
                size = get_dir_size(path)
            except Exception:
                size = 0

        success, err = safe_delete(path, safe_mode)

        if success:
            total_freed += size

        if progress_cb:
            progress_cb(i, path, success, size, err)

    return total_freed