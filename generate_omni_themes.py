#!/usr/bin/env python3
"""
generate_omni_themes.py
========================
Builds 5 complete, deployable Shopify Online Store 2.0 theme packages
derived from the design-mockup families found in uploads/theme-design-mockups
(bright editorial / dark option2 / brutalist) plus the ready content images
(split_hero_*, bento_panel_*, logo) found in uploads/.

Each theme is a full directory tree that can either be:
  * zipped and uploaded via Shopify Admin -> Themes -> Upload theme, or
  * pushed to a live store with deploy_omni_theme.py (Shopify Admin API).

Run:  python3 generate_omni_themes.py
"""

import os
import json
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "omni-uk-themes")
UPLOADS = os.path.join(ROOT, "uploads")

# ---------------------------------------------------------------------------
# 1. CONTENT IMAGES copied into every theme's assets/ folder (real visuals)
# ---------------------------------------------------------------------------
CONTENT_SRC = {
    "omni-hero-left.png":  os.path.join(UPLOADS, "split_hero_left.png"),
    "omni-hero-right.png": os.path.join(UPLOADS, "split_hero_right.png"),
    "omni-logo.png":       os.path.join(UPLOADS, "d99_logo_transparent.png"),
}
for i in range(1, 9):
    CONTENT_SRC[f"omni-panel-{i}.png"] = os.path.join(UPLOADS, f"bento_panel_{i}.png")

# ---------------------------------------------------------------------------
# 2. THEME DEFINITIONS  (5 distinct aesthetics from the mockup families)
# ---------------------------------------------------------------------------
THEMES = [
    {
        "key": "omni-light",
        "name": "OMNI — Light Editorial",
        "inspired_by": "homepage/product/collection mockups (bright, airy minimal)",
        "bg": "#f5f4f2", "fg": "#141414", "accent": "#141414",
        "muted": "#6b6862", "line": "rgba(0,0,0,0.12)", "onaccent": "#ffffff",
        "font_head": "'Helvetica Neue', Arial, sans-serif",
        "font_body": "'Helvetica Neue', Arial, sans-serif",
        "maxw": "1320px",
        "radius": "0px", "border_w": "1px", "track": "0.18em",
        "flavor": """
  .site-header{letter-spacing:var(--track);text-transform:uppercase;font-weight:600;}
  .hero__content h1{font-size:clamp(2.4rem,6vw,5.5rem);letter-spacing:0.04em;font-weight:700;}
  .btn{border:1px solid var(--fg);}
  .bento__cell{border:1px solid var(--line);}
  body{font-weight:400;}
""",
    },
    {
        "key": "omni-noir",
        "name": "OMNI — Noir (Dark Moody)",
        "inspired_by": "option2_variation A/C/E (very dark, black + deep-red accent)",
        "bg": "#0b0b0b", "fg": "#ededed", "accent": "#b3201f",
        "muted": "#8a8a8a", "line": "rgba(255,255,255,0.14)", "onaccent": "#ffffff",
        "font_head": "Georgia, 'Times New Roman', serif",
        "font_body": "'Helvetica Neue', Arial, sans-serif",
        "maxw": "1320px",
        "radius": "0px", "border_w": "1px", "track": "0.16em",
        "flavor": """
  .site-header{letter-spacing:var(--track);text-transform:uppercase;}
  .hero__content h1{font-size:clamp(2.4rem,6vw,5.5rem);font-family:var(--font-head);}
  .btn{background:var(--accent);border-color:var(--accent);color:#fff;}
  .btn:hover{background:transparent;color:var(--accent);}
  a:hover{color:var(--accent);}
  .announce{background:var(--accent);color:#fff;}
""",
    },
    {
        "key": "omni-brutalist",
        "name": "OMNI — Brutalist (Dark Raw)",
        "inspired_by": "brutalist_variation_7 (stark black, mono, exposed grid)",
        "bg": "#0a0a0a", "fg": "#f2f2f2", "accent": "#f2f2f2",
        "muted": "#9a9a9a", "line": "#2a2a2a", "onaccent": "#0a0a0a",
        "font_head": "'Courier New', Courier, monospace",
        "font_body": "'Courier New', Courier, monospace",
        "maxw": "1400px",
        "radius": "0px", "border_w": "2px", "track": "0.10em",
        "flavor": """
  *{border-radius:0 !important;}
  .site-header{border-bottom:var(--border-w) solid var(--fg);text-transform:uppercase;}
  .header__inner{gap:0;}
  .header__link,.header__cart{border-left:var(--border_w) solid var(--line);padding:1rem 1.4rem;}
  .btn{border:var(--border_w) solid var(--fg);text-transform:uppercase;letter-spacing:var(--track);}
  .bento__cell{border:var(--border_w) solid var(--line);}
  .hero__media{border:var(--border_w) solid var(--fg);}
  body{font-weight:400;}
""",
    },
    {
        "key": "omni-warm",
        "name": "OMNI — Warm Editorial (Copper)",
        "inspired_by": "brutalist_variation_15 (light warm beige + copper accent)",
        "bg": "#efe9e1", "fg": "#2a2522", "accent": "#9c6b4a",
        "muted": "#7d746b", "line": "rgba(0,0,0,0.16)", "onaccent": "#fff7f0",
        "font_head": "Georgia, 'Times New Roman', serif",
        "font_body": "'Helvetica Neue', Arial, sans-serif",
        "maxw": "1280px",
        "radius": "2px", "border_w": "1px", "track": "0.14em",
        "flavor": """
  .site-header{letter-spacing:0.06em;}
  .hero__content h1{font-family:var(--font-head);font-size:clamp(2.6rem,6vw,5.5rem);}
  .btn{background:var(--accent);border-color:var(--accent);color:var(--onaccent);}
  .btn:hover{background:transparent;color:var(--accent);}
  .card__title{font-family:var(--font-head);}
""",
    },
    {
        "key": "omni-mono",
        "name": "OMNI — Mono Contrast (Stark B&W)",
        "inspired_by": "cart_drawer_mockup (high-contrast black & white)",
        "bg": "#ffffff", "fg": "#000000", "accent": "#000000",
        "muted": "#555555", "line": "#000000", "onaccent": "#ffffff",
        "font_head": "'Arial Black', Arial, sans-serif",
        "font_body": "'Helvetica Neue', Arial, sans-serif",
        "maxw": "1300px",
        "radius": "0px", "border_w": "2px", "track": "0.20em",
        "flavor": """
  *{border-radius:0 !important;}
  .site-header{border-bottom:var(--border_w) solid #000;text-transform:uppercase;letter-spacing:var(--track);}
  .btn{border:var(--border_w) solid #000;background:#000;color:#fff;}
  .btn:hover{background:#fff;color:#000;}
  .bento__cell{border:var(--border_w) solid #000;}
  .hero__media{border:var(--border_w) solid #000;}
  .card{border:1px solid #000;}
""",
    },
]

