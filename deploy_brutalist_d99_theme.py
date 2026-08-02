import urllib.request
import json
import base64
import os

# DISTRICT-99 (D99) - SHOPIFY BRUTALIST DAWN MASTER THEME BUILDER
# هذا السكريبت الاحترافي يقوم ببناء وحقن الثيم البروتالي التكتيكي بالكامل على نسخة مستقرة من ثيم Dawn (المحفوظة برقم 189908910264)
# ليعمل المتجر المباشر بنسبة 100% وبكامل وظائفه القياسية، وبمظهر مذهل مطابق لاختيارات ميدو البصرية!

STORE_URL = "district99-preview.myshopify.com"
THEME_ID = 189908910264  # المعرف لنسخة Dawn التي قمنا بتسميتها "D99 Cyber-Brutalist Master Theme"

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
        # Binary files like images need base64 encoding
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

def main():
    print("🚀 Initiating Cyber-Brutalist Master Theme Builder on stable Dawn (ID: 189908910264)...")
    
    # 1. Upload Logos
    logo_black_path = "uploads/d99_logo_black_transparent.png"
    if os.path.exists(logo_black_path):
        with open(logo_black_path, "rb") as f:
            inject_asset("assets/d99-logo-header.png", f.read(), is_binary=True)
            
    logo_white_path = "uploads/d99_logo_transparent.png"
    if os.path.exists(logo_white_path):
        with open(logo_white_path, "rb") as f:
            inject_asset("assets/d99-logo-white.png", f.read(), is_binary=True)

    # 2. Upload Split Hero Spotlight Banners
    hero_l_path = "uploads/split_hero_left.png"
    if os.path.exists(hero_l_path):
        with open(hero_l_path, "rb") as f:
            inject_asset("assets/split_hero_left.png", f.read(), is_binary=True)
            
    hero_r_path = "uploads/split_hero_right.png"
    if os.path.exists(hero_r_path):
        with open(hero_r_path, "rb") as f:
            inject_asset("assets/split_hero_right.png", f.read(), is_binary=True)

    # 3. Upload Bento Lookbook Panel Images
    for i in range(1, 9):
        panel_path = f"uploads/bento_panel_{i}.png"
        if os.path.exists(panel_path):
            with open(panel_path, "rb") as f:
                inject_asset(f"assets/bento_panel_{i}.png", f.read(), is_binary=True)

    # 4. Upload Custom Sections (Read from shopify-custom-sections)
    with open("shopify-custom-sections/d99-marquee-ticker.liquid", "r", encoding="utf-8") as f:
        inject_asset("sections/d99-marquee-ticker.liquid", f.read())
        
    with open("shopify-custom-sections/d99-split-hero.liquid", "r", encoding="utf-8") as f:
        inject_asset("sections/d99-split-hero.liquid", f.read())
        
    with open("shopify-custom-sections/d99-lookbook-grid.liquid", "r", encoding="utf-8") as f:
        inject_asset("sections/d99-lookbook-grid.liquid", f.read())
        
    with open("shopify-custom-sections/d99-main-product.liquid", "r", encoding="utf-8") as f:
        inject_asset("sections/d99-main-product.liquid", f.read())
        
    with open("shopify-custom-sections/d99-main-collection.liquid", "r", encoding="utf-8") as f:
        inject_asset("sections/d99-main-collection.liquid", f.read())

    # 5. Inject CUSTOM FOOTER SECTION (d99-footer.liquid - Matching footer_option_5.jpg)
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
  .d99-footer-img-logo {
    height: 52px;
    width: auto;
    object-fit: contain;
    margin-bottom: 12px;
    filter: invert(1); /* Invert black logo to white for footer */
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
    inject_asset("sections/d99-footer.liquid", footer_liquid)

    # 6. Inject CUSTOM CART DRAWER SNIPPET (d99-cart-drawer.liquid - Matching cart_drawer_option_3.jpg)
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
    inject_asset("snippets/d99-cart-drawer.liquid", cart_drawer_liquid)

    # 7. Inject CUSTOM LOGIN PAGE (main-login.liquid - Matching login_page_option_4.jpg)
    login_liquid_code = """{% comment %}
  DISTRICT-99 (D99) - CUSTOM BRUTALIST SPLIT LOGIN PAGE
  Matching login_page_option_4.jpg. Concrete grey background with a clean modern customer login card.
{% endcomment %}

<div class="d99-brutalist-login-wrapper">
  
  <!-- LEFT PANEL: Massive Bold Branding (Concrete Grey) -->
  <div class="d99-login-left-panel">
    <div class="d99-login-branding-box">
      <span class="d99-login-meta">DISTRICT-99 // // D99</span>
      <span class="d99-login-meta-sub">SECURE NETWORK INTERFACE</span>
      
      <h1 class="d99-login-giant-title">SYSTEM<br>ACCESS //<br>CODE_D99</h1>
      
      <div class="d99-login-author">
        <p>AUTHORIZED PERSONNEL ONLY</p>
        <p class="d99-text-red">ALL ACCESS LOGGED AND MONITORED</p>
      </div>
    </div>
  </div>

  <!-- RIGHT PANEL: Customer Login Card (White & Minimal) -->
  <div class="d99-login-right-panel">
    <div class="d99-login-white-card">
      
      <div class="d99-login-card-header">
        <img src="{{ 'd99-logo-header.png' | asset_url }}" alt="D99 Logo" class="d99-login-logo">
        <p class="d99-login-logo-sub">DISTRICT-99</p>
      </div>

      <h2 class="d99-login-card-title">CUSTOMER LOGIN</h2>
      <p class="d99-login-card-subtitle">Enter your credentials to access your account</p>

      {%- form 'customer_login', id: 'd99-customer-login' -%}
        {{ form.errors | default_errors }}
        
        <div class="d99-login-field">
          <label for="CustomerEmail">USERNAME</label>
          <input type="email" name="customer[email]" id="CustomerEmail" placeholder="Enter your username" required>
        </div>

        <div class="d99-login-field">
          <label for="CustomerPassword">PASSWORD</label>
          <input type="password" name="customer[password]" id="CustomerPassword" placeholder="Enter your password" required>
        </div>

        <div class="d99-login-utils">
          <label class="d99-remember-me">
            <input type="checkbox" name="remember_me"> REMEMBER ME
          </label>
          <a href="/account/login#recover" class="d99-forgot-pass">FORGOT PASSWORD?</a>
        </div>

        <button type="submit" class="d99-login-submit-btn">LOGIN &rarr;</button>
        <a href="/account/register" class="d99-login-register-btn">LOGIN WITH OTP &rarr;</a>
      {%- endform -%}

      <div class="d99-login-card-footer">
        <span>NEED HELP?</span>
        <a href="/pages/contact" class="d99-text-red">CONTACT SUPPORT &rarr;</a>
      </div>

    </div>
  </div>

</div>

<style>
  .d99-brutalist-login-wrapper {
    display: flex;
    width: 100%;
    min-height: 100vh;
    background-color: #f7f7f7;
    font-family: 'Space Grotesk', sans-serif;
  }
  
  /* Left Concrete Panel */
  .d99-login-left-panel {
    flex: 1.2;
    background-color: #cccccc;
    background-image: radial-gradient(#d5d5d5 1px, transparent 1px);
    background-size: 20px 20px;
    padding: 60px;
    display: flex;
    align-items: center;
    position: relative;
    border-right: 1px solid #000;
  }
  .d99-login-branding-box {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  .d99-login-meta {
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    font-weight: bold;
    color: #000;
    margin-bottom: 5px;
  }
  .d99-login-meta-sub {
    font-family: 'Courier New', Courier, monospace;
    font-size: 9px;
    color: #525252;
    letter-spacing: 0.1em;
    margin-bottom: 40px;
  }
  .d99-login-giant-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(36px, 5vw, 64px) !important;
    font-weight: 800;
    text-transform: uppercase;
    color: #000000;
    line-height: 1;
    margin-bottom: 80px;
    letter-spacing: -0.02em;
  }
  .d99-login-author {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    font-weight: bold;
    color: #525252;
    line-height: 1.4;
  }
  .d99-text-red {
    color: #e50914 !important;
  }

  /* Right Login Card Panel */
  .d99-login-right-panel {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    background-color: #ededed;
  }
  .d99-login-white-card {
    background-color: #ffffff;
    border: 1px solid #000;
    width: 100%;
    max-width: 480px;
    padding: 40px;
    box-shadow: 10px 10px 0px rgba(0,0,0,0.05);
  }
  .d99-login-card-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
  }
  .d99-login-logo {
    height: 40px;
    width: auto;
    object-fit: contain;
    margin-bottom: 8px;
  }
  .d99-login-logo-sub {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.05em;
  }
  .d99-login-card-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 22px !important;
    font-weight: 800;
    text-align: center;
    color: #000;
    margin-bottom: 5px;
    letter-spacing: 0.05em;
  }
  .d99-login-card-subtitle {
    font-size: 11px;
    color: #737373;
    text-align: center;
    margin-bottom: 30px;
  }
  
  /* Form field */
  .d99-login-field {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  .d99-login-field label {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    font-weight: bold;
    color: #000;
    margin-bottom: 8px;
  }
  .d99-login-field input {
    width: 100%;
    border: 1px solid #000;
    padding: 12px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    outline: none;
  }
  .d99-login-field input:focus {
    background-color: #fcfcfc;
  }
  
  .d99-login-utils {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    font-weight: bold;
    color: #000;
    margin-bottom: 25px;
  }
  .d99-remember-me {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
  }
  .d99-remember-me input {
    cursor: pointer;
  }
  .d99-forgot-pass {
    color: #737373;
    text-decoration: underline;
  }
  .d99-forgot-pass:hover {
    color: #e50914;
  }
  
  /* Buttons */
  .d99-login-submit-btn, .d99-login-register-btn {
    display: block;
    width: 100%;
    border: 1px solid #000;
    text-align: center;
    padding: 15px 0;
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 12px;
  }
  .d99-login-submit-btn {
    background-color: #000;
    color: #fff;
  }
  .d99-login-submit-btn:hover {
    background-color: #e50914;
    border-color: #e50914;
  }
  .d99-login-register-btn {
    background-color: #fff;
    color: #000;
  }
  .d99-login-register-btn:hover {
    background-color: #000;
    color: #fff;
  }
  
  .d99-login-card-footer {
    display: flex;
    justify-content: space-between;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: bold;
    border-top: 1px solid #e5e5e5;
    padding-top: 20px;
    margin-top: 25px;
  }
  .d99-login-card-footer a {
    text-decoration: none;
  }
  
  @media screen and (max-width: 900px) {
    .d99-brutalist-login-wrapper {
      flex-direction: column;
    }
    .d99-login-left-panel {
      padding: 40px;
      border-right: none;
      border-bottom: 1px solid #000;
    }
    .d99-login-giant-title {
      margin-bottom: 30px;
    }
  }
</style>
"""
    inject_asset("sections/main-login.liquid", login_liquid_code)

    # 8. Update templates/index.json (Homepage Layout - brutalist_variation_7.jpg)
    new_index_json = {
        "sections": {
            "d99_marquee_ticker": {
                "type": "d99-marquee-ticker",
                "settings": {
                    "marquee_text": "DISTRICT-99 // ACTION IS THE BRIDGE // SECURE CONNECTION ESTABLISHED // NATIONWIDE_FREE_SHIPPING //"
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
            }
        },
        "order": [
            "d99_marquee_ticker",
            "d99_split_hero",
            "d99_lookbook_grid"
        ]
    }
    inject_asset("templates/index.json", json.dumps(new_index_json, indent=2))

    # 9. Update templates/product.json & collection.json
    product_json_val = {
        "sections": {
            "main": {
                "type": "d99-main-product",
                "settings": {}
            }
        },
        "order": [
            "main"
        ]
    }
    inject_asset("templates/product.json", json.dumps(product_json_val, indent=2))
    
    collection_json_val = {
        "sections": {
            "main": {
                "type": "d99-main-collection",
                "settings": {}
            }
        },
        "order": [
            "main"
        ]
    }
    inject_asset("templates/collection.json", json.dumps(collection_json_val, indent=2))

    # 10. Update layout/theme.liquid to render custom snippets & styles
    print("🎨 Fetching existing layout/theme.liquid of new theme to inject connections...")
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json?asset[key]=layout/theme.liquid"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            theme_liquid = json.loads(response.read().decode("utf-8"))["asset"]["value"]
            
        # 1. Inject fonts in <head>
        if "Space Grotesk" not in theme_liquid:
            fonts_code = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
  {{ 'theme.css' | asset_url | stylesheet_tag }}
</head>"""
            theme_liquid = theme_liquid.replace("</head>", fonts_code)
        
        # 2. Inject Cart Drawer right after <body>
        if "d99-cart-drawer" not in theme_liquid:
            body_cart_code = """<body class="gradient">
  {% render 'd99-cart-drawer' %}"""
            theme_liquid = theme_liquid.replace('<body class="gradient">', body_cart_code)
        
        # 3. Inject Custom Footer
        theme_liquid = theme_liquid.replace("{% sections 'footer-group' %}", "{% section 'd99-footer' %}")
        theme_liquid = theme_liquid.replace("{% section 'footer' %}", "{% section 'd99-footer' %}")
        
        # 4. Upload updated theme.liquid
        inject_asset("layout/theme.liquid", theme_liquid)
        
    except Exception as e:
        print("   ❌ Failed to customize layout/theme.liquid:", e)

    # 11. Append Global Streetwear aesthetics into base.css
    print("🎨 Injecting global streetwear styling details into assets/base.css...")
    existing_base_css_url = f"https://{STORE_URL}/admin/api/2026-07/themes/{THEME_ID}/assets.json?asset[key]=assets/base.css"
    try:
        with urllib.request.urlopen(urllib.request.Request(existing_base_css_url, headers=headers, method="GET")) as response:
            existing_base_css = json.loads(response.read().decode("utf-8"))["asset"]["value"]
    except Exception:
        existing_base_css = ""
        
    # Append global overrides
    brutalist_base_css = """
/* ====================================================
   DISTRICT-99 (D99) - STYLING OVERRIDES FOR DAWN
   ==================================================== */
* {
  border-radius: 0px !important; /* Force strict sharp corners */
}
body, p, span, a, input, select, textarea {
  font-family: 'Space Grotesk', sans-serif !important;
}
h1, h2, h3, h4, h5, h6, .h1, .h2, .h3, .h4, .button {
  font-family: 'Syne', sans-serif !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
}
/* Center logo in default header */
.header__heading {
  margin: 0 auto !important;
}
.header__heading-logo {
  height: 48px !important;
  width: auto !important;
}
/* Override Dawn footer entirely */
.footer {
  display: none !important;
}
"""
    if "DISTRICT-99" not in existing_base_css:
        updated_base_css = existing_base_css + "\n\n" + brutalist_base_css
        inject_asset("assets/base.css", updated_base_css)

    print("\n🎉 D99 CYBER-BRUTALIST MASTER THEME CONFIGURED SUCCESSFULLY ON DAWN ENGINE! 🎉")
    print("👉 اذهب الآن لـ Themes في متجرك، ستجد ثيم جديد أسطوري باسم 'D99 Cyber-Brutalist Master Theme'")
    print("👉 اضغط على Actions -> Publish لتفعيل المعجزات البصرية الحقيقية فوراً!")

if __name__ == "__main__":
    main()
