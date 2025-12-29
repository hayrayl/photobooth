import os
from PyQt5 import QtCore, QtGui, QtWidgets

def pink_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../images/pink_background.png")
    background.setPixmap(QtGui.QPixmap(background_path))