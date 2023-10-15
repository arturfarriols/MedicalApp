# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA AND ARTUR FARRIOLS RAIMÍ
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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import sys
import os
from functools import partial

import numpy as np

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

from gui.uis.windows.main_window.functions_main_window import *

from gui.widgets import *
from gui.uis.windows.image_dialog import *

from gui.uis.utils import *

from models import * 

from exceptions.exceptions_core import *

# def _check_file_extension_is_valid(file_path):
#     valid_extensions = ['py', 'mp4', 'avi', 'mov', 'mkv', 'wmv'] #Remove .py
    
#     file_extension = file_path.split('.')[-1].lower()
#     print(file_extension)
    
#     if file_extension in valid_extensions:
#         return True
#     else:
#         return False

# def open_file_browser(window):
#     options = QFileDialog.Options()
#     file_path, _ = QFileDialog.getOpenFileName(window, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
    
#     if file_path:
#         print("Selected file:", file_path)
    
#         if not _check_file_extension_is_valid(file_path):
#             # File format is not valid

#             # CREATE CUSTOM BUTTON 2
#             # message_box = PyMessageBox(
#             #     text = "The selected file format is not valid.",
#             #     title = "Invalid File Format",
#             #     icon = QMessageBox.Warning, 
#             #     color = "#333333",
#             #     radius = 0,
#             #     msg_bg_color = "#F0F0F0",
#             #     btn_bg_color = "#F8F8F8",
#             #     btn_bg_color_hover = "#E8E8E8",
#             #     btn_bg_color_pressed = "#D0D0D0",
#             #     id = "warning pop up"
#             # )

#             # message_box.exec_()
#             return None
#         else:
#             add_row(window, file_path)
#             return file_path

def _create_table_widget(widget_content, widget_type):
    # Create a centered widget for the table cell
    widget = QWidget()
    layout = QVBoxLayout(widget)

    if widget_type == "image":
        layout.addWidget(QLabel())
        label = widget.findChild(QLabel)
        label.setPixmap(widget_content)
    else:
        layout.addWidget(widget_content)

    layout.setAlignment(Qt.AlignCenter)
    layout.setContentsMargins(0, 0, 0, 0)

    # Set the image item in the center of the cell

    return widget

def _add_item_to_table(table):
    return None

def _generate_closing_button(window, row):
    btn = PyTablePushButton(
        text = "",
        radius = 8,
        color = window.themes["app_color"]["text_foreground"],
        bg_color = window.themes["app_color"]["dark_one"],
        bg_color_hover = window.themes["app_color"]["dark_three"],
        bg_color_pressed = window.themes["app_color"]["dark_four"],
        text_align = "Hcenter",
        id = "table_widget",
        row = row
    )

    btn.setMaximumWidth(50)
    # btn.setMinimumWidth(50)
    btn.setMinimumSize(btn.sizeHint())
    btn.setMinimumHeight(40)

    print(btn.row)

    icon = QIcon(Functions.set_svg_icon("icon_close.svg"))
    btn.setIcon(icon)
    btn.clicked.connect(partial(delete_row, btn, window.table_widget))

    return btn    

def add_row(window, file_path):
    #OBTAIN THE FILE NAME
    file_name = os.path.basename(file_path)

    video = Video(file_name, file_path)
    #INSERT ROW
    row_number = window.table_widget.rowCount()
    window.table_widget.insertRow(row_number)
    
    #OBTAIN ETA
    number_of_frames = video.get_number_of_frames()
    eta = obtain_ETA(number_of_frames)

    if eta is None:
        eta = "Unknown"

    #OTAIN THE FIRST FRAME
    status, frame = video.get_first_frame()
    cell_width = window.table_widget.columnWidth(0)
    cell_height = 50

    #Get the pixmap from the image
    scaled_pixmap = convert_frame_to_pixmap(frame, dimensions = [cell_width, cell_height])

    #Generate widget to include the pixmap in
    image_widget = _create_table_widget(scaled_pixmap, "image")

    #OBTAIN THE BUTTON
    btn = _generate_closing_button(window, row_number)
    btn_widget = _create_table_widget(btn, "button")


    #ADD THE ELEMENTS TO THE ROW
    file_name_item = QTableWidgetItem(file_name)
    file_name_item.setFlags(file_name_item.flags() & ~Qt.ItemIsEditable)
    eta_item = QTableWidgetItem(eta)
    eta_item.setFlags(eta_item.flags() & ~Qt.ItemIsEditable)
    date_item = QTableWidgetItem(str(get_local_date()))
    date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
    window.table_widget.setItem(row_number, 0, file_name_item) 
    # window.table_widget.setItem(row_number, 1, eta_item)
    window.table_widget.setItem(row_number, 1, date_item)  
    window.table_widget.setCellWidget(row_number, 2, image_widget)
    window.table_widget.setCellWidget(row_number, 3, btn_widget) 

    window.table_widget.setRowHeight(row_number, cell_height)
    window.table_widget.add_item(video)


