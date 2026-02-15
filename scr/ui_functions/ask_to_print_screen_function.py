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
        
        self.strip_path = None  # ADD THIS

        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)

    def connect_signals(self):
        self.pushButton_yes.clicked.connect(self.go_to_print)
        self.pushButton_no.clicked.connect(self.go_to_home)

    def set_strip(self, strip_path):
        """Set the photo strip to print"""
        self.strip_path = strip_path
        print(f"Strip path set: {strip_path}")

    def showEvent(self, event):
        """Check printer status when screen appears"""
        super().showEvent(event)
        
        # Re-apply color scheme
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)
        
        # If no printer connected, skip straight to home
        if not self.main_window.printer_manager.is_printer_connected():
            print("No printer connected - skipping print screen")
            QtCore.QTimer.singleShot(0, self.go_to_home)
            return
        
        # Printer is connected - show screen normally
        self.pushButton_yes.setEnabled(True)
        self.pushButton_yes.setText("Yes, print it!")
        self.label_main.setText("Would you like to print\nyour photo strip?")

    def go_to_print(self):
        """User wants to print"""
        if not self.strip_path:
            print("ERROR: No strip path set")
            self.go_to_home()
            return
        
        # Show printing message
        self.label_main.setText("Printing...")
        self.pushButton_yes.setEnabled(False)
        self.pushButton_no.setEnabled(False)
        QtWidgets.QApplication.processEvents()
        
        # Print the strip
        success = self.main_window.printer_manager.print_photo_strip(self.strip_path)
        
        if success:
            self.label_main.setText("Printing! ✓")
            QtCore.QTimer.singleShot(2000, self.go_to_home)
        else:
            self.label_main.setText("Print failed.\nTry again?")
            self.pushButton_yes.setEnabled(True)
            self.pushButton_no.setEnabled(True)

    def go_to_home(self):
        """Go back to home screen"""
        self.pushButton_yes.setEnabled(True)
        self.pushButton_no.setEnabled(True)
        self.pushButton_yes.setText("Yes, print it!")
        self.parentWidget().setCurrentIndex(1)