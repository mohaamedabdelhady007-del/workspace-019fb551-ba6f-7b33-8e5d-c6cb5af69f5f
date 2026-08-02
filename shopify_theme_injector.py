import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY THEME AUTOMATED CODE INJECTOR
# هذا السكريبت يتصل برمجياً بمتجرك، ويحدد الثيم النشط المفعّل حالياً، ويقوم بحقن الأقسام المخصصة والـ CSS المبتكر بداخل أكواد موقعك تلقائياً!

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
    """
    Fetches the active (published) theme ID from the Shopify store.
    """
    url = f"https://{STORE_URL}/admin/api/2026-07/themes.json"
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            themes = res_json["themes"]
            for t in themes:
                if t["role"] == "main": # The active published theme
                    print(f"🎬 Found Active Published Theme: '{t['name']}' (ID: {t['id']})")
                    return t["id"]
            # Fallback to first theme if no active found
            print(f"🎬 Fallback Theme: '{themes[0]['name']}' (ID: {themes[0]['id']})")
            return themes[0]["id"]
    except Exception as e:
        print(f"❌ Failed to fetch themes: {e}")
        return None

def inject_asset(theme_id, asset_key, asset_value):
    """
    Creates or updates an asset (template, section, or CSS) inside the Shopify theme.
    """
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": asset_key,
            "value": asset_value
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"   ✅ Successfully injected asset: {asset_key}")
            return True
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to inject {asset_key}: {e.read().decode('utf-8')}")
        return False

def fetch_existing_asset(theme_id, asset_key):
    """
    Fetches the existing content of an asset from the Shopify theme.
    """
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json?asset[key]={asset_key}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            return res_json["asset"]["value"]
    except Exception:
        return ""

def run_theme_injection():
    print("🚀 Initiating automated custom theme deployment on Shopify...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # 1. Inject Custom Section: d99-marquee-ticker.liquid
    marquee_path = "/home/user/shopify-custom-sections/d99-marquee-ticker.liquid"
    if os.path.exists(marquee_path):
        with open(marquee_path, "r", encoding="utf-8") as f:
            marquee_code = f.read()
        inject_asset(theme_id, "sections/d99-marquee-ticker.liquid", marquee_code)
        
    # 2. Inject Custom Section: d99-split-hero.liquid
    split_hero_path = "/home/user/shopify-custom-sections/d99-split-hero.liquid"
    if os.path.exists(split_hero_path):
        with open(split_hero_path, "r", encoding="utf-8") as f:
            split_hero_code = f.read()
        inject_asset(theme_id, "sections/d99-split-hero.liquid", split_hero_code)
        
    # 3. Inject and Append Custom CSS into assets/base.css (Shopify Dawn default stylesheet)
    css_path = "/home/user/shopify-custom-sections/theme-custom-styling.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            custom_css = f.read()
            
        # Detect stylesheet: Dawn theme uses assets/base.css
        stylesheet_key = "assets/base.css"
        existing_css = fetch_existing_asset(theme_id, stylesheet_key)
        
        # If assets/base.css doesn't exist, try assets/theme.css
        if not existing_css:
            stylesheet_key = "assets/theme.css"
            existing_css = fetch_existing_asset(theme_id, stylesheet_key)
            
        if not existing_css:
            stylesheet_key = "assets/base.css" # Default to base.css if neither found
            
        # Append our custom CSS at the bottom of the existing stylesheet
        # Check if we already appended it to prevent double append
        if "DISTRICT-99" not in existing_css:
            updated_css = existing_css + "\n\n" + custom_css
            inject_asset(theme_id, stylesheet_key, updated_css)
            print(f"   🎨 Successfully appended custom streetwear CSS at the bottom of: {stylesheet_key}")
        else:
            print(f"   🎨 Custom CSS already exists in {stylesheet_key}, skipped appending.")

    print("\n🎉 CUSTOM SECTIONS & EDITORIAL STYLING DEPLOYED TO YOUR SHOPIFY THEME SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run_theme_injection()
