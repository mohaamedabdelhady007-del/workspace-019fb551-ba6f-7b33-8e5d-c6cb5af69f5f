import urllib.request
import json
import os

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

def print_theme_liquid():
    theme_id = get_active_theme_id()
    if not theme_id:
        return
        
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid"
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            value = res_json["asset"]["value"]
            print("Layout liquid found! Length:", len(value))
            print(value)
    except Exception as e:
        print(f"❌ Failed to fetch layout/theme.liquid: {e}")

if __name__ == "__main__":
    print_theme_liquid()
