# IMPORT QT CORE
from . py_push_button import *

# Custom PyPushButton subclass
class PyTablePushButton(PyPushButton):
    def __init__(
        self, 
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        text_align="center",
        id=None,
        parent=None,
        row=None  # Additional variable 'row'
    ):
        super().__init__(
            text,
            radius,
            color,
            bg_color,
            bg_color_hover,
            bg_color_pressed,
            text_align,
            id,
            parent,
        )
        self.row = row  # Set the 'row' variable

    def get_row(self):
        return self.row

    def set_row(self, row):
        self.row = row

    def get_style_sheet(self):
        return self.styleSheet()

    def set_style_sheet(self, custom_style):
        self.setStyleSheet(custom_style)