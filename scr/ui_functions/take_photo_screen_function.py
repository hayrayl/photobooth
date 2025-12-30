import sys
import os  
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities import utils_screen
from camera.camera_controller import CameraController
from ui_screens.take_photo import Ui_TakePhoto

class TakePhotoScreen(QtWidgets.QWidget, Ui_TakePhoto):
    def __init__(self, main_window, camera, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        self.camera = camera
        
        # Timer for camera preview updates
        self.preview_timer = QtCore.QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        
        # Timer for countdown
        self.countdown_timer = QtCore.QTimer()
        self.countdown_timer.timeout.connect(self.countdown_tick)
        
        self.countdown_value = 3
        self.is_taking_photo = False
        self.captured_photo_path = None
        self.showing_captured_photo = False
        
        # Setup design and connect buttons
        self.design_setup()
        self.connect_signals()

    def design_setup(self):
        utils_screen.pink_background(self.background)
        self.background.lower()
        
        # Make sure photo label can display images
        self.label_counte.setScaledContents(True)
        
        # Initially hide countdown
        self.label_countdown.hide()

    def connect_signals(self):
        self.pushButton_take_pic.clicked.connect(self.start_photo_capture)
        self.pushButton_to_home.clicked.connect(self.go_to_home)

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
            self.showing_captured_photo = False
            self.preview_timer.start(30)  # Update preview ~30 fps

    def stop_preview(self):
        """Stop camera preview"""
        self.preview_timer.stop()

    def update_preview(self):
        """Update the photo label with live camera feed"""
        # Don't update preview if showing captured photo
        if self.showing_captured_photo:
            return
        
        frame = self.camera.get_frame()
        if frame is not None:
            self.display_frame(frame, self.label_counte)

    def display_frame(self, frame, label):
        """Convert OpenCV frame to QPixmap and display in label (center crop to square)"""
        import cv2
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get frame dimensions
        h, w, ch = rgb_frame.shape
        
        # Crop to square (center crop)
        if w > h:
            # Frame is wider - crop width
            crop_size = h
            start_x = (w - crop_size) // 2
            cropped = rgb_frame[0:crop_size, start_x:start_x+crop_size]
        else:
            # Frame is taller - crop height
            crop_size = w
            start_y = (h - crop_size) // 2
            cropped = rgb_frame[start_y:start_y+crop_size, 0:crop_size]
        
        # Get label size
        label_width = label.width()
        label_height = label.height()
        
        # Use the smaller dimension to maintain square
        display_size = min(label_width, label_height)
        
        # Resize square frame to fit label
        resized = cv2.resize(cropped, (display_size, display_size))
        
        # Convert to QImage
        bytes_per_line = ch * display_size
        qt_image = QtGui.QImage(resized.data, display_size, display_size, 
                                bytes_per_line, QtGui.QImage.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    def start_photo_capture(self):
        """Start countdown and photo capture process"""
        if self.is_taking_photo:
            return
        
        self.is_taking_photo = True
        self.countdown_value = 3
        
        # Make sure we're showing preview (not captured photo)
        self.showing_captured_photo = False
        
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
            self.label_countdown.setText("📸")
            
            # Take photo after brief delay
            QtCore.QTimer.singleShot(200, self.capture_photo)

    def capture_photo(self):
        """Actually capture the photo"""
        # Get custom filename from main window
        filename = self.main_window.get_next_photo_name()
        
        # Take the photo with custom name
        photo_path = self.camera.take_photo(save_dir="photos", filename=filename)
        
        if photo_path:
            self.captured_photo_path = photo_path
            self.showing_captured_photo = True  # Flag to stop preview updates
            print(f"Photo captured: {photo_path}")
            
            # Display the captured photo
            self.display_captured_photo(photo_path)
            
            # Update main text
            self.label_main_text.setText("Photo Captured!")
            
            # Hide countdown after 1 second
            QtCore.QTimer.singleShot(1000, self.label_countdown.hide)
            
            # Resume preview after 3 seconds (or keep showing photo)
            # Uncomment next line if you want to auto-resume preview:
            # QtCore.QTimer.singleShot(3000, self.resume_preview)
        else:
            print("Failed to capture photo")
            self.label_main_text.setText("Photo failed!")
            self.showing_captured_photo = False
        
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
        else:
            print(f"Failed to load photo: {photo_path}")

    def resume_preview(self):
        """Resume live preview after showing captured photo"""
        self.showing_captured_photo = False
        self.label_main_text.setText("Taking a photo!!!")

    def go_to_home(self):
        self.parentWidget().setCurrentIndex(1)


        


