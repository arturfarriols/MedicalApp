# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////

style = '''
    QMessageBox {{
        background-color: {_msg_bg_color};
    }}
    
    QMessageBox QLabel {{
        color: {_color};
    }}
    
    QMessageBox QPushButton {{
        background-color: {_btn_bg_color};
        border: 1px solid #DDDDDD;
        border-radius: {_radius};
        padding: 5px 10px;
        min-width: 80px;
    }}
    
    QMessageBox QPushButton:hover {{
        background-color: {_btn_bg_color_hover};
    }}
    
    QMessageBox QPushButton:pressed {{
        background-color: {_btn_bg_color_pressed};
    }}
'''

# PY MESSAGE BOX
# ///////////////////////////////////////////////////////////////
class PyMessageBox(QMessageBox):
    def __init__(
        self, 
        text,
        title,
        icon,
        color,
        radius,
        msg_bg_color,
        btn_bg_color,
        btn_bg_color_hover,
        btn_bg_color_pressed,
        parent = None,
        id = None
    ):
        super().__init__()

        # SET PARAMETRES
        self.setText(text)
        self.setWindowTitle(title)
        self.setIcon(icon)
        if parent != None:
            self.setParent(parent)
        self.setCursor(Qt.PointingHandCursor)

        # SET STYLESHEET
        custom_style = style.format(
            _msg_bg_color = msg_bg_color,
            _color = color,
            _btn_bg_color = btn_bg_color,
            _radius = radius,
            _btn_bg_color_hover = btn_bg_color_hover,
            _btn_bg_color_pressed = btn_bg_color_pressed,
        )
        self.setStyleSheet(custom_style)


    def get_style_sheet(self):
        return self.styleSheet()
    
    def set_style_sheet(self, custom_style):
        self.setStyleSheet(custom_style)

        