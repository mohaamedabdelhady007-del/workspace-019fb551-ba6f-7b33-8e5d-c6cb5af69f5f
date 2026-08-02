import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY LIVE HEADER DEPLOYER
# هذا السكريبت يتصل برمجياً بمتجرك، ويقوم بحقن الـ Custom Header والـ CSS المطور ذو الدوائر والخطوط الحديثة والـ Home المتميزة باللون الأحمر القاني مباشرة في موقعك الحي!

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

def deploy_custom_header():
    print("🚀 Deploying premium customized header with centered logo, left menu circles, and branded 'Home.'...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return
        
    # 1. New custom layout/theme.liquid structure
    new_theme_liquid = """<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ page_title }} | {{ shop.name }}</title>
  {{ content_for_header }}
  {{ 'theme.css' | asset_url | stylesheet_tag }}
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
</head>
<body>
  <header class="header d99-custom-header">
    <div class="container">
      <div class="nav d99-header-grid">
        
        <!-- 1. LEFT SIDE: Navigation Links -->
        <nav class="d99-nav-links">
          <a href="/" class="d99-link-home">Home<span class="d99-home-dot">.</span></a>
          
          <div class="d99-dropdown">
            <a href="/collections/all" class="d99-link-circle d99-dropdown-toggle">
              T-shirts <i class="fas fa-chevron-down d99-arrow"></i>
            </a>
            <div class="d99-dropdown-menu">
              <a href="/collections/all?filter.p.m.custom.type=Oversized">Oversized</a>
              <a href="/collections/all?filter.p.m.custom.type=Premium">Premium</a>
            </div>
          </div>
          
          <a href="/collections/all" class="d99-link-circle">Hoodies</a>
          <a href="/collections/all" class="d99-link-circle">Jeans</a>
        </nav>
        
        <!-- 2. CENTER: Transparent Black Logo -->
        <div class="logo d99-logo-center">
          <a href="/" style="display: inline-block; line-height: 0;">
            <img src="{{ 'd99-logo-header.png' | asset_url }}" alt="DISTRICT-99" class="d99-logo-img">
          </a>
        </div>
        
        <!-- 3. RIGHT SIDE: Cart & Actions -->
        <div class="nav-actions d99-actions-right">
          <a href="/cart" class="d99-cart-icon"><i class="fas fa-shopping-cart"></i></a>
          <a href="/account" class="d99-account-icon"><i class="fas fa-user"></i></a>
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

    # 2. Bespoke custom styling CSS for the header elements
    custom_header_css = """
/* ====================================================
   DISTRICT-99 (D99) - PREMIUM CUSTOM HEADER STYLING
   ==================================================== */
.d99-custom-header {
  background-color: #ffffff !important;
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
  padding: 15px 0 !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 1000 !important;
}

/* Grid Layout: Left (Menu), Center (Logo), Right (Actions) */
.d99-header-grid {
  display: grid !important;
  grid-template-columns: 2fr 1fr 2fr !important;
  align-items: center !important;
  width: 100% !important;
}

/* 1. LEFT SIDE: Navigation Links */
.d99-nav-links {
  display: flex !important;
  align-items: center !important;
  gap: 25px !important;
  justify-content: flex-start !important;
}

/* Home Link: Larger, Bold, with Red Dot */
.d99-link-home {
  font-family: 'Syne', sans-serif !important;
  font-size: 20px !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  text-decoration: none !important;
  color: #000000 !important;
  letter-spacing: -0.01em !important;
  transition: all 0.3s ease !important;
  position: relative !important;
  display: inline-flex !important;
  align-items: center !important;
}

.d99-link-home:hover {
  color: #e50914 !important; /* DISTRICT-99 Red */
  transform: scale(1.05) !important;
}

.d99-home-dot {
  color: #e50914 !important; /* DISTRICT-99 Red */
  font-weight: 900 !important;
  font-size: 24px !important;
  line-height: 0 !important;
  margin-left: 2px !important;
}

/* Circular Links (T-shirts, Hoodies, Jeans) */
.d99-link-circle {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  text-decoration: none !important;
  color: #000000 !important;
  border: 1px solid #000000 !important; /* Thin black circle */
  border-radius: 50px !important;       /* Perfect circle/oval border */
  padding: 8px 18px !important;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
  letter-spacing: 0.05em !important;
}

.d99-link-circle:hover {
  background-color: #000000 !important;
  color: #ffffff !important;
  border-color: #000000 !important;
  transform: translateY(-2px) !important;
}

/* 2. CENTER: Logo Styling */
.d99-logo-center {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}

.d99-logo-img {
  height: 52px !important; /* Perfect luxury height */
  width: auto !important;
  object-fit: contain !important;
  transition: transform 0.3s ease !important;
}

.d99-logo-img:hover {
  transform: scale(1.08) !important; /* Interactive hover */
}

/* 3. RIGHT SIDE: Cart & Actions */
.d99-actions-right {
  display: flex !important;
  gap: 20px !important;
  justify-content: flex-end !important;
  align-items: center !important;
}

.d99-cart-icon, .d99-account-icon {
  font-size: 18px !important;
  color: #000000 !important;
  transition: all 0.3s ease !important;
  text-decoration: none !important;
}

.d99-cart-icon:hover, .d99-account-icon:hover {
  color: #e50914 !important; /* DISTRICT-99 Red */
  transform: scale(1.1) !important;
}

/* Dropdown Hover System (T-shirts Submenu) */
.d99-dropdown {
  position: relative !important;
  display: inline-block !important;
}

.d99-dropdown-menu {
  display: none !important;
  position: absolute !important;
  top: 100% !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  background-color: #ffffff !important;
  box-shadow: 0px 8px 24px rgba(0,0,0,0.1) !important;
  border: 1px solid rgba(0,0,0,0.05) !important;
  padding: 10px 0 !important;
  min-width: 140px !important;
  z-index: 1100 !important;
  border-radius: 0px !important; /* Sharp corners */
  margin-top: 10px !important;
}

.d99-dropdown-menu::before {
  content: '' !important;
  position: absolute !important;
  top: -6px !important;
  left: 50% !important;
  transform: translateX(-50%) rotate(45deg) !important;
  width: 10px !important;
  height: 10px !important;
  background-color: #ffffff !important;
  border-left: 1px solid rgba(0,0,0,0.05) !important;
  border-top: 1px solid rgba(0,0,0,0.05) !important;
}

.d99-dropdown-menu a {
  display: block !important;
  color: #000000 !important;
  padding: 10px 20px !important;
  text-decoration: none !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  text-transform: uppercase !important;
  text-align: center !important;
  transition: all 0.2s ease !important;
}

.d99-dropdown-menu a:hover {
  background-color: #000000 !important;
  color: #ffffff !important;
}

.d99-dropdown:hover .d99-dropdown-menu {
  display: block !important;
}

.d99-dropdown:hover .d99-arrow {
  transform: rotate(180deg) !important;
}

.d99-arrow {
  transition: transform 0.3s ease !important;
  font-size: 10px !important;
}
"""

    # 3. Deploy layout/theme.liquid to Shopify
    print("🔗 Uploading layout/theme.liquid with centered logo and custom menu...")
    urllib.request.urlopen(urllib.request.Request(
        f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json",
        data=json.dumps({"asset": {"key": "layout/theme.liquid", "value": new_theme_liquid}}).encode("utf-8"),
        headers=headers, method="PUT"
    ))
    
    # 4. Fetch the existing theme.css, append our custom header CSS, and save it
    print("🎨 Fetching existing theme.css to append custom header styles...")
    existing_css_url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json?asset[key]=assets/theme.css"
    try:
        with urllib.request.urlopen(urllib.request.Request(existing_css_url, headers=headers, method="GET")) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            existing_css = res_json["asset"]["value"]
    except Exception:
        existing_css = ""
        
    # Append header styles if not already appended
    if "D99 - PREMIUM CUSTOM HEADER" not in existing_css:
        updated_css = existing_css + "\n\n" + custom_header_css
        print("📤 Injecting premium header styles into theme.css...")
        urllib.request.urlopen(urllib.request.Request(
            f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json",
            data=json.dumps({"asset": {"key": "assets/theme.css", "value": updated_css}}).encode("utf-8"),
            headers=headers, method="PUT"
        ))
        print("   ✅ Successfully appended custom header CSS!")
    else:
        print("   🎨 Custom Header CSS already exists, skipped appending.")
        
    print("\n🎉 CUSTOM HEADER IS NOW 100% LIVE ON YOUR SHOPIFY WEBSITE! 🎉")
    print("👉 افتح متجرك المباشر الآن وشاهد الإبداع الخرافي الجديد!")

if __name__ == "__main__":
    deploy_custom_header()
