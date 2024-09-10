import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class Category:
    def __init__(self, url):
        self.url = url
        self.name = []
        self.href = []
    
    def get_categories_names(self):
        res = requests.get(self.url)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html5lib')
            categories = soup.find("div", class_="side_categories").ul.find_all("a")
            for i in tqdm(categories, desc="Scraping categories name"):
                if 'Books' not in i.text:
                    self.name.append(i.text.replace('\n', '').replace('  ', ''))
            return self.name
        else:
            print("Error fetching NAMES:", res.status_code)
            
    def get_categories_href(self):
        res = requests.get(self.url)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html5lib')
            categories = soup.find("div", class_="side_categories").ul.find_all("a")
            for i in tqdm(categories, desc="Scraping categories name"):
                if 'books_1' not in i.get('href'):
                    self.href.append('http://books.toscrape.com/' + i.get("href"))
            return self.href
        else:
            print("Error fetching HREF:", res.status_code)
        