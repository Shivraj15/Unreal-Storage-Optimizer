from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from utils.file_utils import format_size


class ProjectPanel(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(2)
        self.setHeaderLabels(["Project", "Size"])

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        self.analysis = {}

    def populate(self, analysis):
        self.clear()
        self.analysis = analysis

        for proj, breakdown in analysis.items():
            total = sum(size for _, size in breakdown)

            parent = QTreeWidgetItem(self)
            parent.setText(0, proj)
            parent.setText(1, format_size(total))
            parent.setCheckState(0, Qt.Checked)

            for path, size in breakdown:
                child = QTreeWidgetItem(parent)
                child.setText(0, path.split("\\")[-1])
                child.setText(1, format_size(size))

        self.expandAll()

    def get_selected_targets(self):
        targets = []

        root = self.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)

            if item.checkState(0) == Qt.Checked:
                proj = item.text(0)
                targets.extend(self.analysis.get(proj, []))

        return targets