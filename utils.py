import re
import textwrap

import html2text

text_maker = html2text.HTML2Text()
text_maker.body_width = 0


def strip_html_tags(text):
    return re.sub('<[^<]+?>', '', text)


def html_to_md(string, strip_html=True):
    if strip_html is True:
        string = strip_html_tags(string)
    return text_maker.handle(string)


def get_formatted_book_data(book_data):
    template = textwrap.dedent("""\
        *Title:* {0} by {1}
        *Rating:* {2} by {3} users
        *Description:* {4}
        *Link*: {5}

        Tip: {6}""")
    title = book_data['title']
    authors = book_data['authors']
    average_rating = book_data['average_rating']
    ratings_count = book_data['ratings_count']
    description = html_to_md(book_data.get('description', ''))
    url = book_data['url']

    tip = 'Use author name also for better search results'
    template = template.format(title, authors, average_rating, ratings_count,
                               description, url, tip)
    return template
