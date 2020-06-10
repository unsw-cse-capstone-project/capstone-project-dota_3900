import pandas as pd
import json
import requests
from tqdm import tqdm
import time
import sys


def get_book(ISBN):
    try:
        # url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:9780758272799'
        url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + ISBN
        src_data = requests.get(url)
        json_data = json.loads(src_data.text)
        book_data = json_data['items'][0]
        book_data = book_data['volumeInfo']

        title = book_data['title']
        authors = book_data['authors']
        publisher = book_data['publisher']
        published_date = book_data['publishedDate']
        description = book_data['description']
        ISBN13 = ISBN
        categories = book_data['categories']
        google_rating = book_data['averageRating']
        google_ratings_count = book_data['ratingsCount']
        book_cover_url = book_data['imageLinks']['thumbnail']
        language = book_data['language']
    except Exception:
        return None

    return [title, authors, publisher, published_date, description,
            ISBN13, categories, google_rating, google_ratings_count,
            book_cover_url, language]


def insert_to_df(df, index, book_info):
    if book_info is not None:
        df.loc[index] = book_info
        return True
    return False


if __name__ == '__main__':
    columns = ['title', 'authors', 'publisher', 'published_date',
               'description', 'ISBN13', 'categories', 'google_rating',
               'google_ratings_count', 'book_cover_url', 'language']
    book_df = pd.DataFrame(columns=columns)
    with open(sys.argv[1], 'r') as f:
        isbn_list = f.read().split('\n')
    index = 0
    for i in tqdm(range(0, len(isbn_list))):
        if insert_to_df(book_df, index, get_book(isbn_list[i])):
            index = index + 1
    book_df.to_csv(sys.argv[1].replace('.txt', '') + '.csv')





