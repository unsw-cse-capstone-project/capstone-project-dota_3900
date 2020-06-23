import datetime
import json
import time

from pandas import read_sql

from cls.book import Book
from cls.user import User
from lib.sql_linker import connect_sys_db, mysql


class Collection:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def is_collection_exists_by_both_id(user_id, collection_id):
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    @staticmethod
    def is_collection_exists_by_id(collection_id):
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE id = \'{id}\'".format(
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

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
            ds[index]['book_num'] = Collection.get_num_book_collection(int(ds[index]['id']))
            ds[index]['finished_num'] = Collection.get_num_read_collection(user_id, int(ds[index]['id']))
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
        if not Collection.is_collection_exists_by_both_id(user_id, collection_id):
            return False, 'Collection not found'

        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND name = \'{name}\')".format(
            user_id=user_id,
            name=new_name
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
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
        if not Collection.is_collection_exists_by_both_id(user_id, collection_id):
            return False, 'Collection not found'

        query = "DELETE FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    @staticmethod
    def get_book_in_collection(collection_id, user_id):
        conn = connect_sys_db()
        if not Collection.is_collection_exists_by_id(collection_id):
            return False, []

        query = "SELECT user_id FROM collections WHERE id = \'{collection_id}\'".format(
            collection_id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        user_id = db_result.iloc[0].user_id

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
            finish_date = Collection.get_book_read_date(user_id, ds[index]['book_id'])
            if finish_date != 0:
                ds[index]['finish_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            # ds[index]['finish_time'] = finish_date
            result.append(ds[index])
        return True, result

    @staticmethod
    def add_book_to_collection(collection_id, book_id):

        if not Book.is_book_exists_by_id(book_id):
            return 404, "Resource not found"

        if not Collection.is_collection_exists_by_id(collection_id):
            return False, []

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
        if not Collection.is_collection_exists_by_id(collection_id):
            return False, []
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

    # @staticmethod
    #     # def get_book_read_date(user_id, book_id):
    #     #     conn = connect_sys_db()
    #     #     query = "SELECT id FROM users WHERE (id=\'{id}\')".format(
    #     #         id = user_id
    #     #     )

    @staticmethod
    def get_readcollection_id(user_id):
        conn = connect_sys_db()
        query = "SELECT id FROM collections WHERE (user_id = \'{user_id}\' and name = 'read')".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return None
        else:
            return db_result.iloc[0].id

    @staticmethod
    def mark_as_read(user_id, book_id):
        if not User.is_user_exists_by_id(user_id):
            return False
        if not Book.is_book_exists_by_id(book_id):
            return False
        read_collection_id = Collection.get_readcollection_id(user_id)
        conn = connect_sys_db()
        query = "INSERT INTO collects VALUES(\'{book_id}\', \'{collection_id}\', \'{collect_time}\')".format(
            book_id=book_id,
            collection_id=read_collection_id,
            collect_time=datetime.datetime.now()
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    @staticmethod
    def get_num_read_collection(user_id, collection_id):
        read_collection_id = Collection.get_readcollection_id(user_id)
        # print(read_collection_id)
        conn = connect_sys_db()
        query = "select book_id from(select book_id from collects where collection_id = \'{collection_id}\' UNION all select book_id from collects where collection_id = \'{read_collection_id}\')a group by book_id having count(*) > 1".format(
            collection_id=collection_id,
            read_collection_id=read_collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        # print(db_result.size)
        return  int(db_result.size)

    @staticmethod
    def get_num_book_collection(collection_id):
        conn = connect_sys_db()
        query = "SELECT count(*) as num FROM collects WHERE collection_id = \'{collection_id}\'".format(
            collection_id = collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        return int(db_result.iloc[0].num)

    @staticmethod
    def get_book_read_date(user_id, book_id):
        conn = connect_sys_db()
        read_collection_id = Collection.get_readcollection_id(user_id)
        query = "select collect_time FROM collects WHERE (collection_id = \'{collection_id}\' AND book_id = \'{book_id}\')".format(
            collection_id=read_collection_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return 0
        return db_result.iloc[0].collect_time
