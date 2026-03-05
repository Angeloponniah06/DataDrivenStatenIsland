"""
Script to save the attached Staten Island logo as JPG
The logo shows Staten Island map with an upward trending arrow overlay
"""
import base64
from PIL import Image
import io
import os

# Create a proper logo file - since I cannot directly access the attachment,
# I'll create instructions for manual save OR download from base64

# The attached image needs to be saved manually as:
# static/images/logo.jpg

# For now, let's check if we have the logo file
logo_path = 'static/images/logo.jpg'

if os.path.exists(logo_path):
    print(f"✓ Logo file found at {logo_path}")
else:
    print(f"✗ Logo file not found at {logo_path}")
    print("\nPlease manually save the attached logo image as:")
    print("  static/images/logo.jpg")
    print("\nThe logo should show:")
    print("  - Staten Island map silhouette in dark blue")
    print("  - Upward trending arrow/growth chart in light blue")
