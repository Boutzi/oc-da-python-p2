import csv

def write_csv(data, filename = "Data.csv"):
    fieldnames = [
    'product_page_url', 'upc', 'title', 'price_including_tax', 
    'price_excluding_tax', 'number_available', 'product_description', 
    'category', 'review_rating', 'image_url'
    ]
    if not data:
        return
    for item in data:
        for field in fieldnames:
            if field not in item:
                item[field] = ""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)