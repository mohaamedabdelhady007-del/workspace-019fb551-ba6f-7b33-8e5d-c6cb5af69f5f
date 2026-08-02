import os
from PIL import Image

def make_logo_transparent():
    input_path = "uploads/4.png"
    output_path = "uploads/d99_logo_transparent.png"
    
    if not os.path.exists(input_path):
        print(f"❌ Input logo path {input_path} not found.")
        return
        
    print(f"⚙️ Processing logo {input_path} to make it transparent...")
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # We want to remove the black background.
        # Solid black is (0, 0, 0). Let's detect pixels that are very close to black.
        # If the brightness (average of R, G, B) is very low, make it transparent.
        r, g, b, a = item
        brightness = (r + g + b) / 3.0
        
        if brightness < 30: # threshold for black pixels
            # Make it fully transparent
            new_data.append((0, 0, 0, 0))
        else:
            # Keep the pixel but make it white and preserve the alpha channel based on its brightness
            # This ensures smooth anti-aliased white edges!
            alpha = int(min(255, brightness * 1.2))
            new_data.append((255, 255, 255, alpha))
            
    img.putdata(new_data)
    
    # Let's crop the image to the actual bounds of the logo to remove empty space!
    bbox = img.getbbox()
    if bbox:
        img_cropped = img.crop(bbox)
        img_cropped.save(output_path, "PNG")
        # Also let's save a version in theme assets folder and D99 social media assets
        img_cropped.save("D99-Social-Media/06-Brand-Assets/d99-logo-header.png", "PNG")
        print(f"   ✅ Transparent cropped logo saved successfully to {output_path} and D99-Social-Media assets!")
    else:
        img.save(output_path, "PNG")
        print(f"   ✅ Transparent logo saved successfully to {output_path}!")

if __name__ == "__main__":
    make_logo_transparent()
