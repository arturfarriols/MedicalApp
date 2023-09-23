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
from . functions_main_window import *
from .logic_functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *

# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_page_2",
            "btn_text" : "Video Analyzer",
            "btn_tooltip" : "Video analyzer page",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_file.svg",
            "btn_id" : "btn_page_3",
            "btn_text" : "Results",
            "btn_tooltip" : "Results page",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_info.svg",
            "btn_id" : "btn_menu_2",
            "btn_text" : "Open Information Menu",
            "btn_tooltip" : "Open information menu",
            "show_top" : False,
            "is_active" : False
        },
        # {
        #     "btn_icon" : "icon_settings.svg",
        #     "btn_id" : "btn_settings",
        #     "btn_text" : "Open Settings",
        #     "btn_tooltip" : "Open settings",
        #     "show_top" : False,
        #     "is_active" : False
        # }
    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_search",
            "btn_tooltip" : "Search",
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_top_settings",
            "btn_tooltip" : "Top settings",
            "is_active" : False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        # print(self)
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
        



    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # CREATE CUSTOM BUTTON
        self.btn_1 = PyPushButton(
            text = "Btn 1",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"],
            # text_align = "right"
        )

        self.btn_1.setMinimumHeight(40)
    
        # CREATE CUSTOM BUTTON 2
        self.btn_2 = PyPushButton(
            text = "Browse Files",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"],
            text_align = "left",
            id = "browse_files_btn"
        )

        self.btn_2.setMinimumHeight(40)
        self.btn_2.setObjectName("btn_2")
        self.btn_2.setMaximumWidth(100)
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_folder_open.svg"))
        self.btn_2.setIcon(self.icon_2)

        self.btn_2.clicked.connect(lambda: self.button_clicked(self.btn_2.id))


        # TABLE WIDGETS
        self.table_widget = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.table_widget.setColumnCount(5)
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("FILE NAME")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("ESTIMATED PROCESSING TIME")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("DATE")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("PREVIEW")

        self.column_5 = QTableWidgetItem()
        self.column_5.setTextAlignment(Qt.AlignCenter)
        self.column_5.setText("DELETE")

        # Set column
        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)
        self.table_widget.setHorizontalHeaderItem(3, self.column_4)
        self.table_widget.setHorizontalHeaderItem(4, self.column_5)

        # Set column widths
        # total_width = self.table_widget.width()
        # first_column_width = total_width   # First column width is set to half of the table width
        # remaining_width = total_width - first_column_width  # Remaining width for the second and third columns
        # half_remaining_width = remaining_width * 0.5  # Width for the second and third columns is set to half of the remaining width

        # Set width policies
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Stretch column width
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Stretch column width
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Stretch column width
        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Fix column width
        self.table_widget.setColumnWidth(3, 150)
        self.table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Adjust width to contents
        self.table_widget.setColumnWidth(4, 150)

        # CREATE CUSTOM BUTTON 2
        self.btn_3 = PyPushButton(
            text = "Analysis",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"],
            text_align = "center",
            id = "analysis_btn"
        )

        self.btn_3.setMinimumHeight(40)
        self.btn_3.setObjectName("btn_3")
        self.btn_3.setMinimumWidth(200)
        self.btn_3.setMaximumWidth(200)
        self.btn_3.clicked.connect(lambda: self.button_clicked(self.btn_3.id, [self.table_widget]))

        # CREATE CUSTOM TOGGLE BUTTON
        self.toggle_1 = PyToggle(
            active_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["dark_one"],
            circle_color = self.themes["app_color"]["icon_color"],
            width = 50
        )

        self.label_1 = PyLabel("Any videos processed", "white", "Segoe UI", 24)

        # ADD TO LAYOUT
        self.ui.left_column.menus.btn_1_layout.addWidget(self.btn_1)
        self.ui.left_column.menus.btn_2_layout.addWidget(self.toggle_1, Qt.AlignCenter, Qt.AlignCenter)

        self.ui.load_pages.file_browser_layout.addWidget(self.btn_2,  Qt.AlignCenter, Qt.AlignRight)
        self.ui.load_pages.table_layout.addWidget(self.table_widget)
        self.ui.load_pages.analysis_btn_layout.addWidget(self.btn_3, Qt.AlignCenter, Qt.AlignCenter)
        self.ui.load_pages.no_videos_layout.addWidget(self.label_1, Qt.AlignCenter, Qt.AlignCenter)

        # self.logo = QSvgWidget(Functions.set_svg_image("logo_home.svg"))
        self.logo = QSvgWidget(Functions.set_svg_image("main_logo.svg"))

        self.ui.load_pages.page_1_layout.addWidget(self.logo, Qt.AlignCenter, Qt.AlignCenter)

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

    def set_analysis_tab(self):
        MainFunctions.clear_analysis_tab(self)

        # CREATE CUSTOM BUTTON 2
        self.btn_cancel = PyPushButton(
            text = "Cancel analysis",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"],
            text_align = "center",
            id = "cancel_btn"
        )

        self.btn_cancel.setMinimumHeight(40)
        self.btn_cancel.setObjectName("cancel_btn")
        self.btn_cancel.setMinimumWidth(200)
        self.btn_cancel.setMaximumWidth(200)
        self.btn_cancel.clicked.connect(lambda: self.button_clicked(self.btn_cancel.id))

        row_count = self.table_widget.rowCount()
        print("row_count is: ", row_count)

        # TABLE WIDGETS
        self.results_table = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.results_table.setColumnCount(14)
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_6 = QTableWidgetItem()
        self.column_6.setTextAlignment(Qt.AlignCenter)
        self.column_6.setText("File name")

        self.column_7 = QTableWidgetItem()
        self.column_7.setTextAlignment(Qt.AlignCenter)
        self.column_7.setText("IVSs")

        self.column_8 = QTableWidgetItem()
        self.column_8.setTextAlignment(Qt.AlignCenter)
        self.column_8.setText("IVSd")

        self.column_9 = QTableWidgetItem()
        self.column_9.setTextAlignment(Qt.AlignCenter)
        self.column_9.setText("LVIDs")

        self.column_10 = QTableWidgetItem()
        self.column_10.setTextAlignment(Qt.AlignCenter)
        self.column_10.setText("LVIDd")

        self.column_11 = QTableWidgetItem()
        self.column_11.setTextAlignment(Qt.AlignCenter)
        self.column_11.setText("LVPWs")

        self.column_12 = QTableWidgetItem()
        self.column_12.setTextAlignment(Qt.AlignCenter)
        self.column_12.setText("LVPWd")

        self.column_13 = QTableWidgetItem()
        self.column_13.setTextAlignment(Qt.AlignCenter)
        self.column_13.setText("LVESV")

        self.column_14 = QTableWidgetItem()
        self.column_14.setTextAlignment(Qt.AlignCenter)
        self.column_14.setText("LVEDV")

        self.column_15 = QTableWidgetItem()
        self.column_15.setTextAlignment(Qt.AlignCenter)
        self.column_15.setText("FS")

        self.column_16 = QTableWidgetItem()
        self.column_16.setTextAlignment(Qt.AlignCenter)
        self.column_16.setText("EF")

        # self.column_17 = QTableWidgetItem()
        # self.column_17.setTextAlignment(Qt.AlignCenter)
        # self.column_17.setText("LV")

        self.column_17 = QTableWidgetItem()
        self.column_17.setTextAlignment(Qt.AlignCenter)
        self.column_17.setText("SV")

        self.column_18 = QTableWidgetItem()
        self.column_18.setTextAlignment(Qt.AlignCenter)
        self.column_18.setText("CO")

        self.column_19 = QTableWidgetItem()
        self.column_19.setTextAlignment(Qt.AlignCenter)
        self.column_19.setText("HR")

        # Set column
        self.results_table.setHorizontalHeaderItem(0, self.column_6)
        self.results_table.setHorizontalHeaderItem(1, self.column_7)
        self.results_table.setHorizontalHeaderItem(2, self.column_8)
        self.results_table.setHorizontalHeaderItem(3, self.column_9)
        self.results_table.setHorizontalHeaderItem(4, self.column_10)
        self.results_table.setHorizontalHeaderItem(5, self.column_11)
        self.results_table.setHorizontalHeaderItem(6, self.column_12)
        self.results_table.setHorizontalHeaderItem(7, self.column_13)
        self.results_table.setHorizontalHeaderItem(8, self.column_14)
        self.results_table.setHorizontalHeaderItem(9, self.column_15)
        self.results_table.setHorizontalHeaderItem(10, self.column_16)
        self.results_table.setHorizontalHeaderItem(11, self.column_17)
        self.results_table.setHorizontalHeaderItem(12, self.column_18)
        self.results_table.setHorizontalHeaderItem(13, self.column_19)

        # Set the width of a specific column
        # target_column = 0
        # target_width = 400
        # table_widget.setColumnWidth(target_column, target_width)

        # # Set the horizontal header resize mode to stretch
        # header = table_widget.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setColumnWidth(0, 200)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  
        self.results_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)  
        self.results_table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(13, QHeaderView.ResizeMode.Stretch)

        self.results_table.setRowCount(row_count)

        for i in range(row_count):
            text = self.table_widget.item(i, 0).text()
            self.results_table.setItem(i, 0, QTableWidgetItem(text))


        # CIRCULAR PROGRESS 2
        self.circular_progress = PyCircularProgress(
            value = 0,
            progress_width = 8,
            progress_color = self.themes["app_color"]["context_color"],
            text_color = self.themes["app_color"]["context_color"],
            font_size = 14,
            bg_color = self.themes["app_color"]["bg_three"]
        )
        self.circular_progress.setFixedSize(160,160)

        # CREATE CUSTOM BUTTON 2
        self.btn_export = PyPushButton(
            text = "Export results",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"],
            text_align = "center",
            id = "export_btn"
        )
        # self.btn_export.setEnabled(False)
        self.btn_export.setMinimumHeight(40)
        self.btn_export.setObjectName("export_btn")
        self.btn_export.setMinimumWidth(200)
        self.btn_export.setMaximumWidth(200)
        self.btn_export.clicked.connect(lambda: self.button_clicked(self.btn_export.id))

        self.ui.load_pages.percentage_layout.addWidget(self.circular_progress,  Qt.AlignCenter, Qt.AlignCenter)
        self.ui.load_pages.percentage_layout.addWidget(self.btn_cancel,  Qt.AlignCenter, Qt.AlignRight)
        self.ui.load_pages.results_table_layout.addWidget(self.results_table)
        self.ui.load_pages.export_layout.addWidget(self.btn_export)

    def actualize_percentage(self, percentage):
        self.circular_progress.set_value(percentage)

    def actualize_results_table(self, processed_results, video):
        add_result(self, processed_results, video)