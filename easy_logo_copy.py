"""
Easy Logo Copier - Finds and copies your Staten Island logo
"""
import os
import shutil
from pathlib import Path
import glob

def find_and_copy_logo():
    """Search for the logo in common locations and copy it"""
    
    # Possible search locations
    search_locations = [
        str(Path.home() / "Downloads" / "*staten*island*.jpg"),
        str(Path.home() / "Downloads" / "*staten*island*.jpeg"),
        str(Path.home() / "Downloads" / "*logo*.jpg"),
        str(Path.home() / "Downloads" / "*.jpg"),
        str(Path.home() / "Pictures" / "*staten*.jpg"),
        str(Path.home() / "Desktop" / "*logo*.jpg"),
        "./*logo*.jpg",
        "../*logo*.jpg",
    ]
    
    dest = Path("static/images/logo.jpg")
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    print("🔍 Searching for Staten Island logo image...\n")
    
    found_files = []
    for pattern in search_locations:
        matches = glob.glob(pattern)
        found_files.extend([(f, os.path.getmtime(f)) for f in matches])
    
    if found_files:
        # Sort by modification time (most recent first)
        found_files.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Found {len(found_files)} possible logo file(s):\n")
        for i, (filepath, mtime) in enumerate(found_files[:10], 1):
            size = os.path.getsize(filepath)
            print(f"{i}. {Path(filepath).name}")
            print(f"   Path: {filepath}")
            print(f"   Size: {size:,} bytes\n")
        
        # Ask user which one to use
        print("Enter the number of your logo file (or 0 to cancel): ", end="")
        try:
            choice = int(input())
            if 1 <= choice <= len(found_files):
                source = found_files[choice-1][0]
                shutil.copy2(source, dest)
                print(f"\n✅ Logo copied successfully to {dest}")
                print(f"✅ Restart your server to see it!")
                return True
        except (ValueError, IndexError):
            print("Invalid selection")
    
    print("\n❌ Logo not found automatically.")
    print("\nMANUAL STEPS:")
    print("1. Save your attached logo image (right-click → Save As)")
    print(f"2. Save it to: {dest.absolute()}")
    print("3. Make sure the filename is exactly: logo.jpg")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("   Staten Island Logo Finder & Copier")
    print("=" * 60 + "\n")
    find_and_copy_logo()
