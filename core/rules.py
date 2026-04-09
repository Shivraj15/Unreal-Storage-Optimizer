PRESETS = {
    "Safe": {
        "DerivedDataCache": True,
        "Intermediate": True,
        "Saved": ["Logs", "Temp"],
        "Binaries": False,
        "Plugins": False,
        "GlobalDDC": False,
        "Vault": False
    },
    "Balanced": {
        "DerivedDataCache": True,
        "Intermediate": True,
        "Saved": ["Logs", "Temp", "Crashes", "Autosaves"],
        "Binaries": True,
        "Plugins": True,
        "GlobalDDC": False,
        "Vault": False
    },
    "Aggressive": {
        "DerivedDataCache": True,
        "Intermediate": True,
        "Saved": "full",
        "Binaries": True,
        "Plugins": True,
        "GlobalDDC": True,
        "Vault": True
    }
}