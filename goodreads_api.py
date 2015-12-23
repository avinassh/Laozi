import re

import requests
import xmltodict

from settings import GOODREADS_API_KEY

goodreads_api_key = GOODREADS_API_KEY


def get_top_google_goodreads_search(search_term):
    # For a give search term, it searches Goodreads using Google and returns
    # top 4 result urls
    query = "site:goodreads.com {0}".format(search_term)
    url = "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={0}"
    r = requests.get(url.format(query))
    response = r.json()
    return [result['url'] for result in response['responseData']['results']]


def get_top_google_goodreads_books(search_term):
    result_urls = get_top_google_goodreads_search(search_term=search_term)
    return [url for url in result_urls if 'goodreads.com/book/show/' in url]


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
    except (TypeError, KeyError):
        return False
    keys = ['title', 'average_rating', 'ratings_count', 'description', 'url']
    book = {}
    for k in keys:
        book[k] = book_data[k]
    if type(book_data['authors']['author']) == list:
        authors = [author['name'] for author in book_data['authors']['author']]
        authors = ', '.join(authors)
    else:
        authors = book_data['authors']['author']['name']
    book['authors'] = authors
    return book
