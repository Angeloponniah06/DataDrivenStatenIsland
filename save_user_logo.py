"""
Helper script to save the Staten Island logo
Run this script: python save_user_logo.py <path_to_your_logo_image>
Or simply right-click your attached logo and save it as: static/images/logo.jpg
"""
import sys
import shutil
import os
from pathlib import Path

def save_logo(source_path):
    """Copy the logo to the correct location"""
    dest_path = Path("static/images/logo.jpg")
    
    # Ensure the images directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not os.path.exists(source_path):
        print(f"Error: Source file not found: {source_path}")
        return False
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"✓ Logo successfully saved to {dest_path}")
        print(f"✓ File size: {dest_path.stat().st_size} bytes")
        return True
    except Exception as e:
        print(f"✗ Error copying logo: {e}")
        return False

if __name__ == "__main__":
    print("=== Staten Island Logo Saver ===\n")
    
    if len(sys.argv) > 1:
        # User provided a source path
        source = sys.argv[1]
        save_logo(source)
    else:
        print("OPTION 1: Run with path argument")
        print("  python save_user_logo.py <path_to_your_logo>\n")
        print("OPTION 2: Manually save (RECOMMENDED)")
        print("  1. Right-click your attached logo image")
        print("  2. Select 'Save Image As...'")
        print("  3. Save to: static/images/logo.jpg")
        print(f"  4. Full path: {Path('static/images/logo.jpg').absolute()}\n")
        print("The logo should show:")
        print("  - Dark blue Staten Island map silhouette")
        print("  - Light blue upward growth arrow overlay")
