import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from ui_screens.ask_to_email import Ui_Ask_Email

class AskToEmailScreen(QtWidgets.QWidget, Ui_Ask_Email):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        
        self.captured_photos = []  # Will be set by previous screen
        
        # Setup design and connect buttons
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)

    def connect_signals(self):
        self.pushButton_yes.clicked.connect(self.go_to_email_input)
        self.pushButton_no.clicked.connect(self.go_to_home)

    def set_photos(self, photo_paths):
        """Set the photos that were just taken"""
        self.captured_photos = photo_paths

    def go_to_email_input(self):
        """User wants to email - go to email input screen"""
        print("User wants to email photos")
        
        # Get the photo strip path
        strip_path = os.path.join(
            self.main_window.party_folder,
            f"strip_{self.main_window.photo_session_counter - 1}.jpg"
        )
        
        # Pass photos to email screen
        email_screen = self.main_window.send_email_screen
        email_screen.set_photos(self.captured_photos, strip_path)
        
        # Navigate to email input screen
        self.parentWidget().setCurrentIndex(5)  # Index 5 is send_email_screen

    def go_to_home(self):
        """User doesn't want to email - go back to home"""
        print("User declined email")
        self.parentWidget().setCurrentIndex(1)  # Adjust to your home screen index