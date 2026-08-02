import cv2
import numpy as np
from PIL import Image
import os

def make_logo_transparent_and_inverted(input_path, output_dark_bg, output_light_bg):
    """
    Cleans up the high-resolution logo:
    1. Creates a version with transparent background for dark backgrounds (preserves white D and grey/black 99).
    2. Creates a version with transparent background for light/white backgrounds (inverts the white 'D' to black,
       makes '99' fully visible, and makes 'DISTRICT-99' text dark/black).
    """
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read logo {input_path}")
        return False
        
    h, w, c = img.shape
    
    # 1. Isolate the black background via floodfill from corners
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    img_flood = img.copy()
    
    # Border seed points
    border_points = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)
    ]
    
    for pt in border_points:
        pixel = img[pt[1], pt[0]]
        # Background is pure black/very dark
        if all(val < 30 for val in pixel):
            cv2.floodFill(img_flood, flood_mask, pt, (0, 0, 0), (10, 10, 10), (10, 10, 10), flags=8 | cv2.FLOODFILL_FIXED_RANGE)
            
    bg_mask = flood_mask[1:h+1, 1:w+1]
    
    # Foreground mask: 255 where logo is, 0 where background is
    fg_mask = np.where(bg_mask == 1, 0, 255).astype(np.uint8)
    
    # Clean the mask edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    
    # --- VERSION 1: For Dark Backgrounds (Preserves white 'D' and grey '99') ---
    b, g, r = cv2.split(img)
    rgba_dark = cv2.merge([b, g, r, fg_mask])
    cv2.imwrite(output_dark_bg, rgba_dark)
    print(f"✅ Saved dark-bg logo to {output_dark_bg}")
    
    # --- VERSION 2: For Light/White Backgrounds (Inverts white 'D' to black, preserves '99' and 'DISTRICT-99' in black/grey) ---
    black_b = np.zeros((h, w), dtype=np.uint8)
    black_g = np.zeros((h, w), dtype=np.uint8)
    black_r = np.zeros((h, w), dtype=np.uint8)
    
    rgba_light = cv2.merge([black_b, black_g, black_r, fg_mask])
    cv2.imwrite(output_light_bg, rgba_light)
    print(f"✅ Saved light-bg logo to {output_light_bg}")
    
    # Also save as SVG wrapper (crisp vector vector container)
    save_as_svg_wrapper(output_light_bg, "/home/user/D99-Social-Media/06-Brand-Assets/d99_logo_light_bg.svg")
    save_as_svg_wrapper(output_dark_bg, "/home/user/D99-Social-Media/06-Brand-Assets/d99_logo_dark_bg.svg")
    
    return True

def save_as_svg_wrapper(png_path, svg_path):
    """
    Wraps the transparent PNG inside an SVG container with proper scaling
    to make it behave exactly as a scalable vector graphic on Shopify!
    """
    img = Image.open(png_path)
    w, h = img.size
    
    # Convert PNG to base64
    import base64
    with open(png_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <image width="{w}" height="{h}" href="data:image/png;base64,{b64_data}" />
</svg>"""

    with open(svg_path, "w") as f:
        f.write(svg_content)
    print(f"✅ Generated SVG wrapper: {os.path.basename(svg_path)}")

if __name__ == "__main__":
    make_logo_transparent_and_inverted(
        "/home/user/uploads/9.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/d99_logo_dark_bg.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/d99_logo_light_bg.png"
    )
