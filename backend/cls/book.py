import json
from pandas import read_sql
from lib.sql_linker import connect_sys_db, mysql


class Book:
    def __init__(self, id):
        self._id = id

    # Search result of input content
    @staticmethod
    def book_search(input):
        # SQL
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

    # Get book's all detail by book_id
    @staticmethod
    def get_info_by_id(id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT id, title, authors, publisher, published_date, description," \
                "ISBN13, categories, google_rating, google_ratings_count, book_cover_url, " \
                "language FROM books WHERE id = \'{id}\' ".format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            # if ID not existed
            return None
        else:
            info = db_result.iloc[0]
            return info

    # Is book exist by book_id
    @staticmethod
    def is_book_exists_by_id(id):
        # SQL
        conn = connect_sys_db()
        query = 'SELECT id FROM books Where id = \'{id}\''.format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True