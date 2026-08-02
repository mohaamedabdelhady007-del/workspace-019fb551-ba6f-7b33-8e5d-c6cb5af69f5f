import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY HEADER LOGO CONFIGURATOR
# هذا السكريبت يتصل برمجياً بـ layout/theme.liquid ويقوم باستبدال اسم المتجر النصي باللوجو الجديد الشفاف فورا!

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

def configure_header_logo():
    print("🚀 Initiating automatic header logo deployment on Shopify storefront...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # The updated layout/theme.liquid code with our logo replacement!
    updated_layout = """<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ page_title }} | {{ shop.name }}</title>
  {{ content_for_header }}
  {{ 'theme.css' | asset_url | stylesheet_tag }}
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
  <header class="header">
    <div class="container">
      <div class="nav">
        <div class="logo" style="display: flex; align-items: center; justify-content: center;">
          <a href="/" style="display: inline-block; line-height: 0;">
            <img src="{{ 'd99-logo-transparent.png' | asset_url }}" alt="DISTRICT-99" style="height: 45px; width: auto; object-fit: contain; vertical-align: middle;">
          </a>
        </div>
        <nav>
          <a href="/">Home</a>
          <a href="/collections/all">Shop</a>
          <a href="#categories">Categories</a>
          <a href="#featured">Featured</a>
        </nav>
        <div class="nav-actions">
          <a href="/cart"><i class="fas fa-shopping-cart"></i></a>
          <a href="/account"><i class="fas fa-user"></i></a>
        </div>
      </div>
    </div>
  </header>

  <main>
    {{ content_for_layout }}
  </main>

  <footer>
    <div class="container">
      <p>&copy; {{ 'now' | date: '%Y' }} {{ shop.name }}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>"""

    # Call PUT Asset API
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {
        "asset": {
            "key": "layout/theme.liquid",
            "value": updated_layout
        }
    }
    
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("   ✅ Successfully updated layout/theme.liquid with the new logo!")
            print("\n🎉 THE LOGO IS NOW LIVE ON YOUR WEBSITE HEADER! 🎉")
            print("👉 افتح متجرك المباشر الآن لتراه بمنتهى الجمال والفخامة!")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to configure logo in theme: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    configure_header_logo()
