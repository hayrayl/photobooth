import cv2
from datetime import datetime
import os
from PIL import Image
import numpy as np

class CameraController:
    def __init__(self, camera_index=0, resolution=(1920, 1080)):
        """
        Initialize camera controller
        
        Args:
            camera_index: Camera device index (0 or 1)
            resolution: Tuple of (width, height)
        """
        self.camera_index = camera_index
        self.resolution = resolution
        self.camera = None
        self.is_open = False
        self.last_frame = None
        
    def open_camera(self):
        """Open the camera connection"""
        self.camera = cv2.VideoCapture(self.camera_index)
        
        if self.camera.isOpened():
            # Set resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Optional: Set other properties
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # Enable auto exposure
            
            self.is_open = True
            print(f"Camera opened at {self.get_actual_resolution()}")
            return True
        else:
            print("Failed to open camera")
            self.is_open = False
            return False
    
    def get_actual_resolution(self):
        """Get the actual resolution the camera is using"""
        if not self.is_open:
            return None
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)
    
    def get_frame(self):
        """
        Get a single frame from camera
        Returns: numpy array (BGR format) or None
        """
        if not self.is_open or self.camera is None:
            print("Camera not open")
            return None
            
        ret, frame = self.camera.read()
        if ret:
            self.last_frame = frame
            return frame
        else:
            print("Failed to capture frame")
            return None
    
    def get_preview_frame(self, target_size=None):
        """
        Get a frame optimized for preview display
        
        Args:
            target_size: Tuple (width, height) to resize to, or None for original
        Returns: numpy array or None
        """
        frame = self.get_frame()
        if frame is None:
            return None
        
        if target_size:
            frame = cv2.resize(frame, target_size)
        
        return frame
    
    def take_photo(self, save_dir="photos", filename=None):
        """
        Capture and save a photo
        
        Args:
            save_dir: Directory to save photos
            filename: Custom filename (without extension) or None for timestamp
        Returns: filepath if successful, None if failed
        """
        frame = self.get_frame()
        
        if frame is None:
            return None
        
        # Create photos directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate filename
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}"
        
        filepath = os.path.join(save_dir, f"{filename}.jpg")
        
        # Save the photo with high quality
        cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"Photo saved: {filepath}")
        
        return filepath
    
    def capture_multiple(self, count=4, delay=1.0, save_dir="photos"):
        """
        Capture multiple photos with delay between each
        
        Args:
            count: Number of photos to take
            delay: Delay in seconds between captures
            save_dir: Directory to save photos
        Returns: List of filepaths
        """
        import time
        filepaths = []
        
        for i in range(count):
            if i > 0:
                time.sleep(delay)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}_img{i+1}"
            filepath = self.take_photo(save_dir=save_dir, filename=filename)
            
            if filepath:
                filepaths.append(filepath)
        
        return filepaths
    
    def apply_filter(self, frame, filter_type="none"):
        """
        Apply filters to a frame
        
        Args:
            frame: Input frame (numpy array)
            filter_type: "none", "grayscale", "sepia", "blur", "sharpen"
        Returns: Filtered frame
        """
        if frame is None:
            return None
        
        if filter_type == "grayscale":
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        elif filter_type == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
            return cv2.transform(frame, kernel)
        
        elif filter_type == "blur":
            return cv2.GaussianBlur(frame, (15, 15), 0)
        
        elif filter_type == "sharpen":
            kernel = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])
            return cv2.filter2D(frame, -1, kernel)
        
        else:  # "none"
            return frame
    
    def save_frame(self, frame, filepath):
        """
        Save a frame to file
        
        Args:
            frame: Frame to save
            filepath: Full path including filename and extension
        Returns: True if successful
        """
        if frame is None:
            return False
        
        return cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    def get_last_frame(self):
        """Get the last captured frame"""
        return self.last_frame
    
    def create_collage(self, image_paths, output_path="photos/collage.jpg", layout=(2, 2)):
        """
        Create a photo collage from multiple images
        
        Args:
            image_paths: List of image file paths
            output_path: Where to save the collage
            layout: Tuple (rows, cols)
        Returns: Path to collage or None
        """
        if not image_paths:
            return None
        
        images = []
        for path in image_paths:
            img = cv2.imread(path)
            if img is not None:
                images.append(img)
        
        if not images:
            return None
        
        rows, cols = layout
        
        # Resize all images to same size
        h, w = images[0].shape[:2]
        target_size = (w // cols, h // rows)
        
        resized_images = [cv2.resize(img, target_size) for img in images]
        
        # Create collage
        collage_rows = []
        for i in range(rows):
            row_images = resized_images[i*cols:(i+1)*cols]
            if row_images:
                row = np.hstack(row_images)
                collage_rows.append(row)
        
        if collage_rows:
            collage = np.vstack(collage_rows)
            cv2.imwrite(output_path, collage)
            return output_path
        
        return None
    
    def flip_frame(self, frame, horizontal=True):
        """
        Flip frame horizontally or vertically
        
        Args:
            frame: Input frame
            horizontal: True for horizontal flip, False for vertical
        Returns: Flipped frame
        """
        if frame is None:
            return None
        
        flip_code = 1 if horizontal else 0
        return cv2.flip(frame, flip_code)
    
    def adjust_brightness(self, frame, factor=1.0):
        """
        Adjust brightness of frame
        
        Args:
            frame: Input frame
            factor: Brightness factor (1.0 = normal, <1.0 darker, >1.0 brighter)
        Returns: Adjusted frame
        """
        if frame is None:
            return None
        
        return cv2.convertScaleAbs(frame, alpha=factor, beta=0)
    
    def close_camera(self):
        """Release the camera"""
        if self.camera is not None:
            self.camera.release()
            self.is_open = False
            print("Camera closed")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close_camera()