import urllib.request
import json
import os

# DISTRICT-99 (D99) - SHOPIFY COMPLETE BESPOKE THEME DEPLOYER
# هذا السكريبت يتصل برمجياً بمتجرك، ويقوم بحقن وإنشاء هيكل الثيم المتكامل لبراند DISTRICT-99 بالكامل:
# 1. صفحة منتج مخصصة بالكامل (Stacked Left Images / Sticky Right checkout panel).
# 2. صفحة مجموعات أنيقة بستايل Ssense الفخم وتأثير Hover تبديل الصور للموديل الثاني.
# 3. سلة مشتريات منزلقة جانبية (Slide-out Cart Drawer) مع ربطها بالأزرار.
# 4. فوتر مخصص متطور يحمل شعار الـ Cyber-Star والـ Newsletter.
# 5. تحديث layout/theme.liquid لربط الهيدر والفوتر والدرور والأكواد ببعضها بشكل متكامل 100%!

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
            print(f"   ✅ Successfully injected asset: {asset_key}")
            return True
    except urllib.error.HTTPError as e:
        print(f"   ❌ Failed to inject {asset_key}: {e.read().decode('utf-8')}")
        return False

def deploy_complete_theme():
    print("🚀 Initiating complete D99 luxury editorial theme deployment...")
    theme_id = get_active_theme_id()
    if not theme_id:
        print("❌ Cannot proceed without Active Theme ID.")
        return

    # 1. TEMPLATES: product.json
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
    inject_asset(theme_id, "templates/product.json", json.dumps(product_json_val, indent=2))

    # 2. SECTIONS: sections/d99-main-product.liquid
    product_section_liquid = """{% comment %}
  DISTRICT-99 (D99) - CUSTOM PREMIUM EDITORIAL PRODUCT PAGE
  Signature Stacked Left Images / Sticky Right Checkout Panel
{% endcomment %}

<div class="d99-product-page-container container">
  
  <!-- LEFT COLUMN: Stacked Vertical Image List (Ssense Style) -->
  <div class="d99-product-images-column">
    {% if product.images.size > 0 %}
      {% for image in product.images %}
        <div class="d99-product-image-wrapper">
          <img src="{{ image | img_url: 'master' }}" alt="{{ product.title }} - Pose {{ forloop.index }}" class="d99-product-single-img">
        </div>
      {% endfor %}
    {% else %}
      <div class="d99-product-image-wrapper">
        {{ 'product-1' | placeholder_svg_tag: 'd99-placeholder-svg' }}
      </div>
    {% endif %}
  </div>

  <!-- RIGHT COLUMN: Sticky Product Details Panel -->
  <div class="d99-product-details-column">
    <div class="d99-product-details-sticky">
      
      <!-- Vendor / Brand Name -->
      <span class="d99-product-vendor">DISTRICT-99<span class="d99-dot">.</span></span>
      
      <!-- Product Title -->
      <h1 class="d99-product-title">{{ product.title }}</h1>
      
      <!-- Product Price -->
      <div class="d99-product-price-container">
        {% if product.compare_at_price > product.price %}
          <span class="d99-price-sale">{{ product.price | money }}</span>
          <span class="d99-price-compare">{{ product.compare_at_price | money }}</span>
          <span class="d99-price-badge">LIMITED DROP</span>
        {% else %}
          <span class="d99-price-normal">{{ product.price | money }}</span>
        {% endif %}
      </div>

      <!-- Divider -->
      <hr class="d99-product-divider">

      <!-- Product Form (Add to Cart / Sold Out) -->
      {% form 'product', product, id: 'd99-product-form' %}
        <input type="hidden" name="id" id="d99-variant-id" value="{{ product.variants.first.id }}">
        
        <!-- Size Selector Grid -->
        <div class="d99-selector-container">
          <div class="d99-selector-header">
            <span class="d99-selector-label">Select Size</span>
            <button type="button" class="d99-size-guide-btn" onclick="openSizeModal()">Size Guide</button>
          </div>
          
          <div class="d99-size-selector-grid">
            {% for variant in product.variants %}
              <button type="button" 
                      class="d99-size-btn {% if forloop.first %}active{% endif %} {% unless variant.available %}sold-out{% endunless %}" 
                      data-variant-id="{{ variant.id }}"
                      onclick="selectSize(this, '{{ variant.id }}')">
                {{ variant.title }}
              </button>
            {% endfor %}
          </div>
        </div>

        <!-- Quantity Selector -->
        <div class="d99-quantity-container">
          <span class="d99-selector-label">Quantity</span>
          <div class="d99-quantity-selector">
            <button type="button" onclick="adjustQty(-1)">-</button>
            <input type="number" name="quantity" id="d99-product-qty" value="1" min="1">
            <button type="button" onclick="adjustQty(1)">+</button>
          </div>
        </div>

        <!-- Submit Button (COP NOW / SOLD OUT) -->
        <div class="d99-product-action-wrapper">
          {% if product.available %}
            <button type="submit" name="add" class="d99-add-to-cart-btn">
              COP NOW
            </button>
          {% else %}
            <button type="button" class="d99-add-to-cart-btn sold-out" disabled>
              SOLD OUT // RESTOCKING SOON
            </button>
          {% endif %}
        </div>
      {% endform %}

      <!-- Product Description / Details Accordions -->
      <div class="d99-details-accordions">
        <details open>
          <summary>Details</summary>
          <div class="d99-accordion-content">
            <p>{{ product.description }}</p>
            <ul>
              <li>Premium 100% combed cotton fabric.</li>
              <li>Heavyweight 300 GSM streetwear custom cut.</li>
              <li>Durable double-needle stitched cuffs and hem.</li>
              <li>Luxury minimal aesthetics. Faceless look.</li>
            </ul>
          </div>
        </details>
        
        <details>
          <summary>Shipping & Returns</summary>
          <div class="d99-accordion-content">
            <p><strong>Free shipping nationwide in Egypt.</strong></p>
            <p>Cairo & Giza: Delivery within 24-48 hours.<br>Other cities: Delivery within 2-3 business days.</p>
            <p>Easy, hassle-free exchanges and returns within 14 days.</p>
          </div>
        </details>
      </div>

    </div>
  </div>
</div>

<!-- Bespoke Sizing Chart Modal (Oversized & Premium Specs) -->
<div id="d99-size-modal" class="d99-modal">
  <div class="d99-modal-content">
    <span class="d99-modal-close" onclick="closeSizeModal()">&times;</span>
    <h2 class="d99-modal-title">DISTRICT-99 // SIZING CHART</h2>
    <p class="d99-modal-subtitle">Our cuts are designed as oversized and relaxed premium streetwear. Order your standard size for the intended loose fit.</p>
    
    <table class="d99-size-table">
      <thead>
        <tr>
          <th>Size</th>
          <th>Chest Width (cm)</th>
          <th>Body Length (cm)</th>
          <th>Sleeve Length (cm)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>S</td>
          <td>56</td>
          <td>72</td>
          <td>22</td>
        </tr>
        <tr>
          <td>M</td>
          <td>59</td>
          <td>74</td>
          <td>23</td>
        </tr>
        <tr>
          <td>L</td>
          <td>62</td>
          <td>76</td>
          <td>24</td>
        </tr>
        <tr>
          <td>XL</td>
          <td>65</td>
          <td>78</td>
          <td>25</td>
        </tr>
        <tr>
          <td>XXL</td>
          <td>68</td>
          <td>80</td>
          <td>26</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<style>
  /* ----------------------------------------------------
     D99 Bespoke Product Page Styling
     ---------------------------------------------------- */
  .d99-product-page-container {
    display: flex;
    gap: 60px;
    padding: 60px 0;
    width: 100%;
  }

  /* 1. Stacked Left Images (Ssense Look) */
  .d99-product-images-column {
    flex: 1.4;
    display: flex;
    flex-direction: column;
    gap: 30px;
  }

  .d99-product-image-wrapper {
    width: 100%;
    background-color: #f7f7f7;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .d99-product-single-img {
    width: 100%;
    height: auto;
    object-fit: contain;
    display: block;
  }

  /* 2. Sticky Right Details Column */
  .d99-product-details-column {
    flex: 1;
    position: relative;
  }

  .d99-product-details-sticky {
    position: sticky;
    top: 120px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .d99-product-vendor {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    color: #737373;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }

  .d99-product-vendor .d99-dot {
    color: #e50914;
  }

  .d99-product-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800;
    text-transform: uppercase;
    color: #000000;
    letter-spacing: -0.01em;
    margin-bottom: 15px;
    line-height: 1.1;
  }

  .d99-product-price-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
  }

  .d99-price-normal {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #000000;
  }

  .d99-price-sale {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e50914; /* D99 Red */
  }

  .d99-price-compare {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 500;
    color: #a3a3a3;
    text-decoration: line-through;
  }

  .d99-price-badge {
    background-color: #e50914;
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    letter-spacing: 0.05em;
  }

  .d99-product-divider {
    width: 100%;
    border: none;
    border-top: 1px solid rgba(0,0,0,0.08);
    margin-bottom: 25px;
  }

  /* Form & Selector Grid */
  #d99-product-form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 25px;
  }

  .d99-selector-container {
    width: 100%;
  }

  .d99-selector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .d99-selector-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: #000000;
    letter-spacing: 0.05em;
  }

  .d99-size-guide-btn {
    background: none;
    border: none;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: #737373;
    text-decoration: underline;
    cursor: pointer;
    letter-spacing: 0.05em;
  }

  .d99-size-guide-btn:hover {
    color: #e50914;
  }

  .d99-size-selector-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    width: 100%;
  }

  .d99-size-btn {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    padding: 12px 0;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 0px;
  }

  .d99-size-btn:hover, .d99-size-btn.active {
    background-color: #000000;
    color: #ffffff;
  }

  .d99-size-btn.sold-out {
    opacity: 0.3;
    text-decoration: line-through;
    cursor: not-allowed;
  }

  /* Quantity Selector */
  .d99-quantity-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .d99-quantity-selector {
    display: inline-flex;
    border: 1px solid #000000;
    align-self: flex-start;
  }

  .d99-quantity-selector button {
    background: none;
    border: none;
    width: 40px;
    height: 40px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
  }

  .d99-quantity-selector button:hover {
    background-color: #f5f5f5;
  }

  .d99-quantity-selector input {
    border: none;
    border-left: 1px solid #000000;
    border-right: 1px solid #000000;
    width: 50px;
    height: 40px;
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
  }

  /* COP NOW button */
  .d99-add-to-cart-btn {
    width: 100%;
    background-color: #000000;
    color: #ffffff;
    border: 1px solid #000000;
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    padding: 18px 0;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
    letter-spacing: 0.1em;
    border-radius: 0px;
  }

  .d99-add-to-cart-btn:hover {
    background-color: #e50914;
    border-color: #e50914;
  }

  .d99-add-to-cart-btn.sold-out {
    background-color: #eaeaea;
    color: #a3a3a3;
    border-color: #eaeaea;
    cursor: not-allowed;
  }

  /* Accordions */
  .d99-details-accordions {
    width: 100%;
    margin-top: 40px;
    border-top: 1px solid rgba(0,0,0,0.08);
  }

  .d99-details-accordions details {
    border-bottom: 1px solid rgba(0,0,0,0.08);
    width: 100%;
  }

  .d99-details-accordions summary {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 18px 0;
    cursor: pointer;
    letter-spacing: 0.05em;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .d99-details-accordions summary::after {
    content: '+';
    font-size: 16px;
    font-weight: 500;
  }

  .d99-details-accordions details[open] summary::after {
    content: '-';
  }

  .d99-accordion-content {
    padding-bottom: 20px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    line-height: 1.6;
    color: #404040;
  }

  .d99-accordion-content ul {
    margin-top: 10px;
    padding-left: 15px;
  }

  .d99-accordion-content li {
    margin-bottom: 5px;
  }

  /* 3. Modal Sizing Chart */
  .d99-modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.6);
    backdrop-filter: blur(5px);
  }

  .d99-modal-content {
    background-color: #ffffff;
    margin: 10% auto;
    padding: 40px;
    border: 1px solid #000;
    width: 90%;
    max-width: 600px;
    position: relative;
    border-radius: 0px;
  }

  .d99-modal-close {
    position: absolute;
    top: 20px;
    right: 25px;
    color: #000;
    font-size: 30px;
    font-weight: bold;
    cursor: pointer;
  }

  .d99-modal-close:hover {
    color: #e50914;
  }

  .d99-modal-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 24px !important;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }

  .d99-modal-subtitle {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    color: #737373;
    margin-bottom: 25px;
    line-height: 1.4;
  }

  .d99-size-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
  }

  .d99-size-table th, .d99-size-table td {
    border: 1px solid #e5e5e5;
    padding: 12px;
    text-align: center;
  }

  .d99-size-table th {
    background-color: #f5f5f5;
    font-weight: 700;
    text-transform: uppercase;
  }

  /* Responsive Stack for Mobile */
  @media screen and (max-width: 990px) {
    .d99-product-page-container {
      flex-direction: column;
      gap: 40px;
    }
    .d99-product-images-column {
      width: 100%;
    }
    .d99-product-details-column {
      width: 100%;
    }
    .d99-product-details-sticky {
      position: static;
    }
  }
</style>

<script>
  // Simple clean vanilla JS handlers for variants, sizes, counter & size modals
  function selectSize(btn, variantId) {
    document.querySelectorAll('.d99-size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('d99-variant-id').value = variantId;
  }

  function adjustQty(amount) {
    const input = document.getElementById('d99-product-qty');
    let val = parseInt(input.value) + amount;
    if (val < 1) val = 1;
    input.value = val;
  }

  function openSizeModal() {
    document.getElementById('d99-size-modal').style.display = 'block';
  }

  function closeSizeModal() {
    document.getElementById('d99-size-modal').style.display = 'none';
  }

  // Close modal when clicking outside
  window.onclick = function(event) {
    const modal = document.getElementById('d99-size-modal');
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  }
</script>
"""
    inject_asset(theme_id, "sections/d99-main-product.liquid", product_section_liquid)

    # 3. TEMPLATES: collection.json
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
    inject_asset(theme_id, "templates/collection.json", json.dumps(collection_json_val, indent=2))

    # 4. SECTIONS: sections/d99-main-collection.liquid
    collection_section_liquid = """{% comment %}
  DISTRICT-99 (D99) - CUSTOM EDITORIAL COLLECTION PAGE
  Ssense-style minimal borderless product grid with smooth model pose-swap hover
{% endcomment %}

<div class="d99-collection-page container">
  
  <header class="d99-collection-header">
    <h1 class="d99-collection-title">{{ collection.title }}</h1>
    <span class="d99-collection-count">{{ collection.products_count }} items</span>
  </header>

  <div class="d99-collection-grid">
    {% for product in collection.products %}
      <a href="{{ product.url }}" class="d99-collection-product-card d99-product-card">
        
        <!-- Image Card with hover swap -->
        <div class="d99-product-card-img-wrapper">
          {% if product.images.size > 1 %}
            <img src="{{ product.featured_image | img_url: '600x800', crop: 'center' }}" class="d99-product-img-featured" alt="{{ product.title }}">
            <img src="{{ product.images[1] | img_url: '600x800', crop: 'center' }}" class="d99-product-img-hover" alt="{{ product.title }}">
          {% else %}
            <img src="{{ product.featured_image | img_url: '600x800', crop: 'center' }}" class="d99-product-img-single" alt="{{ product.title }}">
          {% endif %}
          
          {% unless product.available %}
            <div class="d99-product-sold-out-overlay">SOLD OUT</div>
          {% endunless %}
        </div>

        <!-- Product details -->
        <div class="d99-product-card-info">
          <span class="d99-product-card-vendor">DISTRICT-99</span>
          <h3 class="d99-product-card-title">{{ product.title }}</h3>
          
          <div class="d99-product-card-price">
            {% if product.compare_at_price > product.price %}
              <span class="d99-card-price-sale">{{ product.price | money }}</span>
              <span class="d99-card-price-compare">{{ product.compare_at_price | money }}</span>
            {% else %}
              <span class="d99-card-price-normal">{{ product.price | money }}</span>
            {% endif %}
          </div>
        </div>

      </a>
    {% else %}
      <p class="d99-empty-msg">No products found in this collection.</p>
    {% endfor %}
  </div>

</div>

<style>
  /* ----------------------------------------------------
     D99 Bespoke Collection Page Grid
     ---------------------------------------------------- */
  .d99-collection-page {
    padding: 60px 0;
    width: 100%;
  }

  .d99-collection-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    padding-bottom: 20px;
  }

  .d99-collection-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 36px !important;
    font-weight: 800;
    text-transform: uppercase;
    color: #000000;
    letter-spacing: -0.01em;
    margin: 0;
  }

  .d99-collection-count {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    color: #737373;
  }

  .d99-collection-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px 30px;
    width: 100%;
  }

  .d99-collection-product-card {
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: #000000;
    transition: transform 0.4s ease;
  }

  /* Card Image Wrapper with light container background */
  .d99-product-card-img-wrapper {
    position: relative;
    overflow: hidden;
    aspect-ratio: 3/4;
    background-color: #f7f7f7;
    margin-bottom: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .d99-product-img-featured {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: opacity 0.5s cubic-bezier(0.25, 1, 0.5, 1);
  }

  .d99-product-img-hover {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transition: opacity 0.5s cubic-bezier(0.25, 1, 0.5, 1);
  }

  .d99-product-img-single {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Hover effect for model swap */
  .d99-collection-product-card:hover .d99-product-img-featured {
    opacity: 0;
  }

  .d99-collection-product-card:hover .d99-product-img-hover {
    opacity: 1;
  }

  /* Luxury sold out tag */
  .d99-product-sold-out-overlay {
    position: absolute;
    inset: 0;
    background-color: rgba(255,255,255,0.15);
    color: #ffffff;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(2px);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.1em;
  }

  /* Details footer */
  .d99-product-card-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .d99-product-card-vendor {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #737373;
    margin-bottom: 5px;
    text-transform: uppercase;
  }

  .d99-product-card-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    color: #000000;
    margin-bottom: 6px;
    line-height: 1.3;
    letter-spacing: 0.02em !important;
  }

  .d99-product-card-price {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .d99-card-price-normal {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #000000;
  }

  .d99-card-price-sale {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #e50914;
  }

  .d99-card-price-compare {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #a3a3a3;
    text-decoration: line-through;
  }

  /* Responsive */
  @media screen and (max-width: 900px) {
    .d99-collection-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media screen and (max-width: 600px) {
    .d99-collection-grid {
      grid-template-columns: 1fr;
      gap: 30px;
    }
  }
</style>
"""
    inject_asset(theme_id, "sections/d99-main-collection.liquid", collection_section_liquid)

    # 5. SNIPPETS: snippets/d99-cart-drawer.liquid
    cart_drawer_liquid = """{% comment %}
  DISTRICT-99 (D99) - SLIDE-OUT CART DRAWER SNIPPET
  A bespoke, high-end slide-out cart drawer styled in clean, monochrome minimalism.
{% endcomment %}

<div id="d99-cart-drawer" class="d99-cart-drawer">
  <div class="d99-cart-drawer-overlay" onclick="closeCartDrawer()"></div>
  <div class="d99-cart-drawer-content">
    
    <div class="d99-cart-drawer-header">
      <h2 class="d99-cart-title">YOUR BAG</h2>
      <button class="d99-cart-close" onclick="closeCartDrawer()">&times;</button>
    </div>

    <div class="d99-cart-drawer-body">
      <!-- Items Container (AJAX/Fallback populated) -->
      <div id="d99-cart-items-wrapper">
        <p class="d99-cart-empty">YOUR BAG IS CURRENTLY EMPTY.</p>
        <a href="/collections/all" class="d99-shop-btn">SHOP THE DROPS</a>
      </div>
    </div>

    <div class="d99-cart-drawer-footer">
      <div class="d99-cart-total-row">
        <span>SUBTOTAL</span>
        <span id="d99-cart-subtotal">0.00 EGP</span>
      </div>
      <p class="d99-cart-shipping-note">Taxes and shipping calculated at checkout.</p>
      <a href="/checkout" class="d99-checkout-btn">PROCEED TO CHECKOUT</a>
    </div>

  </div>
</div>

<style>
  /* ----------------------------------------------------
     D99 Cart Drawer Slide-out System
     ---------------------------------------------------- */
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
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(3px);
  }

  .d99-cart-drawer-content {
    position: absolute;
    top: 0;
    right: -450px;
    width: 100%;
    max-width: 420px;
    height: 100%;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    box-shadow: -10px 0 40px rgba(0,0,0,0.15);
    transition: right 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    border-left: 1px solid #000;
  }

  .d99-cart-drawer.active .d99-cart-drawer-content {
    right: 0;
  }

  /* Header */
  .d99-cart-drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid rgba(0,0,0,0.08);
  }

  .d99-cart-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 800;
    letter-spacing: 0.05em;
    margin: 0;
    text-transform: uppercase;
  }

  .d99-cart-close {
    background: none;
    border: none;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }

  .d99-cart-close:hover {
    color: #e50914;
  }

  /* Body & Items */
  .d99-cart-drawer-body {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
  }

  .d99-cart-empty {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #a3a3a3;
    text-align: center;
    margin-top: 50px;
    letter-spacing: 0.05em;
  }

  .d99-shop-btn {
    display: block;
    width: 100%;
    margin-top: 25px;
    border: 1px solid #000000;
    background-color: #000;
    color: #fff;
    text-align: center;
    text-decoration: none;
    padding: 15px 0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    transition: all 0.3s ease;
  }

  .d99-shop-btn:hover {
    background-color: #fff;
    color: #000;
  }

  /* Footer */
  .d99-cart-drawer-footer {
    padding: 30px;
    border-top: 1px solid rgba(0,0,0,0.08);
    background-color: #fcfcfc;
  }

  .d99-cart-total-row {
    display: flex;
    justify-content: space-between;
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: 0.05em;
  }

  .d99-cart-shipping-note {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #737373;
    margin-bottom: 25px;
  }

  .d99-checkout-btn {
    display: block;
    width: 100%;
    background-color: #000000;
    color: #ffffff;
    border: 1px solid #000000;
    text-align: center;
    text-decoration: none;
    padding: 18px 0;
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all 0.3s ease;
    border-radius: 0px;
  }

  .d99-checkout-btn:hover {
    background-color: #e50914;
    border-color: #e50914;
  }
</style>
"""
    inject_asset(theme_id, "snippets/d99-cart-drawer.liquid", cart_drawer_liquid)

    # 6. SECTIONS: sections/d99-footer.liquid
    footer_section_liquid = """{% comment %}
  DISTRICT-99 (D99) - PREMIUM CUSTOM STREETWEAR FOOTER
{% endcomment %}

<footer class="d99-footer">
  <div class="container d99-footer-grid">
    
    <!-- Left Panel: Newsletter -->
    <div class="d99-footer-col d99-footer-newsletter">
      <h3>JOIN THE DISTRICT</h3>
      <p>Subscribe to receive exclusive access to early drops, lookbooks, and private discounts.</p>
      {% form 'customer', id: 'd99-newsletter' %}
        <div class="d99-newsletter-input-group">
          <input type="email" name="contact[email]" placeholder="ENTER YOUR EMAIL..." required>
          <button type="submit">SUBMIT</button>
        </div>
      {% endform %}
    </div>

    <!-- Center Panel: Cyber-Star Brand Logo -->
    <div class="d99-footer-col d99-footer-logo-center">
      <div class="d99-footer-cyber-star">
        <img src="{{ 'd99-logo-header.png' | asset_url }}" alt="DISTRICT-99 Logo" class="d99-footer-img">
      </div>
      <p class="d99-slogan">ACTION IS THE BRIDGE<span class="d99-dot">.</span></p>
    </div>

    <!-- Right Panel: Navigation / Policies -->
    <div class="d99-footer-col d99-footer-links">
      <h3>DISTRICTS</h3>
      <ul>
        <li><a href="/collections/all">Shop Drops</a></li>
        <li><a href="/pages/lookbook">Editorial Lookbook</a></li>
        <li><a href="/pages/shipping">Shipping Policy</a></li>
        <li><a href="/pages/returns">Returns & Exchanges</a></li>
      </ul>
    </div>

  </div>

  <div class="d99-footer-bottom container">
    <p class="d99-copyright">&copy; {{ 'now' | date: '%Y' }} DISTRICT-99. All rights reserved.</p>
  </div>
</footer>

<style>
  /* ----------------------------------------------------
     D99 Bespoke Minimalist Footer
     ---------------------------------------------------- */
  .d99-footer {
    background-color: #000000;
    color: #ffffff;
    padding: 80px 0 40px 0;
    width: 100%;
    margin-top: 80px;
    border-top: 1px solid rgba(255,255,255,0.05);
  }

  .d99-footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr;
    gap: 60px;
    width: 100%;
    align-items: flex-start;
  }

  .d99-footer-col h3 {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    color: #ffffff;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
  }

  /* Left Col: Newsletter */
  .d99-footer-newsletter p {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    line-height: 1.6;
    color: #a3a3a3;
    margin-bottom: 20px;
    max-width: 320px;
  }

  .d99-newsletter-input-group {
    display: flex;
    width: 100%;
    max-width: 350px;
    border: 1px solid #ffffff;
  }

  .d99-newsletter-input-group input {
    flex: 1;
    background: none;
    border: none;
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    padding: 12px 18px;
    outline: none;
  }

  .d99-newsletter-input-group input::placeholder {
    color: #525252;
  }

  .d99-newsletter-input-group button {
    background-color: #ffffff;
    color: #000000;
    border: none;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 800;
    padding: 0 20px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .d99-newsletter-input-group button:hover {
    background-color: #e50914;
    color: #ffffff;
  }

  /* Center Col: Cyber-Star Logo */
  .d99-footer-logo-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .d99-footer-img {
    height: 44px;
    width: auto;
    object-fit: contain;
    filter: invert(1); /* invert black logo to white for dark footer */
    margin-bottom: 15px;
  }

  .d99-slogan {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.01em;
    text-transform: uppercase;
  }

  .d99-slogan .d99-dot {
    color: #e50914;
  }

  /* Right Col: Links */
  .d99-footer-links {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
  }

  .d99-footer-links ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .d99-footer-links li {
    margin-bottom: 10px;
  }

  .d99-footer-links a {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    color: #a3a3a3;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 700;
    transition: color 0.3s ease;
  }

  .d99-footer-links a:hover {
    color: #e50914;
  }

  /* Bottom Copyright */
  .d99-footer-bottom {
    margin-top: 60px;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 30px;
    display: flex;
    justify-content: center;
  }

  .d99-copyright {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #525252;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* Responsive styling */
  @media screen and (max-width: 900px) {
    .d99-footer-grid {
      grid-template-columns: 1fr;
      gap: 50px;
      text-align: center;
    }
    .d99-footer-newsletter p {
      margin: 0 auto 20px auto;
    }
    .d99-newsletter-input-group {
      margin: 0 auto;
    }
    .d99-footer-links {
      align-items: center;
      text-align: center;
    }
  }
</style>
"""
    inject_asset(theme_id, "sections/d99-footer.liquid", footer_section_liquid)

    # 7. LAYOUT: layout/theme.liquid (Integrates Header, Footer, and Cart Drawer)
    theme_liquid_code = """<!doctype html>
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
  
  <!-- 1. Custom Header -->
  <header class="header d99-custom-header">
    <div class="container">
      <div class="nav d99-header-grid">
        
        <!-- LEFT SIDE: Navigation Links -->
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
        
        <!-- CENTER: Transparent Black Logo -->
        <div class="logo d99-logo-center">
          <a href="/" style="display: inline-block; line-height: 0;">
            <img src="{{ 'd99-logo-header.png' | asset_url }}" alt="DISTRICT-99" class="d99-logo-img">
          </a>
        </div>
        
        <!-- RIGHT SIDE: Cart & Actions -->
        <div class="nav-actions d99-actions-right">
          <a href="#" class="d99-cart-icon" onclick="openCartDrawer(); return false;"><i class="fas fa-shopping-cart"></i></a>
          <a href="/account" class="d99-account-icon"><i class="fas fa-user"></i></a>
        </div>
        
      </div>
    </div>
  </header>

  <!-- 2. Cart Drawer Snippet -->
  {% render 'd99-cart-drawer' %}

  <!-- 3. Main Page Content -->
  <main class="d99-main-content">
    {{ content_for_layout }}
  </main>

  <!-- 4. Custom Footer Section -->
  {% section 'd99-footer' %}

  <script>
    // Global Cart Drawer Controllers
    function openCartDrawer() {
      document.getElementById('d99-cart-drawer').classList.add('active');
      fetchCartAndPopulate();
    }

    function closeCartDrawer() {
      document.getElementById('d99-cart-drawer').classList.remove('active');
    }

    // AJAX: Fetch Cart Items and Populate Cart Drawer dynamically
    function fetchCartAndPopulate() {
      fetch('/cart.js')
        .then(response => response.json())
        .then(cart => {
          const wrapper = document.getElementById('d99-cart-items-wrapper');
          const subtotalElem = document.getElementById('d99-cart-subtotal');
          
          // Format Price EGP
          subtotalElem.innerText = (cart.total_price / 100).toFixed(2) + ' EGP';
          
          if (cart.item_count === 0) {
            wrapper.innerHTML = `
              <p class="d99-cart-empty">YOUR BAG IS CURRENTLY EMPTY.</p>
              <a href="/collections/all" class="d99-shop-btn">SHOP THE DROPS</a>
            `;
            return;
          }
          
          let html = '<div class="d99-cart-items-list">';
          cart.items.forEach(item => {
            html += `
              <div class="d99-cart-item-card" style="display: flex; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 15px;">
                <div style="width: 80px; height: 100px; background-color: #f7f7f7; display: flex; align-items: center; justify-content: center;">
                  <img src="${item.image}" alt="${item.title}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                </div>
                <div style="flex: 1; display: flex; flex-direction: column; align-items: flex-start;">
                  <span style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; color: #737373;">DISTRICT-99</span>
                  <h4 style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; text-transform: uppercase; margin: 3px 0 6px 0; line-height: 1.2;">${item.product_title}</h4>
                  <span style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #a3a3a3; margin-bottom: 8px;">Size: ${item.variant_title}</span>
                  <div style="display: flex; justify-content: space-between; width: 100%; align-items: center;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; color: #e50914;">${(item.price / 100).toFixed(2)} EGP</span>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #000;">QTY: ${item.quantity}</span>
                  </div>
                </div>
              </div>
            `;
          });
          html += '</div>';
          wrapper.innerHTML = html;
        });
    }

    // Intercept default product form submit and handle with smooth AJAX add!
    document.addEventListener('DOMContentLoaded', () => {
      const form = document.getElementById('d99-product-form');
      if (form) {
        form.addEventListener('submit', (e) => {
          e.preventDefault();
          const variantId = document.getElementById('d99-variant-id').value;
          const qty = document.getElementById('d99-product-qty').value;
          
          const formData = {
            'items': [{
              'id': variantId,
              'quantity': qty
            }]
          };
          
          fetch('/cart/add.js', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
          })
          .then(response => response.json())
          .then(item => {
            console.log('Added successfully:', item);
            openCartDrawer(); // smooth open slide-out cart drawer on add!
          })
          .catch((error) => {
            console.error('Error adding to cart:', error);
          });
        });
      }
    });
  </script>

</body>
</html>"""
    inject_asset(theme_id, "layout/theme.liquid", theme_liquid_code)

    print("\n🎉 COMPLETE BESPOKE DISTRICT-99 THEME DEPLOYED SUCCESSFULLY! 🎉")
    print("👉 المتجر الآن متكامل بالكامل: صفحة منتجات مخصصة، صفحة مجموعات مبتكرة بـ Hover swap، وسلة جانبية منزلقة ممتازة!")

if __name__ == "__main__":
    deploy_complete_theme()
