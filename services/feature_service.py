from services.license_service import is_pro


def can_use(feature):
    if is_pro():
        return True

    # Free limitations
    restricted = {
        "multi_project",
        "global_cache",
        "vault_cache",
        "aggressive_mode"
    }

    return feature not in restricted