# ---------------------------------------------------------------------------
# 3. SHARED LIQUID / JSON CONTENT (same structure for every theme)
# ---------------------------------------------------------------------------

LAYOUT = """<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ page_title }}{% unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless %}</title>
  <meta name="description" content="{{ page_description | default: shop.description | escape }}">
  {{ 'theme.css' | asset_url | stylesheet_tag }}
  {{ content_for_header }}
</head>
<body>
  <a class="skip-link" href="#MainContent">Skip to content</a>
  {% section 'header' %}
  {% section 'announcement' %}
  <main id="MainContent">
    {{ content_for_layout }}
  </main>
  {% section 'footer' %}
  {{ 'theme.js' | asset_url | script_tag }}
</body>
</html>
"""

SECTION_HEADER = """<header class="site-header" data-header>
  <div class="header__inner">
    <a href="{{ routes.root_url }}" class="header__logo">
      {%- if section.settings.logo -%}
        <img src="{{ section.settings.logo | img_url:'200x' }}" alt="{{ shop.name | escape }}">
      {%- else -%}
        {{ shop.name }}
      {%- endif -%}
    </a>
    <nav class="header__nav" aria-label="Primary">
      {% for link in linklists.main-menu.links %}
        <a href="{{ link.url }}" class="header__link">{{ link.title }}</a>
      {% endfor %}
    </nav>
    <div class="header__actions">
      <a href="{{ routes.cart_url }}" class="header__cart">Cart ({{ cart.item_count }})</a>
    </div>
  </div>
</header>
{% schema %}
{
  "name": "OMNI Header",
  "settings": [
    { "type": "image_picker", "id": "logo", "label": "Logo" }
  ]
}
{% endschema %}
"""

