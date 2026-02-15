import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens.home_screen import Ui_Home

class HomeScreen(QtWidgets.QWidget, Ui_Home):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)
        

    def connect_signals(self):
        self.pushButton_take_photo.clicked.connect(self.take_photo)

    def take_photo(self):
        print("Pressed take photo button")
        self.parentWidget().setCurrentIndex(2)

    def showEvent(self, event):
        """Update color scheme and USB status when screen appears"""
        super().showEvent(event)
        # Re-apply color scheme in case it changed
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)
        self.check_usb_status()

    def check_usb_status(self):
        """Check and display USB connection status"""
        if self.main_window.usb_manager.is_usb_connected():
            free_space = self.main_window.usb_manager.get_usb_free_space()
            if free_space:
                space_str = self.main_window.usb_manager.format_bytes(free_space)
                print(f"USB Connected ({space_str} free)")
            else:
                print("USB Connected")
        else:
            print("No USB - saving locally")