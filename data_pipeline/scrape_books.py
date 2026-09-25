import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

books = []

for page in range(1, 6):  # first 5 pages

    url = base_url.format(page)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:

        title = article.h3.a["title"]

        price = article.find(
            "p",
            class_="price_color"
        ).text

        rating = article.p["class"][1]

        availability = article.find(
            "p",
            class_="instock availability"
        ).text.strip()

        books.append({
            "title": title,
            "price": price,
            "star_rating": rating,
            "availability": availability,
            "category": "All Products"
        })

df = pd.DataFrame(books)

print("Books Scraped:", len(df))

df.to_csv("raw_books.csv", index=False)

print("raw_books.csv created")