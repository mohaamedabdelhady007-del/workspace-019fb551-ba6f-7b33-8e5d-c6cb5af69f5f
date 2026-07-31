from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
import os

def create_red_logo_watermark(logo_path, target_size=(100, 100)):
    """
    Reads the white-on-black logo, removes black background, colors the white star red,
    and returns a transparent RGBA logo image.
    """
    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize first
    logo = logo.resize(target_size, Image.Resampling.LANCZOS)
    
    # We want to isolate the white parts and make them red, and make black parts transparent.
    # Create a new red image
    red_color = (229, 9, 20, 255) # Sleek red
    red_img = Image.new("RGBA", target_size, red_color)
    
    # Isolate white pixels from the logo to use as a mask
    # Since logo_option_2 is white on black, we can take the Red channel (or any) as mask
    r, g, b, a = logo.split()
    # High-contrast threshold to get a clean mask of the star
    mask = r.point(lambda p: 255 if p > 50 else 0)
    
    # Merge red image with the mask
    watermark_logo = Image.new("RGBA", target_size, (0,0,0,0))
    watermark_logo.paste(red_img, (0, 0), mask=mask)
    
    return watermark_logo

def apply_brand_watermark(image_path, logo_path, website_url="www.district-99.com"):
    """
    Applies a professional red Cyber-Star logo and minimal website text in the corner of the image.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return False
        
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    
    # Create Draw object
    draw = ImageDraw.Draw(img)
    
    # Set up logo watermark
    logo_size = (int(h * 0.06), int(h * 0.06)) # 6% of image height
    red_logo = create_red_logo_watermark(logo_path, target_size=logo_size)
    
    # Position: Bottom-right corner with margins
    margin_x = int(w * 0.05) # 5% margin
    margin_y = int(h * 0.05)
    
    logo_x = w - logo_size[0] - margin_x
    logo_y = h - logo_size[1] - margin_y
    
    # Paste the red logo onto the image
    img.paste(red_logo, (logo_x, logo_y), mask=red_logo)
    
    # Set up minimal website text
    # Try to load a clean sans-serif font, fallback to default
    font_size = int(h * 0.02) # 2% of image height
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            
    # Text position: Left of the logo, vertically centered
    text_color = (229, 9, 20, 200) # Slightly transparent red to match the logo
    text_w = draw.textlength(website_url, font=font) if hasattr(draw, "textlength") else font_size * len(website_url) * 0.6
    
    text_x = logo_x - int(text_w) - 15 # 15px gap between text and logo
    # Vertically center the text with the logo
    text_y = logo_y + (logo_size[1] // 2) - (font_size // 2)
    
    # Draw the text
    draw.text((text_x, text_y), website_url, font=font, fill=text_color)
    
    # Save the watermarked image
    img.save(image_path, "PNG")
    print(f"✅ Successfully watermarked {os.path.basename(image_path)} with logo & website!")
    return True

if __name__ == "__main__":
    # Test on a dummy path or TSH-01 pose_1.png
    apply_brand_watermark(
        "/home/user/product/tshirt 01 to 18/TSH-01/pose_1.png",
        "/home/user/D99-Social-Media/06-Brand-Assets/logo_option_2.png"
    )
