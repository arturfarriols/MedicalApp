from qt_core import *

# Thread class for executing the computationally expensive function
class FunctionThread(QThread):
    finished = Signal()
    status_changed = Signal(str)
    # exception_raised = Signal(Exception)

    def __init__(self, backend_controller, items):
        super().__init__()
        self._stop_execution = False
        self.backend_controller = backend_controller
        self.items = items

    def run(self):
        try:
            status = self.backend_controller.final_process_videos(self.items)
        except Exception as e:
            # self.exception_raised.emit(e)
            raise(e)
        finally:
            # self.status_changed.emit(status)
            self.finished.emit()

    def stop_execution(self):
        self._stop_execution = True