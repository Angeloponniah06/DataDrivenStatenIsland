"""
Save the Staten Island logo from data
"""
# The logo image (Staten Island with growth arrow) - base64 encoded JPEG
logo_data = b"""
"""

# Since I cannot directly access the attachment data, 
# I'll use PIL to create/copy the logo manually

import os
import shutil

source = "path_to_attached_image"  # This would be the attachment
dest = "static/images/logo.jpg"

# Manual step: Please save the attached image directly as static/images/logo.jpg
print("Please manually save the attached Staten Island logo image to:")
print("  static/images/logo.jpg")
print("\nThe logo should be the exact image you attached showing:")
print("  - Dark blue Staten Island map outline")  
print("  - Light blue upward trending growth arrow")
