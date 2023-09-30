import sys

from qt_core import *

from main import MainWindow
from singleton_meta_class import SingletonMeta

class MainController(metaclass=SingletonMeta):
    def __init__(self):
        pass
    

if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    main_controller = MainController()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("SP.ico"))
    window = MainWindow()
    main_controller.window = window

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())