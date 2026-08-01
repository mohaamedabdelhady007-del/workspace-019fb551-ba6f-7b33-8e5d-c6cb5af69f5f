import urllib.request
import json
import os
import glob

# DISTRICT-99 (D99) - SHOPIFY API BULK PRODUCTS UPLOADER
# هذا السكريبت مجهز بالكامل للاتصال المباشر بمتجرك عبر الـ API ورفع الـ 18 تيشيرت تلقائياً بالصور والمقاسات!

def upload_product_to_shopify(store_url, access_token, product_data):
    """
    Connects to Shopify Admin REST API to create a product with variants.
    """
    url = f"https://{store_url}/admin/api/2026-07/products.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    req_data = {"product": product_data}
    req_body = json.dumps(req_data).encode("utf-8")
    
    req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            product_id = res_json["product"]["id"]
            print(f"✅ Successfully uploaded: {product_data['title']} (ID: {product_id})")
            return product_id
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to upload product: {e.read().decode('utf-8')}")
        return None

def prepare_tshirt_payload(folder_name, handle, title, body_html, price, compare_at_price, image_cdn_urls):
    """
    Generates the standard product payload with S to XXL sizing variants and linked image URLs.
    """
    sizes = ["S", "M", "L", "XL", "XXL"]
    variants = []
    
    # Generate S to XXL Sizing Variants with SKUs and Pricing
    for size in sizes:
        variants.append({
            "option1": size,
            "price": str(price),
            "compare_at_price": str(compare_at_price) if compare_at_price else None,
            "sku": f"D99-{folder_name}-BLK-{size}",
            "inventory_management": "shopify",
            "inventory_policy": "deny",
            "fulfillment_service": "manual",
            "requires_shipping": True,
            "taxable": True,
            "grams": 300
        })
        
    # Map the 5 product images to the product
    images_payload = []
    for url in image_cdn_urls:
        images_payload.append({"src": url})
        
    payload = {
        "title": title,
        "body_html": body_html,
        "vendor": "DISTRICT-99",
        "product_type": "Oversized T-Shirt",
        "handle": handle,
        "tags": f"Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, {folder_name}",
        "options": [{"name": "Size", "values": sizes}],
        "variants": variants,
        "images": images_payload,
        "status": "active"
    }
    return payload

if __name__ == "__main__":
    # هذا مجرد كود توضيحي، وبمجرد إرسالك للـ Token والـ Store URL سنقوم بتشغيل المولد الفعلي ورفع الـ 18 تيشيرت بالكامل!
    print("🤖 D99 Auto-Uploader is ready to launch!")
