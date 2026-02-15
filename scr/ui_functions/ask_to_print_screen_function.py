import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from ui_screens.ask_to_print import Ui_Ask_Print

class AskToPrintScreen(QtWidgets.QWidget, Ui_Ask_Print):
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
        self.pushButton_yes.clicked.connect(self.go_to_print)
        self.pushButton_no.clicked.connect(self.go_to_home)

    def go_to_print(self):
        """User wants to print - handle printing"""
        print("User wants to print photos")
        # TODO: Implement printing functionality
        self.go_to_home()

    def go_to_home(self):
        """Go back to home screen"""
        print("User declined print")
        self.parentWidget().setCurrentIndex(1)