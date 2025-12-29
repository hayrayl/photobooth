import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens import Ui_Launch

class LaunchScreen(QtWidgets.QWidget, Ui_Launch):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window= main_window
        
        self.design_setup()

        
    def design_setup(self):
        utils_screen.pink_background(self.background)