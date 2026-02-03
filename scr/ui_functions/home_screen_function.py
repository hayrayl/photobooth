import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens.home_screen import Ui_Home

class HomeScreen(QtWidgets.QWidget, Ui_Home):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window= main_window
        
        self.design_setup()
        self.connect_signals()


    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)

    def connect_signals(self):
        self.pushButton_take_photo.clicked.connect(self.take_photo)
        self.pushButton_to_launch.clicked.connect(self.go_to_launch)
        

    def take_photo(self):
        print("Pressed take photo button")
        self.parentWidget().setCurrentIndex(2)

    def go_to_launch(self):
        self.parentWidget().setCurrentIndex(0)

    def showEvent(self, event):
        """Update USB status when screen appears"""
        super().showEvent(event)
        self.check_usb_status()

    def check_usb_status(self):
        """Check and display USB connection status"""
        if self.main_window.usb_manager.is_usb_connected():
            usb_path = self.main_window.usb_manager.get_first_usb()
            free_space = self.main_window.usb_manager.get_usb_free_space()
            
            if free_space:
                space_str = self.main_window.usb_manager.format_bytes(free_space)
                status = f"USB Connected ({space_str} free)"
            else:
                status = "USB Connected"
            
            print(status)
            # Optional: Display on screen
            # self.label_header.setText(f"Welcome!\n{status}")
        else:
            print("No USB - saving locally")
            # Optional: Display on screen
            # self.label_header.setText("Welcome!\nNo USB - saving locally")