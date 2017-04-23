import re

import requests
import xmltodict
from xml.parsers.expat import ExpatError
from googleapiclient.discovery import build

from settings import (GOODREADS_API_KEY, GOOGLE_DEV_API_KEY,
                      GOOGLE_CUSTOM_SEARCH_CX)


class BookNotFound(Exception):
    pass


def get_top_google_goodreads_search(search_term):
    service = build("customsearch", "v1", developerKey=GOOGLE_DEV_API_KEY)
    results = service.cse().list(q=search_term, cx=GOOGLE_CUSTOM_SEARCH_CX,
                                 ).execute()
    if results.get('items'):
        return [r['link'] for r in results.get('items')
                if 'goodreads.com/book/show/' in r['link']]


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
    r = requests.get(api_url.format(goodreads_id, GOODREADS_API_KEY))
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
    urls = get_top_google_goodreads_search(search_term=book_name)
    if not urls:
        raise BookNotFound
    top_search_url = urls[0]
    goodreads_id = get_goodreads_id(url=top_search_url)
    return get_book_details_by_id(goodreads_id=goodreads_id)
