import os
from PIL import Image

def make_logo_black_transparent():
    input_path = "uploads/4.png"
    output_path = "uploads/d99_logo_black_transparent.png"
    
    if not os.path.exists(input_path):
        print(f"❌ Input logo path {input_path} not found.")
        return
        
    print(f"⚙️ Processing logo {input_path} to make it black and transparent...")
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        r, g, b, a = item
        brightness = (r + g + b) / 3.0
        
        if brightness < 30: # threshold for black pixels
            new_data.append((0, 0, 0, 0))
        else:
            # Make the pixel black but set alpha based on its original brightness
            alpha = int(min(255, brightness * 1.2))
            new_data.append((0, 0, 0, alpha))
            
    img.putdata(new_data)
    
    bbox = img.getbbox()
    if bbox:
        img_cropped = img.crop(bbox)
        img_cropped.save(output_path, "PNG")
        # Overwrite the theme assets header logo with this beautiful black transparent version!
        img_cropped.save("D99-Social-Media/06-Brand-Assets/d99-logo-header-black.png", "PNG")
        print(f"   ✅ Black transparent cropped logo saved successfully to {output_path}!")
    else:
        img.save(output_path, "PNG")
        print(f"   ✅ Black transparent logo saved successfully to {output_path}!")

if __name__ == "__main__":
    make_logo_black_transparent()
