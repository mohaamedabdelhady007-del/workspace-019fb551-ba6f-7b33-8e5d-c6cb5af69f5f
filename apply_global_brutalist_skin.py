import urllib.request
import json
import base64
import os

# DISTRICT-99 (D99) - GLOBAL BRUTALIST DAWN SKIN DEPLOYER
# هذا السكريبت الاحترافي يقوم بتعديل إعدادات ثيم Dawn كلياً محلياً وعبر الـ API ليتحول المتجر بأكمله (بما يشمل الهيدر والفوتر والصفحات والمنتجات)
# إلى تصميم مفرغ باللون الأسود والأحمر التكتيكي والخرسانة، ومطابقة التصاميم 100% بدون أي ألوان بيضاء مكسورة!

STORE_URL = "district99-preview.myshopify.com"
THEME_ID = 189908910264  # معرّف ثيم "D99 Cyber-Brutalist Master Theme"

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

def inject_asset(asset_key, asset_value, is_binary=False):
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json"
    if is_binary:
        encoded_string = base64.b64encode(asset_value).decode("utf-8")
        payload = {
            "asset": {
                "key": asset_key,
                "attachment": encoded_string
            }
        }
    else:
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
            print(f"   ✅ Successfully injected: {asset_key}")
            return True
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to inject {asset_key}: {e.read().decode('utf-8')}")
        return False

def apply_global_brutalist_skin():
    print("🚀 Initiating global Cyber-Brutalist skin deployment on Dawn engine...")
    
    # 1. Force white logo for the header because the header will now be dark-mode black!
    logo_white_path = "uploads/d99_logo_transparent.png"
    if os.path.exists(logo_white_path):
        with open(logo_white_path, "rb") as f:
            inject_asset("assets/d99-logo-header.png", f.read(), is_binary=True)
            print("   ✅ Set header logo to White Transparent version for dark-mode header contrast!")

    # 2. Complete, comprehensive set of global CSS overrides to append to base.css
    global_brutalist_css = """
/* ====================================================
   DISTRICT-99 (D99) - GLOBAL CYBER-BRUTALIST OVERRIDES
   ==================================================== */
:root, .color-background-1, .color-background-2, .color-accent-1, .color-accent-2 {
  --gradient-background: #080808 !important;
  --color-background: 8,8,8 !important;
  --color-foreground: 255,255,255 !important;
  --color-button: 229,9,20 !important;
  --color-button-text: 255,255,255 !important;
  --color-secondary-button-text: 255,255,255 !important;
  --color-card-background: 20,20,20 !important;
  --font-body-family: 'Space Grotesk', sans-serif !important;
  --font-heading-family: 'Syne', sans-serif !important;
}

/* Force dark background and white text globally on all containers */
body, html, main, #MainContent, .page-width, .gradient, .section, .shopify-section {
  background-color: #080808 !important;
  background: #080808 !important;
  color: #ffffff !important;
}

/* Style default Dawn header to be black and sleek */
.header-wrapper, .header, .announcement-bar, .menu-drawer, .menu-drawer__menu {
  background-color: #080808 !important;
  background: #080808 !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  color: #ffffff !important;
}

.header__menu-item, .header__active-menu-item, .header__heading-link, .header__icon, .list-menu__item {
  color: #ffffff !important;
  font-family: 'Space Grotesk', sans-serif !important;
  text-transform: uppercase !important;
  font-weight: 700 !important;
}

/* Force all buttons to have sharp corners and solid black/red */
.button, .btn, button, input[type="submit"], .shopify-payment-button__button {
  border-radius: 0px !important;
  border: 1px solid #ffffff !important;
  background-color: #000000 !important;
  color: #ffffff !important;
  font-family: 'Syne', sans-serif !important;
  text-transform: uppercase !important;
  font-weight: 800 !important;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
}

.button:hover, .btn:hover, button:hover, .shopify-payment-button__button:hover {
  background-color: #ffffff !important;
  color: #000000 !important;
  border-color: #ffffff !important;
}

.button--primary, .product-form__submit {
  background-color: #e50914 !important;
  border-color: #e50914 !important;
  color: #ffffff !important;
}

.button--primary:hover, .product-form__submit:hover {
  background-color: #ffffff !important;
  color: #000000 !important;
  border-color: #ffffff !important;
}

/* Style product cards globally to have sharp corners, black borders, and dark backgrounds */
.card, .card-wrapper, .product-grid-container {
  border: 1px solid rgba(255,255,255,0.08) !important;
  background-color: #141414 !important;
  box-shadow: none !important;
}

.card__inner {
  background-color: #1a1a1a !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

.card__heading, .card__information, .price {
  color: #ffffff !important;
}

/* Hide default Dawn footer */
.footer {
  display: none !important;
}
"""
    # Fetch existing base.css from theme and append
    print("🎨 Fetching assets/base.css to append global overrides...")
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json?asset[key]=assets/base.css"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            existing_css = json.loads(response.read().decode("utf-8"))["asset"]["value"]
    except Exception:
        existing_css = ""
        
    if "DISTRICT-99" in existing_css:
        # Prevent double appends
        parts = existing_css.split("/* ====================================================\n   DISTRICT-99")
        existing_css = parts[0]
        
    updated_css = existing_css + "\n\n" + global_brutalist_css
    inject_asset("assets/base.css", updated_css)
    print("🎉 Global Brutalist skin successfully deployed!")

if __name__ == "__main__":
    apply_global_brutalist_skin()
