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
        utils_screen.purple_background(self.background)

    def connect_signals(self):
        self.pushButton_take_photo.clicked.connect(self.take_photo)
        self.pushButton_to_launch.clicked.connect(self.go_to_launch)
        

    def take_photo(self):
        print("Pressed take photo button")

    def go_to_launch(self):
        self.parentWidget().setCurrentIndex(0)