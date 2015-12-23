import requests
import xmltodict

from secret import GOODREADS_API_KEY

goodreads_api_key = GOODREADS_API_KEY


def get_first_search_result(search_term):
    api_url = "https://www.goodreads.com/search/index.xml?key={0}&q={1}&search[field]=title"
    r = requests.get(api_url.format(search_term, goodreads_api_key))
    try:
        book_data = xmltodict.parse(r.content)['GoodreadsResponse']['search']
        book_id = book_data['results']['work'][0]['best_book']['id']['#text']
        return book_id
    except (TypeError, KeyError):
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
