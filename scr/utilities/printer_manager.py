import os
import subprocess
import platform

class PrinterManager:
    def __init__(self):
        self.printer_name = "selphy"
        self.is_windows = platform.system() == "Windows"
    
    def is_printer_connected(self):
        """
        Check if Selphy is connected and ready
        Returns: True if connected, False otherwise
        """
        if self.is_windows:
            print("Windows detected - printer not available in development")
            return False
        
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
        if self.is_windows:
            print(f"Windows detected - would print: {strip_path}")
            return False
        
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
                '-o', 'media=w288h432',
                '-o', 'print-scaling=fill',
                '-o', 'media-type=photographic',
                '-o', 'print-quality=5',
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