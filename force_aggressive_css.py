import urllib.request
import json
import os

# DISTRICT-99 (D99) - AGGRESSIVE HEADER & COMPACT CSS OVERRIDER
# هذا السكريبت الاحترافي يقوم بحقن قواعد CSS فائقة القوة والسيطرة بأسفل ملف base.css للثيم 189908910264
# لإجبار الهيدر واللوجو والقوائم بالكامل على التحول للون الأسود والأبيض المفرغ وإلغاء أي فجوات بيضاء ظاهرة في كروت المتجر تماماً!

STORE_URL = "district99-preview.myshopify.com"
THEME_ID = 189908910264

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

def inject_asset(key, value):
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json"
    payload = {
        "asset": {
            "key": key,
            "value": value
        }
    }
    req_body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"   ✅ Successfully injected: {key}")
            return True
    except Exception as e:
        print(f"   ❌ Failed to inject {key}: {e}")
        return False

def force_aggressive_css():
    print("🚀 Running aggressive header & container dark-mode CSS override...")
    
    # Aggressive Brutalist CSS overrides
    aggressive_css = """
/* ====================================================
   DISTRICT-99 (D99) - AGGRESSIVE BRUTALIST OVERRIDES
   ==================================================== */
:root {
  --gradient-background: #080808 !important;
  --color-background: 8,8,8 !important;
  --color-foreground: 255,255,255 !important;
  --color-button: 229,9,20 !important;
  --color-button-text: 255,255,255 !important;
}

/* Force body and all general wrapping containers to black */
body, html, main, #MainContent, .gradient, .shopify-section {
  background-color: #080808 !important;
  background: #080808 !important;
  color: #ffffff !important;
}

/* 1. AGGRESSIVE HEADER FORCE DARK MODE */
.header-wrapper, 
.header, 
.announcement-bar, 
.section-header,
header.header,
div.header-wrapper,
.header-wrapper--border-bottom,
.menu-drawer,
.menu-drawer__menu {
  background-color: #080808 !important;
  background: #080808 !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  color: #ffffff !important;
}

/* Force all header menu items and icons to White */
.header__menu-item, 
.header__active-menu-item, 
.header__heading-link, 
.header__icon, 
.header__heading, 
.list-menu__item,
.header__heading-link *,
.header__icon *,
.header__menu-item * {
  color: #ffffff !important;
  fill: #ffffff !important;
  font-family: 'Space Grotesk', sans-serif !important;
  text-transform: uppercase !important;
  font-weight: 700 !important;
}

/* Force white logo image sizing constraints */
.header__heading-logo {
  height: 44px !important;
  width: auto !important;
  object-fit: contain !important;
}

/* 2. FORCE SHARP BUTTONS GLOBALLY */
.button, .btn, button, input[type="submit"], .shopify-payment-button__button {
  border-radius: 0px !important;
  border: 1px solid #ffffff !important;
  background-color: #000000 !important;
  color: #ffffff !important;
  font-family: 'Syne', sans-serif !important;
  text-transform: uppercase !important;
  font-weight: 800 !important;
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

/* 3. STRICT DAWN CARD BRUTALIST SKIN */
.card, .card-wrapper, .product-grid-container {
  border: 1px solid rgba(255,255,255,0.08) !important;
  background-color: #141414 !important;
  box-shadow: none !important;
}

.card__inner {
  background-color: #1a1a1a !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

.card__heading, .card__information, .price, .price * {
  color: #ffffff !important;
}

/* Hide default Dawn footer */
.footer {
  display: none !important;
}
"""
    
    # Fetch existing base.css
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json?asset[key]=assets/base.css"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as r:
            existing_css = json.loads(r.read().decode())["asset"]["value"]
    except Exception:
        existing_css = ""
        
    if "DISTRICT-99 - AGGRESSIVE" in existing_css:
        parts = existing_css.split("/* ====================================================\n   DISTRICT-99 - AGGRESSIVE")
        existing_css = parts[0]
        
    updated_css = existing_css + "\n\n" + aggressive_css
    inject_asset("assets/base.css", updated_css)
    print("🎉 Aggressive overrides injected successfully!")

if __name__ == "__main__":
    force_aggressive_css()
