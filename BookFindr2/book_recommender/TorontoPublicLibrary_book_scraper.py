import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}


# THIS FUNCTION IS USED TO CLEAN UP THE MESSY DATA FOR THE HOLDS
def getNumberInAString(string):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    string2 = list(string)

    numeric_chars = [char for char in string2 if char in numbers]
    final_num = ''.join(numeric_chars)

    return final_num


def getTopSearchResultsInfoTPL(list_of_books):
    book_information = []

    for book_html_content in list_of_books:
        link = book_html_content.find('a', class_=False, id=False)['href']
        title = book_html_content.find('span', class_='notranslate').text.strip()
        book_link = urljoin("https://www.torontopubliclibrary.ca", link)

        book_page = requests.get(book_link, headers=HEADERS).content
        book_soup = BeautifulSoup(book_page, 'html.parser')  # Parse the content

        number_of_holds_element = book_soup.find("span", class_='holds')
        number_of_copies_element = book_soup.find("span", id='number-copies')
        bib_info = book_soup.find("div", class_="bib-info")

        if number_of_holds_element:
            number_of_holds = number_of_holds_element.text.strip()
        else:
            number_of_holds = "N/A"

        if number_of_copies_element:
            number_of_copies = number_of_copies_element.text.strip()
        else:
            number_of_copies = "N/A"

        year = bib_info.find_all("span", class_="text")[0].text.strip()
        type_of_media = bib_info.find_all("span", class_="text")[1].text.strip()
        print_length = bib_info.find_all("span", class_="text")[2].text.strip()

        # image_div = book_soup.find('div', attrs={'class': "main-image"})
        image_src = "https://www.torontopubliclibrary.ca/images/bibs/LC/no-image-book.svg"
        book_obj = {
            "title": title,
            "link": book_link,
            'holds_info': f"{getNumberInAString(number_of_holds)} holds / {number_of_copies} copies",
            "year": year,
            "type": type_of_media,
            'print_length': f"{getNumberInAString(print_length)} pages",
            "book_image": image_src
        }
        book_information.append(book_obj)

    return book_information


'''x = "AP Physics"
results = getTopSearchResultsTPL(x)
y = getTopSearchResultsInfoTPL(results)
formatted_json = json.dumps(y, indent=4)
print(formatted_json)'''