SECTION_ANNOUNCE = """<div class="announce" role="region" aria-label="Announcement">
  <div class="announce__track">
    {% for i in (1..8) %}
      <span>{{ section.settings.text }}</span>
      <span class="announce__dot">&#9670;</span>
    {% endfor %}
  </div>
</div>
{% schema %}
{
  "name": "OMNI Announcement",
  "settings": [
    { "type": "text", "id": "text", "label": "Text", "default": "ACTION IS THE BRIDGE — FREE SHIPPING WORLDWIDE" }
  ]
}
{% endschema %}
"""

SECTION_HERO = """<section class="hero">
  <div class="hero__media">
    {%- assign hero_img = section.settings.image | default: 'omni-hero-left.png' | asset_url -%}
    <img src="{{ hero_img }}" alt="{{ section.settings.heading | escape }}" loading="eager">
  </div>
  <div class="hero__content">
    <h1>{{ section.settings.heading }}</h1>
    {% if section.settings.sub %}<p class="hero__sub">{{ section.settings.sub }}</p>{% endif %}
    <a class="btn" href="{{ section.settings.link | default: routes.all_products_collection_url }}">{{ section.settings.button }}</a>
  </div>
</section>
{% schema %}
{
  "name": "OMNI Hero",
  "settings": [
    { "type": "image_picker", "id": "image", "label": "Image" },
    { "type": "text", "id": "heading", "label": "Heading", "default": "NEW ARRIVALS" },
    { "type": "text", "id": "sub", "label": "Subheading", "default": "Action is the bridge." },
    { "type": "text", "id": "button", "label": "Button", "default": "COP NOW" },
    { "type": "url", "id": "link", "label": "Link" }
  ]
}
{% endschema %}
"""

SECTION_LOOKBOOK = """<section class="lookbook">
  <h2 class="lookbook__title">{{ section.settings.heading }}</h2>
  <div class="bento">
    {% for block in section.blocks %}
      <a class="bento__cell" href="{{ block.settings.link | default: routes.all_products_collection_url }}"
         style="grid-column: span {{ block.settings.col }}; grid-row: span {{ block.settings.row }};">
        {%- if block.settings.image -%}
          <img src="{{ block.settings.image | img_url:'900x' }}" alt="{{ block.settings.title | escape }}">
        {%- else -%}
          <span class="bento__placeholder">{{ block.settings.title }}</span>
        {%- endif -%}
      </a>
    {% endfor %}
  </div>
  <p class="lookbook__hint">Open the theme customizer to drop your product & model shots into each panel.</p>
</section>
{% schema %}
{
  "name": "OMNI Lookbook",
  "settings": [
    { "type": "text", "id": "heading", "label": "Heading", "default": "DEFINE YOUR DISTRICT" }
  ],
  "blocks": [
    {
      "type": "panel",
      "name": "Panel",
      "settings": [
        { "type": "text", "id": "title", "label": "Label", "default": "Panel" },
        { "type": "image_picker", "id": "image", "label": "Image" },
        { "type": "url", "id": "link", "label": "Link" },
        { "type": "range", "id": "col", "label": "Columns", "min": 1, "max": 4, "default": 2 },
        { "type": "range", "id": "row", "label": "Rows", "min": 1, "max": 2, "default": 1 }
      ]
    }
  ],
  "presets": [{ "name": "Lookbook", "blocks": [] }]
}
{% endschema %}
"""

SECTION_FEATURED = """<section class="featured">
  <h2 class="section-title">{{ section.settings.title }}</h2>
  <div class="featured__grid">
    {% assign coll = collections[section.settings.collection] %}
    {% if coll %}
      {% for product in coll.products limit: section.settings.limit %}
        {% render 'card-product', product: product %}
      {% endfor %}
    {% else %}
      {% for product in collections.all.products limit: section.settings.limit %}
        {% render 'card-product', product: product %}
      {% endfor %}
    {% endif %}
  </div>
</section>
{% schema %}
{
  "name": "OMNI Featured",
  "settings": [
    { "type": "text", "id": "title", "label": "Title", "default": "FEATURED" },
    { "type": "collection", "id": "collection", "label": "Collection" },
    { "type": "range", "id": "limit", "label": "Limit", "min": 2, "max": 12, "default": 4 }
  ]
}
{% endschema %}
"""

