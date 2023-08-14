import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}


def convert_string_to_search_engine_keywords(search_item):
    if search_item is not None:
        return quote(str(search_item))
    return ""


def getTopSearchResults(search_item):
    amazon_ca_search_url = "https://www.amazon.ca/s?k="
    search_result_url = amazon_ca_search_url + convert_string_to_search_engine_keywords(search_item)
    print(search_result_url)
    book_urls = []

    try:
        retries = 3
        retry_delay = 2

        while retries > 0:
            try:
                webpage = requests.get(search_result_url, headers=HEADERS)
                webpage.raise_for_status()
                break  # Success, break out of the retry loop
            except requests.exceptions.RequestException as e:
                print(f"Error while making the request: {e}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff for the next retry
                else:
                    print("Max retries exceeded. Unable to fetch the page.")
                    return []

        soup = BeautifulSoup(webpage.content, "html.parser")
        product_links = soup.find_all('a',
                                      attrs={
                                          'class': "a-link-normal s-underline-text s-underline-link-text s-link-style "
                                                   "a-text-normal"})

        # If the number of links is less than 3, iterate through the available links
        if len(product_links) < 3:
            for link in product_links:
                current_product_link = link.get('href')
                if current_product_link:
                    book_urls.append("https://www.amazon.ca" + current_product_link)
        else:
            for link in product_links[:3]:
                current_product_link = link.get('href')
                if current_product_link:
                    book_urls.append("https://www.amazon.ca" + current_product_link)

        return book_urls

    except Exception as e:
        book_urls = []
        return book_urls