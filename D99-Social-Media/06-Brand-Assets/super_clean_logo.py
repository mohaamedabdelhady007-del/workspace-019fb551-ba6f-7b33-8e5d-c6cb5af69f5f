import cv2
import numpy as np
from PIL import Image
import os

# DISTRICT-99 (D99) - SUPER CLEAN LOGO GENERATOR
# هذا السكريبت الاحترافي يقوم بتصفية اللوجو بالكامل ومسح أي غشاوة رمادية أو ظلال مستطيلة حول الحروف، ليصبح أسوداً ناصعاً وخلفيته شفافة 100%!

def generate_super_clean_logo(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read logo {input_path}")
        return False
        
    h, w, c = img.shape
    
    # Convert to grayscale to isolate the logo elements
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # We want to extract the logo elements from the black background.
    # Any pixel that is NOT the black background (i.e., intensity > 35) is part of the logo.
    # We create a binary mask of the logo (255 where logo is, 0 where background is)
    _, logo_mask = cv2.threshold(gray, 35, 255, cv2.THRESH_BINARY)
    
    # Refine the mask edges to remove any compression noise or haze
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    logo_mask = cv2.morphologyEx(logo_mask, cv2.MORPH_CLOSE, kernel)
    logo_mask = cv2.morphologyEx(logo_mask, cv2.MORPH_OPEN, kernel)
    
    # Create a solid pure black image (BGR = 0, 0, 0)
    black_b = np.zeros((h, w), dtype=np.uint8)
    black_g = np.zeros((h, w), dtype=np.uint8)
    black_r = np.zeros((h, w), dtype=np.uint8)
    
    # Merge the solid black BGR channels with the clean logo mask as Alpha!
    # This guarantees that the logo is pure solid black (0,0,0) and the background is 100% transparent (0)
    # with absolutely NO grey boxes, NO shadows, and NO rectangular bounding borders!
    rgba_clean = cv2.merge([black_b, black_g, black_r, logo_mask])
    
    # Save the super clean transparent black logo
    cv2.imwrite(output_path, rgba_clean)
    print(f"✅ Generated 100% transparent, razor-sharp solid black logo: {output_path}")
    return True

if __name__ == "__main__":
    generate_super_clean_logo(
        "/home/user/uploads/9.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/d99-logo-header.png"
    )
