class Book:
    def __init__(self, url, upc, title, price, price_with_tax, quantity, category, rating, img_url, path):
        self.url = url
        self.upc = upc
        self.title = title
        self.price = price
        self.price_with_tax = price_with_tax
        self.quantity = quantity
        self.category = category
        self.rating = rating
        self.img_url = img_url
        self.path = path
        
    