import os

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

# import updatedAmazon_search

load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}


def extractTopSearchResultInformation(book_list):
    book_json_objects = []
    for book_url in book_list:
        webpage = requests.get(book_url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        audible_price_tag = soup.find('span', attrs={'class': 'audible_mm_price'})
        # price_error_message = "Unable to find price."
        unable_to_find = 'Unable to retrieve data.'

        title = soup.find("span", attrs={'data-cel-widget': 'productTitle'})
        title_text = title.text.strip() if title else "Could not find title"

        product_image = soup.find("img", attrs={"id": "imgBlkFront"})
        product_image_src = product_image.get('src') if product_image else "Could not find"

        main_price = soup.find("span", attrs={'class': 'a-size-base a-color-price a-color-price'})
        main_price_text = main_price.text.strip() if main_price else "Could not find"

        kindle_price = soup.find("span", attrs={'class': "a-size-base a-color-secondary"})
        kindle_price_text = kindle_price.text.strip() if kindle_price else "Could not find"

        audible_price_text = unable_to_find
        if audible_price_tag:
            audible_price = audible_price_tag.find("span", attrs={'class': "a-color-secondary"})
            audible_price_text = audible_price.text.strip() if audible_price else unable_to_find

        availability_div = soup.find("div", attrs={'id': 'availability'})
        availability_status_text = unable_to_find

        if availability_div:
            availability_status = availability_div.find("span", attrs={"class": "a-size-medium a-color-success"})
            availability_status_text = availability_status.text.strip() if availability_status else unable_to_find

        book_object = {
            "product_image": product_image_src,
            "title": title_text,
            "main_price": main_price_text,
            "kindle_price": kindle_price_text,
            "audible_price": audible_price_text,
            "availability": availability_status_text,
            "link": book_url
        }

        book_json_objects.append(book_object)

    return book_json_objects


"""course = "ap chemistry"
print(extractTopSearchResultInformation(updatedAmazon_search.getTopSearchResults(course)))"""
