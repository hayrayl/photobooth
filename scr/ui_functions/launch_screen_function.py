import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens.launch_screen import Ui_Launch

class LaunchScreen(QtWidgets.QWidget, Ui_Launch):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window= main_window
        
        # setup the design and connect all of the buttons 
        self.design_setup()
        self.connect_signals()

        self.count = 0 

    # initial design setup
    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)

    def connect_signals(self):
        self.pushButton_test.clicked.connect(self.show_secret)
        self.pushButton_to_home.clicked.connect(self.go_to_home)
        self.pushButton_change_background.clicked.connect(self.change_background)

    # Show the hidden secret on button press 
    def show_secret(self):
        self.label_test.setText("HAYLIE IS THE BESTEST!")

    # change the screen to the home
    def go_to_home(self):
        self.parentWidget().setCurrentIndex(1)

    # change the background color button 
    def change_background(self):
        self.count = self.count + 1 
        self.main_window.color_scheme = (self.count % 7) + 1
        self.design_setup()
