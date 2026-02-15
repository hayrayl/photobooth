import sys
import os  

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_screens.launch_screen import Ui_Launch

class LaunchScreen(QtWidgets.QWidget, Ui_Launch):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        
        # Start on color 1, track current color
        self.current_color = 1
        
        # Total number of colors available (matches utils_screen)
        self.total_colors = len(utils_screen.get_all_color_schemes())

        # Setup design and connect all of the buttons 
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        # Apply initial color scheme
        self.apply_color_scheme()
        
        # Set placeholder text
        self.lineEdit_party.setPlaceholderText("Enter Party Name...")
        
        # Clear any previous text
        self.lineEdit_party.clear()

    def apply_color_scheme(self):
        """Apply current color scheme to all elements"""
        # Set background
        utils_screen.set_background(self.background, self.current_color)
        
        # Style all buttons
        utils_screen.style_all_buttons(self, self.current_color)
        
        # Style all labels
        utils_screen.style_all_labels(self, self.current_color)
        
        # Style line edit
        utils_screen.style_all_line_edits(self, self.current_color)
        
        # Save color choice to main window
        self.main_window.color_scheme = self.current_color

    def connect_signals(self):
        self.pushButton_to_home.clicked.connect(self.go_to_home)
        self.pushButton_change_background.clicked.connect(self.change_color)

    def validate_party_name(self, party_name):
        """
        Validate party name
        Returns: True if valid, error message if not
        """
        if not party_name or party_name.strip() == "":
            return False, "Please enter a party name"
        
        if party_name.strip() == "Party Name":
            return False, "Please enter a real party name"
        
        # Check for invalid filename characters
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in party_name:
                return False, "Name cannot contain: / \\ : * ? \" < > |"
        
        return True, ""

    def go_to_home(self):
        """Validate party name and go to home screen"""
        party_name = self.lineEdit_party.text().strip()
        
        # Validate party name
        is_valid, error_message = self.validate_party_name(party_name)
        
        if not is_valid:
            self.label_test.setText(error_message)
            
            # Highlight the line edit in red
            self.lineEdit_party.setStyleSheet("""
                QLineEdit {
                    border: 4px solid red;
                    border-radius: 15px;
                    padding: 10px;
                    background-color: white;
                    color: red;
                }
            """)
            return
        
        # Set party name and color in main window
        self.main_window.set_new_party(party_name)
        print(f"Party name set to: {party_name}")
        print(f"Color scheme set to: {self.current_color}")
        
        # Go to home screen
        self.parentWidget().setCurrentIndex(1)

    def change_color(self):
        """Cycle through all available color schemes"""
        # Increment color, loop back to 1 after reaching total
        self.current_color = (self.current_color % self.total_colors) + 1
        
        # Apply new color scheme
        self.apply_color_scheme()
        
        print(f"Color changed to scheme: {self.current_color}")