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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import sys
import os
from functools import partial

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

from gui.widgets import *

from gui.uis.utils import *

from models import * 

def _check_file_extension_is_valid(file_path):
    valid_extensions = ['py', 'mp4', 'avi', 'mov', 'mkv', 'wmv'] #Remove .py
    
    file_extension = file_path.split('.')[-1].lower()
    print(file_extension)
    
    if file_extension in valid_extensions:
        return True
    else:
        return False

def open_file_browser(window):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(window, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
    
    if file_path:
        print("Selected file:", file_path)
    
        if not _check_file_extension_is_valid(file_path):
            # File format is not valid

            # CREATE CUSTOM BUTTON 2
            message_box = PyMessageBox(
                text = "The selected file format is not valid.",
                title = "Invalid File Format",
                icon = QMessageBox.Warning, 
                color = "#333333",
                radius = 0,
                msg_bg_color = "#F0F0F0",
                btn_bg_color = "#F8F8F8",
                btn_bg_color_hover = "#E8E8E8",
                btn_bg_color_pressed = "#D0D0D0",
                id = "warning pop up"
            )
            # message_box = QMessageBox()
            # message_box.setIcon(QMessageBox.Warning)
            # message_box.setWindowTitle("Invalid File Format")
            # message_box.setText("The selected file format is not valid.")
            message_box.exec_()
            return None
        else:
            add_row(window, file_path)
            return file_path

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
    # file_name = os.path.basename(file_path)
    # video = Video(None, file_path)

    # status, frame = video.get_first_frame()
    # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

    # # Create a QPixmap from the QImage
    # pixmap = QPixmap.fromImage(image)
    # # Scale the image to fit the width and height of the table cell
    # cell_width = table.columnWidth(1)  # Width of the first column
    # cell_height = 50  # Height of the new row
    # scaled_pixmap = pixmap.scaled(cell_width, cell_height, Qt.KeepAspectRatio)

    # frame_item = QTableWidgetItem()
    # frame_item.setData(Qt.DecorationRole, scaled_pixmap)  # Load the image
    # frame_item.setTextAlignment(Qt.AlignCenter)  # Center the image vertically

    # print(type(frame))


    # row_number = table.rowCount()
    # table.insertRow(row_number)
    # table.setItem(row_number, 0, QTableWidgetItem(file_name)) # Add nick
    # # table.cellWidget(row_number, 0).setPixmap(scaled_pixmap)
    # # table.setItem(row_number, 1, QTableWidgetItem(""))  # Add an empty item for the second column
    # table.setItem(row_number, 1, frame_item) # Add nick
    # pass_text = QTableWidgetItem()
    # pass_text.setTextAlignment(Qt.AlignCenter)
    # pass_text.setText("12345" + "12")
    # table.setItem(row_number, 2, pass_text) # Add pass
    # table.setRowHeight(row_number, 50)

    video = Video(None, file_path)
    #INSERT ROW
    row_number = window.table_widget.rowCount()
    window.table_widget.insertRow(row_number)
    
    #OBTAIN THE FILE NAME
    file_name = os.path.basename(file_path)

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
    window.table_widget.setItem(row_number, 0, QTableWidgetItem(file_name)) 
    window.table_widget.setItem(row_number, 1, QTableWidgetItem(eta))
    window.table_widget.setItem(row_number, 2, QTableWidgetItem(str(get_local_date())))  
    window.table_widget.setCellWidget(row_number, 3, image_widget)
    window.table_widget.setCellWidget(row_number, 4, btn_widget) 

    # pass_text = QTableWidgetItem()
    # pass_text.setTextAlignment(Qt.AlignCenter)
    # pass_text.setText("12345" + "12")
    # window.table_widget.setItem(row_number, 2, pass_text)  # Add pass

    window.table_widget.setRowHeight(row_number, cell_height)


def delete_row(btn_table, table_widget):
    row = btn_table.get_row()
    row_number = table_widget.rowCount()

    if row is not None:
        for i in range(row + 1, row_number):
            table_widget.cellWidget(i, 2).findChildren(PyTablePushButton)[0].set_row(i - 1)
        table_widget.removeRow(row)

    # if isinstance(sender, QPushButton):
    #     btn_row = sender.get_row()  # Get the row number stored in the button
    #     if btn_row is not None:
    #         window.table_widget.removeRow(btn_row)  # Remove the row from the table
    #         # Update the row numbers of the remaining buttons
    #         for row in range(window.table_widget.rowCount()):
    #             btn_widget = window.table_widget.cellWidget(row, 2)
    #             if isinstance(btn_widget, PyTablePushButton):
    #                 btn_widget.set_row(row)
    
