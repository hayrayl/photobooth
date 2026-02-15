import os
import subprocess

class PrinterManager:
    def __init__(self):
        self.printer_name = "selphy"
    
    def is_printer_connected(self):
        """
        Check if Selphy is connected and ready
        Returns: True if connected, False otherwise
        """
        try:
            result = subprocess.run(
                ['lpstat', '-p', self.printer_name],
                capture_output=True, text=True
            )
            return self.printer_name in result.stdout
        except Exception as e:
            print(f"Error checking printer: {e}")
            return False
    
def print_photo_strip(self, strip_path):
    """
    Print a photo strip on the Selphy
    
    Args:
        strip_path: Path to photo strip image
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(strip_path):
        print(f"ERROR: Strip not found: {strip_path}")
        return False
    
    if not self.is_printer_connected():
        print("ERROR: Selphy not connected or not ready")
        return False
    
    try:
        result = subprocess.run([
            'lp',
            '-d', self.printer_name,
            '-o', 'media=w288h432',         # 4x6 paper in points
            '-o', 'print-scaling=fill',      # Fill the entire paper
            '-o', 'media-type=photographic', # Photo paper type
            '-o', 'print-quality=5',         # Highest quality
            strip_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Print job sent: {strip_path}")
            return True
        else:
            print(f"ERROR printing: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to print: {e}")
        return False