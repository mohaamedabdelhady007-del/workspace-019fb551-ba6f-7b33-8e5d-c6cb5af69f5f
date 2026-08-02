import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY LIVE BENTO LOOKBOOK DEPLOYER
# هذا السكريبت يتصل برمجياً بمتجرك، ويقوم بحقن وتفعيل قسم الـ Bento Lookbook المطور ذو الـ 8 إطارات التفاعلية العصرية مباشرة في ثيم موقعك!

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
        return None

def deploy_bento_lookbook():
    print("🚀 Initiating live Bento Lookbook section deployment on Shopify storefront...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # Read the updated bento grid liquid code from our workspace
    liquid_path = "/home/user/shopify-custom-sections/d99-lookbook-grid.liquid"
    if not os.path.exists(liquid_path):
        print("❌ Error: d99-lookbook-grid.liquid not found locally.")
        return
        
    with open(liquid_path, "r", encoding="utf-8") as f:
        lookbook_code = f.read()
        
    # Call PUT Asset API to create/update sections/d99-lookbook-grid.liquid
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": "sections/d99-lookbook-grid.liquid",
            "value": lookbook_code
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("   ✅ Successfully injected 'sections/d99-lookbook-grid.liquid' into Shopify theme!")
            print("\n🎉 THE ASYMMETRICAL BENTO LOOKBOOK IS NOW LIVE! 🎉")
            print("👉 اذهب الآن لـ Customize -> Add Section")
            print("👉 واكتب 'D99 Bento Lookbook' لتفعيله على صفحتك الرئيسية فوراً ورؤية المعجزات!")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to deploy lookbook section: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    deploy_bento_lookbook()
