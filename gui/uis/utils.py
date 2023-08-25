import sys
import os

import datetime

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from  gui.uis.windows.main_window.ui_main import *

from gui.widgets import *

from models import * 

time_file = "mean_time.txt"

actual_row = 1

def convert_frame_to_pixmap(frame, dimensions = None):
    image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(image)

    if dimensions is not None:
        # Scale the image to fit the width and height of the table cell
        pixmap = pixmap.scaled(dimensions[0], dimensions[1], Qt.KeepAspectRatio)
    
    return pixmap

def get_local_date():
    # local_datetime = datetime.datetime.now().replace(microsecond=0)
    local_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return local_datetime

def save_time_to_file(value):
    with open(time_file, 'w') as file:
        file.write(str(value))

def load_time_from_file():
    try:
        with open(time_file, 'r') as file:
            value = file.read()
            return int(value)  
    except FileNotFoundError:
        return None
    
def obtain_ETA(number_of_frames):
    time = load_time_from_file()

    if time is not None:
        hours, minutes, seconds =  convert_seconds_to_hms(time * number_of_frames)
        eta = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return eta
    else:
        return None
    
def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds

def change_button_selection(deactivated_btn, activated_btn):
    deactivated_btn.set_active(False)
    activated_btn.set_active(True)

# def generate_table_columns(window, texts):
#     for text in texts:
