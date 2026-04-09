from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
import threading

from services.project_service import scan_all_drives
from services.cache_service import get_global_ddc, get_vault_cache
from services.logging_service import logger
from services.feature_service import can_use

from core.analyzer import analyze_project
from core.cleaner import execute_cleanup
from core.rules import PRESETS
from core.safety import is_ue_running

from utils.file_utils import format_size

from ui.panels.log_panel import LogPanel
from ui.panels.cache_panel import CachePanel
from ui.panels.project_panel import ProjectPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qubit UE Optimizer")
        self.resize(1200, 700)

        self.analysis = {}
        self.is_busy = False

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Toolbar
        toolbar = QHBoxLayout()

        self.scan_btn = QPushButton("Scan")
        self.clean_btn = QPushButton("Clean")

        self.preset = QComboBox()
        self.preset.addItems(PRESETS.keys())

        toolbar.addWidget(self.scan_btn)
        toolbar.addWidget(self.clean_btn)
        toolbar.addWidget(self.preset)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Panels
        splitter = QSplitter(Qt.Horizontal)

        self.project_panel = ProjectPanel()
        self.log_panel = LogPanel()
        self.cache_panel = CachePanel()

        splitter.addWidget(self.project_panel)
        splitter.addWidget(self.log_panel)
        splitter.addWidget(self.cache_panel)

        layout.addWidget(splitter)

        # Bottom
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Signals
        self.scan_btn.clicked.connect(self.scan)
        self.clean_btn.clicked.connect(self.clean)

        logger.subscribe(self.log_panel.append_log)

    # =========================
    # SCAN
    # =========================
    def scan(self):
        if self.is_busy:
            return

        self.is_busy = True
        self.scan_btn.setEnabled(False)
        self.progress.setValue(0)

        threading.Thread(target=self._scan, daemon=True).start()

    def _scan(self):
        logger.log("Scanning for projects...")

        projects = scan_all_drives()

        total = len(projects)
        new_analysis = {}

        for i, proj in enumerate(projects):
            breakdown, size = analyze_project(proj)
            new_analysis[proj] = breakdown

            pct = int((i + 1) / max(1, total) * 100)

            logger.log(f"Found: {proj} ({format_size(size)})")

            QMetaObject.invokeMethod(
                self.progress,
                "setValue",
                Qt.QueuedConnection,
                Q_ARG(int, pct)
            )

        # Update UI safely
        QMetaObject.invokeMethod(
            self,
            "_finish_scan",
            Qt.QueuedConnection,
            Q_ARG(object, new_analysis)
        )

    def _finish_scan(self, analysis):
        self.analysis = analysis
        self.project_panel.populate(analysis)

        self.scan_btn.setEnabled(True)
        self.is_busy = False

    # =========================
    # CLEAN
    # =========================
    def clean(self):
        if self.is_busy:
            return

        if is_ue_running():
            logger.log("Unreal Engine is running!", "WARN")
            return

        preset_name = self.preset.currentText()

        if preset_name == "Aggressive" and not can_use("aggressive_mode"):
            logger.log("Aggressive mode requires PRO", "WARN")
            return

        targets = self.project_panel.get_selected_targets()

        if not targets:
            logger.log("No projects selected", "WARN")
            return

        # Global cache gating
        if self.cache_panel.ddc_checkbox.isChecked():
            if not can_use("global_cache"):
                logger.log("Global DDC requires PRO", "WARN")
            else:
                ddc = get_global_ddc()
                if ddc:
                    targets.append((ddc, 0))

        if self.cache_panel.vault_checkbox.isChecked():
            if not can_use("vault_cache"):
                logger.log("Vault cache requires PRO", "WARN")
            else:
                vault = get_vault_cache()
                if vault:
                    targets.append((vault, 0))

        self.is_busy = True
        self.clean_btn.setEnabled(False)
        self.progress.setValue(0)

        threading.Thread(target=self._clean, args=(targets,), daemon=True).start()

    def _clean(self, targets):
        logger.log("Starting cleanup...")

        total = len(targets)

        def progress(i, path, success, size, err):
            pct = int((i + 1) / max(1, total) * 100)

            QMetaObject.invokeMethod(
                self.progress,
                "setValue",
                Qt.QueuedConnection,
                Q_ARG(int, pct)
            )

            if success:
                logger.log(f"Deleted: {path} ({format_size(size)})")
            else:
                logger.log(f"Failed: {path} -> {err}", "ERROR")

        freed = execute_cleanup(targets, progress)

        QMetaObject.invokeMethod(
            self,
            "_finish_clean",
            Qt.QueuedConnection,
            Q_ARG(str, format_size(freed))
        )

    def _finish_clean(self, size):
        logger.log(f"Cleanup complete. Freed {size}")

        self.clean_btn.setEnabled(True)
        self.is_busy = False