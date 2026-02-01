import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from ui_screens.display_photo import Ui_Display_Images

class DisplayPhotoScreen(QtWidgets.QWidget, Ui_Display_Images):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        
        self.photo_paths = []
        
        # Setup design and connect buttons
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.pink_background(self.background)

        
        # Make labels display images properly
        self.label_image_1.setScaledContents(True)
        self.label_image_2.setScaledContents(True)
        self.label_image_3.setScaledContents(True)

    def connect_signals(self):
        self.pushButton_to_print.clicked.connect(self.go_to_ask_email)

    def set_photos(self, photo_paths):
        """Set the photos to display"""
        self.photo_paths = photo_paths
        
        # Display each photo
        if len(photo_paths) >= 1:
            self.display_photo(photo_paths[0], self.label_image_1)
        
        if len(photo_paths) >= 2:
            self.display_photo(photo_paths[1], self.label_image_2)
        
        if len(photo_paths) >= 3:
            self.display_photo(photo_paths[2], self.label_image_3)

    def display_photo(self, photo_path, label):
        """Load and display a photo in a label"""
        frame = cv2.imread(photo_path)
        
        if frame is None:
            print(f"Failed to load: {photo_path}")
            return
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get label size
        label_width = label.width()
        label_height = label.height()
        
        # Resize to fit label (square images fit into square labels)
        resized = cv2.resize(rgb_frame, (label_width, label_height))
        
        # Convert to QImage
        h, w, ch = resized.shape
        bytes_per_line = ch * w
        qt_image = QtGui.QImage(resized.data, w, h, bytes_per_line, 
                                QtGui.QImage.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    def go_to_ask_email(self):
        """Go back to home screen"""
        self.parentWidget().setCurrentIndex(4)  