import csv
import json

# Initialize lists and counters
categories = {}
subcategories = {}
category_pk = 1

store = {"model": "inventory.store", "pk": 1, "fields": {"name": "Chakkiwale"}}
store_pk = store["pk"]

inventory = []
inventory_pk = 1

imageUrls = [
    "https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/3737645/pexels-photo-3737645.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1211887/pexels-photo-1211887.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/11809347/pexels-photo-11809347.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/6287581/pexels-photo-6287581.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/326082/pexels-photo-326082.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://example.com/images/finger_millet.jpg",
    "https://images.pexels.com/photos/932587/pexels-photo-932587.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://example.com/images/almond_flour.jpg",
    "https://images.pexels.com/photos/90894/pexels-photo-90894.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/4725726/pexels-photo-4725726.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://example.com/images/canola_oil.jpg",
]

UNIT_MAPPING = ["kg", "g", "l", "ml", "p"]

# Read from CSV file
with open("inventory_data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    index = 0
    for row in reader:
        name = row["Name"]
        code = row["Item Code"]
        price = float(row["Selling Price"])
        amount = float(row["Qty"])
        category = row["Category"].lower().replace(", ", "_").replace(" ", "_")
        subcategory = row["Sub Category"].lower().replace(", ", "_").replace(" ", "_")
        status = row["Status"].lower()

        if category not in categories:
            categories[category] = {
                "model": "inventory.category",
                "pk": category_pk,
                "fields": {"name": category, "path": category, "parent": None},
            }
            category_pk += 1

        if subcategory and subcategory not in subcategories:
            subcategories[subcategory] = {
                "model": "inventory.category",
                "pk": category_pk,
                "fields": {
                    "name": subcategory,
                    "path": f"{category}.{subcategory}",
                    "parent": categories[category]["pk"],
                },
            }
            category_pk += 1

        if subcategory:
            category = subcategories[subcategory]["pk"]
        else:
            category = categories[category]["pk"]

        inventory.append(
            {
                "model": "inventory.inventory",
                "pk": int(inventory_pk),
                "fields": {
                    "name": name,
                    "code": code,
                    "visible": status == "active",
                    "price": f"{price:.2f}",
                    "max_price": f"{price:.2f}",
                    "amount": f"{amount:.3f}",
                    "executed_amount": "0.000",
                    "unit": UNIT_MAPPING[index % len(UNIT_MAPPING)],
                    "image_url": imageUrls[index % len(imageUrls)],
                    "note": "",
                    "description": "",
                    "store": store_pk,
                    "category": category,
                },
            }
        )
        inventory_pk += 1
        index += 1

# Prepare output structure
categories_list = list(categories.values())
subcategories_list = list(subcategories.values())

output = categories_list + subcategories_list + [store] + inventory

# Write output to JSON file
with open("inventory_data.json", "w") as jsonfile:
    json.dump(output, jsonfile, indent=2)

print("Data has been written to inventory_data.json")
