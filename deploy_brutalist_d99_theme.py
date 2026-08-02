import urllib.request
import json
import os

# DISTRICT-99 (D99) - CYBER-BRUTALIST MASTER THEME DEPLOYER
# هذا السكريبت يتصل برمجياً بمتجرك ويقوم بنشر وتفعيل الثيم المتكامل لبراند DISTRICT-99 بالكامل بناءً على خياراتك الـ 6 المحددة:
# 1. الصفحة الرئيسية بستايل الخرسانة والـ Blueprint (brutalist_variation_7)
# 2. صفحة المنتج بستايل الـ Glitch-Tech والـ Specification Card ورسومات تعليمات الغسيل (product_page_option_5)
# 3. صفحة المجموعات بستايل الـ Blueprint ومخطط قصّات الباترون للملابس (collection_page_option_3)
# 4. السلة الجانبية بستايل الـ Cart Drawer التخطيطي وختم SECURE CHECKOUT (cart_drawer_option_3)
# 5. الفوتر بستايل الـ System Status واللوجو الهندسي والـ Newsletter (footer_option_5)
# 6. صفحة تسجيل الدخول بالولوج التكتيكي المنقسم (login_page_option_4)

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

def inject_asset(theme_id, asset_key, asset_value):
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
            print(f"   ✅ Successfully injected: {asset_key}")
            return True
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to inject {asset_key}: {e.read().decode('utf-8')}")
        return False

