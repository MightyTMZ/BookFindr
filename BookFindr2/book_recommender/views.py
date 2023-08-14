from . import updatedAmazon_book_scraper
from . import updatedAmazon_search
from .TorontoPublicLibrary_book_scraper import *
from .TorontoPublicLibrary_search import *
from .Indigo_book_search import *
from .Indigo_book_scraper import *
import requests
from django.http import JsonResponse
from django.shortcuts import render
import logging
import openai
import json


load_dotenv()

# Use environment variables for headers and OpenAI API key
HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE")
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_answer_from_chatgpt(prompt_input, system_content=None, model="gpt-3.5-turbo-0613"):
    if system_content is None:
        system_content = "You are an AI assistant for answering questions " \
                         "based on the extracted parts of a long document"

    openai.api_key = OPENAI_API_KEY

    # Set up OpenAI API and make the API call
    answer = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt_input}
        ],
        temperature=0.4,
        max_tokens=1000
    )

    # Step 2: Extract the answer
    wit_response = answer["choices"][0]["message"]["content"]
    return wit_response


def chat_with_gpt(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            personal_interests = data.get("personalInterests")
            past_reading_experiences = data.get("pastReadingExperiences")
            age_group = data.get('ageGroup')
            specific_needs = data.get('specificNeeds')
            # search_path_url = "/book-generator/search"
            prompt_input = f"Personal Interests: {personal_interests}\nPast Reading Experiences: {past_reading_experiences}\nMy age is {age_group}\n As for my specific needs they are: {specific_needs}\nCan you give me some appropriate book recommendations for a person my age? One tip, can you write the book titles using single quotes followed by the author. Thanks!"
            chat_response = get_answer_from_chatgpt(prompt_input)
            convert_chat_response_to_html = get_answer_from_chatgpt(f'''In the chat response below:\n{chat_response}\n Can you extract all the book titles plus the author and convert each of them to a paragraph element? For example: <p>'The Art of Computer Programming' by Donald E. Knuth</p>. Make sure just to give the HTML content as this exact text will be sent as the innerHTML. Thanks!''')
            soup = BeautifulSoup(convert_chat_response_to_html, 'html.parser')

            # print(convert_chat_response_to_html)
            valid_links = []
            for link in soup.find_all('a'):
                book_title = link.text.strip()
                author = book_title.split("' by ")[1]
                book_title = book_title.split("' by ")[0][1:]
                href = link.get('href')
                target = link.get('target', '_self')  # Default value is '_self' if 'target' attribute is not present
                valid_links.append({"title": book_title, "author": author, "href": href, "target": target})
            '''print(prompt_input)
            print(chat_response)
            print(valid_links)'''

            return JsonResponse({
                "chatResponse": chat_response,
                "htmlLinks": valid_links
            })

        except requests.exceptions.RequestException as e:
            logger = logging.getLogger(__name__)
            logger.error("API Error: %s", e)
    # Handle any other request method (e.g., GET) with a default response
    return render(request, "book-recommendation.html")


def search_book(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON data sent from the frontend
            book = data.get("search-book")

            # Replace the following lines with your actual processing logic
            top_search_results = updatedAmazon_search.getTopSearchResults(book)
            top_search_results_info = updatedAmazon_book_scraper.extractTopSearchResultInformation(top_search_results)

            tpl_results_data = getTopSearchResultsTPL(book)
            tpl_results_info = getTopSearchResultsInfoTPL(tpl_results_data)

            indigo_results_data = getTopSearchResultsIndigo(book)
            indigo_results_info = getTopSearchResultsInfoIndigo(indigo_results_data)

            response_data = {
                'topSearchResults': top_search_results_info,
                'topSearchResultsTPL': tpl_results_info,
                'topSearchResultsIndigo': indigo_results_info
            }

            return JsonResponse(response_data)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("An error occurred while processing the request:")
            return JsonResponse({"error": str(e)}, status=500)  # Return the exception message

    return render(request, "search_book.html")


def search_book_view(request):
    return render(request, 'search_book.html', context={})
