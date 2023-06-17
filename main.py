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
from gui.uis.windows.main_window.functions_main_window import *
from gui.uis.windows.main_window.logic_functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        
        print("name is", self.sender().objectName())
        btn = SetupMainWindow.setup_btns(self)
        # btn = self.sender()
        print("name is", btn.objectName())
        print("name is", self.sender().objectName())
        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # HOME PAGE
        if btn.objectName() == "btn_home":
            # Select button
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # PAGE 2
        if btn.objectName() == "btn_page_2":
            # Select button
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # PAGE 3
        if btn.objectName() == "btn_page_3":
            # Select button
            self.ui.left_menu.select_only_one(btn.objectName()) 

            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # GET TOP SETTINGS
        top_btn_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")  

        # PAGE SETTINGS
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            #Deselect title bar buttons
            top_btn_settings.set_active(False)

            # Check if Left column is visible
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column": 
                    # Deselect all tabs
                    self.ui.left_menu.deselect_all_tab()

                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                # Select tab
                self.ui.left_menu.select_only_one_tab(btn.objectName())

        # PAGE MENU 2
        if btn.objectName() == "btn_menu_2" or btn.objectName() == "btn_close_left_column":
            #Deselect title bar buttons
            top_btn_settings.set_active(False)

            # Check if Left column is visible
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column": 
                    # Deselect all tabs
                    self.ui.left_menu.deselect_all_tab()

                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                # Select tab
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            #Change Left Page
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                    )

        # PAGE SETTINGS
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # Check if Left column is visible
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column": 
                    # Deselect all tabs
                    self.ui.left_menu.deselect_all_tab()

                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                # Select tab
                self.ui.left_menu.select_only_one_tab(btn.objectName())

           #Change Left Page
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings tab",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                    )
        # print(btn.objectName())
        #FILE BROWSER
        if btn.objectName() == "btn_2":
            MainFunctions.open_file_browser(self)

        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Settings            
            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            btn_settings.set_active_tab(False)  

            # Get Left Menu Info            
            btn_info = MainFunctions.get_left_menu_btn(self, "btn_menu_2")
            btn_info.set_active_tab(False)        

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    @Slot(str)
    def button_clicked(self, button_id):
        if button_id == "browse_files_btn":
            print("""Button "browse_files_btn" was clicked""")
            result = open_file_browser(self)
        if button_id == 2:
            print("Button 2 was clicked")

        return result

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())