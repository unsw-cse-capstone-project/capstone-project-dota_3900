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

    # Is collection existed by user_id and collection_id
    @staticmethod
    def is_collection_exists_by_both_id(user_id, collection_id):
        # SQL
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

    # Is collection exist by collection_id
    @staticmethod
    def is_collection_exists_by_id(collection_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE id = \'{id}\'".format(
            id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    # Get all collection of user
    @staticmethod
    def get_user_collection(user_id):
        # Is user exist
        if not User.is_user_exists_by_id(user_id):
            return None
        # SQL
        conn = connect_sys_db()
        query = "SELECT id, user_id, name, creation_time FROM collections WHERE user_id = \'{user_id}\'".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            # Timestamp -> datetime
            if ds[index]['name'] == "Read":
                continue
            # ds[index]['creation_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
            #                                            time.localtime(ds[index]['creation_time'] / 1000 - 28800))
            ds[index]['book_num'] = Collection.get_num_book_collection(int(ds[index]['id']))
            ds[index]['finished_num'] = Collection.get_num_read_collection(user_id, int(ds[index]['id']))
            result.append(ds[index])
        return result

    # Create new collection
    @staticmethod
    def post_new_collection(user_id, name):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND name = \'{name}\')".format(
            user_id=user_id,
            name=name
        )
        db_result = read_sql(sql=query, con=conn)
        # If collection's name already existed
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

    # Update existed collection's name
    @staticmethod
    def update_collection_name(user_id, collection_id, new_name):
        # Is collection exist
        if not Collection.is_collection_exists_by_both_id(user_id, collection_id):
            return False, 'Collection not found'
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collections WHERE (user_id = \'{user_id}\' AND name = \'{name}\')".format(
            user_id=user_id,
            name=new_name
        )
        db_result = read_sql(sql=query, con=conn)
        # Is new collection name already exist
        if not db_result.empty:
            return False, 'This collection already existed'
        # SQL
        query = "UPDATE collections SET name = \'{name}\' WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            name=new_name,
            user_id=user_id,
            id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True, 'Collection update success'

    # Delete existed collection
    @staticmethod
    def delete_collection(user_id, collection_id):
        # Is collection exist
        if not Collection.is_collection_exists_by_both_id(user_id, collection_id):
            return False, 'Collection not found'
        # SQL
        conn = connect_sys_db()
        query = "DELETE FROM collections WHERE (user_id = \'{user_id}\' AND id = \'{id}\')".format(
            user_id=user_id,
            id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Get list of books in collection
    @staticmethod
    def get_book_in_collection(collection_id):
        # Is collection exist
        if not Collection.is_collection_exists_by_id(collection_id):
            return False, []
        # SQL
        conn = connect_sys_db()
        query = "SELECT user_id FROM collections WHERE id = \'{collection_id}\'".format(
            collection_id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        user_id = db_result.iloc[0].user_id
        # SQL
        query = "SELECT * FROM collects WHERE collection_id = \'{collection_id}\'".format(
            collection_id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            # Timestamp -> datetime
            # ds[index]['collect_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
            #                                           time.localtime(ds[index]['collect_time'] / 1000 - 28800))
            finish_date = Collection.get_book_read_date(user_id, ds[index]['book_id'])
            # post finish_time if finish
            if finish_date != 0:
                # ds[index]['finish_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                ds[index]['finish_time'] = finish_date
            result.append(ds[index])
        return True, result

    # Add book to existed collection
    @staticmethod
    def add_book_to_collection(collection_id, book_id):
        # Is book exist
        if not Book.is_book_exists_by_id(book_id):
            return 404, "Resource not found"
        # Is collection exist
        if not Collection.is_collection_exists_by_id(collection_id):
            return 404, "Resource not found"
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collects WHERE (collection_id = \'{collection_id}\' and book_id = \'{book_id}\')".format(
            collection_id=collection_id,
            book_id=book_id,
        )
        db_result = read_sql(sql=query, con=conn)
        # Is book already existed in collection
        if not db_result.empty:
            return 201, "This book already existed in this collection"
        # SQL
        query = "INSERT INTO collects VALUES(\'{book_id}\', \'{collection_id}\', \'{collect_time}\')".format(
            book_id=book_id,
            collection_id=collection_id,
            collect_time=datetime.datetime.now()
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return 200, "Add book to collection success"

    # Delete existed book in collection
    @staticmethod
    def delete_book_in_collection(collection_id, book_id):
        # Is collection existed
        if not Collection.is_collection_exists_by_id(collection_id):
            return False, []
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collects WHERE (collection_id = \'{collection_id}\' and book_id = \'{book_id}\')".format(
            collection_id=collection_id,
            book_id=book_id,
        )
        db_result = read_sql(sql=query, con=conn)
        # Is book exist in this collection
        if db_result.empty:
            return False
        # SQL
        query = "DELETE FROM collects WHERE (collection_id = \'{collection_id}\' AND book_id = \'{book_id}\')".format(
            book_id=book_id,
            collection_id=collection_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Get readcollection's id of user
    @staticmethod
    def get_readcollection_id(user_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT id FROM collections WHERE (user_id = \'{user_id}\' and name = 'read')".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return None
        else:
            return db_result.iloc[0].id

    # Mark certain book as read
    @staticmethod
    def mark_as_read(user_id, book_id):
        # Is user exist
        if not User.is_user_exists_by_id(user_id):
            return False
        # Is book exist
        if not Book.is_book_exists_by_id(book_id):
            return False
        read_collection_id = Collection.get_readcollection_id(user_id)
        # SQL
        conn = connect_sys_db()
        query = "INSERT INTO collects VALUES(\'{book_id}\', \'{collection_id}\', \'{collect_time}\')".format(
            book_id=book_id,
            collection_id=read_collection_id,
            collect_time=datetime.datetime.now()
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Get number of books which have been read in collection
    @staticmethod
    def get_num_read_collection(user_id, collection_id):
        read_collection_id = Collection.get_readcollection_id(user_id)
        # SQL
        conn = connect_sys_db()
        query = "select book_id from(select book_id from collects where collection_id = \'{collection_id}\' UNION all select book_id from collects where collection_id = \'{read_collection_id}\')a group by book_id having count(*) > 1".format(
            collection_id=collection_id,
            read_collection_id=read_collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        return int(db_result.size)

    # Get number of books in certain collection
    @staticmethod
    def get_num_book_collection(collection_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT count(*) as num FROM collects WHERE collection_id = \'{collection_id}\'".format(
            collection_id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        return int(db_result.iloc[0].num)

    # Get read_date of certain book
    @staticmethod
    def get_book_read_date(user_id, book_id):
        read_collection_id = Collection.get_readcollection_id(user_id)
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM collects WHERE (collection_id = \'{collection_id}\' AND book_id = \'{book_id}\')".format(
            collection_id=read_collection_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return 0
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            return ds[index]['collect_time']
        return 0

    # Get number of collections of user
    @staticmethod
    def get_num_collection(user_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT count(*) as num FROM collections WHERE (user_id = \'{user_id}\')".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        return int(db_result.iloc[0].num) - 1
