from PIL import Image, ImageDraw, ImageFont
import os

def apply_brand_watermark(image_path, website_url="www.district-99.com"):
    """
    Applies a highly-styled, modern, and youthful website text watermark
    (www.district-99.com) onto the image using a clean DejaVuSans-Bold font.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return False
        
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    
    # Create Draw object
    draw = ImageDraw.Draw(img)
    
    # Set up font size (scaled to 2.5% of image height for high legibility)
    font_size = int(h * 0.025)
    
    # Load the beautiful DejaVuSans-Bold font which is installed on the system
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Set up modern semi-transparent white/gray color for clean streetwear vibe (editorial style)
    text_color = (255, 255, 255, 180) # Clean white with slight opacity (Alpha = 180)
    
    # Position: Bottom-center or bottom-left. Let's do bottom-center!
    # Calculate text dimensions
    if hasattr(draw, "textlength"):
        text_w = draw.textlength(website_url, font=font)
    else:
        text_w = font_size * len(website_url) * 0.6
        
    text_x = (w - text_w) // 2 # Centered
    text_y = h - int(h * 0.08) # 8% from bottom
    
    # Optional: Draw a very subtle dark shadow behind text for perfect contrast on any background
    shadow_color = (0, 0, 0, 80)
    draw.text((text_x + 2, text_y + 2), website_url, font=font, fill=shadow_color)
    
    # Draw the main text
    draw.text((text_x, text_y), website_url, font=font, fill=text_color)
    
    # Save the watermarked image
    img.save(image_path, "PNG")
    print(f"✅ Successfully watermarked {os.path.basename(image_path)} with: {website_url}")
    return True

if __name__ == "__main__":
    # Test on a dummy path or a completed pose
    apply_brand_watermark(
        "/home/user/product/tshirt 01 to 18/TSH-01/pose_1.png"
    )