SECTION_NEWSLETTER = """<section class="news">
  <div class="news__inner">
    <h2>{{ section.settings.heading }}</h2>
    {% if section.settings.sub %}<p>{{ section.settings.sub }}</p>{% endif %}
    {% form 'customer' %}
      <div class="news__form">
        <input type="email" name="contact[email]" placeholder="your@email.com" required>
        <button type="submit" class="btn">Subscribe</button>
      </div>
    {% endform %}
  </div>
</section>
{% schema %}
{
  "name": "OMNI Newsletter",
  "settings": [
    { "type": "text", "id": "heading", "label": "Heading", "default": "JOIN THE DISTRICT" },
    { "type": "text", "id": "sub", "label": "Subheading", "default": "Get drops first." }
  ]
}
{% endschema %}
"""

SECTION_FOOTER = """<footer class="site-footer">
  <div class="footer__cols">
    <div class="footer__col">
      <h3>{{ shop.name }}</h3>
      <p>{{ section.settings.tagline }}</p>
    </div>
    <div class="footer__col">
      <h4>Shop</h4>
      <ul>
        {% for link in linklists.main-menu.links %}<li><a href="{{ link.url }}">{{ link.title }}</a></li>{% endfor %}
      </ul>
    </div>
    <div class="footer__col">
      <h4>Info</h4>
      <ul>
        {% for link in linklists.footer.links %}<li><a href="{{ link.url }}">{{ link.title }}</a></li>{% endfor %}
      </ul>
    </div>
  </div>
  <div class="footer__bottom">
    <span>&copy; {{ 'now' | date: '%Y' }} {{ shop.name }}. All rights reserved.</span>
    <span>{{ section.settings.note }}</span>
  </div>
</footer>
{% schema %}
{
  "name": "OMNI Footer",
  "settings": [
    { "type": "text", "id": "tagline", "label": "Tagline", "default": "Action is the bridge." },
    { "type": "text", "id": "note", "label": "Bottom note", "default": "DISTRICT-99 // OMNI UK" }
  ]
}
{% endschema %}
"""

SNIPPET_CARD = """<div class="card">
  <a href="{{ product.url }}">
    <div class="card__media">
      <img src="{{ product.featured_image | img_url:'600x' }}" alt="{{ product.title | escape }}" loading="lazy">
    </div>
    <h3 class="card__title">{{ product.title }}</h3>
    <span class="card__price">{{ product.price | money }}</span>
  </a>
</div>
"""

SETTINGS_SCHEMA = """[
  {
    "name": "Theme",
    "settings": [
      { "type": "header", "content": "Colors" },
      { "type": "color", "id": "color_bg", "label": "Background", "default": "#ffffff" },
      { "type": "color", "id": "color_fg", "label": "Foreground", "default": "#111111" },
      { "type": "color", "id": "color_accent", "label": "Accent", "default": "#111111" },
      { "type": "header", "content": "Layout" },
      { "type": "range", "id": "max_width", "label": "Max width", "min": 1000, "max": 1600, "step": 20, "default": 1320 }
    ]
  }
]
"""

def settings_data():
    return json.dumps({
        "current": {"sections": {}, "blocks": {}},
        "presets": {"default": {"sections": {}, "blocks": {}}}
    }, indent=2)

TEMPLATE_INDEX = """{
  "sections": {
    "hero": { "type": "hero", "settings": { "heading": "NEW ARRIVALS", "sub": "Action is the bridge.", "button": "COP NOW" } },
    "lookbook": { "type": "lookbook", "settings": { "heading": "DEFINE YOUR DISTRICT" } },
    "featured": { "type": "featured-collection", "settings": { "title": "FEATURED", "limit": 4 } },
    "news": { "type": "newsletter", "settings": { "heading": "JOIN THE DISTRICT", "sub": "Get drops first." } }
  },
  "order": ["hero", "lookbook", "featured", "news"]
}
"""

TEMPLATE_PRODUCT = """{
  "sections": {
    "main": {
      "type": "product-template",
      "settings": { "show_price": true, "show_description": true }
    }
  },
  "order": ["main"]
}
"""

