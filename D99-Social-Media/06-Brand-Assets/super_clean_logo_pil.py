from PIL import Image
import os

# DISTRICT-99 (D99) - SUPER CLEAN LOGO GENERATOR (PIL EDITION)
# هذا السكريبت يستغل حقيقة أن اللوجو الأصلي مفرغ بالفعل ويقوم بتحويل لونه بالكامل لأسود ناصع وخلفية شفافة 100% وبدون أي غشاوة رمادية أو مربعات سوداء!

def clean_logo_pil(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    # Extract the original pixels
    pixels = img.getdata()
    
    new_pixels = []
    for p in pixels:
        r, g, b, a = p
        
        # Threshold the alpha channel: if alpha is less than 80, it's just background noise
        if a >= 80:
            # Change its color to solid black (0,0,0) while preserving its exact original transparency/alpha value!
            new_pixels.append((0, 0, 0, a))
        else:
            # Keep it fully transparent (0,0,0,0)
            new_pixels.append((0, 0, 0, 0))
            
    img.putdata(new_pixels)
    
    # Save the super clean transparent black logo
    img.save(output_path, "PNG")
    print(f"✅ Generated 100% transparent, razor-sharp solid black logo via PIL: {output_path}")

if __name__ == "__main__":
    clean_logo_pil(
        "/home/user/uploads/9.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/d99-logo-header.png"
    )
