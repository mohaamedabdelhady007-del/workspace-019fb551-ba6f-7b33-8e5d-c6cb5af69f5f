from PIL import Image, ImageDraw, ImageFont
import os

def create_red_star_logo(logo_path, target_size=(50, 50)):
    """
    Isolates the star from logo_option_2 and colors it in deep streetwear scarlet red.
    """
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize(target_size, Image.Resampling.LANCZOS)
    
    # Create red color mask
    red_color = (230, 10, 20, 230) # Premium streetwear red with slight transparency
    red_img = Image.new("RGBA", target_size, red_color)
    
    r, g, b, a = logo.split()
    mask = r.point(lambda p: 255 if p > 50 else 0)
    
    watermark_logo = Image.new("RGBA", target_size, (0,0,0,0))
    watermark_logo.paste(red_img, (0, 0), mask=mask)
    return watermark_logo

def apply_brand_watermark(image_path, logo_path="/home/user/D99-Social-Media/06-Brand-Assets/logo_option_2.png", website_url="www.district-99.com"):
    """
    Applies the ultimate premium streetwear watermark to the image:
    A red Cyber-Star logo on the left, and 'www.district-99.com' next to it,
    rendered in the ultra-cool 'Syne-Variable.ttf' font, centered at the bottom.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return False
        
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    
    # Create Draw object
    draw = ImageDraw.Draw(img)
    
    # Set up size metrics
    logo_h = int(h * 0.035) # 3.5% of image height
    logo_size = (logo_h, logo_h)
    
    # Load custom ultra-cool font (Syne-Variable)
    font_size = int(h * 0.024)
    font_path = "/home/user/D99-Social-Media/06-Brand-Assets/Syne-Variable.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Get text dimensions
    if hasattr(draw, "textlength"):
        text_w = draw.textlength(website_url, font=font)
    else:
        text_w = font_size * len(website_url) * 0.6
        
    # Total width of the watermark block (logo + spacing + text)
    spacing = 15 # Gap between logo and text
    total_w = logo_size[0] + spacing + text_w
    
    # Centered positions
    start_x = (w - total_w) // 2
    logo_y = h - int(h * 0.08) # 8% from bottom
    text_y = logo_y + (logo_size[1] // 2) - (font_size // 2) - 2 # Center text vertically with logo
    
    # 1. Paste the Red Cyber-Star Logo
    red_star = create_red_star_logo(logo_path, target_size=logo_size)
    img.paste(red_star, (int(start_x), int(logo_y)), mask=red_star)
    
    # 2. Draw the website text (Pure White with subtle drop shadow)
    text_x = start_x + logo_size[0] + spacing
    
    # Shadow for maximum contrast on any background
    draw.text((text_x + 2, text_y + 2), website_url, font=font, fill=(0, 0, 0, 100))
    # Main white text
    draw.text((text_x, text_y), website_url, font=font, fill=(255, 255, 255, 220))
    
    # Save the watermarked image
    img.save(image_path, "PNG")
    print(f"✅ Applied premium streetwear watermark (Red Star + Syne Web) to: {os.path.basename(image_path)}")
    return True

if __name__ == "__main__":
    apply_brand_watermark(
        "/home/user/product/tshirt 01 to 18/TSH-01/pose_1.png"
    )