def delete_row(btn_table, table_widget):
    row = btn_table.get_row()
    row_number = table_widget.rowCount()

    if row is not None:
        table_widget.remove_item(row)
        for i in range(row + 1, row_number):
            print(i)
            table_widget.cellWidget(i, 3).findChildren(PyTablePushButton)[0].set_row(i - 1)
        table_widget.removeRow(row)

def round_if_necessary(value):
    if isinstance(value, (int, float)):
        rounded_value = round(value, 2)
        if isinstance(rounded_value, (int)) or rounded_value.is_integer():
            return int(rounded_value)  # Convert to int if it's a whole number
        else:
            return rounded_value
    else:
        return value  # Keep non-numeric values as they are

def add_result(window, processed_results, video):
    name = os.path.basename(video.path)
    row_count = window.results_table.rowCount()
    column_count = window.results_table.columnCount()

    # results_table_mutex = QMutex()
    
    for row in range(row_count):
        file_name = window.results_table.item(row, 0).text()
        if file_name == name:
            for col in range(1, column_count):
                header_item = window.results_table.horizontalHeaderItem(col)
                header_text = header_item.text() if header_item else ""
                print("header_text", header_text)
                result = round_if_necessary(processed_results[header_text])
                item = QTableWidgetItem(str(result))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                print(result)
                item.setTextAlignment(Qt.AlignCenter)
                window.results_table.table_mutex.lock()
                try:
                    window.results_table.setItem(row, col, item)
                finally:
                    window.results_table.table_mutex.unlock()
                # Now you have both the header_text and the cell text
                # result_item = QTableWidgetItem(str(processed_results[header_text]))  # Subtract 1 because the first column is for file names
                # result_item.setTextAlignment(Qt.AlignCenter)
                # window.results_table.setItem(row, col, result_item)
            # for i, result in enumerate(processed_results):
            #     result_item = QTableWidgetItem(str(result))
            #     result_item.setTextAlignment(Qt.AlignCenter)
            #     window.results_table.setItem(row, i + 1, result_item)
            break
    
def display_cropped_frames(window):
    number_of_rows = window.table_widget.rowCount()
    if number_of_rows == 0:
        # CREATE CUSTOM BUTTON 2
        raise ResourceNotFoundException(RT.VIDEO)
    points = {}
    for video in window.table_widget.items:
        status, frames = video.get_cropped_frames()
        if status != "Ok":
            raise VideoErrorException(video_name=video.get_file_name())
        else:
            try:
                point = open_analysis_dialog(frames)
                if point is None:
                    return 
                print(point)
                video.set_point(False, point)
                
                points[video.id] = point
            except Exception as e:
                raise(e)

    MainFunctions.set_page(window, window.ui.load_pages.page_3)
    window.ui.load_pages.page_3_pages.setCurrentIndex(1)
    print("this", window.btn_2)

    top_btn_settings = MainFunctions.get_title_bar_btn(window, "btn_top_settings")
    # top_btn_settings.set_active(False)
    window.ui.left_menu.select_only_one_tab(window.btn_3.objectName())

    btn_page_3 = window.ui.left_menu.findChildren(QPushButton, "btn_page_3")
    btn_page_2 = window.ui.left_menu.findChildren(QPushButton, "btn_page_2")
    btn_page_2[0].set_active(False)
    btn_page_3[0].set_active(True)
    return "Ok"

# @Slot(int)    
# def actualize_percentage(window, new_percentage):
#     print("new_percentage", new_percentage)
#     window.circular_progress.set_value(new_percentage)
#     # self.show()                
        

def open_analysis_dialog(frames):
    dialog = AnalysisDialog(frames)
    dialog.exec_()
    point = dialog.point
    print("point", point)
    del dialog
    
    return point