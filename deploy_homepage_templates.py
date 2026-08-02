import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY LIVE HOMEPAGE DEPLOYER
# هذا السكريبت يتصل برمجياً بمتجرك، ويقوم بتحديث ملف templates/index.json لتفعيل وترتيب الأقسام المخصصة مباشرة على الصفحة الرئيسية!

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

def deploy_homepage_layout():
    print("🚀 Initiating live homepage layout deployment on Shopify storefront...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # Construct the premium homepage structure using Online Store 2.0 JSON layout
    new_index_json = {
        "sections": {
            "d99_marquee_ticker": {
                "type": "d99-marquee-ticker",
                "settings": {
                    "marquee_text": "DISTRICT-99 // ACTION IS THE BRIDGE // FREE SHIPPING NATIONWIDE //"
                }
            },
            "d99_split_hero": {
                "type": "d99-split-hero",
                "settings": {
                    "title_left": "New Arrivals",
                    "btn_label_left": "COP NOW",
                    "title_right": "The Lookbook",
                    "btn_label_right": "Explore"
                }
            },
            "d99_lookbook_grid": {
                "type": "d99-lookbook-grid",
                "settings": {
                    "heading": "Define Your District"
                }
            },
            "featured_products": {
                "type": "bento-products",
                "settings": {}
            }
        },
        "order": [
            "d99_marquee_ticker",
            "d99_split_hero",
            "d99_lookbook_grid",
            "featured_products"
        ]
    }
    
    # Call PUT Asset API to update templates/index.json
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": "templates/index.json",
            "value": json.dumps(new_index_json, indent=2)
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("   ✅ Successfully injected templates/index.json into Shopify theme!")
            print("\n🎉 THE BRAND NEW PREMIUM HOMEPAGE IS NOW LIVE ON YOUR SHOPIFY WEBSITE! 🎉")
            print("👉 افتح متجرك المباشر الآن وشاهد الإبداع الخرافي الجديد!")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to deploy homepage: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    deploy_homepage_layout()
