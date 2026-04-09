from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox
)
from services.license_service import save_license, is_pro


class LicensePanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.status = QLabel()
        self.status.setStyleSheet("font-weight: bold;")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter License Key (XXXX-XXXX-XXXX)")

        self.btn = QPushButton("Activate License")

        layout.addWidget(self.status)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        layout.addStretch()

        self.btn.clicked.connect(self.activate)

        self.update_status()

    def activate(self):
        key = self.input.text().strip()

        if not key:
            QMessageBox.warning(self, "Error", "Please enter a license key.")
            return

        save_license(key)

        if is_pro():
            QMessageBox.information(self, "Success", "PRO version activated!")
        else:
            QMessageBox.warning(self, "Invalid", "Invalid license key.")

        self.update_status()

    def update_status(self):
        if is_pro():
            self.status.setText("✅ PRO Version Activated")
        else:
            self.status.setText("Free Version (Limited Features)")