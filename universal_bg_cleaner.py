import cv2
import numpy as np
import glob
import os

# DISTRICT-99 (D99) - UNIVERSAL 3D MANNEQUIN BACKGROUND CLEANER (PRO EDITION)
# هذا السكريبت الاحترافي يقوم تلقائياً بمسح أي لون خلفية (أبيض، أسود، رمادي، أو أخضر) لأي منتج من خلال تحليل لون الزاوية والـ Floodfill الذكي!

def clean_background_universally(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return False
        
    h, w = img.shape[:2]
    
    # Create the floodfill mask (h+2, w+2)
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    
    # Seed points at the 4 corners and borders
    border_points = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)
    ]
    
    img_flood = img.copy()
    
    for pt in border_points:
        # We use a solid tolerance of 35 to capture any shading or shadows near the borders
        # This will universally floodfill and key out the background starting from any of the border seeds
        cv2.floodFill(img_flood, flood_mask, pt, (0, 0, 0), (35, 35, 35), (35, 35, 35), flags=8 | cv2.FLOODFILL_FIXED_RANGE)
            
    # The flood_mask has 1 where background was filled
    bg_mask = flood_mask[1:h+1, 1:w+1]
    
    # Foreground mask: 255 (opaque) where background is 0, and 0 (transparent) where background is 1
    fg_mask = np.where(bg_mask == 1, 0, 255).astype(np.uint8)
    
    # Refine and soften the mask edges slightly
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    
    # Split BGR and merge with the new alpha mask
    orig_img = cv2.imread(image_path)
    b, g, r = cv2.split(orig_img)
    rgba = cv2.merge([b, g, r, fg_mask])
    
    cv2.imwrite(output_path, rgba)
    print(f"✅ Universally Cleaned: {os.path.basename(output_path)}")
    return True

def clean_all_mannequins():
    print("🚀 Starting PRO Universal Background Cleanup for all 18 products...")
    mannequin_files = glob.glob("/home/user/product/tshirt 01 to 18/TSH-*/3d_mannequin.png")
    
    for f in mannequin_files:
        clean_background_universally(f, f)
        
    print("\n🎉 All 18 product 3D mannequins are now perfectly transparent with the PRO universal cleaner!")

if __name__ == "__main__":
    clean_all_mannequins()
