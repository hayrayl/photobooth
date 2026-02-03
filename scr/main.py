import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt 


sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from ui_functions.launch_screen_function import LaunchScreen
from ui_functions.home_screen_function import HomeScreen
from ui_functions.take_photo_screen_function import TakePhotoScreen
from ui_functions.display_photo_screen_function import DisplayPhotoScreen
from ui_functions.ask_to_email_screen_function import AskToEmailScreen
from ui_functions.send_email_screen_function import SendEmailScreen

from camera.camera_controller import CameraController
from utilities.usb_manager import USBManager

# Index for which screen: 
# 0 : launch screen

class PhotoboothWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUI()
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # Party name and photo counter
        self.party_name = "haylie_party"  # Change this for each event
        self.photo_session_counter = 1  # Tracks session number (increments for each 3-photo burst)

        # USB Manager
        self.usb_manager = USBManager()

        # Check internet connection at startup
        self.has_internet = self.usb_manager.is_connected_to_internet()
        print(f"Internet connection: {'Yes' if self.has_internet else 'No'}")
        
        # Create unique party folder (on USB if available, local if not)
        self.party_folder = self.create_party_folder_smart(self.party_name)

        # Initialize camera once
        self.camera = CameraController(camera_index=0, resolution=(1920, 1080))
        self.camera.open_camera()


        # initialize all of the screens 
        self.launch_screen = LaunchScreen(self)
        self.home_screen = HomeScreen(self)
        self.take_photo_screen = TakePhotoScreen(self, self.camera)
        self.display_photo_screen = DisplayPhotoScreen(self)
        self.ask_to_email_screen = AskToEmailScreen(self)  
        self.send_email_screen = SendEmailScreen(self)

        # This adds the screens to the stack. The index is how you know what screen to switch to
        # add the screen to the stack                           # Index 
        self.stackedWidget.addWidget(self.launch_screen)        # 0
        self.stackedWidget.addWidget(self.home_screen)          # 1 
        self.stackedWidget.addWidget(self.take_photo_screen)    # 2 
        self.stackedWidget.addWidget(self.display_photo_screen) # 3
        self.stackedWidget.addWidget(self.ask_to_email_screen)  # 4 
        self.stackedWidget.addWidget(self.send_email_screen)    # 5

        
        # initializing to the launch screen 
        self.stackedWidget.setCurrentIndex(1)

        self.resize(1024,600) # setting the size of the screen 
        self.setMaximumSize(1024,600)

        self.move(0,0)
        
    def setIndex(self, index):
        self.stackedWidget.setCurrentIndex(int(index))

    def get_next_photo_name(self):
        """Generate next photo filename"""
        filename = f"{self.party_name}_{self.photo_counter}"
        self.photo_counter += 1
        return filename
    
    def reset_photo_counter(self):
        """Reset counter for new party/session"""
        self.photo_counter = 1

    # this adds an escape to exit the application, press Esc 
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def create_party_folder(self, party_name, base_dir="photos"):
        """
        Create a unique folder for the party
        If folder exists, append _1, _2, etc.
        """
        os.makedirs(base_dir, exist_ok=True)
        
        folder_path = os.path.join(base_dir, party_name)
        
        counter = 1
        while os.path.exists(folder_path):
            folder_path = os.path.join(base_dir, f"{party_name}_{counter}")
            counter += 1
        
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created party folder: {folder_path}")
        
        return folder_path
    
    def create_party_folder_smart(self, party_name):
        """
        Create party folder on USB if available, otherwise local
        
        Args:
            party_name: Name of the party
        Returns:
            Path to the created folder
        """
        # Check if USB is connected
        if self.usb_manager.is_usb_connected():
            usb_path = self.usb_manager.get_first_usb()
            base_dir = os.path.join(usb_path, "photobooth_photos")
            print(f"USB detected! Saving to: {base_dir}")
        else:
            base_dir = "photos"
            print("No USB detected. Saving locally to: photos/")
        
        # Create the party folder
        return self.create_party_folder(party_name, base_dir=base_dir)
    
    def is_saving_to_usb(self):
        """Check if currently saving to USB"""
        return self.party_folder.startswith("/media") or self.party_folder.startswith("/mnt")
    
    def set_new_party(self, party_name):
        """
        Set a new party name and create its folder
        Use this when starting a new party/event
        
        Args:
            party_name: Name of the new party
        """
        self.party_name = party_name
        self.party_folder = self.create_party_folder(party_name)
        self.photo_session_counter = 1
        print(f"New party: {party_name}, folder: {self.party_folder}")


    def get_template_path(self):
        """
        Get template path - checks USB first, then uses default
        
        Returns:
            Path to template image
        """
        # Default template path
        default_template = os.path.join(
            os.path.dirname(__file__),
            "images/photo_strip_template.png"
        )
        
        # Check for template on USB
        usb_template = self.usb_manager.find_template_on_usb()
        
        if usb_template and os.path.exists(usb_template):
            print(f"Using USB template: {usb_template}")
            return usb_template
        else:
            print(f"Using default template: {default_template}")
            return default_template
        
    def check_internet_connection(self):
        """
        Check internet connection status
        Updates self.has_internet
        """
        self.has_internet = self.usb_manager.is_connected_to_internet()
        return self.has_internet

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoboothWindow()

    # this will show the full screen for the raspberry pi
    # window.showFullScreen() 

    # this is better for development 
    window.show()
    sys.exit(app.exec_())