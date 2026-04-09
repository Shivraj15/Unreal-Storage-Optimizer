import os


def get_global_ddc():
    path = os.path.expanduser(
        "~/AppData/Local/UnrealEngine/Common/DerivedDataCache"
    )
    return path if os.path.exists(path) else None


def get_vault_cache():
    path = os.path.expanduser(
        "~/AppData/Local/EpicGamesLauncher/Saved/VaultCache"
    )
    return path if os.path.exists(path) else None