TEMPLATE_COLLECTION = """{
  "sections": {
    "main": {
      "type": "collection-template",
      "settings": { "title": "", "columns": 3 }
    }
  },
  "order": ["main"]
}
"""

TEMPLATE_CART = """{
  "sections": {
    "main": { "type": "cart-template", "settings": {} }
  },
  "order": ["main"]
}
"""

TEMPLATE_PAGE = """{
  "sections": {
    "main": { "type": "page-template", "settings": {} }
  },
  "order": ["main"]
}
"""

TEMPLATE_404 = """{
  "sections": {
    "main": { "type": "four-o-four", "settings": {} }
  },
  "order": ["main"]
}
"""

TEMPLATE_LIST_COLLECTIONS = """{
  "sections": {
    "main": { "type": "list-collections", "settings": {} }
  },
  "order": ["main"]
}
"""

# Product / collection / page / cart / 404 single-section fallbacks
SECTION_PRODUCT = """<section class="product-page">
  <div class="product-page__media">
    {% for image in product.images %}<img src="{{ image | img_url:'800x' }}" alt="{{ product.title | escape }}">{% endfor %}
  </div>
  <div class="product-page__info">
    <h1>{{ product.title }}</h1>
    <p class="product-page__price">{{ product.price | money }}</p>
    <div class="product-page__desc">{{ product.description }}</div>
    {% form 'product', product %}
      <button type="submit" class="btn">Add to cart</button>
    {% endform %}
  </div>
</section>
{% schema %}{ "name": "OMNI Product", "settings": [ { "type":"checkbox","id":"show_price","label":"Show price","default":true }, { "type":"checkbox","id":"show_description","label":"Show description","default":true } ] }{% endschema %}
"""

SECTION_COLLECTION = """<section class="collection-page">
  <h1 class="collection-page__title">{{ collection.title }}</h1>
  <div class="featured__grid">
    {% for product in collection.products %}
      {% render 'card-product', product: product %}
    {% endfor %}
  </div>
</section>
{% schema %}{ "name": "OMNI Collection", "settings": [ { "type":"text","id":"title","label":"Title" }, { "type":"range","id":"columns","label":"Columns","min":2,"max":4,"default":3 } ] }{% endschema %}
"""

SECTION_PAGE = """<section class="static-page">
  <h1>{{ page.title }}</h1>
  <div class="static-page__body">{{ page.content }}</div>
</section>
{% schema %}{ "name": "OMNI Page", "settings": [] }{% endschema %}
"""

SECTION_CART = """<section class="cart-page">
  <h1>Your Cart</h1>
  {% if cart.item_count > 0 %}
    <div class="cart-page__items">
      {% for item in cart.items %}
        <div class="cart-item">
          <img src="{{ item.image | img_url:'160x' }}" alt="{{ item.product.title | escape }}">
          <div><a href="{{ item.url }}">{{ item.product.title }}</a><br>Qty: {{ item.quantity }}</div>
          <span>{{ item.line_price | money }}</span>
        </div>
      {% endfor %}
    </div>
    <div class="cart-page__total">Total: {{ cart.total_price | money }}</div>
    <a class="btn" href="/checkout">Checkout</a>
  {% else %}
    <p>Your cart is empty.</p>
    <a class="btn" href="{{ routes.all_products_collection_url }}">Shop now</a>
  {% endif %}
</section>
{% schema %}{ "name": "OMNI Cart", "settings": [] }{% endschema %}
"""

SECTION_404 = """<section class="notfound">
  <h1>404</h1>
  <p>This page drifted out of the district.</p>
  <a class="btn" href="{{ routes.root_url }}">Back home</a>
</section>
{% schema %}{ "name": "OMNI 404", "settings": [] }{% endschema %}
"""

SECTION_LIST_COLLECTIONS = """<section class="list-collections">
  <h1>Collections</h1>
  <div class="featured__grid">
    {% for collection in collections %}
      <a class="card" href="{{ collection.url }}">
        <div class="card__media">
          {% if collection.image %}<img src="{{ collection.image | img_url:'600x' }}" alt="{{ collection.title | escape }}">{% endif %}
        </div>
        <h3 class="card__title">{{ collection.title }}</h3>
      </a>
    {% endfor %}
  </div>
</section>
{% schema %}{ "name": "OMNI List Collections", "settings": [] }{% endschema %}
"""