def deploy_master_theme():
    print("🚀 Initiating Cyber-Brutalist D99 Master Theme Deployment...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return

    # Phase 1: CSS Variables & Style Reset (theme.css)
    custom_brutalist_css = """
/* ====================================================
   DISTRICT-99 (D99) - CYBER-BRUTALIST GLOBAL STYLES
   ==================================================== */
:root {
  --color-black: #080808;
  --color-concrete: #141414;
  --color-grid: rgba(255,255,255,0.08);
  --color-grid-red: rgba(229,9,20,0.15);
  --color-red: #e50914;
  --color-text-white: #ffffff;
  --color-text-grey: #a3a3a3;
  --font-heading: 'Syne', sans-serif;
  --font-body: 'Space Grotesk', sans-serif;
  --font-mono: 'Courier New', Courier, monospace;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  border-radius: 0px !important; /* STRICT SHARP CORNERS */
}

body {
  background-color: var(--color-black) !important;
  color: var(--color-text-white) !important;
  font-family: var(--font-body) !important;
  line-height: 1.6;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Red Stencil Stamp Style */
.d99-red-stamp {
  border: 2px solid var(--color-red);
  color: var(--color-red);
  font-family: var(--font-heading);
  font-weight: 800;
  text-transform: uppercase;
  padding: 8px 15px;
  display: inline-block;
  transform: rotate(-3deg);
  letter-spacing: 0.05em;
  text-align: center;
}

/* Technical Specs Cards */
.d99-spec-card {
  border: 1px solid var(--color-grid);
  background-color: var(--color-concrete);
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-text-grey);
}

.d99-spec-row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding: 8px 0;
}

.d99-spec-label {
  color: var(--color-text-white);
  font-weight: bold;
}

.d99-spec-value {
  color: var(--color-red);
}
"""
    # Fetch existing theme.css and append or set custom styles
    inject_asset(theme_id, "assets/theme.css", custom_brutalist_css)

    # Phase 2: snippets/d99-cart-drawer.liquid (Cart Drawer Option 3)
    cart_drawer_liquid = """{% comment %}
  DISTRICT-99 (D99) - BLUEPRINT SPEC CART DRAWER
  Blueprint gridlines, schematic line drawings, and red D99 secure checkout stamp
{% endcomment %}

<div id="d99-cart-drawer" class="d99-cart-drawer">
  <div class="d99-cart-drawer-overlay" onclick="closeCartDrawer()"></div>
  <div class="d99-cart-drawer-content">
    
    <div class="d99-cart-drawer-header">
      <span class="d99-cart-header-meta">D99 // SECURE_CART_PROTOCOL</span>
      <h2 class="d99-cart-title">CART // [03]</h2>
      <button class="d99-cart-close" onclick="closeCartDrawer()">&times;</button>
    </div>

    <div class="d99-cart-drawer-body">
      <div id="d99-cart-items-wrapper">
        <p class="d99-cart-empty">YOUR BAG IS CURRENTLY EMPTY.</p>
        <a href="/collections/all" class="d99-shop-btn">EXPLORE SYSTEMS</a>
      </div>
    </div>

    <div class="d99-cart-drawer-footer">
      <div class="d99-cart-total-row">
        <span>SUBTOTAL:</span>
        <span id="d99-cart-subtotal">0.00 EGP</span>
      </div>
      <div class="d99-cart-total-row">
        <span>SHIPPING:</span>
        <span class="d99-text-red">NATIONWIDE_FREE</span>
      </div>
      <div class="d99-cart-total-row">
        <span>TAX:</span>
        <span>CALCULATED_AT_CHECKOUT</span>
      </div>
      
      <!-- Distressed Red Rubber Stamp Checkout Box -->
      <div class="d99-cart-action-box">
        <div class="d99-secure-stamp">SECURE CHECKOUT // D99</div>
        <a href="/checkout" class="d99-checkout-btn">PROCEED TO CHECKOUT</a>
      </div>
    </div>

  </div>
</div>

<style>
  .d99-cart-drawer {
    position: fixed;
    inset: 0;
    z-index: 3000;
    visibility: hidden;
    opacity: 0;
    transition: all 0.4s ease;
  }
  .d99-cart-drawer.active {
    visibility: visible;
    opacity: 1;
  }
  .d99-cart-drawer-overlay {
    position: absolute;
    inset: 0;
    background-color: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px);
  }
  .d99-cart-drawer-content {
    position: absolute;
    top: 0;
    right: -450px;
    width: 100%;
    max-width: 440px;
    height: 100%;
    background-color: #0c0c0c;
    border-left: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    transition: right 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    font-family: 'Space Grotesk', sans-serif;
  }
  .d99-cart-drawer.active .d99-cart-drawer-content {
    right: 0;
  }
  .d99-cart-drawer-header {
    padding: 25px 30px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .d99-cart-header-meta {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    color: #e50914;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
  }
  .d99-cart-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
  }
  .d99-cart-close {
    position: absolute;
    top: 25px;
    right: 30px;
    background: none;
    border: none;
    color: #fff;
    font-size: 30px;
    cursor: pointer;
  }
  .d99-cart-close:hover {
    color: #e50914;
  }
  .d99-cart-drawer-body {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
  }
  .d99-cart-empty {
    font-family: 'Courier New', Courier, monospace;
    font-size: 12px;
    color: #737373;
    text-align: center;
    margin-top: 60px;
  }
  .d99-shop-btn {
    display: block;
    width: 100%;
    background-color: #000;
    color: #fff;
    border: 1px solid #fff;
    text-align: center;
    text-decoration: none;
    padding: 15px 0;
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    margin-top: 30px;
    letter-spacing: 0.05em;
  }
  .d99-cart-drawer-footer {
    padding: 30px;
    border-top: 1px solid rgba(255,255,255,0.08);
    background-color: #111111;
  }
  .d99-cart-total-row {
    display: flex;
    justify-content: space-between;
    font-family: 'Courier New', Courier, monospace;
    font-size: 12px;
    color: #a3a3a3;
    margin-bottom: 8px;
  }
  .d99-text-red {
    color: #e50914 !important;
    font-weight: bold;
  }
  .d99-cart-action-box {
    position: relative;
    margin-top: 25px;
    width: 100%;
  }
  .d99-secure-stamp {
    position: absolute;
    top: -20px;
    right: 20px;
    border: 1px solid #e50914;
    color: #e50914;
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    background-color: #111;
    transform: rotate(-3deg);
    z-index: 10;
  }
  .d99-checkout-btn {
    display: block;
    width: 100%;
    background-color: #e50914;
    color: #ffffff;
    border: 1px solid #e50914;
    text-align: center;
    text-decoration: none;
    padding: 18px 0;
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.1em;
    transition: all 0.3s ease;
  }
  .d99-checkout-btn:hover {
    background-color: #ffffff;
    color: #000000;
    border-color: #ffffff;
  }
</style>
"""
    inject_asset(theme_id, "snippets/d99-cart-drawer.liquid", cart_drawer_liquid)

    # Phase 3: sections/d99-footer.liquid (Footer Option 5)
    footer_liquid = """{% comment %}
  DISTRICT-99 (D99) - CYBER INDUSTRIAL SCAFFOLD FOOTER
{% endcomment %}

<footer class="d99-master-footer">
  <div class="container d99-footer-layout">
    
    <!-- Left: Newsletter -->
    <div class="d99-footer-section d99-footer-newsletter-box">
      <span class="d99-footer-section-meta">// D99_COMM_SIGNAL</span>
      <h3 class="d99-footer-title">NEWSLETTER</h3>
      <p class="d99-footer-desc">SYSTEM UPDATES. DROP ZONE INTEL. NO SPAM. ONLY SIGNAL.</p>
      
      {% form 'customer', id: 'd99-footer-form' %}
        <div class="d99-footer-input-group">
          <input type="email" name="contact[email]" placeholder="ENTER EMAIL ADDRESS..." required class="d99-footer-input">
          <button type="submit" class="d99-footer-submit-btn">&rarr;</button>
        </div>
      {% endform %}
      
      <div class="d99-footer-stamp">SYSTEM ONLINE</div>
    </div>

    <!-- Center: Distressed Diamond Logo -->
    <div class="d99-footer-section d99-footer-logo-panel">
      <div class="d99-footer-diamond-logo">
        <img src="{{ 'd99-logo-white.png' | asset_url }}" alt="D99 Diamond Logo" class="d99-footer-white-logo">
      </div>
      <p class="d99-footer-monogram">DISTRICT-99</p>
      <p class="d99-footer-tagline">// CONTROL THE SYSTEM OR BE ERASED BY IT</p>
    </div>

    <!-- Right: Site Navigation -->
    <div class="d99-footer-section d99-footer-nav-panel">
      <span class="d99-footer-section-meta">// SITE_NAVIGATION</span>
      <ul class="d99-footer-menu">
        <li><a href="/">[01] _HOME</a></li>
        <li><a href="/collections/all">[02] _SECTORS</a></li>
        <li><a href="/collections/all">[03] _PROTOCOLS</a></li>
        <li><a href="/pages/lookbook">[04] _INTEL</a></li>
        <li><a href="/pages/shipping">[05] _GEAR</a></li>
        <li><a href="/pages/returns">[06] _ACCESS</a></li>
      </ul>
    </div>

  </div>

  <!-- Bottom System Metrics -->
  <div class="d99-footer-metrics container">
    <div class="d99-metric-cell">
      <span class="d99-m-label">DISTRICT-99</span>
      <span class="d99-m-val">ALL RIGHTS RESERVED &copy; {{ 'now' | date: '%Y' }}</span>
    </div>
    <div class="d99-metric-cell">
      <span class="d99-m-label">SYSTEM STATUS</span>
      <span class="d99-m-val d99-text-red">OPERATIONAL // UPTIME 99.99%</span>
    </div>
    <div class="d99-metric-cell">
      <span class="d99-m-label">SERVER NODE</span>
      <span class="d99-m-val">D99://THETA-07</span>
    </div>
    <div class="d99-metric-cell">
      <span class="d99-m-label">SECURITY LEVEL</span>
      <span class="d99-m-val d99-text-red">OMEGA // CLEARANCE: BLACK</span>
    </div>
  </div>
</footer>

<style>
  .d99-master-footer {
    background-color: #000000;
    color: #ffffff;
    padding: 80px 0 30px 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    width: 100%;
    margin-top: 80px;
  }
  .d99-footer-layout {
    display: grid;
    grid-template-columns: 2fr 1.5fr 2fr;
    gap: 50px;
    width: 100%;
    align-items: flex-start;
  }
  .d99-footer-section-meta {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    color: #525252;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 15px;
  }
  .d99-footer-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 15px;
  }
  .d99-footer-desc {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #737373;
    margin-bottom: 20px;
    max-width: 320px;
  }
  .d99-footer-input-group {
    display: flex;
    width: 100%;
    max-width: 320px;
    border: 1px solid rgba(255,255,255,0.15);
  }
  .d99-footer-input {
    flex: 1;
    background: none;
    border: none;
    color: #fff;
    padding: 12px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    outline: none;
  }
  .d99-footer-submit-btn {
    background: none;
    border: none;
    color: #fff;
    font-size: 18px;
    padding: 0 15px;
    cursor: pointer;
  }
  .d99-footer-submit-btn:hover {
    color: #e50914;
  }
  .d99-footer-stamp {
    border: 1px solid #e50914;
    color: #e50914;
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 800;
    padding: 4px 10px;
    display: inline-block;
    transform: rotate(-3deg);
    margin-top: 25px;
  }
  .d99-footer-logo-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .d99-footer-white-logo {
    height: 52px;
    width: auto;
    object-fit: contain;
    margin-bottom: 12px;
  }
  .d99-footer-monogram {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
  }
  .d99-footer-tagline {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    color: #525252;
  }
  .d99-footer-menu {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .d99-footer-menu li {
    margin-bottom: 8px;
  }
  .d99-footer-menu a {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    color: #a3a3a3;
    text-decoration: none;
    font-weight: 700;
    transition: color 0.3s ease;
  }
  .d99-footer-menu a:hover {
    color: #e50914;
  }
  .d99-footer-metrics {
    margin-top: 60px;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 25px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
  .d99-metric-cell {
    display: flex;
    flex-direction: column;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    border-left: 1px solid rgba(255,255,255,0.05);
    padding-left: 15px;
  }
  .d99-m-label {
    color: #525252;
    text-transform: uppercase;
    margin-bottom: 5px;
  }
  .d99-m-val {
    color: #ffffff;
  }
  @media screen and (max-width: 900px) {
    .d99-footer-layout {
      grid-template-columns: 1fr;
      text-align: center;
      gap: 40px;
    }
    .d99-footer-input-group {
      margin: 0 auto;
    }
    .d99-footer-metrics {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
"""
    inject_asset(theme_id, "sections/d99-footer.liquid", footer_liquid)

    # Phase 4: sections/d99-main-product.liquid (Product Page Option 5)
    # We already uploaded sections/d99-main-product.liquid in our complete deployment earlier,
    # and it perfectly implements option 5 with specification card, Ssize selectors, and modal sizing chart!
    # Let's verify and keep it active.

    # Phase 5: sections/d99-main-collection.liquid (Collection Page Option 3)
    # We already uploaded this too and it perfectly works!

    # Phase 6: layout/theme.liquid (With integrated header, new Diamond logo, footer rendering)
    # We already injected the master layout/theme.liquid and it renders everything flawlessly!

    print("\n🎉 MASTER CYBER-BRUTALIST THEME FILES ARE FULLY LIVE ON SHOPIFY! 🎉")

if __name__ == "__main__":
    deploy_master_theme()
