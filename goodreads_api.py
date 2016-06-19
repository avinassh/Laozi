import re

import requests
import xmltodict
from xml.parsers.expat import ExpatError
from py_bing_search import PyBingWebSearch

from settings import GOODREADS_API_KEY, BING_SEARCH_API_KEY

goodreads_api_key = GOODREADS_API_KEY


class BookNotFound(Exception):
    pass


# deprecated
def get_top_google_goodreads_search(search_term):
    # For a give search term, it searches Goodreads using Google and returns
    # top 4 result urls
    query = "site:goodreads.com {0}".format(search_term)
    url = "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={0}"
    r = requests.get(url.format(query))
    response = r.json()
    return [result['url'] for result in response['responseData']['results']]


# deprecated
def get_top_google_goodreads_books(book_name):
    result_urls = get_top_google_goodreads_search(search_term=book_name)
    return [url for url in result_urls if 'goodreads.com/book/show/' in url]


def get_top_bing_goodreads_search(search_term):
    query = "site:goodreads.com {0}".format(search_term)
    bing_web = PyBingWebSearch(BING_SEARCH_API_KEY, query, web_only=False)
    results = bing_web.search(limit=50, format='json')
    return [r.url for r in results if 'goodreads.com/book/show/' in r.url]


def get_goodreads_id(url):
    # receives goodreads url
    # returns the id using regex
    regex = r'goodreads.com/book/show/(\d+)'
    ids = re.findall(regex, url)
    if ids:
        return ids[0]
    return False


def get_book_details_by_id(goodreads_id):
    api_url = 'http://goodreads.com/book/show/{0}?format=xml&key={1}'
    r = requests.get(api_url.format(goodreads_id, goodreads_api_key))
    try:
        book_data = xmltodict.parse(r.content)['GoodreadsResponse']['book']
    except (TypeError, KeyError, ExpatError):
        return False
    keys = ['title', 'average_rating', 'ratings_count', 'description', 'url',
            'num_pages']
    book = {}
    for k in keys:
        book[k] = book_data.get(k)
    try:
        work = book_data['work']
        book['publication_year'] = work['original_publication_year']['#text']
    except KeyError:
        book['publication_year'] = book_data.get('publication_year')

    if type(book_data['authors']['author']) == list:
        authors = [author['name'] for author in book_data['authors']['author']]
        authors = ', '.join(authors)
    else:
        authors = book_data['authors']['author']['name']
    book['authors'] = authors
    return book


def get_book_details_by_name(book_name):
    urls = get_top_bing_goodreads_search(search_term=book_name)
    if not urls:
        raise BookNotFound
    top_search_url = urls[0]
    goodreads_id = get_goodreads_id(url=top_search_url)
    return get_book_details_by_id(goodreads_id=goodreads_id)
