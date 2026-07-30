import cv2
import numpy as np
import os
from PIL import Image

def remove_white_background(image_path, output_path, tolerance=245):
    """
    Removes white background from an image using a robust floodfill approach
    to prevent removing any white highlights inside the object itself.
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return False
        
    h, w, c = img.shape
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # We will perform floodfill from the four corners to detect background.
    # The floodfill mask must be 2 pixels wider and taller than the image.
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    
    # Copy of image for floodfilling
    img_flood = img.copy()
    
    # Flood fill parameters: we match pixels close to white
    # Lower/upper difference for floodfill (how far from seed point color we allow)
    # Since background is very white, a small difference from (255,255,255) is enough.
    lo_diff = (15, 15, 15)
    up_diff = (15, 15, 15)
    
    # Seed points at the 4 corners
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    
    # We can also sample more points along the borders just in case
    border_points = corners + [
        (w // 2, 0), (w // 2, h - 1),
        (0, h // 2), (w - 1, h // 2)
    ]
    
    for pt in border_points:
        # Check if the pixel is near white before seeding
        pixel_val = img[pt[1], pt[0]]
        if all(val > 220 for val in pixel_val):
            cv2.floodFill(img_flood, flood_mask, pt, (0, 0, 0), lo_diff, up_diff, flags=8 | cv2.FLOODFILL_FIXED_RANGE)
            
    # The flood_mask will have 1 (or 255) in areas that were filled (background)
    # Let's crop flood_mask back to original image size
    bg_mask = flood_mask[1:h+1, 1:w+1]
    
    # Background is marked as 1 in bg_mask, foreground is 0.
    # Let's invert it so foreground is 255 and background is 0.
    alpha_mask = np.where(bg_mask == 1, 0, 255).astype(np.uint8)
    
    # Clean up the mask slightly: we can use morphological opening/closing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_CLOSE, kernel)
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_OPEN, kernel)
    
    # Smooth the edges slightly
    alpha_mask = cv2.GaussianBlur(alpha_mask, (3, 3), 0)
    
    # Merge original image BGR with the Alpha channel
    orig_img = cv2.imread(image_path) # reload original to avoid floodfill artifacts in colors
    b, g, r = cv2.split(orig_img)
    rgba = cv2.merge([b, g, r, alpha_mask])
    
    # Save output as PNG
    cv2.imwrite(output_path, rgba)
    print(f"Successfully removed background. Saved to: {output_path}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        remove_white_background(sys.argv[1], sys.argv[2])
    else:
        # Test on the uploaded image
        input_img = "/home/user/uploads/تنزيل (15).jpg"
        output_img = "/home/user/TSH-01/3d_mannequin.png"
        remove_white_background(input_img, output_img)
