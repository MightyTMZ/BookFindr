import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}



def convert_string_to_url_keywords(word):
    listed_word = list(word)
    for index in range(len(listed_word)):
        if listed_word[index] == " ":
            listed_word[index] = "+"

    url_keywords = ""
    for letter in listed_word:
        url_keywords += letter

    return url_keywords


def getTopSearchResultsIndigo(search_keywords):
    url_keywords = convert_string_to_url_keywords(search_keywords)
    indigo_base_search_url = "https://www.indigo.ca/en-ca/search?q="
    search_url = urljoin(indigo_base_search_url, f"?keywords={url_keywords}&search-button=&lang=en_CA")

    book_urls = []
    print(search_url)

    try:
        retries = 3
        retry_delay = 2

        while retries > 0:
            try:
                webpage = requests.get(search_url, headers=HEADERS)
                webpage.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                print(f"Error while making the request: {e}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff for the next retry
                else:
                    print("Max retries exceeded. Unable to fetch the page.")

        soup = BeautifulSoup(webpage.content, "html.parser")
        resultsDiv = soup.find('div', class_='row product-grid mt-4 search-analytics')  # Fix: Use find instead of find_all
        if resultsDiv:
            book_divs = resultsDiv.find_all("div", class_='tiles col-6 col-lg-4 px-lg-1 searchProductTiles')
            if book_divs:
                for book in book_divs:
                    current_book_instance = book.find('a', attrs={'data-a8n': "productTiles_productImage_link"})
                    current_book_url = "https://www.indigo.ca" + current_book_instance.get('href')
                    book_urls.append(current_book_url)

        return book_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        book_urls = []
        return book_urls



