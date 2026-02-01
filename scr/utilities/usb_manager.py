import os
import shutil

class USBManager:
    def __init__(self):
        self.usb_path = None
    
    def find_usb_drives(self):
        """
        Find all mounted USB drives
        Returns: List of USB drive paths
        """
        usb_drives = []
        
        # On Raspberry Pi, USB drives typically mount to /media/pi/ or /media/username/
        media_paths = [
            "/media/pi",
            f"/media/{os.getenv('USER')}",
            "/mnt"
        ]
        
        for media_path in media_paths:
            if os.path.exists(media_path):
                # List all directories in media path
                try:
                    drives = [os.path.join(media_path, d) 
                             for d in os.listdir(media_path) 
                             if os.path.isdir(os.path.join(media_path, d))]
                    usb_drives.extend(drives)
                except PermissionError:
                    continue
        
        return usb_drives
    
    def get_first_usb(self):
        """
        Get the first available USB drive
        Returns: Path to USB drive or None
        """
        drives = self.find_usb_drives()
        if drives:
            self.usb_path = drives[0]
            return drives[0]
        return None
    
    def is_usb_connected(self):
        """Check if any USB drive is connected"""
        return len(self.find_usb_drives()) > 0
    
    def copy_folder_to_usb(self, source_folder, usb_path=None):
        """
        Copy entire folder to USB drive
        
        Args:
            source_folder: Path to folder to copy
            usb_path: Path to USB drive (or None to auto-detect)
        Returns:
            True if successful, False otherwise
        """
        if usb_path is None:
            usb_path = self.get_first_usb()
        
        if usb_path is None:
            print("No USB drive found")
            return False
        
        try:
            # Get folder name
            folder_name = os.path.basename(source_folder)
            
            # Destination path
            dest_path = os.path.join(usb_path, "photobooth_photos", folder_name)
            
            # Copy folder
            if os.path.exists(source_folder):
                shutil.copytree(source_folder, dest_path, dirs_exist_ok=True)
                print(f"Copied {source_folder} to {dest_path}")
                return True
            else:
                print(f"Source folder not found: {source_folder}")
                return False
                
        except Exception as e:
            print(f"Error copying to USB: {e}")
            return False
    
    def get_usb_free_space(self, usb_path=None):
        """
        Get free space on USB drive in bytes
        
        Args:
            usb_path: Path to USB drive
        Returns:
            Free space in bytes or None
        """
        if usb_path is None:
            usb_path = self.get_first_usb()
        
        if usb_path is None:
            return None
        
        try:
            stat = os.statvfs(usb_path)
            free_space = stat.f_bavail * stat.f_frsize
            return free_space
        except Exception as e:
            print(f"Error checking USB space: {e}")
            return None
    
    def format_bytes(self, bytes_value):
        """Format bytes to human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
    
    def find_template_on_usb(self, usb_path=None):
        """
        Look for a template image in the 'template' folder on USB
        
        Args:
            usb_path: Path to USB drive (or None to auto-detect)
        Returns:
            Path to template image if found, None otherwise
        """
        if usb_path is None:
            usb_path = self.get_first_usb()
        
        if usb_path is None:
            return None
        
        # Look for template folder on USB
        template_folder = os.path.join(usb_path, "template")
        
        if not os.path.exists(template_folder):
            print(f"No template folder found on USB at: {template_folder}")
            return None
        
        # Look for image files in template folder
        image_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
        
        try:
            files = os.listdir(template_folder)
            for file in files:
                if any(file.endswith(ext) for ext in image_extensions):
                    template_path = os.path.join(template_folder, file)
                    print(f"Found template on USB: {template_path}")
                    return template_path
        except Exception as e:
            print(f"Error searching for template: {e}")
        
        print("No template image found in USB template folder")
        return None