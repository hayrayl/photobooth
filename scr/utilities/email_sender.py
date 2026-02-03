import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(self):
        # Get credentials from environment variables
        self.email_address = os.getenv('PHOTOBOOTH_EMAIL')
        self.email_password = os.getenv('PHOTOBOOTH_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Check if credentials are set
        if not self.email_address or not self.email_password:
            print("WARNING: Email credentials not found in environment variables")
    
    def send_photo_strip(self, recipient_email, photo_strip_path, individual_photos=None):
        """
        Send photo strip via email
        
        Args:
            recipient_email: Email address to send to
            photo_strip_path: Path to photo strip image
            individual_photos: Optional list of individual photo paths
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Attempting to send email to: {recipient_email}")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Subject'] = "Your Photobooth Photos! 📸"
            
            # Email body
            body = """
Thank you for using our photobooth!

Your photo strip is attached to this email. We hope you had a great time!

Feel free to share your photos on social media and tag us!

---
This is an automated email from Capture The Foto - CTF photobooth.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach photo strip
            if photo_strip_path and os.path.exists(photo_strip_path):
                with open(photo_strip_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', 
                                   filename='photobooth_strip.jpg')
                    msg.attach(img)
                print(f"Attached photo strip: {photo_strip_path}")
            else:
                print(f"Photo strip not found: {photo_strip_path}")
                return False
            
            # Optionally attach individual photos
            if individual_photos:
                for i, photo_path in enumerate(individual_photos):
                    if os.path.exists(photo_path):
                        with open(photo_path, 'rb') as f:
                            img = MIMEImage(f.read())
                            img.add_header('Content-Disposition', 'attachment',
                                          filename=f'photo_{i+1}.jpg')
                            msg.attach(img)
                        print(f"Attached photo {i+1}: {photo_path}")
            
            # Connect to Gmail SMTP server
            print("Connecting to Gmail SMTP server...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure connection
            
            # Login
            print("Logging in...")
            server.login(self.email_address, self.email_password)
            
            # Send email
            print("Sending email...")
            server.send_message(msg)
            
            # Close connection
            server.quit()
            
            print(f"✓ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("ERROR: Authentication failed. Check email/password.")
            return False
        except smtplib.SMTPException as e:
            print(f"ERROR: SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"ERROR: Failed to send email: {e}")
            import traceback
            traceback.print_exc()
            return False