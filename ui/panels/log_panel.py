from PySide6.QtWidgets import QTextEdit


class LogPanel(QTextEdit):
    MAX_LINES = 1000

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def append_log(self, text):
        self.append(text)

        # Limit log size (prevent memory bloat)
        if self.document().blockCount() > self.MAX_LINES:
            cursor = self.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()