from .resource_not_found import ResourceNotFoundException
from .invalid_data import InvalidDataException
from .model_error import ModelErrorException
from .resources_enum import *
from .exception_utils import *

from gui.widgets.py_message_box import PyMessageBox

from qt_core import *


class ExceptionHandler:
    def handle_exception(self, exception):
        found = False
        for exception_type in CUSTOM_EXCEPTION_MESSAGES.keys():
            if isinstance(exception, exception_type):
                print(EXCEPTION_FUNCTIONS.get(exception_type)) 
                handling_function = getattr(self, EXCEPTION_FUNCTIONS.get(exception_type)) 
                print("handling_function", handling_function)
                handling_function(exception)
                found = True

        print ("found", found)
        if not found:
            self.handle_generic_exception(exception)

    def generate_message_box(self, text, title):
        message_box = PyMessageBox(
        text = text,
        title = title,
        icon = QMessageBox.Warning, 
        color = "#333333",
        radius = 0,
        msg_bg_color = "#F0F0F0",
        btn_bg_color = "#F8F8F8",
        btn_bg_color_hover = "#E8E8E8",
        btn_bg_color_pressed = "#D0D0D0",
        id = "warning pop up"
        )

        message_box.exec_()

    def handle_resource_not_found(self, exception):
        text, title = CUSTOM_EXCEPTION_MESSAGES.get(type(exception)).get(exception.resource_type).values()
        self.generate_message_box(text=text, title=title)

    def handle_invalid_data(self, exception):
        text, title = CUSTOM_EXCEPTION_MESSAGES.get(type(exception)).values()
        formated_text = text.format(details=exception.data_type, available_formats=exception.accepted_formats)
        self.generate_message_box(text=formated_text, title=title)

    def handle_model_error(self, exception):
        pass

    def handle_generic_exception(self, exception):
        text, title = DEFAULT_EXCEPTION_MESSAGE.values()
        self.generate_message_box(text=text, title=title)
