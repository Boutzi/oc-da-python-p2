import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"

res = requests.get(url)
res.encoding = res.apparent_encoding

if res.status_code == 200:
    print("Success:", res.status_code)
    html = res.text
        
    with open("scrapped.html", "w") as file:
        file.write(html)
        
    soup = BeautifulSoup(html, 'html5lib')
    element = soup.find("h1").text.strip()
    print("Element H1 for testing:", element)
else:
    print("Error:", res.status_code)