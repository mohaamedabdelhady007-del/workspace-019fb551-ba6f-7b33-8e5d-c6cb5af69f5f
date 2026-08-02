import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_studio_backdrop_fast(width, height, color_center, color_border, center_y_ratio=0.45):
    # Create a small image first for super-smooth and fast gradient scaling
    sw, sh = 100, 133
    cx, cy = sw / 2, sh * center_y_ratio
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

def generate_bento_assets():
    print("🎨 Generating 8 bespoke bento lookbook panel assets...")
    
    # Base color palette for our luxury studio-grey look (SSENSE style)
    color_center = (248, 248, 248) # Off-white
    color_border = (220, 220, 222) # Soft grey
    
    # Lookbook Panels Map
    # Panel ID: (TSH_Code, Pose_Num, Target Width, Canvas Width, Canvas Height)
    panels_map = {
        1: ("TSH-01", 1, 620, 800, 1000),  # Panel 1: Large Featured (800x1000)
        2: ("TSH-02", 2, 450, 600, 800),   # Panel 2: Medium (600x800)
        3: ("TSH-03", 3, 450, 600, 800),   # Panel 3: Medium (600x800)
        4: ("TSH-04", 1, 450, 600, 800),   # Panel 4: Small (600x800)
        5: ("TSH-05", 4, 550, 1000, 600),  # Panel 5: Wide Horizontal (1000x600) - Sitting pose!
        6: ("TSH-06", 2, 450, 600, 800),   # Panel 6: Medium (600x800)
        7: ("TSH-07", 3, 450, 600, 800),   # Panel 7: Medium (600x800)
        8: ("TSH-08", 1, 450, 600, 800)    # Panel 8: Small (600x800)
    }
    
    for panel_id, (tsh, pose_num, target_w, cw, ch) in panels_map.items():
        model_path = f"product/tshirt 01 to 18/{tsh}/pose_{pose_num}.png"
        if not os.path.exists(model_path):
            print(f"   ❌ Missing model path: {model_path}")
            continue
            
        print(f"   ⚙️ Processing Panel {panel_id} ({tsh} pose_{pose_num})...")
        
        # 1. Create spotlight background
        # For wide panels, center the spotlight slightly lower
        cy_ratio = 0.5 if cw > ch else 0.45
        bg = create_studio_backdrop_fast(cw, ch, color_center, color_border, center_y_ratio=cy_ratio)
        
        # 2. Open and resize model
        model = Image.open(model_path).convert("RGBA")
        scale_ratio = target_w / model.width
        target_h = int(model.height * scale_ratio)
        model_resized = model.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # 3. Calculate alignment offsets
        offset_x = (cw - target_w) // 2
        
        # Standing vs sitting poses vertical alignment
        if pose_num == 4: # Sitting pose (Panel 5)
            offset_y = ch - target_h - 40 # slightly raised for seating shadow
        else:
            offset_y = ch - target_h - 10 # aligned near bottom
            
        # 4. Create shadow
        shadow_w = int(target_w * 0.75)
        shadow_h = 30 if cw > ch else 24
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, 50))
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(12))
        
        # Paste shadow first
        shadow_y = ch - 40 if pose_num == 4 else ch - 25
        bg.paste(shadow_blurred, ((cw - shadow_w) // 2, shadow_y), shadow_blurred)
        
        # Paste model
        bg.paste(model_resized, (offset_x, offset_y), model_resized)
        
        # 5. Save as high-quality PNG
        output_filename = f"uploads/bento_panel_{panel_id}.png"
        bg.save(output_filename, "PNG", quality=95)
        print(f"      ✅ Saved {output_filename}")

if __name__ == "__main__":
    generate_bento_assets()
