from PIL import Image
import os

# DISTRICT-99 (D99) - LOGO CLEANER & GENERATOR
# هذا السكريبت يأخذ اللوجو الشفاف الأصلي ويقوم بتحويل الأجزاء البيضاء فيه إلى اللون الأسود بالملّي ليكون ظاهراً ومذهلاً على خلفية الهيدر البيضاء!

def process_original_logo(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # If the pixel is near-white (the letter 'D'), we convert it to solid black
        # so that the entire logo (D and 99 and DISTRICT-99 text) becomes perfectly visible on a white header!
        if item[0] > 150 and item[1] > 150 and item[2] > 150 and item[3] > 50:
            # Convert to solid black while preserving its alpha transparency
            new_data.append((0, 0, 0, item[3]))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    
    # Save the cleaned logo
    img.save(output_path, "PNG")
    print(f"✅ Generated perfect transparent black logo for white header: {output_path}")

if __name__ == "__main__":
    process_original_logo(
        "/home/user/uploads/9.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/d99-logo-header.png"
    )
