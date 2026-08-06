import json
import os
import urllib.request
from pathlib import Path

STORE_URL = os.environ.get("SHOPIFY_STORE", "rvsdgy-e1.myshopify.com")
REPO_ROOT = Path(__file__).resolve().parent
SECTION_FILE = REPO_ROOT / "shopify-theme" / "sections" / "d99-home-grid.liquid"
INDEX_TEMPLATE = REPO_ROOT / "shopify-theme" / "templates" / "index.json"
THEME_NAME_HINT = os.environ.get("SHOPIFY_THEME_NAME", "Horizon")


def read_token():
    candidates = [Path.home() / ".shopify_token", Path("/home/user/.shopify_token")]
    for path in candidates:
        if path.exists():
            token = path.read_text(encoding="utf-8").strip()
            if token:
                return token
    raise RuntimeError("No Shopify token found. Save it to ~/.shopify_token first.")


def request_json(url, token, method="GET", payload=None):
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def get_live_horizon_theme(token):
    url = f"https://{STORE_URL}/admin/api/2026-07/themes.json"
    themes = request_json(url, token)["themes"]

    for theme in themes:
        if theme.get("role") == "main" and THEME_NAME_HINT.lower() in theme.get("name", "").lower():
            return theme

    for theme in themes:
        if theme.get("role") == "main":
            return theme

    raise RuntimeError("Could not find a live theme.")


def upload_asset(token, theme_id, key, value):
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"
    payload = {"asset": {"key": key, "value": value}}
    request_json(url, token, method="PUT", payload=payload)
    print(f"Uploaded: {key}")


def main():
    token = read_token()
    theme = get_live_horizon_theme(token)
    print(f"Target live theme: {theme['name']} (ID: {theme['id']})")

    section_code = SECTION_FILE.read_text(encoding="utf-8")
    index_json = INDEX_TEMPLATE.read_text(encoding="utf-8")

    upload_asset(token, theme["id"], "sections/d99-home-grid.liquid", section_code)
    upload_asset(token, theme["id"], "templates/index.json", index_json)

    print("\nDone. Homepage was pushed to the live theme.")
    print(f"Storefront: https://{STORE_URL}")
    print(f"Customizer: https://{STORE_URL}/admin/themes/{theme['id']}/editor")


if __name__ == "__main__":
    main()
