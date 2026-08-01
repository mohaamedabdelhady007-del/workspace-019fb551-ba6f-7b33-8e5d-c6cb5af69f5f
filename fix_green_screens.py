import cv2
import numpy as np
import glob
import os

def remove_green_or_white_background(image_path, output_path):
    """
    Removes both white and bright phosphor green backgrounds from an image.
    Uses HSV color space to cleanly isolate chroma-key green, and grayscale thresholding for white.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return False
        
    h, w, c = img.shape
    
    # 1. Convert to HSV to detect bright phosphor green
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range of bright phosphor green
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    
    # Threshold the HSV image to get only green colors
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # 2. Convert to Grayscale to detect white
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, white_mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    
    # Combine masks (pixels that are green OR white)
    combined_bg_mask = cv2.bitwise_or(green_mask, white_mask)
    
    # Create copy for floodfilling from corners to keep interior whites/greens safe
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    
    # Border points to seed floodfill
    border_points = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)
    ]
    
    # Copy of mask to floodfill
    bg_mask = combined_bg_mask.copy()
    
    # Perform floodfill from borders on the combined background mask
    for pt in border_points:
        if bg_mask[pt[1], pt[0]] == 255:
            cv2.floodFill(bg_mask, flood_mask, pt, 255, flags=8)
            
    # The flood_mask has 1 (or 255) for background. Crop it back to image size.
    final_bg_mask = flood_mask[1:h+1, 1:w+1] * 255
    
    # Foreground is the inverse of the background mask
    final_fg_mask = cv2.bitwise_not(final_bg_mask)
    
    # Soften edges slightly
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    final_fg_mask = cv2.morphologyEx(final_fg_mask, cv2.MORPH_CLOSE, kernel)
    final_fg_mask = cv2.morphologyEx(final_fg_mask, cv2.MORPH_OPEN, kernel)
    final_fg_mask = cv2.GaussianBlur(final_fg_mask, (3, 3), 0)
    
    # Merge original BGR channels with final foreground alpha mask
    orig_img = cv2.imread(image_path)
    b, g, r = cv2.split(orig_img)
    rgba = cv2.merge([b, g, r, final_fg_mask])
    
    # Save output as PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, rgba)
    print(f"✅ Successfully cleaned background (white & green removed): {os.path.basename(output_path)}")
    return True

def fix_all_mannequins():
    print("🚀 Starting green-screen and white background cleanup...")
    # Scan all 3D mannequins
    mannequin_files = glob.glob("/home/user/product/tshirt 01 to 18/TSH-*/3d_mannequin.png")
    
    for f_path in mannequin_files:
        # Check if the folder contains green pixels (to avoid reprocessing if not needed, but safe to reprocess all)
        remove_green_or_white_background(f_path, f_path)
        
if __name__ == "__main__":
    fix_all_mannequins()
