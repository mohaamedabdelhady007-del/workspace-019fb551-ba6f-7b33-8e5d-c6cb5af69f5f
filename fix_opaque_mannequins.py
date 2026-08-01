import cv2
import numpy as np
import os

def remove_black_or_colored_background(image_path, output_path):
    """
    Cleans up pure black, green, or white backgrounds from the 3D mannequin flat-lays.
    Specifically designed to handle black t-shirts on pure black backgrounds by floodfilling
    from the borders with a tight tolerance.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return False
        
    h, w, c = img.shape
    
    # We will perform floodfill on a combined mask of green, white, and black background.
    # 1. Detect bright green (HSV)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # 2. Detect white (Grayscale threshold)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, white_mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    
    # 3. Detect near-black background (pixels very close to 0,0,0)
    # Since background is pure solid black (0,0,0), we threshold for very dark pixels
    _, black_mask = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY_INV)
    
    # Combine all backgrounds
    combined_bg = cv2.bitwise_or(green_mask, white_mask)
    combined_bg = cv2.bitwise_or(combined_bg, black_mask)
    
    # Floodfill from borders to isolate only the background
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    border_points = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)
    ]
    
    bg_mask = combined_bg.copy()
    for pt in border_points:
        # Check if the border pixel is indeed a background pixel
        pixel_val = img[pt[1], pt[0]]
        is_bg = (
            all(val > 240 for val in pixel_val) or  # White
            all(val < 20 for val in pixel_val) or   # Black
            (pixel_val[1] > 180 and pixel_val[1] > pixel_val[0] * 1.5) # Green
        )
        if is_bg:
            cv2.floodFill(bg_mask, flood_mask, pt, 255, flags=8)
            
    final_bg_mask = flood_mask[1:h+1, 1:w+1] * 255
    final_fg_mask = cv2.bitwise_not(final_bg_mask)
    
    # Refine mask edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    final_fg_mask = cv2.morphologyEx(final_fg_mask, cv2.MORPH_CLOSE, kernel)
    final_fg_mask = cv2.morphologyEx(final_fg_mask, cv2.MORPH_OPEN, kernel)
    final_fg_mask = cv2.GaussianBlur(final_fg_mask, (3, 3), 0)
    
    # Split original BGR and merge with the new alpha mask
    orig_img = cv2.imread(image_path)
    b, g, r = cv2.split(orig_img)
    rgba = cv2.merge([b, g, r, final_fg_mask])
    
    cv2.imwrite(output_path, rgba)
    print(f"✅ Successfully cleaned opaque/black background for: {os.path.basename(output_path)}")
    return True

def fix_opaque_mannequins():
    print("🚀 Starting target cleanup of the 7 opaque mannequins...")
    target_folders = ["TSH-08", "TSH-09", "TSH-10", "TSH-12", "TSH-14", "TSH-16", "TSH-18"]
    
    for folder in target_folders:
        path = f"/home/user/product/tshirt 01 to 18/{folder}/3d_mannequin.png"
        remove_black_or_colored_background(path, path)

if __name__ == "__main__":
    fix_opaque_mannequins()
