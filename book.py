import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
class Book:
    def __init__(self, url):
        self.url = url
        self.href = []
    
    def get_soup(self, custom_url):
        res = requests.get(custom_url)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            html = res.text
            return html
        else:
            return f"Error getting soup: {res.status_code}"
        
    def get_all_pages_links(self, number_of_pages):
        for i in tqdm(range(number_of_pages + 1), desc="Scraping all pages links"):
            if i != 0:
                html = self.get_soup(f"{self.url}page-{i}.html")
                soup = BeautifulSoup(html, 'html5lib')
                book_links_divs = soup.find_all("div", class_="image_container")
                for div in book_links_divs:
                    a_tag = div.find("a").get("href").replace("../../", "")
                    self.href.append(f"http://books.toscrape.com/catalogue/{a_tag}")
            else:
                continue
        return self.href
        
    def get_one_page_link(self, number_of_the_page):
        html = self.get_soup(f"{self.url}page-{number_of_the_page}.html")
        soup = BeautifulSoup(html, 'html5lib')
        book_links_divs = soup.find_all("div", class_="image_container")
        for div in tqdm(book_links_divs, desc="Scraping page link"):
            a_tag = div.find("a").get("href").replace("../../", "")
            self.href.append(f"http://books.toscrape.com/catalogue/{a_tag}")
        return self.href
        
    def get_number_of_pages(self):
        html = self.get_soup(self.url)
        if html != None:
            soup = BeautifulSoup(html, "html5lib")
            form = soup.find("form", class_="form-horizontal")
            strong = form.find_all("strong")
            strong_infos = []
            for i in strong:
                strong_infos.append(int(i.text))
            number_of_pages = int(strong_infos[0] / strong_infos[2])
            return number_of_pages
        else:
            print("Error getting number of pages.")
            
    def get_book_data(self, book_link):
        book_info = {}
        html = self.get_soup(book_link)
        soup = BeautifulSoup(html, "html5lib")
        book_info.update({ "product_page_url" : book_link })
        book_info.update(self.get_book_upc(soup))
        book_info.update(self.get_book_title(soup))
        book_info.update(self.get_book_price_exc(soup))
        book_info.update(self.get_book_price_inc(soup))
        book_info.update(self.get_book_number_available(soup))
        book_info.update(self.get_book_description(soup))
        book_info.update(self.get_book_category(soup))
        book_info.update(self.get_book_rating(soup))
        book_info.update(self.get_book_image_url(soup))
        return book_info
        
    def get_book_upc(self, soup):
        for tr in soup.find_all("tr"):
            if "UPC" in tr.text:
                return { "universal_ product_code": tr.td.text }
        
    def get_book_title(self, soup):
        return {'title': soup.h1.text}
    
    def get_book_price_exc(self, soup):
        for tr in soup.find_all("tr"):
            if "Price (excl. tax)" in tr.text:
                return {'price_including_tax': tr.td.text}
    
    def get_book_price_inc(self, soup):
        for tr in soup.find_all("tr"):
            if "Price (incl. tax)" in tr.text:
                return {'price_excluding_tax': tr.td.text}
    
    def get_book_number_available(self, soup):
        for tr in soup.find_all("tr"):
            if "Availability" in tr.text:
                availability_text = tr.td.text.strip()
                match = re.search(r'\((\d+)\savailable\)', availability_text)
                if match:
                    number_available = int(match.group(1))
                    return {'number_available': number_available}
                else:
                    return {'number_available': 0}
    
    def get_book_description(self, soup):
        article = soup.find("article", class_="product_page")
        desc = article.find("p", class_= None)
        if desc:
            return {'product_description': desc.text}
        else:
            return {'product_description': ""}
    
    def get_book_category(self, soup):
        ul = soup.find("ul", class_="breadcrumb")
        category = ul.find_all("a")
        return {'category': category[len(category) - 1].text}
    
    def get_book_rating(self, soup):
        p_tag = soup.find("p", class_="star-rating")
        if p_tag:
            classes = p_tag.get('class', [])
            if 'One' in classes[1]:
                return { 'review_rating': 1 }
            elif 'Two' in classes[1]:
                return { 'review_rating': 2 }
            elif 'Three' in classes[1]:
                return { 'review_rating': 3 }
            elif 'Four' in classes[1]:
                return { 'review_rating': 4 }
            elif 'Five' in classes[1]:
                return { 'review_rating': 5 }
            else:
                return { 'review_rating': 0 }
        else:
            return { 'review_rating': 0 }
        
    def get_book_image_url(self, soup):
        thumbnail = soup.find("div", class_="thumbnail")
        image = thumbnail.find("img")
        image_url = image.get("src").replace("../../", "")
        return { "image_url" : "https://books.toscrape.com/" + image_url }