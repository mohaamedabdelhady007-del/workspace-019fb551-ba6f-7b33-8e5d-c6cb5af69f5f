import urllib.request
import json
import time
import os

# DISTRICT-99 (D99) - SHOPIFY IMAGE RESYNCER & FORCE UPDATER
# هذا السكريبت يتصل بمتجرك ويقوم بمسح الصور القديمة وإعادة ربط صور جيت هاب الجديدة الشفافة لإجبار شوبيفاي على تحديثها فوراً!

STORE_URL = "district99-preview.myshopify.com"

# Read token safely from local file ignored by git
if os.path.exists("/home/user/.shopify_token"):
    with open("/home/user/.shopify_token", "r") as f:
        ACCESS_TOKEN = f.read().strip()
else:
    ACCESS_TOKEN = "shpat_YOUR_TOKEN_HERE"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def force_resync_product_images():
    print("🚀 Starting DISTRICT-99 Shopify Image Force-Update...")
    
    # Fetch all 18 products
    url = f"https://{STORE_URL}/admin/api/2026-07/products.json?limit=50"
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            products = res_json["products"]
            print(f"📦 Found {len(products)} products on the store to update.")
            
            for p in products:
                product_id = p["id"]
                title = p["title"]
                handle = p["handle"]
                
                # Extract folder name (e.g. TSH-01 from tags or SKU)
                # Let's search tags or SKU to find which TSH-XX it is
                folder_name = None
                for tag in p["tags"].split(","):
                    tag_clean = tag.strip()
                    if tag_clean.startswith("TSH-"):
                        folder_name = tag_clean
                        break
                        
                if not folder_name:
                    # fallback from variants sku
                    sku = p["variants"][0]["sku"] # e.g. D99-TSH-01-BLK-S
                    parts = sku.split("-")
                    if len(parts) >= 3:
                        folder_name = f"{parts[1]}-{parts[2]}" # TSH-01
                
                if not folder_name:
                    print(f"⚠️ Could not resolve folder name for {title}, skipping.")
                    continue
                
                print(f"\n🔄 Force-updating images for: {title} ({folder_name})")
                
                # 1. Delete all existing images from this product on Shopify
                if "images" in p and len(p["images"]) > 0:
                    for img in p["images"]:
                        img_id = img["id"]
                        del_url = f"https://{STORE_URL}/admin/api/2026-07/products/{product_id}/images/{img_id}.json"
                        del_req = urllib.request.Request(del_url, headers=headers, method="DELETE")
                        try:
                            with urllib.request.urlopen(del_req) as del_res:
                                print(f"   🗑️ Deleted old Shopify cached image ID: {img_id}")
                        except Exception as e_del:
                            print(f"   ⚠️ Failed to delete image {img_id}: {e_del}")
                            
                # 2. Prepare the 5 clean transparent image URLs from GitHub raw CDN
                github_repo_url = "https://raw.githubusercontent.com/mohaamedabdelhady007-del/workspace-019fb551-ba6f-7b33-8e5d-c6cb5af69f5f/main/product/tshirt%2001%20to%2018"
                new_images = [
                    {"src": f"{github_repo_url}/{folder_name}/3d_mannequin.png"},
                    {"src": f"{github_repo_url}/{folder_name}/pose_1.png"},
                    {"src": f"{github_repo_url}/{folder_name}/pose_2.png"},
                    {"src": f"{github_repo_url}/{folder_name}/pose_3.png"},
                    {"src": f"{github_repo_url}/{folder_name}/pose_4.png"}
                ]
                
                # Update product with the new images list
                update_url = f"https://{STORE_URL}/admin/api/2026-07/products/{product_id}.json"
                update_payload = {
                    "product": {
                        "id": product_id,
                        "images": new_images
                    }
                }
                
                update_body = json.dumps(update_payload).encode("utf-8")
                update_req = urllib.request.Request(update_url, data=update_body, headers=headers, method="PUT")
                
                try:
                    with urllib.request.urlopen(update_req) as update_res:
                        print(f"   ✅ Successfully linked and forced refresh of all 5 transparent images for {title}!")
                    time.sleep(1.5) # Slight delay to let Shopify servers fetch images without choke
                except Exception as e_up:
                    print(f"   ❌ Failed to re-link images for {title}: {e_up}")
                    
        print("\n🎉 ALL SHOPIFY PRODUCTS FORCE-REFRESHED WITH NEW TRANSPARENT IMAGES! 🎉")
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")

if __name__ == "__main__":
    force_resync_product_images()
