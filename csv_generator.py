import csv
import os

def generate_shopify_csv(
    handle, title, body_html, vendor, product_type, tags,
    option1_name, option1_values, option2_name, option2_values,
    price, compare_at_price, weight_g, folder_name, output_path
):
    """
    Generates a Shopify-compliant product import CSV with variations and metadata.
    Omit image columns as per user's latest request.
    """
    headers = [
        "Handle", "Title", "Body (HTML)", "Vendor", "Standard Product Type", "Custom Product Type", 
        "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", 
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty", 
        "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", 
        "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Gift Card", "SEO Title", 
        "SEO Description", "Google Shopping / Google Product Category", "Variant Weight Unit", 
        "Variant Tax Code", "Cost per item", "Status"
    ]
    
    rows = []
    
    # Generate variant combinations (Size x Color)
    variant_index = 0
    for color in option2_values:
        for size in option1_values:
            row = {h: "" for h in headers}
            
            # First row gets main product details
            if variant_index == 0:
                row["Title"] = title
                row["Body (HTML)"] = body_html
                row["Vendor"] = vendor
                row["Custom Product Type"] = product_type
                row["Tags"] = tags
                row["Published"] = "true"
                row["Status"] = "active"
                row["Gift Card"] = "false"
            
            row["Handle"] = handle
            row["Option1 Name"] = option1_name
            row["Option1 Value"] = size
            row["Option2 Name"] = option2_name
            row["Option2 Value"] = color
            
            # SKU Format: D99-TSH-01-BLK-S
            color_code = color[:3].upper()
            row["Variant SKU"] = f"D99-{folder_name}-{color_code}-{size}"
            row["Variant Grams"] = str(weight_g)
            row["Variant Inventory Tracker"] = "shopify"
            row["Variant Inventory Qty"] = "100"
            row["Variant Inventory Policy"] = "deny"
            row["Variant Fulfillment Service"] = "manual"
            row["Variant Price"] = str(price)
            if compare_at_price:
                row["Variant Compare At Price"] = str(compare_at_price)
            row["Variant Requires Shipping"] = "true"
            row["Variant Taxable"] = "true"
            row["Variant Weight Unit"] = "g"
            
            rows.append(row)
            variant_index += 1
            
    # Write CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
            
    print(f"Shopify Product CSV successfully generated (without images) at: {output_path}")

if __name__ == "__main__":
    # Test generation for TSH-01
    generate_shopify_csv(
        handle="tsh-01-smokingtime-oversized-tee",
        title="Smoking Time Oversized Premium Graphic Tee",
        body_html="<p>Introducing the Smoking Time Oversized Premium Graphic Tee. Crafted from 280-300 GSM heavyweight premium cotton, featuring a custom vintage wash and relaxed drop-shoulder fit. Complete the signature DISTRICT-99 streetwear aesthetic.</p>",
        vendor="DISTRICT-99",
        product_type="Oversized T-Shirt",
        tags="Streetwear, Oversized, Heavyweight Cotton, Graphic Tee, D99, Smoking Time",
        option1_name="Size",
        option1_values=["S", "M", "L", "XL", "XXL"],
        option2_name="Color",
        option2_values=["Charcoal Black"],
        price="45.00",
        compare_at_price="65.00",
        weight_g=300,
        folder_name="TSH-01",
        output_path="/home/user/TSH-01/tsh-01-shopify-product.csv"
    )
