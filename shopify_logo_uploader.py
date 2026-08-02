import urllib.request
import json
import base64
import os

# DISTRICT-99 (D99) - SHOPIFY THEME LOGO UPLOADER
# هذا السكريبت يقوم بتشفير اللوجو الشفاف كـ Base64 ورفعه مباشرة بداخل ملفات أصول الثيم عندك لتختاره بكبسة زر!

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
        print(f"❌ Failed to fetch themes: {e}")
        return None

def upload_logo_as_theme_asset():
    print("🚀 Initiating custom transparent logo upload to your active theme...")
    theme_id = get_active_theme_id()
    if not theme_id:
        return
        
    logo_path = "/home/user/D99-Social-Media/06-Brand-Assets/d99-logo-transparent.png"
    if not os.path.exists(logo_path):
        print("❌ Error: d99-logo-transparent.png not found locally.")
        return
        
    # Read the binary file and encode it to base64
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    # Call Shopify PUT Asset API
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": "assets/d99-logo-transparent.png",
            "attachment": encoded_string
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("   ✅ Successfully uploaded 'd99-logo-transparent.png' to theme assets!")
            print("\n🎉 LOGO IS NOW AVAILABLE IN YOUR THEME! 🎉")
            print("👉 اذهب الآن لـ Customize -> Header -> Logo image")
            print("👉 واضغط على Select Image، ستجد اللوجو الجديد الشفاف جاهزاً لتختاره فوراً!")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to upload logo: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    upload_logo_as_theme_asset()
