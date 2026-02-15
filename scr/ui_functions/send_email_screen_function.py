import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from utilities.email_sender import EmailSender 
from ui_screens.send_email import Ui_Send_Email

class SendEmailScreen(QtWidgets.QWidget, Ui_Send_Email):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        
        self.captured_photos = []  # Photos to email
        self.photo_strip_path = None  # Path to photo strip

        self.email_sender = EmailSender()
        
        # Setup design and connect buttons
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)
        utils_screen.style_all_line_edits(self, self.main_window.color_scheme)
        
        # Set placeholder text for email input
        self.lineEdit_email.setPlaceholderText("your.email@example.com")
        
        # Clear any previous email
        self.lineEdit_email.clear()

        # Initially hide the sending label
        self.label_sending.hide()

    def showEvent(self, event):
        super().showEvent(event)
        # Apply the chosen color scheme
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        utils_screen.style_all_buttons(self, self.main_window.color_scheme)
        utils_screen.style_all_labels(self, self.main_window.color_scheme)
        utils_screen.style_all_line_edits(self, self.main_window.color_scheme)

    def connect_signals(self):
        self.pushButton_send.clicked.connect(self.send_email)
        self.pushButton_skip.clicked.connect(self.skip_email)

    def set_photos(self, photo_paths, strip_path=None):
        """Set the photos and photo strip to email"""
        self.captured_photos = photo_paths
        self.photo_strip_path = strip_path

    def validate_email(self, email):
        """
        Validate email format
        Returns: True if valid, False otherwise
        """
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def show_sending_screen(self, message):
        """
        Show only the sending label with a message, hide everything else
        
        Args:
            message: Text to display (e.g., "Sending..." or "Email sent!")
        """
        # Hide input elements
        self.lineEdit_email.hide()
        self.label_main.hide()
        self.pushButton_send.hide()
        self.pushButton_skip.hide()
        
        # Show and update sending label
        self.label_sending.setText(message)
        self.label_sending.show()

    def show_input_screen(self):
        """Show the email input elements, hide sending label"""
        # Show input elements
        self.lineEdit_email.show()
        self.label_main.show()
        self.pushButton_send.show()
        self.pushButton_skip.show()
        
        # Hide sending label
        self.label_sending.hide()

    def send_email(self):
        """Send email with photos"""
        email = self.lineEdit_email.text().strip()
        
        # Validate email
        if not email:
            self.label_main.setText("Please enter an email address")
            return
        
        if not self.validate_email(email):
            self.label_main.setText("Invalid email format")
            return
        
        # Show sending screen
        self.show_sending_screen("Sending...")
        
        # Force UI to update
        QtWidgets.QApplication.processEvents()
        
        # Send email
        success = self.send_photos_via_email(email)
        
        if success:
            self.show_sending_screen("Email sent! ✓")
            # Wait a moment then go home
            QtCore.QTimer.singleShot(2000, self.go_to_home)
        else:
            # Show error and go back to input
            self.show_input_screen()
            self.label_main.setText("Failed to send. Try again?")

    def send_photos_via_email(self, recipient_email):
        """
        Actually send the email with photos
        
        Args:
            recipient_email: Email address to send to
        Returns:
            True if successful, False otherwise
        """
        print(f"Sending photos to: {recipient_email}")
        print(f"Photo strip: {self.photo_strip_path}")

        print(f"Email address: {self.email_sender.email_address}")
        print(f"Strip path exists: {os.path.exists(self.photo_strip_path)}")
        
        # Send the email using EmailSender
        success = self.email_sender.send_photo_strip(
            recipient_email=recipient_email,
            photo_strip_path=self.photo_strip_path,
            individual_photos=self.captured_photos
        )
        
        return success

    def skip_email(self):
        """User clicked skip - go home without emailing"""
        print("User skipped email")
        self.go_to_home()

    def go_to_home(self):
        """Go back to home screen"""
        # Clear email input for next user
        self.lineEdit_email.clear()
        self.label_main.setText("Enter Your Email")
        
        # Reset to input screen state
        self.show_input_screen()
        
        # Re-enable buttons
        self.pushButton_send.setEnabled(True)
        self.pushButton_skip.setEnabled(True)
        
        # Navigate to home
        self.parentWidget().setCurrentIndex(1)