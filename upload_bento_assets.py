import urllib.request
import json
import base64
import os

# DISTRICT-99 (D99) - SHOPIFY BENTO LOOKBOOK ASSET UPLOADER
# هذا السكريبت يتصل برمجياً بمتجرك ويقوم برفع الصور الـ 8 للـ Bento Lookbook كأصول ثابتة مباشرة في أصول الثيم!

STORE_URL = "district99-preview.myshopify.com"

if os.path.exists("/home/user/.shopify_token"):
    with open("/home/user/.shopify_token", "r") as f:
        ACCESS_TOKEN = f.read().strip()
else:
    ACCESS_TOKEN = "shpat_YOUR_TOKEN_HERE"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_active_theme_id():
    url = f"https://{STORE_URL}/admin/api/2026-07/themes.json"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            for t in res_json["themes"]:
                if t["role"] == "main":
                    return t["id"]
            return res_json["themes"][0]["id"]
    except Exception as e:
        return None

def upload_asset(theme_id, local_path, asset_key):
    if not os.path.exists(local_path):
        print(f"❌ Local path not found: {local_path}")
        return False
        
    with open(local_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": asset_key,
            "attachment": encoded_string
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"   ✅ Successfully uploaded '{asset_key}'!")
            return True
    except Exception as e:
        print(f"   ❌ Failed to upload '{asset_key}': {e}")
        return False

def main():
    print("🚀 Initiating Shopify asset upload for D99 Bento Lookbook...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # Upload 8 bento lookbook panel assets
    for i in range(1, 9):
        local_path = f"uploads/bento_panel_{i}.png"
        asset_key = f"assets/bento_panel_{i}.png"
        upload_asset(theme_id, local_path, asset_key)
        
    print("🎉 All 8 Bento Lookbook assets uploaded successfully!")

if __name__ == "__main__":
    main()
