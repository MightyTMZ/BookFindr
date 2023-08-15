import os
import time
from bs4 import BeautifulSoup
from urllib.parse import quote
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


def getTopSearchResultsTPL(search_keywords):
    url_keywords = convert_string_to_url_keywords(search_keywords)
    tpl_base_search_url = "https://www.torontopubliclibrary.ca/search.jsp?Ntt="
    search_url = tpl_base_search_url + url_keywords
    book_urls = []
    print(search_url)

    try:
        retries = 3
        retry_delay = 2
        webpage = requests.get(search_url, headers=HEADERS)
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
                    return []

        soup = BeautifulSoup(webpage.content, "html.parser")  # Fix: Use webpage.content instead of search_url
        book_divs = soup.find_all('div', class_="title align-top")  # Fix: Use class_ instead of attrs

    except Exception as e:
        print(f"An error occurred: {e}")
        book_divs = []

    return book_divs



