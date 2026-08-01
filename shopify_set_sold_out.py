import urllib.request
import json
import os
import time

# DISTRICT-99 (D99) - SHOPIFY INVENTORY SOLD-OUT SETTER
# هذا السكريبت يتصل بمتجرك ويقوم بتعيين مخزون جميع مقاسات التيشيرتات الـ 18 إلى 0 لتظهر كـ SOLD OUT فوراً!

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

def get_first_location_id():
    """
    Fetches the first location ID from Shopify (needed to modify inventory).
    """
    url = f"https://{STORE_URL}/admin/api/2026-07/locations.json"
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            location_id = res_json["locations"][0]["id"]
            print(f"📍 Found Shopify Location ID: {location_id}")
            return location_id
    except Exception as e:
        print(f"❌ Failed to fetch location: {e}")
        return None

def set_all_products_sold_out():
    print("⏳ Starting inventory update to SOLD OUT...")
    location_id = get_first_location_id()
    if not location_id:
        print("❌ Cannot proceed without Location ID.")
        return
        
    # Fetch all products (up to 50)
    url = f"https://{STORE_URL}/admin/api/2026-07/products.json?limit=50"
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            products = res_json["products"]
            print(f"📦 Found {len(products)} products on the store.")
            
            for p in products:
                print(f"🔄 Processing variants for product: {p['title']}")
                for v in p["variants"]:
                    inv_item_id = v["inventory_item_id"]
                    sku = v["sku"]
                    
                    # Set inventory level to 0
                    inv_url = f"https://{STORE_URL}/admin/api/2026-07/inventory_levels/set.json"
                    inv_payload = {
                        "location_id": location_id,
                        "inventory_item_id": inv_item_id,
                        "available": 0
                    }
                    
                    inv_body = json.dumps(inv_payload).encode("utf-8")
                    inv_req = urllib.request.Request(inv_url, data=inv_body, headers=headers, method="POST")
                    
                    try:
                        with urllib.request.urlopen(inv_req) as inv_res:
                            print(f"   ✅ Set SKU {sku} (Inventory ID: {inv_item_id}) to SOLD OUT (Qty: 0)")
                        time.sleep(0.5) # Avoid API rate limit
                    except Exception as e_inv:
                        print(f"   ❌ Failed to set inventory for SKU {sku}: {e_inv}")
                        
        print("\n🎉 ALL DISTRICT-99 PRODUCTS ARE NOW SET TO SOLD OUT! 🎉")
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")

if __name__ == "__main__":
    set_all_products_sold_out()
