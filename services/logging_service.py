from utils.config_loader import load_config
import datetime


class Logger:
    def __init__(self):
        self.listeners = []

    def log(self, message, level="INFO"):
        config = load_config()

        if not config.get("log_enabled", True):
            return

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"

        print(formatted)

        for callback in self.listeners:
            callback(formatted)

    def subscribe(self, callback):
        self.listeners.append(callback)


logger = Logger()