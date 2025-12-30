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

from camera.camera_controller import CameraController

# Index for which screen: 
# 0 : launch screen

class PhotoboothWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUI()
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # Party name and photo counter
        self.party_name = "haylie"  # Change this for each event
        self.photo_session_counter = 1  # Tracks session number (increments for each 3-photo burst)

        # Create unique party folder
        self.party_folder = self.create_party_folder(self.party_name)

        # Initialize camera once
        self.camera = CameraController(camera_index=0, resolution=(1920, 1080))
        self.camera.open_camera()


        # initialize all of the screens 
        self.launch_screen = LaunchScreen(self)
        self.home_screen = HomeScreen(self)
        self.take_photo_screen = TakePhotoScreen(self, self.camera)
        self.display_photo_screen = DisplayPhotoScreen(self)

        # This adds the screens to the stack. The index is how you know what screen to switch to
        # add the screen to the stack                           # Index 
        self.stackedWidget.addWidget(self.launch_screen)        # 0
        self.stackedWidget.addWidget(self.home_screen)          # 1 
        self.stackedWidget.addWidget(self.take_photo_screen)    # 2 
        self.stackedWidget.addWidget(self.display_photo_screen)

        
        # initializing to the launch screen 
        self.stackedWidget.setCurrentIndex(2)

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
        
        Args:
            party_name: Name of the party
            base_dir: Base directory for photos
        Returns:
            Path to the created folder
        """
        # Create base photos directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        # Start with the original party name
        folder_path = os.path.join(base_dir, party_name)
        
        # If folder exists, append _1, _2, _3, etc.
        counter = 1
        while os.path.exists(folder_path):
            folder_path = os.path.join(base_dir, f"{party_name}_{counter}")
            counter += 1
        
        # Create the folder
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created party folder: {folder_path}")
        
        return folder_path
    
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
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoboothWindow()

    # this will show the full screen for the raspberry pi
    # window.showFullScreen() 

    # this is better for development 
    window.show()
    sys.exit(app.exec_())