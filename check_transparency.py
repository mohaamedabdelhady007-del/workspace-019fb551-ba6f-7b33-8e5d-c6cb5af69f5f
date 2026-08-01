import cv2
import numpy as np
import glob
import os

def check_image_transparency(file_path):
    """
    Checks if an image is properly transparent.
    Returns:
    - True if it has an alpha channel and a significant number of transparent pixels.
    - False if it has no alpha channel or is fully opaque.
    """
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return False, "Could not load image"
        
    # Check channels
    if img.shape[2] < 4:
        return False, "No alpha channel (Opaque BGR)"
        
    # Check alpha channel values
    alpha = img[:, :, 3]
    total_pixels = alpha.size
    transparent_pixels = np.sum(alpha < 240) # Pixels that are mostly or fully transparent
    
    pct_transparent = (transparent_pixels / total_pixels) * 100
    
    if pct_transparent < 5.0: # Less than 5% transparency is basically opaque
        return False, f"Opaque Alpha (Only {pct_transparent:.2f}% transparent)"
        
    return True, f"Valid Alpha ({pct_transparent:.2f}% transparent)"

def scan_all_store_images():
    print("🚀 Scanning all 18 product folders for transparency issues...")
    product_images = glob.glob("/home/user/product/tshirt 01 to 18/TSH-*/*.png")
    
    opaque_files = []
    
    for img_path in product_images:
        is_transparent, msg = check_image_transparency(img_path)
        rel_path = os.path.relpath(img_path, "/home/user/")
        
        if not is_transparent:
            print(f"⚠️ Issue detected: {rel_path} | {msg}")
            opaque_files.append(img_path)
        else:
            # print(f"✅ Clean: {rel_path} | {msg}")
            pass
            
    print(f"\n📊 Scan Complete! Found {len(opaque_files)} files with transparency issues.")
    return opaque_files

if __name__ == "__main__":
    scan_all_store_images()
