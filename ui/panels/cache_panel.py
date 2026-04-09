from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QGroupBox


class CachePanel(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        group = QGroupBox("Global Cache Cleaning")
        layout = QVBoxLayout(group)

        self.ddc_checkbox = QCheckBox("Clean Global DDC (AppData)")
        self.vault_checkbox = QCheckBox("Clean Vault Cache (Marketplace)")

        self.ddc_checkbox.setChecked(False)
        self.vault_checkbox.setChecked(False)

        layout.addWidget(self.ddc_checkbox)
        layout.addWidget(self.vault_checkbox)

        main_layout.addWidget(group)
        main_layout.addStretch()