# ---------------------------------------------------------------------------
# 4. PER-THEME CSS (driven by the THEMES palette + flavor)
# ---------------------------------------------------------------------------
CSS_TEMPLATE = """/* =========================================================================
   %(name)s  —  OMNI UK theme
   Inspired by: %(inspired_by)s
   ========================================================================= */
:root{
  --bg:%(bg)s; --fg:%(fg)s; --accent:%(accent)s; --muted:%(muted)s;
  --line:%(line)s; --onaccent:%(onaccent)s;
  --font-head:%(font_head)s; --font-body:%(font_body)s;
  --maxw:%(maxw)s; --radius:%(radius)s; --border-w:%(border_w)s; --track:%(track)s;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-font-smoothing:antialiased;}
body{
  background:var(--bg); color:var(--fg); font-family:var(--font-body);
  line-height:1.55; font-size:16px;
}
img{max-width:100%%; display:block;}
a{color:inherit; text-decoration:none; transition:color .2s ease;}
a:hover{opacity:.7;}
.skip-link{position:absolute;left:-999px;}
.skip-link:focus{left:1rem;top:1rem;background:var(--fg);color:var(--bg);padding:.5rem 1rem;z-index:99;}

/* ---------- HEADER ---------- */
.site-header{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--line);}
.header__inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  max-width:var(--maxw);margin:0 auto;padding:.9rem 1.5rem;}
.header__logo{font-family:var(--font-head);font-size:1.4rem;font-weight:700;letter-spacing:.02em;}
.header__logo img{height:34px;width:auto;}
.header__nav{display:flex;gap:1.6rem;flex-wrap:wrap;}
.header__link{font-size:.8rem;letter-spacing:var(--track);text-transform:uppercase;}
.header__cart{font-size:.8rem;letter-spacing:var(--track);text-transform:uppercase;}

/* ---------- ANNOUNCEMENT MARQUEE ---------- */
.announce{background:var(--fg);color:var(--bg);overflow:hidden;white-space:nowrap;padding:.5rem 0;}
.announce__track{display:inline-block;animation:marq 22s linear infinite;}
.announce__track span{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;padding:0 1.2rem;}
.announce__dot{opacity:.6;}
@keyframes marq{from{transform:translateX(0);}to{transform:translateX(-50%%);}}

/* ---------- HERO ---------- */
.hero{position:relative;display:grid;grid-template-columns:1.2fr .8fr;align-items:center;
  max-width:var(--maxw);margin:0 auto;min-height:78vh;gap:2rem;padding:3rem 1.5rem;}
.hero__media img{width:100%%;height:70vh;object-fit:cover;border-radius:var(--radius);}
.hero__content h1{font-family:var(--font-head);font-weight:700;line-height:1;margin-bottom:1rem;}
.hero__sub{color:var(--muted);margin-bottom:1.6rem;font-size:1.05rem;}
.btn{display:inline-block;padding:.9rem 2.2rem;border:1px solid var(--fg);border-radius:var(--radius);
  font-size:.78rem;letter-spacing:var(--track);text-transform:uppercase;cursor:pointer;
  background:transparent;color:var(--fg);transition:all .2s ease;}
.btn:hover{background:var(--fg);color:var(--bg);opacity:1;}

/* ---------- LOOKBOOK / BENTO ---------- */
.lookbook{max-width:var(--maxw);margin:4rem auto;padding:0 1.5rem;}
.lookbook__title,.section-title{font-family:var(--font-head);text-transform:uppercase;
  letter-spacing:var(--track);font-size:clamp(1.4rem,3vw,2.4rem);margin-bottom:1.6rem;}
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(240px,auto);gap:18px;}
.bento__cell{position:relative;overflow:hidden;background:var(--line);border-radius:var(--radius);}
.bento__cell img{width:100%%;height:100%%;object-fit:cover;}
.bento__placeholder{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  color:var(--muted);letter-spacing:.2em;text-transform:uppercase;font-size:.8rem;}
.lookbook__hint{margin-top:1rem;color:var(--muted);font-size:.8rem;}

/* ---------- FEATURED / CARDS ---------- */
.featured{max-width:var(--maxw);margin:4rem auto;padding:0 1.5rem;}
.featured__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;}
.card{border-radius:var(--radius);}
.card__media{aspect-ratio:3/4;overflow:hidden;background:var(--line);margin-bottom:.7rem;}
.card__media img{width:100%%;height:100%%;object-fit:cover;transition:transform .4s ease;}
.card:hover .card__media img{transform:scale(1.04);}
.card__title{font-size:.95rem;font-weight:600;}
.card__price{color:var(--muted);font-size:.9rem;}

/* ---------- NEWSLETTER ---------- */
.news{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:4rem 1.5rem;margin-top:4rem;}
.news__inner{max-width:640px;margin:0 auto;text-align:center;}
.news__inner h2{font-family:var(--font-head);text-transform:uppercase;letter-spacing:var(--track);margin-bottom:.6rem;}
.news__form{display:flex;gap:.6rem;justify-content:center;margin-top:1.4rem;flex-wrap:wrap;}
.news__form input{padding:.9rem 1.2rem;border:1px solid var(--line);background:transparent;color:var(--fg);
  border-radius:var(--radius);min-width:260px;}

/* ---------- FOOTER ---------- */
.site-footer{border-top:1px solid var(--line);margin-top:4rem;padding:3rem 1.5rem 2rem;}
.footer__cols{max-width:var(--maxw);margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem;}
.footer__col h3{font-family:var(--font-head);font-size:1.5rem;margin-bottom:.5rem;}
.footer__col h4{text-transform:uppercase;letter-spacing:var(--track);font-size:.78rem;margin-bottom:.8rem;}
.footer__col ul{list-style:none;}
.footer__col li{margin-bottom:.4rem;}
.footer__col p{color:var(--muted);}
.footer__bottom{max-width:var(--maxw);margin:2.5rem auto 0;padding-top:1.5rem;border-top:1px solid var(--line);
  display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:var(--muted);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;}

/* ---------- PRODUCT / COLLECTION / CART PAGES ---------- */
.product-page{max-width:var(--maxw);margin:3rem auto;padding:0 1.5rem;display:grid;grid-template-columns:1fr 1fr;gap:3rem;}
.product-page__media img{border-radius:var(--radius);margin-bottom:1rem;}
.product-page__info h1{font-family:var(--font-head);font-size:2.2rem;margin-bottom:1rem;}
.product-page__price{font-size:1.4rem;margin-bottom:1rem;}
.product-page__desc{color:var(--muted);margin-bottom:1.6rem;}
.collection-page,.static-page,.cart-page,.notfound,.list-collections{max-width:var(--maxw);margin:3rem auto;padding:0 1.5rem;}
.collection-page__title,.static-page h1,.cart-page h1,.notfound h1{font-family:var(--font-head);text-transform:uppercase;letter-spacing:var(--track);margin-bottom:1.6rem;}
.cart-item{display:flex;gap:1rem;align-items:center;padding:1rem 0;border-bottom:1px solid var(--line);}
.cart-item img{width:90px;height:auto;}
.cart-page__total{margin:1.5rem 0;font-size:1.2rem;}

/* ---------- RESPONSIVE ---------- */
@media (max-width:1024px){
  .bento{grid-template-columns:repeat(2,1fr);}
  .featured__grid{grid-template-columns:repeat(2,1fr);}
}
@media (max-width:760px){
  .hero{grid-template-columns:1fr;min-height:auto;}
  .hero__media img{height:52vh;}
  .product-page{grid-template-columns:1fr;}
  .footer__cols{grid-template-columns:1fr;}
  .header__nav{display:none;}
}

/* ---------- THEME FLAVOR OVERRIDES ---------- */
%(flavor)s
"""

