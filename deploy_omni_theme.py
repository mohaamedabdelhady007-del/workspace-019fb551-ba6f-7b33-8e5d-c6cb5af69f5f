#!/usr/bin/env python3
"""
deploy_omni_theme.py
====================
Push one of the generated OMNI UK themes to a live Shopify store via the
Admin REST API (same approach used for the D99 store).

Usage:
  python3 deploy_omni_theme.py --theme omni-light \
      --store your-store.myshopify.com \
      --token shpat_XXXXXXXX

The token is read from --token, else from env SHOPIFY_ADMIN_TOKEN,
else from a local file `shopify_token.txt`. The new theme is created as
UNPUBLISHED so it never overwrites your live theme — preview it, then
publish from Shopify Admin when ready.

Requires: requests  (pip install requests)
"""

import os
import sys
import json
import base64
import argparse

try:
    import requests
except ImportError:
    sys.exit("Missing 'requests'. Install with: pip install requests")

ROOT = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(ROOT, "omni-uk-themes")
API_VERSION = "2026-07"

BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".woff", ".woff2", ".ttf", ".otf"}


def resolve_token(args):
    if args.token:
        return args.token
    if os.environ.get("SHOPIFY_ADMIN_TOKEN"):
        return os.environ["SHOPIFY_ADMIN_TOKEN"]
    tokfile = os.path.join(ROOT, "shopify_token.txt")
    if os.path.exists(tokfile):
        return open(tokfile).read().strip()
    return None


def collect_assets(theme_path):
    assets = []
    for dirpath, _, files in os.walk(theme_path):
        for fn in files:
            full = os.path.join(dirpath, fn)
            key = os.path.relpath(full, theme_path).replace(os.sep, "/")
            assets.append((key, full))
    # Stable, logical order: config -> layout -> templates -> sections -> snippets -> assets
    order = {"config": 0, "layout": 1, "templates": 2, "sections": 3, "snippets": 4, "assets": 5}
    assets.sort(key=lambda kv: (order.get(kv[0].split("/")[0], 9), kv[0]))
    return assets


def upload_asset(session, base, theme_id, key, full):
    ext = os.path.splitext(full)[1].lower()
    with open(full, "rb") as f:
        raw = f.read()
    if ext in BINARY_EXT:
        payload = {"asset": {"key": key, "attachment": base64.b64encode(raw).decode("ascii")}}
    else:
        payload = {"asset": {"key": key, "value": raw.decode("utf-8", "replace")}}
    r = session.put(f"{base}/themes/{theme_id}/assets.json",
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"})
    if r.status_code >= 400:
        print(f"  ! FAIL {key}: {r.status_code} {r.text[:200]}")
        return False
    print(f"  + {key}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", required=True, help="theme folder name inside omni-uk-themes/ (e.g. omni-light)")
    ap.add_argument("--store", required=True, help="store domain, e.g. omni-uk.myshopify.com")
    ap.add_argument("--token", default=None, help="Shopify Admin API access token")
    ap.add_argument("--name", default=None, help="optional theme name on the store")
    ap.add_argument("--api", default=API_VERSION, help="Shopify API version")
    args = ap.parse_args()

    token = resolve_token(args)
    if not token:
        sys.exit("No token found. Pass --token, set SHOPIFY_ADMIN_TOKEN, or create shopify_token.txt")

    theme_path = os.path.join(THEMES_DIR, args.theme)
    if not os.path.isdir(theme_path):
        sys.exit(f"Theme not found: {theme_path}")

    base = f"https://{args.store}/admin/api/{args.api}"
    session = requests.Session()
    session.headers.update({
        "X-Shopify-Access-Token": token,
        "Accept": "application/json",
    })

    theme_name = args.name or f"OMNI — {args.theme}"
    print(f"Creating theme '{theme_name}' on {args.store} ...")
    r = session.post(f"{base}/themes.json", json={"theme": {"name": theme_name, "role": "unpublished"}})
    if r.status_code >= 400:
        sys.exit(f"Failed to create theme: {r.status_code} {r.text[:300]}")
    theme_id = r.json()["theme"]["id"]
    print(f"  theme id = {theme_id}")

    assets = collect_assets(theme_path)
    print(f"Uploading {len(assets)} assets ...")
    ok = 0
    for key, full in assets:
        if upload_asset(session, base, theme_id, key, full):
            ok += 1

    print(f"\nDone. {ok}/{len(assets)} assets uploaded.")
    print(f"Preview: https://{args.store}/?preview_theme_id={theme_id}")


if __name__ == "__main__":
    main()
