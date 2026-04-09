import psutil


def is_ue_running():
    for p in psutil.process_iter(['name']):
        name = p.info['name']
        if name and ("UnrealEditor" in name or "UE4Editor" in name):
            return True
    return False