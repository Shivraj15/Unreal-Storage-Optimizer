import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def load_stylesheet(app):
    base = get_base_path()
    path = os.path.join(base, "ui", "styles", "theme.qss")

    if os.path.exists(path):
        with open(path, "r") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Qubit UE Optimizer")
    app.setOrganizationName("Qubit Tools")

    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()