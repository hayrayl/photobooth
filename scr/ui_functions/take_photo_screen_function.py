import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens.take_photo import Ui_TakePhoto

class TakePhotoScreen(QtWidgets.QWidget, Ui_TakePhoto):
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
        utils_screen.pink_background(self.background)

    def connect_signals(self):
        self.pushButton_take_pic.clicked.connect(self.take_pic)
        self.pushButton_to_home.clicked.connect(self.go_to_home)

    def take_pic(self):
        print("take picture pressed")
        self.count = self.count + 1
        self.label_countdown.setText(f'{self.count}')

    def go_to_home(self):
        self.parentWidget().setCurrentIndex(1)


        


