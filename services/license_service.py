import os
import hashlib

LICENSE_FILE = os.path.join("config", "license.key")

SECRET = "QUBIT_SECRET_2026"


def generate_key(email):
    """
    Generate license key (for you, not user)
    """
    raw = (email.strip().lower() + SECRET).encode()
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def save_license(key):
    try:
        os.makedirs("config", exist_ok=True)

        with open(LICENSE_FILE, "w") as f:
            f.write(key.strip())
    except Exception as e:
        print(f"[LICENSE ERROR] {e}")


def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None

    try:
        with open(LICENSE_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return None


def validate_license(key):
    """
    Basic offline validation (improved)
    """
    if not key:
        return False

    if len(key) != 16:
        return False

    if not key.isalnum():
        return False

    return True


def is_pro():
    key = load_license()
    return validate_license(key)