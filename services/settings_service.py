from utils.config_loader import load_config

class Settings:
    def __init__(self):
        self.data = load_config()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value


settings = Settings()