THEME_README = """# %(name)s

Shopify Online Store 2.0 theme — part of the OMNI UK theme pack.

Design direction: %(inspired_by)s
Palette:
  background : %(bg)s
  foreground : %(fg)s
  accent     : %(accent)s

How to upload:
  1) ZIP this folder and upload via Shopify Admin -> Online Store -> Themes -> Upload theme, OR
  2) Run:  python3 deploy_omni_theme.py --theme %(key)s --store <store.myshopify.com> --token <ADMIN_API_TOKEN>

After upload, open the theme customizer to:
  - pick the hero image (defaults to omni-hero-left.png bundled in assets/)
  - drop product/model shots into the Lookbook (Bento) panels
  - set the Featured collection
"""

# ---------------------------------------------------------------------------
# 5. BUILD
# ---------------------------------------------------------------------------
def write(theme_dir, rel, content):
    path = os.path.join(theme_dir, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build_theme(t):
    theme_dir = os.path.join(OUT, t["key"])
    if os.path.exists(theme_dir):
        shutil.rmtree(theme_dir)
    os.makedirs(theme_dir, exist_ok=True)

    # config
    write(theme_dir, "config/settings_schema.json", SETTINGS_SCHEMA)
    write(theme_dir, "config/settings_data.json", settings_data())

    # layout
    write(theme_dir, "layout/theme.liquid", LAYOUT)

    # templates
    write(theme_dir, "templates/index.json", TEMPLATE_INDEX)
    write(theme_dir, "templates/product.json", TEMPLATE_PRODUCT)
    write(theme_dir, "templates/collection.json", TEMPLATE_COLLECTION)
    write(theme_dir, "templates/cart.json", TEMPLATE_CART)
    write(theme_dir, "templates/page.json", TEMPLATE_PAGE)
    write(theme_dir, "templates/404.json", TEMPLATE_404)
    write(theme_dir, "templates/list-collections.json", TEMPLATE_LIST_COLLECTIONS)

    # sections
    write(theme_dir, "sections/header.liquid", SECTION_HEADER)
    write(theme_dir, "sections/announcement.liquid", SECTION_ANNOUNCE)
    write(theme_dir, "sections/hero.liquid", SECTION_HERO)
    write(theme_dir, "sections/lookbook.liquid", SECTION_LOOKBOOK)
    write(theme_dir, "sections/featured-collection.liquid", SECTION_FEATURED)
    write(theme_dir, "sections/newsletter.liquid", SECTION_NEWSLETTER)
    write(theme_dir, "sections/footer.liquid", SECTION_FOOTER)
    write(theme_dir, "sections/product-template.liquid", SECTION_PRODUCT)
    write(theme_dir, "sections/collection-template.liquid", SECTION_COLLECTION)
    write(theme_dir, "sections/page-template.liquid", SECTION_PAGE)
    write(theme_dir, "sections/cart-template.liquid", SECTION_CART)
    write(theme_dir, "sections/four-o-four.liquid", SECTION_404)
    write(theme_dir, "sections/list-collections.liquid", SECTION_LIST_COLLECTIONS)

    # snippets
    write(theme_dir, "snippets/card-product.liquid", SNIPPET_CARD)

    # assets: css + js
    css = CSS_TEMPLATE % t
    write(theme_dir, "assets/theme.css", css)
    write(theme_dir, "assets/theme.js", "/* OMNI theme JS — hooks for sticky header / cart drawer */\nconsole.log('OMNI theme loaded');\n")

    # copy content images into assets
    for dest, src in CONTENT_SRC.items():
        if os.path.exists(src):
            shutil.copy(src, os.path.join(theme_dir, "assets", dest))

    # README
    write(theme_dir, "README.md", THEME_README % t)
    return theme_dir

def main():
    os.makedirs(OUT, exist_ok=True)
    built = []
    for t in THEMES:
        d = build_theme(t)
        built.append((t["name"], d))
    # pack-level readme
    lines = ["# OMNI UK — 5 Ready-to-Upload Shopify Themes\n"]
    lines.append("Generated by generate_omni_themes.py from the design-mockup families in uploads/.\n")
    lines.append("\n| # | Theme | Direction | Palette |")
    lines.append("|---|--------|-----------|---------|")
    for i, t in enumerate(THEMES, 1):
        lines.append(f"| {i} | **{t['name']}** (`{t['key']}`) | {t['inspired_by']} | bg {t['bg']} / fg {t['fg']} / accent {t['accent']} |")
    lines.append("\n## Upload")
    lines.append("- ZIP any theme folder and upload via Shopify Admin → Themes → Upload theme, OR")
    lines.append("- `python3 deploy_omni_theme.py --theme omni-light --store <store>.myshopify.com --token <TOKEN>`\n")
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Built", len(built), "themes in", OUT)
    for name, d in built:
        print(" -", name, "->", d)

if __name__ == "__main__":
    main()
