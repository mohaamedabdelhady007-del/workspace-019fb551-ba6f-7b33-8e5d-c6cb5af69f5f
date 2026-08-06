import urllib.request
import urllib.error
import json
import time
import os
import subprocess
from pathlib import Path

# DISTRICT-99 (D99) - SHOPIFY IMAGE RESYNCER & FORCE UPDATER
# يربط صور المنتجات الحالية من GitHub بمنتجات شوبيفاي باستخدام آخر commit من هذا الريبو.

STORE_URL = "district99-preview.myshopify.com"
GITHUB_REPO = "mohaamedabdelhady007-del/workspace-019fb551-ba6f-7b33-8e5d-c6cb5af69f5f"
REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_GIT_REF = "094655ffe1ca035a8f08a69a5189422c9929e843"


def current_git_ref():
    env_ref = os.environ.get("D99_GIT_REF", "").strip()
    if env_ref:
        return env_ref
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return DEFAULT_GIT_REF


def github_raw_base():
    git_ref = current_git_ref()
    return (
        f"https://raw.githubusercontent.com/{GITHUB_REPO}/{git_ref}/"
        "product/tshirt%2001%20to%2018"
    )


# Read token safely from local file ignored by git
if os.path.exists("/home/user/.shopify_token"):
    with open("/home/user/.shopify_token", "r") as f:
        ACCESS_TOKEN = f.read().strip()
else:
    ACCESS_TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

PRODUCT_FOLDER_MAP = {
    "tsh-01-smokingtime-oversized-tee": "TSH-01",
    "tsh-02-brand-pleasure-oversized-tee": "TSH-02",
    "tsh-03-balloon-dog-oversized-tee": "TSH-03",
    "tsh-04-woman-stars-oversized-tee": "TSH-04",
    "tsh-05-abstract-rust-oversized-tee": "TSH-05",
    "tsh-06-aura-oversized-tee": "TSH-06",
    "tsh-07-welldone-oversized-tee": "TSH-07",
    "tsh-08-linear-faces-oversized-tee": "TSH-08",
    "tsh-09-starwave-wireframe-oversized-tee": "TSH-09",
    "tsh-10-ghosts-smoke-oversized-tee": "TSH-10",
    "tsh-11-melt-spray-oversized-tee": "TSH-11",
    "tsh-12-never-break-purple-flames-oversized-tee": "TSH-12",
    "tsh-13-smoking-profile-cream-oversized-tee": "TSH-13",
    "tsh-14-desire-stencil-oversized-tee": "TSH-14",
    "tsh-15-breathe-hands-oversized-tee": "TSH-15",
    "tsh-16-fuxk-off-stencil-oversized-tee": "TSH-16",
    "tsh-17-silence-hands-oversized-tee": "TSH-17",
    "tsh-18-sopula-foggy-figures-oversized-tee": "TSH-18",
}


def require_token():
    if not ACCESS_TOKEN:
        raise RuntimeError(
            "No Shopify access token found. Add /home/user/.shopify_token or set SHOPIFY_ACCESS_TOKEN."
        )


def resolve_folder(product):
    handle = product.get("handle", "")
    if handle in PRODUCT_FOLDER_MAP:
        return PRODUCT_FOLDER_MAP[handle]

    tags = product.get("tags", "")
    for tag in tags.split(","):
        tag_clean = tag.strip().upper()
        if tag_clean.startswith("TSH-") and len(tag_clean) == 6:
            return tag_clean

    variants = product.get("variants", [])
    if variants:
        sku = variants[0].get("sku", "")
        for prefix in PRODUCT_FOLDER_MAP.values():
            if prefix in sku.upper():
                return prefix

    return None


def build_images(folder_name):
    base = github_raw_base()
    return [
        {"src": f"{base}/{folder_name}/3d_mannequin.png"},
        {"src": f"{base}/{folder_name}/pose_1.png"},
        {"src": f"{base}/{folder_name}/pose_2.png"},
        {"src": f"{base}/{folder_name}/pose_3.png"},
        {"src": f"{base}/{folder_name}/pose_4.png"},
    ]


def force_resync_product_images():
    require_token()
    git_ref = current_git_ref()
    print("🚀 Starting DISTRICT-99 Shopify Image Force-Update...")
    print(f"🔗 Using Git ref: {git_ref}")

    url = f"https://{STORE_URL}/admin/api/2026-07/products.json?limit=50"
    req = urllib.request.Request(url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as response:
        res_json = json.loads(response.read().decode("utf-8"))
        products = res_json["products"]
        print(f"📦 Found {len(products)} products on the store to update.")

    for p in products:
        product_id = p["id"]
        title = p["title"]
        folder_name = resolve_folder(p)

        if not folder_name:
            print(f"⚠️ Could not resolve folder name for {title}, skipping.")
            continue

        print(f"\n🔄 Updating images for: {title} ({folder_name})")
        update_url = f"https://{STORE_URL}/admin/api/2026-07/products/{product_id}.json"
        update_payload = {
            "product": {
                "id": product_id,
                "images": build_images(folder_name)
            }
        }

        update_body = json.dumps(update_payload).encode("utf-8")
        update_req = urllib.request.Request(update_url, data=update_body, headers=headers, method="PUT")

        try:
            with urllib.request.urlopen(update_req):
                print(f"   ✅ Successfully linked 5 refreshed transparent images for {title}!")
            time.sleep(1.25)
        except urllib.error.HTTPError as e_up:
            print(f"   ❌ Failed to update images for {title}: {e_up.read().decode('utf-8')}")
        except Exception as e_up:
            print(f"   ❌ Failed to update images for {title}: {e_up}")

    print("\n🎉 ALL SHOPIFY PRODUCTS REFRESHED WITH THE LATEST PRODUCT IMAGES! 🎉")


if __name__ == "__main__":
    force_resync_product_images()
