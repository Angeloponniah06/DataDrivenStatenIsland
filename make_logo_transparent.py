from PIL import Image
import numpy as np

# Load the image
img = Image.open(r"C:\Users\angel\OneDrive\Ashley designed logo .jpg")

# Convert to RGBA (if not already)
img = img.convert("RGBA")

# Get the image data
data = np.array(img)

# Define the white background color range (adjust tolerance as needed)
# This will target white and near-white pixels
white_threshold = 240  # Pixels with RGB values above this will be made transparent

# Create a mask for white pixels
# Check if R, G, and B are all above the threshold
mask = (data[:, :, 0] >= white_threshold) & \
       (data[:, :, 1] >= white_threshold) & \
       (data[:, :, 2] >= white_threshold)

# Set the alpha channel to 0 (transparent) for white pixels
data[:, :, 3][mask] = 0

# Create a new image from the modified data
transparent_img = Image.fromarray(data)

# Save as PNG (supports transparency)
output_path = r"C:\Users\angel\OneDrive\Documents\GitHub\DataDrivenStatenIsland\static\images\logo.png"
transparent_img.save(output_path, "PNG")

print(f"✓ Transparent logo saved to: {output_path}")
