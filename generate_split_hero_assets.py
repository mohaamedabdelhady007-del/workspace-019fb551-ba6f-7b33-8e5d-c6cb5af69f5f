import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_studio_backdrop_fast(width, height, color_center, color_border):
    # Create a small image first for super-smooth and fast gradient scaling
    sw, sh = 100, 133
    cx, cy = sw / 2, sh * 0.45
    max_dist = math.sqrt(cx**2 + cy**2)
    
    grad = Image.new("L", (sw, sh), 0)
    for y in range(sh):
        for x in range(sw):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            # Smooth radial spotlight dropoff
            val = int(255 * (1.0 - min(dist / (max_dist * 0.8), 1.0)) ** 1.5)
            grad.putpixel((x, y), val)
            
    grad = grad.filter(ImageFilter.GaussianBlur(4))
    
    center_img = Image.new("RGB", (sw, sh), color_center)
    border_img = Image.new("RGB", (sw, sh), color_border)
    small_bg = Image.composite(center_img, border_img, grad)
    
    # Scale up to full resolution using LANCZOS for flawless quality
    return small_bg.resize((width, height), Image.Resampling.LANCZOS)

def generate_split_hero_banners():
    print("🎨 Generating bespoke luxury studio banners for D99 Split Hero...")
    
    # Editorial Dimensions: 1200 x 1600 (Aspect Ratio 3:4)
    canvas_w, canvas_h = 1200, 1600
    
    # Color Palette: Clean neutral studio grey (SSENSE style)
    # This prevents the black balaclava from disappearing into solid black!
    color_center = (248, 248, 248) # Crisp off-white center spotlight
    color_border = (220, 220, 222) # Soft premium grey border
    
    # Left Banner: TSH-04 pose_3.png (Standing model with red stars tee)
    left_model_path = "product/tshirt 01 to 18/TSH-04/pose_3.png"
    if os.path.exists(left_model_path):
        left_bg = create_studio_backdrop_fast(canvas_w, canvas_h, color_center, color_border)
        model = Image.open(left_model_path).convert("RGBA")
        
        # Scale model: we want it to look prominent but not cut-off.
        # Original height is 1195. Let's scale it so that height is ~1350px.
        scale_ratio = 1350 / model.height
        new_w = int(model.width * scale_ratio)
        new_h = 1350
        model_resized = model.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Overlay model centered horizontally, and aligned near the bottom
        offset_x = (canvas_w - new_w) // 2
        offset_y = canvas_h - new_h - 20 # 20px padding from bottom
        
        # Create a subtle floor shadow
        shadow_w = int(new_w * 0.75)
        shadow_h = 40
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, 50)) # Soft black shadow with alpha
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(15))
        
        # Paste shadow first
        left_bg.paste(shadow_blurred, ((canvas_w - shadow_w) // 2, canvas_h - 60), shadow_blurred)
        # Paste model
        left_bg.paste(model_resized, (offset_x, offset_y), model_resized)
        
        # Save high-quality PNG
        left_bg.save("uploads/split_hero_left.png", "PNG", quality=95)
        print("   ✅ Created uploads/split_hero_left.png")
    else:
        print("   ❌ Left model path not found:", left_model_path)
        
    # Right Banner: TSH-07 pose_4.png (Sitting model with WELL DONE tee)
    right_model_path = "product/tshirt 01 to 18/TSH-07/pose_4.png"
    if os.path.exists(right_model_path):
        right_bg = create_studio_backdrop_fast(canvas_w, canvas_h, color_center, color_border)
        model = Image.open(right_model_path).convert("RGBA")
        
        # Scale model: sitting pose original size is 1024x1024.
        # Let's scale it so width is ~1050px.
        scale_ratio = 1050 / model.width
        new_w = 1050
        new_h = int(model.height * scale_ratio)
        model_resized = model.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Overlay model centered horizontally, and positioned vertically
        offset_x = (canvas_w - new_w) // 2
        offset_y = canvas_h - new_h - 80 # slightly raised
        
        # Create a shadow for the chair/sitting pose
        shadow_w = int(new_w * 0.8)
        shadow_h = 50
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, 60))
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(20))
        
        # Paste shadow first
        right_bg.paste(shadow_blurred, ((canvas_w - shadow_w) // 2, canvas_h - 110), shadow_blurred)
        # Paste model
        right_bg.paste(model_resized, (offset_x, offset_y), model_resized)
        
        # Save high-quality PNG
        right_bg.save("uploads/split_hero_right.png", "PNG", quality=95)
        print("   ✅ Created uploads/split_hero_right.png")
    else:
        print("   ❌ Right model path not found:", right_model_path)

if __name__ == "__main__":
    generate_split_hero_banners()
