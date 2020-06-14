import json
from numpy import iterable
from numpy.ma import count
from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY


class Book:
    def __init__(self, id):
        self._id = id

    @staticmethod
    def book_search(input):
        conn = connect_sys_db()
        query = "SELECT id, authors, title ,ISBN13 FROM books WHERE title like \'%{input}%\' or authors like \'%{input}%\' or ISBN13 like \'%{input}%\'".format(
            input=input
        )
        db_result = read_sql(sql=query, con=conn)

        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    @staticmethod
    def get_info_by_id(id):
        conn = connect_sys_db()
        query = "SELECT id, title, authors, publisher, published_date, description," \
                "ISBN13, categories, google_rating, google_ratings_count, book_cover_url, " \
                "language FROM books WHERE id = \'{id}\' ".format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return None
        else:
            info = db_result.iloc[0]
            return info

