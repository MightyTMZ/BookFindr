import os
from bs4 import BeautifulSoup
import requests
import json
from dotenv import load_dotenv


load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}


def getTopSearchResultsInfoIndigo(book_list):
    book_objects = []
    for book_url in book_list:  # Loop through the URLs in the list
        webpage = requests.get(book_url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        title = soup.find('h1', class_="product-name font-weight-mid")
        title_text = title.text.strip() if title else "Title not found"

        release_date = soup.find('span', class_="release-date")
        release_date_text = release_date.text.strip() if title else "Release date not found"

        price = soup.find('span', class_="value")
        price_text = price.text.strip() if price else "Price not found"

        author = soup.find('a', class_="author-name label-4")
        author_text = author.text.strip() if author else "Author not found"

        product_image = soup.find('img', class_="d-block img-fluid")
        product_image_src = product_image.get('src') if product_image else "N/A"

        access_link = book_url

        book_json_obj = {
            "title": title_text,
            "release_date": release_date_text,
            "price": price_text,
            'author': author_text,
            "book_cover": product_image_src,
            "access_link": access_link
        }

        book_objects.append(book_json_obj)

    return book_objects


