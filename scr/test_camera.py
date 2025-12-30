import cv2
import os
from datetime import datetime

def test_camera():
    print("Testing Arducam USB camera...")
    print("-" * 40)
    
    # Try to open camera (index 0)
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("❌ Failed to open camera on /dev/video0")
        print("Trying /dev/video1...")
        camera = cv2.VideoCapture(1)
        
        if not camera.isOpened():
            print("❌ Failed to open camera on /dev/video1")
            return
    
    print("✓ Camera opened successfully!")
    
    # Set resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    # Get actual resolution
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"✓ Resolution: {int(width)}x{int(height)}")
    
    # Capture a frame
    print("📸 Capturing photo...")
    ret, frame = camera.read()
    
    if ret:
        print("✓ Frame captured!")
        
        # Create photos directory
        os.makedirs("photos", exist_ok=True)
        
        # Save photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photos/test_photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        
        print(f"✓ Photo saved: {filename}")
    else:
        print("❌ Failed to capture frame")
    
    # Release camera
    camera.release()
    print("✓ Camera closed")
    print("-" * 40)
    print("Test complete!")

if __name__ == "__main__":
    test_camera()