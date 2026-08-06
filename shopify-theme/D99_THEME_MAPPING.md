# D99 Theme Mapping

This Shopify theme package converts the supplied desktop mockups into Dawn-based Shopify templates.

## Mockup → Theme file mapping

- `d99_home_page.png` → `templates/index.json` + `sections/d99-home-grid.liquid`
- `d99_about_page.png` → `templates/page.about.json` + `sections/d99-about-manifesto.liquid`
- `d99_collection_page.png` → `templates/collection.json` + `sections/d99-main-collection.liquid`
- `d99_product_page.png` → `templates/product.json` + `sections/d99-main-product.liquid`
- `design_3_technical_blueprint.png` → `templates/product.blueprint.json` + `sections/d99-product-blueprint.liquid`
- `d99_cart_page.png` → `templates/cart.json` + `sections/d99-main-cart.liquid`
- `design_1_industrial_grid.png` → `templates/page.industrial-grid.json` + `sections/d99-industrial-grid-hero.liquid`

## Global shell

- Header: `sections/header.liquid`
- Footer: `sections/footer.liquid`
- Shared design system: `assets/d99-system.css`
- Logo assets:
  - `assets/d99-logo-header-black.png`
  - `assets/d99-logo-white.png`
  - `assets/d99-wordmark.png`

## Notes

- Desktop-first implementation is included.
- The visual shell, borders, grid paper background, stamps, mono typography, and brutalist panels are reusable across pages.
- To get pixel-perfect imagery for the about / home collage panels, upload the exact source images in the theme editor for each custom section.
