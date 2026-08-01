import urllib.request
import json
import os
import time

# DISTRICT-99 (D99) - SHOPIFY API BULK PRODUCTS UPLOADER
# هذا السكريبت يتصل مباشرة بـ Shopify Admin API ويقوم برفع الـ 18 منتج وتعديل المتغيرات والمخزون والصور تلقائياً!

STORE_URL = "district99-preview.myshopify.com"

# Read token safely from local file ignored by git
if os.path.exists("/home/user/.shopify_token"):
    with open("/home/user/.shopify_token", "r") as f:
        ACCESS_TOKEN = f.read().strip()
else:
    ACCESS_TOKEN = "shpat_YOUR_TOKEN_HERE"

# 1. قائمة تفاصيل الـ 18 منتج بدقة متناهية
products_list = [
    {
        "folder": "TSH-01",
        "handle": "tsh-01-smokingtime-oversized-tee",
        "title": "Smoking Time Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Smoking Time",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Smoking Time Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-02",
        "handle": "tsh-02-brand-pleasure-oversized-tee",
        "title": "Brand Pleasure Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Brand Pleasure",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Brand Pleasure Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-03",
        "handle": "tsh-03-balloon-dog-oversized-tee",
        "title": "Balloon Dog Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Balloon Dog",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Balloon Dog Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-04",
        "handle": "tsh-04-woman-stars-oversized-tee",
        "title": "Woman Stars Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Woman Stars",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Woman Stars Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-05",
        "handle": "tsh-05-abstract-rust-oversized-tee",
        "title": "Abstract Rust Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Abstract Rust",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Abstract Rust Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-06",
        "handle": "tsh-06-aura-oversized-tee",
        "title": "AURA Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, AURA",
        "color": "Charcoal Black",
        "description": "<p>Introducing the AURA Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-07",
        "handle": "tsh-07-welldone-oversized-tee",
        "title": "Welldone Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Welldone",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Welldone Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-08",
        "handle": "tsh-08-linear-faces-oversized-tee",
        "title": "Linear Faces Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Linear Faces",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Linear Faces Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-09",
        "handle": "tsh-09-starwave-wireframe-oversized-tee",
        "title": "Starwave Wireframe Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Starwave",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Starwave Wireframe Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-10",
        "handle": "tsh-10-ghosts-smoke-oversized-tee",
        "title": "Ghosts Smoke Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Ghosts Smoke",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Ghosts Smoke Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-11",
        "handle": "tsh-11-melt-spray-oversized-tee",
        "title": "Melt Spray Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Melt Spray",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Melt Spray Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-12",
        "handle": "tsh-12-never-break-purple-flames-oversized-tee",
        "title": "Never Break Purple Flames Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Purple Flames",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Never Break Purple Flames Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-13",
        "handle": "tsh-13-smoking-profile-cream-oversized-tee",
        "title": "Smoking Profile Cream Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Smoking Profile, Cream",
        "color": "Vintage Cream",
        "description": "<p>Introducing the Smoking Profile Cream Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-14",
        "handle": "tsh-14-desire-stencil-oversized-tee",
        "title": "Desire Stencil Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Desire Stencil",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Desire Stencil Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-15",
        "handle": "tsh-15-breathe-hands-oversized-tee",
        "title": "Breathe Hands Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Breathe Hands",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Breathe Hands Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-16",
        "handle": "tsh-16-fuxk-off-stencil-oversized-tee",
        "title": "Fuxk Off Stencil Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Fuxk Off",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Fuxk Off Stencil Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-17",
        "handle": "tsh-17-silence-hands-oversized-tee",
        "title": "Silence Hands Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Silence Hands",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Silence Hands Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    },
    {
        "folder": "TSH-18",
        "handle": "tsh-18-sopula-foggy-figures-oversized-tee",
        "title": "Sopula Foggy Figures Oversized Premium Graphic Tee",
        "tags": "Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Sopula, Foggy",
        "color": "Charcoal Black",
        "description": "<p>Introducing the Sopula Foggy Figures Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>"
    }
]

def upload_all_products():
    print("🚀 Starting DISTRICT-99 Shopify Bulk Upload...")
    
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    url = f"https://{STORE_URL}/admin/api/2026-07/products.json"
    
    sizes = ["S", "M", "L", "XL", "XXL"]
    
    for item in products_list:
        folder = item["folder"]
        title = item["title"]
        handle = item["handle"]
        color = item["color"]
        tags = item["tags"]
        desc = item["description"]
        
        # 2. تجهيز روابط صور المنتج من مستودع الـ GitHub مباشرة
        github_repo_url = "https://raw.githubusercontent.com/mohaamedabdelhady007-del/workspace-019fb551-ba6f-7b33-8e5d-c6cb5af69f5f/main/product/tshirt%2001%20to%2018"
        images_payload = [
            {"src": f"{github_repo_url}/{folder}/3d_mannequin.png"},
            {"src": f"{github_repo_url}/{folder}/pose_1.png"},
            {"src": f"{github_repo_url}/{folder}/pose_2.png"},
            {"src": f"{github_repo_url}/{folder}/pose_3.png"},
            {"src": f"{github_repo_url}/{folder}/pose_4.png"}
        ]
        
        # 3. تجهيز المتغيرات والمقاسات بالأسعار والأكواد
        variants_payload = []
        for s in sizes:
            variants_payload.append({
                "option1": s,
                "price": "950.00",
                "compare_at_price": "1200.00",
                "sku": f"D99-{folder}-BLK-{s}" if color == "Charcoal Black" else f"D99-{folder}-CRM-{s}",
                "inventory_management": "shopify",
                "inventory_policy": "deny",
                "fulfillment_service": "manual",
                "requires_shipping": True,
                "taxable": True,
                "grams": 300
            })
            
        product_payload = {
            "product": {
                "title": title,
                "body_html": desc,
                "vendor": "DISTRICT-99",
                "product_type": "Oversized T-Shirt",
                "handle": handle,
                "tags": tags,
                "options": [{"name": "Size", "values": sizes}],
                "variants": variants_payload,
                "images": images_payload,
                "status": "active"
            }
        }
        
        req_body = json.dumps(product_payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                p_id = res_json["product"]["id"]
                print(f"✅ Successfully uploaded: {title} (ID: {p_id})")
            time.sleep(1) # تأخير طفيف لتجنب حظر السيرفر للطلبات السريعة (Rate Limit)
        except urllib.error.HTTPError as e:
            print(f"❌ Failed to upload {title}: {e.read().decode('utf-8')}")
            
    print("\n🎉 ALL DISTRICT-99 PRODUCTS UPLOADED TO SHOPIFY SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    upload_all_products()
