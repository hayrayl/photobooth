import os
from PyQt5 import QtCore, QtGui, QtWidgets

def pink_background(background):
    path = "../images/pink_background.png"
    set_background(background, path)
    

def purple_background(background):
    path = "../images/purple_background.png"
    set_background(background, path)

def set_background(background, path):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, path)
    background.setPixmap(QtGui.QPixmap(background_path))
    background.lower()