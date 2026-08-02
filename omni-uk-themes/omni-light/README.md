# OMNI — Light Editorial

Shopify Online Store 2.0 theme — part of the OMNI UK theme pack.

Design direction: homepage/product/collection mockups (bright, airy minimal)
Palette:
  background : #f5f4f2
  foreground : #141414
  accent     : #141414

How to upload:
  1) ZIP this folder and upload via Shopify Admin -> Online Store -> Themes -> Upload theme, OR
  2) Run:  python3 deploy_omni_theme.py --theme omni-light --store <store.myshopify.com> --token <ADMIN_API_TOKEN>

After upload, open the theme customizer to:
  - pick the hero image (defaults to omni-hero-left.png bundled in assets/)
  - drop product/model shots into the Lookbook (Bento) panels
  - set the Featured collection
