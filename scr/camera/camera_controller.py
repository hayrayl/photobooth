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
    
    def crop_to_square(self, frame):
        """
        Crop frame to square (center crop)
        
        Args:
            frame: Input frame
        Returns: Square cropped frame
        """
        if frame is None:
            return None
        
        h, w = frame.shape[:2]
        
        # Crop to square (center crop)
        if w > h:
            # Frame is wider - crop width
            crop_size = h
            start_x = (w - crop_size) // 2
            cropped = frame[0:crop_size, start_x:start_x+crop_size]
        else:
            # Frame is taller - crop height
            crop_size = w
            start_y = (h - crop_size) // 2
            cropped = frame[start_y:start_y+crop_size, 0:crop_size]
        
        return cropped

    def take_photo(self, save_dir="photos", filename=None, crop_square=True):
        """
        Capture and save a photo
        
        Args:
            save_dir: Directory to save photos
            filename: Custom filename (without extension) or None for timestamp
            crop_square: Whether to crop image to square before saving
        Returns: filepath if successful, None if failed
        """
        frame = self.get_frame()
        
        if frame is None:
            return None
        
        # Crop to square if requested
        if crop_square:
            frame = self.crop_to_square(frame)
        
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



    def create_photo_strip(self, image_paths, template_path, output_path):
        """
        Create a photo strip collage using a template
        
        Args:
            image_paths: List of 3 photo file paths
            template_path: Path to template image
            output_path: Where to save the final collage
        Returns:
            Path to saved collage or None
        """
        import cv2
        from PIL import Image
        
        if len(image_paths) != 3:
            print(f"Need exactly 3 photos, got {len(image_paths)}")
            return None
        
        try:
            print(f"Loading template from: {template_path}")
            
            # Check if template exists
            if not os.path.exists(template_path):
                print(f"ERROR: Template not found at {template_path}")
                return None
            
            # Load template
            template = Image.open(template_path).convert('RGB')
            print(f"Template loaded, original size: {template.size}")
            
            # 4x6 photo at 300 DPI = 1200x1800 pixels
            target_size = (1200, 1800)
            template = template.resize(target_size, Image.Resampling.LANCZOS)
            print(f"Template resized to: {target_size}")
            
            # Start with the template as the base
            final_image = template.copy()
            
            # Photo positions for LEFT strip (x, y, width, height)
            left_positions = [
                (75, 55, 460, 460),      # Top left photo
                (75, 545, 460, 460),     # Middle left photo
                (75, 1035, 460, 460)      # Bottom left photo
            ]
            
            # Photo positions for RIGHT strip
            right_positions = [
                (675, 55, 460, 460),     # Top right photo
                (675, 545, 460, 460),    # Middle right photo
                (675, 1035, 460, 460)     # Bottom right photo
            ]
            
            # Load and place photos ON TOP of template
            for i, photo_path in enumerate(image_paths):
                print(f"Processing photo {i+1}: {photo_path}")
                
                # Check if photo exists
                if not os.path.exists(photo_path):
                    print(f"ERROR: Photo not found: {photo_path}")
                    continue
                
                # Load photo
                photo = cv2.imread(photo_path)
                if photo is None:
                    print(f"ERROR: Could not load photo: {photo_path}")
                    continue
                
                print(f"Photo {i+1} loaded, size: {photo.shape}")
                
                # Convert BGR to RGB
                photo_rgb = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
                photo_pil = Image.fromarray(photo_rgb)
                
                # Place on LEFT strip
                x, y, w, h = left_positions[i]
                photo_resized = photo_pil.resize((w, h), Image.Resampling.LANCZOS)
                final_image.paste(photo_resized, (x, y))
                print(f"Pasted photo {i+1} on left at ({x}, {y})")
                
                # Place on RIGHT strip
                x, y, w, h = right_positions[i]
                photo_resized_right = photo_pil.resize((w, h), Image.Resampling.LANCZOS)
                final_image.paste(photo_resized_right, (x, y))
                print(f"Pasted photo {i+1} on right at ({x}, {y})")
            
            # Save as high-quality JPEG
            final_image.save(output_path, 'JPEG', quality=95, dpi=(300, 300))
            print(f"Photo strip saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"Error creating photo strip: {e}")
            import traceback
            traceback.print_exc()
            return None