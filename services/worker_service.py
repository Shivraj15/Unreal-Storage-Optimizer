from PySide6.QtCore import QObject, Signal

class Worker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(object)

    def run(self, func, *args):
        try:
            result = func(*args)
            self.finished.emit(result)
        except Exception as e:
            self.log.emit(str(e))