from PIL import Image
import os
import glob

def optimize_all_assets():
    print("🚀 Starting digital asset optimization...")
    # Scan both product folders and social media post folders
    png_files = glob.glob("/home/user/TSH-*/*.png") + glob.glob("/home/user/D99-Social-Media/**/*.png", recursive=True)
    total_old_size = 0
    total_new_size = 0
    
    for file_path in png_files:
        if not os.path.isfile(file_path):
            continue
        old_size = os.path.getsize(file_path)
        total_old_size += old_size
        
        try:
            img = Image.open(file_path)
            # Optimize and quantize to 8-bit adaptive palette (perfect for Shopify & web)
            optimized_img = img.convert('P', palette=Image.Palette.ADAPTIVE)
            optimized_img.save(file_path, 'PNG', optimize=True)
            
            new_size = os.path.getsize(file_path)
            total_new_size += new_size
            print(f"✅ Optimized: {os.path.basename(file_path)} | {old_size/(1024*1024):.2f}MB -> {new_size/(1024*1024):.2f}MB")
        except Exception as e:
            print(f"❌ Failed to optimize {file_path}: {e}")
            
    print(f"\n🎉 Optimization Complete!")
    print(f"📊 Total Old Size: {total_old_size/(1024*1024):.2f} MB")
    print(f"📊 Total New Size: {total_new_size/(1024*1024):.2f} MB")
    if total_old_size > 0:
        print(f"📉 Saved: {((total_old_size - total_new_size) / total_old_size) * 100:.1f}% space!")

if __name__ == "__main__":
    optimize_all_assets()
