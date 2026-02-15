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
        self.show_preview = False
        self.current_photo_number = 0
        self.session_number = 0
        self.captured_photos = []
        
        self.design_setup()

    def design_setup(self):
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        
        # Make camera label display images properly
        self.label_camera.setScaledContents(True)
        
        # Style countdown labels
        color_scheme = utils_screen.get_color_scheme(self.main_window.color_scheme)
        countdown_style = f"""
            QLabel {{
                color: {color_scheme['text']};
                background-color: transparent;
            }}
        """
        self.label_countdown.setStyleSheet(countdown_style)
        self.label_countdown_2.setStyleSheet(countdown_style)
        
        # Initially hide countdown
        self.label_countdown.hide()
        self.label_countdown_2.hide()

    def showEvent(self, event):
        """Called when screen becomes visible - start preview and auto start session"""
        super().showEvent(event)
        utils_screen.set_background(self.background, self.main_window.color_scheme)
        
        # Start camera preview
        self.start_preview()
        
        # Auto start photo session
        if not self.is_taking_photos:
            QtCore.QTimer.singleShot(500, self.start_photo_session)

    def hideEvent(self, event):
        """Called when screen is hidden"""
        super().hideEvent(event)
        self.stop_preview()
        self.countdown_timer.stop()

    def start_preview(self):
        """Start showing live camera preview"""
        if self.camera.is_open:
            self.show_preview = True
            self.preview_timer.start(30)

    def stop_preview(self):
        """Stop camera preview"""
        self.show_preview = False
        self.preview_timer.stop()

    def update_preview(self):
        """Update camera label with live feed"""
        if not self.show_preview:
            return
        
        frame = self.camera.get_frame()
        if frame is not None:
            self.display_frame(frame, self.label_camera)

    def display_frame(self, frame, label):
        """Convert OpenCV frame to QPixmap and display in label"""
        import cv2
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        h, w, ch = rgb_frame.shape
        
        # Crop to square
        if w > h:
            crop_size = h
            start_x = (w - crop_size) // 2
            cropped = rgb_frame[0:crop_size, start_x:start_x+crop_size]
        else:
            crop_size = w
            start_y = (h - crop_size) // 2
            cropped = rgb_frame[start_y:start_y+crop_size, 0:crop_size]
        
        label_width = label.width()
        label_height = label.height()
        display_size = min(label_width, label_height)
        
        resized = cv2.resize(cropped, (display_size, display_size))
        
        bytes_per_line = ch * display_size
        qt_image = QtGui.QImage(resized.data, display_size, display_size,
                                bytes_per_line, QtGui.QImage.Format_RGB888)
        
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)


    def start_photo_session(self):
        """Start a 3-photo session"""
        if self.is_taking_photos:
            return
        
        self.is_taking_photos = True
        self.current_photo_number = 1
        self.captured_photos = []
        
        self.session_number = self.main_window.photo_session_counter
        self.main_window.photo_session_counter += 1
        
        self.start_countdown()

    def start_countdown(self):
        """Start countdown for current photo"""
        self.countdown_value = 3
        
        self.label_countdown.show()
        self.label_countdown_2.show()
        self.label_countdown.setText(str(self.countdown_value))
        self.label_countdown_2.setText(str(self.countdown_value))
        
        self.countdown_timer.start(1000)

    def countdown_tick(self):
        """Handle countdown timer tick"""
        self.countdown_value -= 1
        
        if self.countdown_value > 0:
            self.label_countdown.setText(str(self.countdown_value))
            self.label_countdown_2.setText(str(self.countdown_value))
        else:
            self.countdown_timer.stop()
            self.label_countdown.setText("📸")
            self.label_countdown_2.setText("📸")
            QtCore.QTimer.singleShot(200, self.capture_photo)

    def capture_photo(self):
        """Capture one photo in the session"""
        filename = f"{self.session_number}_{self.current_photo_number}"
        
        photo_path = self.camera.take_photo(
            save_dir=self.main_window.party_folder,
            filename=filename
        )
        
        if photo_path:
            self.captured_photos.append(photo_path)
            print(f"Photo {self.current_photo_number} captured: {photo_path}")
            
            # Show captured photo briefly
            self.show_preview = False
            self.display_captured_photo(photo_path)
            
            self.label_countdown.hide()
            self.label_countdown_2.hide()
            
            if self.current_photo_number < 3:
                # Resume preview and move to next photo
                QtCore.QTimer.singleShot(500, self.next_photo)
            else:
                # All done - go to display screen
                self.finish_session()
        else:
            print(f"Failed to capture photo {self.current_photo_number}")
            self.finish_session()

    def next_photo(self):
        """Prepare for next photo"""
        self.current_photo_number += 1
        self.show_preview = True  # Resume preview
        self.start_countdown()

    def display_frame(self, frame, label):
        """Convert OpenCV frame to QPixmap and display in label"""
        import cv2
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip horizontally so preview mirrors the user
        rgb_frame = cv2.flip(rgb_frame, 1)
        
        h, w, ch = rgb_frame.shape
        
        # Crop to square
        if w > h:
            crop_size = h
            start_x = (w - crop_size) // 2
            cropped = rgb_frame[0:crop_size, start_x:start_x+crop_size]
        else:
            crop_size = w
            start_y = (h - crop_size) // 2
            cropped = rgb_frame[start_y:start_y+crop_size, 0:crop_size]
        
        label_width = label.width()
        label_height = label.height()
        display_size = min(label_width, label_height)
        
        resized = cv2.resize(cropped, (display_size, display_size))
        
        bytes_per_line = ch * display_size
        qt_image = QtGui.QImage(resized.data, display_size, display_size,
                                bytes_per_line, QtGui.QImage.Format_RGB888)
        
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    def finish_session(self):
        """Finish photo session and go to display screen"""
        self.is_taking_photos = False
        self.stop_preview()
        
        self.label_countdown.hide()
        self.label_countdown_2.hide()
        
        # Create photo strip in background
        if len(self.captured_photos) == 3:
            self.create_photo_strip_background()
        
        self.strip_path = os.path.join(
            self.main_window.party_folder,
            f"strip_{self.session_number}.jpg"
        )
        
        # Go to display screen immediately
        self.go_to_display_screen()

    def create_photo_strip_background(self):
        """Create the photo strip collage in background"""
        template_path = self.main_window.get_template_path()
        
        strip_filename = f"strip_{self.session_number}.jpg"
        strip_path = os.path.join(
            self.main_window.party_folder,
            strip_filename
        )
        
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
            display_screen = self.main_window.display_photo_screen
            display_screen.set_photos(self.captured_photos)
            self.parentWidget().setCurrentIndex(3)

    def display_captured_photo(self, photo_path):
        """Display a captured photo in the camera label"""
        import cv2
        frame = cv2.imread(photo_path)
        if frame is not None:
            self.display_frame(frame, self.label_camera)