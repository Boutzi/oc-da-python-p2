from book import Book
from category import Category
from tqdm import tqdm
from csv_builder import write_csv

root_url = "http://books.toscrape.com/index.html"
url_for_books = "http://books.toscrape.com/catalogue/category/books_1/"

# 0 = all | -1 = by category
page = -1
category = "Poetry"

if __name__ == "__main__":
    books_data = []
    category_instance = Category(root_url)
    books_instance = Book(url_for_books)
    print(f"=> Scraping {root_url}")
    if page == 0:
        book_links = books_instance.get_all_pages_links(books_instance.get_number_of_pages())
        print(f"=> Scraped {len(book_links)} book links.")

        for book_link in tqdm(book_links, desc="Scraping books data"):
            books_data.append(books_instance.get_book_data(book_link))
        print(f"=> Scraped {len(books_data)} books.")
        
        write_csv(books_data)
    elif page == -1:
        # categories = { "names": category_instance.get_categories_names() }
        # print(f"=> Scraped {len(categories["names"])} category names.")
        
        # categories = { "href": category_instance.get_categories_href() }
        # print(f"=> Scraped {len(categories["href"])} category links.")
        
        # for category_link in tqdm(categories["href"], desc="Scraping books by category"):
        #     books_data.append(books_instance.get_book_data(category_link))
        print(f"=> Scraped {category.capitalize()} books.")
        
        # write_csv(books_data, f"{category.capitalize()}_data.csv")
    else:
        book_links = books_instance.get_one_page_link(page)
        print(f"=> Scraped {len(book_links)} book links.")

        for book_link in tqdm(book_links, desc="Scraping books data"):
            books_data.append(books_instance.get_book_data(book_link))
        print(f"=> Scraped {len(books_data)} books.")
        
        write_csv(books_data, f"Page_{page}_data.csv")
        
    print(f"=> Scraping complete.")
