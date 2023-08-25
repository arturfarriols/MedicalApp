# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
QLabel {{
    color: {_color};
    font: {_font};
    font-size: {_font_size}px;
}}
'''

# PY LABEL
# ///////////////////////////////////////////////////////////////
class PyLabel(QLabel):
    def __init__(
        self,
        text,
        color,
        font_family,
        font_size,
        parent=None
    ):
        super().__init__()

        # SET PARAMETERS
        self.setText(text)
        if parent is not None:
            self.setParent(parent)

        # SET STYLESHEET
        custom_style = style.format(
            _color=color,
            _font=font_family,
            _font_size=font_size
        )
        self.setStyleSheet(custom_style)

    def get_style_sheet(self):
        return self.styleSheet()

    def set_style_sheet(self, custom_style):
        self.setStyleSheet(custom_style)
