from qt_core import *

# Thread class for executing the computationally expensive function
class FunctionThread(QThread):
    finished = Signal()
    status_changed = Signal(str)

    def __init__(self, backend_controller, items):
        super().__init__()
        self._stop_execution = False
        self.backend_controller = backend_controller
        self.items = items

    def run(self):
        # Execute the computationally expensive function
        status = self.backend_controller.process_videos(self.items)

        self.status_changed.emit(status)

        # Emit the finished signal when done
        self.finished.emit()

    def stop_execution(self):
        self._stop_execution = True