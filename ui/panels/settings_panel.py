from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox
)
from utils.config_loader import load_config


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        config = load_config()

        self.safe_mode = QCheckBox("Enable Safe Mode (Recommended)")
        self.safe_mode.setChecked(config.get("safe_mode", True))

        self.logging = QCheckBox("Enable Logging")
        self.logging.setChecked(config.get("log_enabled", True))

        layout.addWidget(QLabel("Settings"))
        layout.addWidget(self.safe_mode)
        layout.addWidget(self.logging)
        layout.addStretch()