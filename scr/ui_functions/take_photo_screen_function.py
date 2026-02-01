import sys
import os  
from PyQt5 import QtCore, QtGui, QtWidgets
import time

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
        self.is_taking_photos = False
        self.show_preview = False  # Only show preview during capture
        self.current_photo_number = 0  # Track which photo (1, 2, or 3)
        self.session_number = 0  # Track session number for naming
        self.captured_photos = []  # Store paths of captured photos
        
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
        self.label_countdown_2.hide()
        
        # Clear the photo display initially
        self.label_counte.setText("Press 'Take Photo'\nto start!")
        self.label_counte.setAlignment(QtCore.Qt.AlignCenter)

    def connect_signals(self):
        self.pushButton_take_pic.clicked.connect(self.start_photo_session)
        self.pushButton_to_home.clicked.connect(self.go_to_home)

    def showEvent(self, event):
        """Called when screen becomes visible"""
        super().showEvent(event)
        # Don't auto-start preview - wait for button press
        self.show_preview = False
        self.label_counte.setText("Press 'Take Photo'\nto start!")

    def hideEvent(self, event):
        """Called when screen is hidden - stop camera preview"""
        super().hideEvent(event)
        self.stop_preview()

    def start_preview(self):
        """Start showing live camera preview"""
        if self.camera.is_open:
            self.show_preview = True
            self.preview_timer.start(30)  # Update preview ~30 fps

    def stop_preview(self):
        """Stop camera preview"""
        self.show_preview = False
        self.preview_timer.stop()

    def update_preview(self):
        """Update the photo label with live camera feed"""
        if not self.show_preview:
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
            crop_size = h
            start_x = (w - crop_size) // 2
            cropped = rgb_frame[0:crop_size, start_x:start_x+crop_size]
        else:
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

    def start_photo_session(self):
        """Start a 3-photo session"""
        if self.is_taking_photos:
            return
        
        self.is_taking_photos = True
        self.current_photo_number = 1
        self.captured_photos = []
        
        # Increment session number
        self.session_number = self.main_window.photo_session_counter
        self.main_window.photo_session_counter += 1
        
        # Hide buttons during photo session
        self.pushButton_take_pic.hide()
        self.pushButton_to_home.hide()
        
        # Start preview
        self.start_preview()
        
        # Start first photo countdown
        self.start_countdown()

    def start_countdown(self):
        """Start countdown for current photo"""
        self.countdown_value = 3
        
        
        # Show countdown
        self.label_countdown.show()
        self.label_countdown_2.show()
        self.label_countdown.setText(str(self.countdown_value))
        self.label_countdown_2.setText(str(self.countdown_value))
        
        # Start countdown timer (1 second intervals)
        self.countdown_timer.start(1000)

    def countdown_tick(self):
        """Handle countdown timer tick"""
        self.countdown_value -= 1
        
        if self.countdown_value > 0:
            self.label_countdown.setText(str(self.countdown_value))
            self.label_countdown_2.setText(str(self.countdown_value))
        else:
            # Countdown finished - take photo!
            self.countdown_timer.stop()
            self.label_countdown.setText("📸")
            self.label_countdown_2.setText("📸")
            
            # Take photo after brief delay
            QtCore.QTimer.singleShot(200, self.capture_photo)

    def capture_photo(self):
        """Capture  one photo in the session"""
        # Generate filename: session_photo
        filename = f"{self.session_number}_{self.current_photo_number}"
        
        # Take the photo and save to party folder
        photo_path = self.camera.take_photo(
            save_dir=self.main_window.party_folder,  # Use party folder instead of "photos"
            filename=filename
        )
        
        if photo_path:
            self.captured_photos.append(photo_path)
            print(f"Photo {self.current_photo_number} captured: {photo_path}")
            
            # Stop preview to show captured photo
            self.show_preview = False
            
            # Display the captured photo
            self.display_captured_photo(photo_path)
            
            # Hide countdown
            self.label_countdown.hide()
            self.label_countdown_2.hide()
            
            # Show photo for 1 second, then proceed
            if self.current_photo_number < 3:
                # More photos to take
                QtCore.QTimer.singleShot(1000, self.next_photo)
            else:
                # All photos taken - go to display screen
                QtCore.QTimer.singleShot(1000, self.finish_session)
        else:
            print(f"Failed to capture photo {self.current_photo_number}")
            self.finish_session()

    def next_photo(self):
        """Prepare for next photo"""
        self.current_photo_number += 1
        
        # Resume preview
        self.show_preview = True
        
        # Start countdown for next photo
        self.start_countdown()

        
    def finish_session(self):
        """Finish photo session and go to display screen"""
        self.is_taking_photos = False
        self.stop_preview()
        
        # Show buttons again
        self.pushButton_take_pic.show()
        self.pushButton_to_home.show()
        
        self.label_countdown.hide()
        self.label_countdown_2.hide()
        
        # Create photo strip in background (but don't add to display)
        if len(self.captured_photos) == 3:
            self.create_photo_strip_background()
        
        # Check where photos were saved
        if self.main_window.is_saving_to_usb():
            self.label_counte.setText("Saved to USB!")
        else:
            self.label_counte.setText("Saved locally\n(No USB detected)")
        
        # Wait then go to display
        QtCore.QTimer.singleShot(1500, self.go_to_display_screen)

    def create_photo_strip_background(self):
        """Create the photo strip collage in background"""
        import os
        
        # Path to template
        template_path = os.path.join(
            os.path.dirname(__file__), 
            "../images/photo_strip_template.png"
        )
        
        # Output path for photo strip
        strip_filename = f"strip_{self.session_number}.jpg"
        strip_path = os.path.join(
            self.main_window.party_folder,
            strip_filename
        )
        
        # Create the photo strip (don't add to captured_photos list)
        result = self.camera.create_photo_strip(
            self.captured_photos,
            template_path,
            strip_path
        )
        
        if result:
            print(f"Photo strip created: {result}")
        else:
            print("Failed to create photo strip")

    def go_to_display_screen(self):
        """Navigate to display screen with photos"""
        if len(self.captured_photos) == 3:
            # Get the display screen and set photos (only the 3 individual photos)
            display_screen = self.main_window.display_photo_screen
            display_screen.set_photos(self.captured_photos)
            
            # Switch to display screen
            self.parentWidget().setCurrentIndex(3)


    def display_captured_photo(self, photo_path):
        """Display a captured photo in the label"""
        import cv2
        
        # Read the saved photo
        frame = cv2.imread(photo_path)
        if frame is not None:
            self.display_frame(frame, self.label_counte)
        else:
            print(f"Failed to load photo: {photo_path}")

    def go_to_home(self):
        """Go back to home screen"""
        self.stop_preview()
        self.label_counte.setText("Press 'Take Photo'\nto start!")
        self.parentWidget().setCurrentIndex(1)  # Adjust index as needed