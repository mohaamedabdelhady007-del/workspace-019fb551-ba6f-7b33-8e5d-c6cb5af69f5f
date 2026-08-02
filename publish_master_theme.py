import urllib.request
import json
import os

# DISTRICT-99 (D99) - THEME PUBLISHER
# هذا السكريبت الأسطوري يتصل بمتجرك ويقوم بنشر وتفعيل ثيم DISTRICT-99 البروتالي المطور (189908910264) ليكون هو الثيم النشط والحي للمتجر فوراً!
# وبذلك، بمجرد دخولك على رابط موقعك، ستشاهد العظمة البصرية البروتالية الحقيقية لايف على الواجهة بدون كاش أو لغبطة!

STORE_URL = "district99-preview.myshopify.com"
THEME_ID_TO_PUBLISH = 189908910264  # معرّف ثيم "D99 Cyber-Brutalist Master Theme"

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

def publish_theme():
    print(f"🚀 Publishing 'D99 Cyber-Brutalist Master Theme' (ID: {THEME_ID_TO_PUBLISH}) to be LIVE on your storefront...")
    
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID_TO_PUBLISH}.json"
    payload = {
        "theme": {
            "id": THEME_ID_TO_PUBLISH,
            "role": "main"
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            print(f"   ✅ Theme published successfully! Role is now: {res_json['theme']['role']}")
            print("\n🎉 THE CYBER-BRUTALIST MASTER THEME IS NOW 100% LIVE AS YOUR ACTIVE STOREFRONT! 🎉")
            print("👉 افتح متجرك الحي المباشر الآن وشاهد الإبداع الخرافي الجديد!")
    except Exception as e:
        print(f"   ❌ Failed to publish theme: {e}")

if __name__ == "__main__":
    publish_theme()
