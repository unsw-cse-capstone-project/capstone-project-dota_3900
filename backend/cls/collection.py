import datetime
import json
import time

from pandas import read_sql
from lib.sql_linker import connect_sys_db, mysql


class Collection:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get_user_collection(user_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT id, user_id, name, creation_time FROM collections WHERE user_id = \'{user_id}\'".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['creation_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                       time.localtime(ds[index]['creation_time'] / 1000 - 28800))
            result.append(ds[index])
        return result

    @staticmethod
    def post_new_collection(user_id, name):
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND name = \'{name}\')".format(
            user_id=user_id,
            name=name
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            query = "INSERT INTO collections VALUES(0,\'{user_id}\',\'{name}\',\'{time}\')".format(
                user_id=user_id,
                name=name,
                time=datetime.datetime.now()
            )
            with mysql(conn) as cursor:
                cursor.execute(query)
            return True
        else:
            return False

    @staticmethod
    def update_collection_name(user_id, collection_id, new_name):
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            # query = "UPDATE collections SET name = \'{name}\' WHERE (user_id = \'{user_id}\' AND name = \'{name}\')"
            return False, 'Collection not found'

        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND name = \'{name}\')".format(
            user_id=user_id,
            name=new_name
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
            # query = "UPDATE collections SET name = \'{name}\' WHERE (user_id = \'{user_id}\' AND name = \'{name}\')"
            return False, 'This collection already existed'

        query = "UPDATE collections SET name = \'{name}\' WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            name=new_name,
            user_id=user_id,
            id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True, 'Collection update success'

    @staticmethod
    def delete_collection(user_id, collection_id):
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False

        query = "DELETE FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    @staticmethod
    def get_book_in_collection(collection_id):
        conn = connect_sys_db()
        query = "SELECT id FROM collections WHERE (id = \'{id}\')".format(
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False, []

        query = "SELECT * FROM collects WHERE collection_id = \'{collection_id}\'".format(
            collection_id=collection_id
        )

        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['collect_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(ds[index]['collect_time'] / 1000 - 28800))
            # ds[index].append('test')
            # ds[index]['test'] = 'nicenice'
            result.append(ds[index])
        return True, result

    @staticmethod
    def add_book_to_collection(collection_id, book_id):
        conn = connect_sys_db()
        query = "SELECT id FROM books WHERE (id = \'{id}\')".format(
            id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return 404, "Resource not found"

        conn = connect_sys_db()
        query = "SELECT id FROM collections WHERE (id = \'{id}\')".format(
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return 404, "Resource not found"

        conn = connect_sys_db()
        query = "SELECT * FROM collects WHERE (collection_id = \'{collection_id}\' and book_id = \'{book_id}\')".format(
            collection_id=collection_id,
            book_id=book_id,
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
            return 201, "This book already existed in this collection"

        query = "INSERT INTO collects VALUES(\'{book_id}\', \'{collection_id}\', \'{collect_time}\')".format(
            book_id=book_id,
            collection_id=collection_id,
            collect_time=datetime.datetime.now()
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return 200, "Add book to collection success"

    @staticmethod
    def delete_book_in_collection(collection_id, book_id):
        conn = connect_sys_db()
        query = "SELECT id FROM collections WHERE (id = \'{id}\')".format(
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False

        query = "SELECT * FROM collects WHERE (collection_id = \'{collection_id}\' and book_id = \'{book_id}\')".format(
            collection_id=collection_id,
            book_id=book_id,
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False

        query = "DELETE FROM collects WHERE (collection_id = \'{collection_id}\' AND book_id = \'{book_id}\')".format(
            book_id=book_id,
            collection_id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True