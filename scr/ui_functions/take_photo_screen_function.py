import sys
import os  
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from camera.camera_controller import CameraController
from ui_screens.take_photo import Ui_TakePhoto

class TakePhotoScreen(QtWidgets.QWidget, Ui_TakePhoto):
    def __init__(self,main_window, camera, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window= main_window
        self.camera = camera

        # Timer for camera preview updates
        self.preview_timer = QtCore.QTimer()
        self.preview_timer.timeout.connect(self.update_preview)

        self.countdown_value = 3
        self.is_taking_photo = False
        self.captured_photo_path = None
        
        # setup the design and connect all of the buttons 
        self.design_setup()
        self.connect_signals()

        self.count = 0 

    # initial design setup
    def design_setup(self):
        utils_screen.pink_background(self.background)

        self.label_countdown.hide()

    def connect_signals(self):
        self.pushButton_take_pic.clicked.connect(self.start_photo_capture)
        self.pushButton_to_home.clicked.connect(self.go_to_home)

    def take_pic(self):
        print("take picture pressed")
        self.count = self.count + 1
        self.label_countdown.setText(f'{self.count}')

    def showEvent(self, event):
        """Called when screen becomes visible - start camera preview"""
        super().showEvent(event)
        self.start_preview()

    def hideEvent(self, event):
        """Called when screen is hidden - stop camera preview"""
        super().hideEvent(event)
        self.stop_preview()

    def start_preview(self):
        """Start showing live camera preview"""
        if self.camera.is_open:
            self.preview_timer.start(30)  # Update preview ~30 fps

    def stop_preview(self):
        """Stop camera preview"""
        self.preview_timer.stop()

    def update_preview(self):
        """Update the photo label with live camera feed"""
        if self.is_taking_photo:
            return  # Don't update preview during photo capture
        
        frame = self.camera.get_frame()
        if frame is not None:
            # Convert frame to QPixmap and display
            self.display_frame(frame, self.label_counte)

    def display_frame(self, frame, label):
        """Convert OpenCV frame to QPixmap and display in label"""
        import cv2
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get label size
        label_width = label.width()
        label_height = label.height()
        
        # Resize frame to fit label while maintaining aspect ratio
        h, w, ch = rgb_frame.shape
        aspect_ratio = w / h
        label_aspect = label_width / label_height
        
        if aspect_ratio > label_aspect:
            # Frame is wider - fit to width
            new_width = label_width
            new_height = int(label_width / aspect_ratio)
        else:
            # Frame is taller - fit to height
            new_height = label_height
            new_width = int(label_height * aspect_ratio)
        
        resized = cv2.resize(rgb_frame, (new_width, new_height))
        
        # Convert to QImage
        bytes_per_line = ch * new_width
        qt_image = QtGui.QImage(resized.data, new_width, new_height, 
                                bytes_per_line, QtGui.QImage.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    def start_photo_capture(self):
        """Start countdown and photo capture process"""
        if self.is_taking_photo:
            return  # Already taking photo
        
        self.is_taking_photo = True
        self.countdown_value = 3
        
        # Show countdown label
        self.label_countdown.show()
        self.label_countdown.setText(str(self.countdown_value))
        
        # Disable take photo button during capture
        self.pushButton_take_pic.setEnabled(False)
        
        # Start countdown timer (1 second intervals)
        self.countdown_timer.start(1000)

    def countdown_tick(self):
        """Handle countdown timer tick"""
        self.countdown_value -= 1
        
        if self.countdown_value > 0:
            self.label_countdown.setText(str(self.countdown_value))
        else:
            # Countdown finished - take photo!
            self.countdown_timer.stop()
            self.label_countdown.setText("📸")  # or "SMILE!" or ""
            
            # Take photo after brief delay
            QtCore.QTimer.singleShot(200, self.capture_photo)

    def capture_photo(self):
        """Actually capture the photo"""
        # Take the photo
        photo_path = self.camera.take_photo(save_dir="photos")
        
        if photo_path:
            self.captured_photo_path = photo_path
            print(f"Photo captured: {photo_path}")
            
            # Display the captured photo
            self.display_captured_photo(photo_path)
            
            # Update main text
            self.label_main_text.setText("Photo Captured!")
            
            # Hide countdown after 1 second
            QtCore.QTimer.singleShot(1000, self.label_countdown.hide)
        else:
            print("Failed to capture photo")
            self.label_main_text.setText("Photo failed!")
        
        # Re-enable button
        self.pushButton_take_pic.setEnabled(True)
        self.is_taking_photo = False

    def display_captured_photo(self, photo_path):
        """Display the captured photo in the label"""
        import cv2
        
        # Read the saved photo
        frame = cv2.imread(photo_path)
        if frame is not None:
            self.display_frame(frame, self.label_counte)


    def go_to_home(self):
        self.parentWidget().setCurrentIndex(1)


        


