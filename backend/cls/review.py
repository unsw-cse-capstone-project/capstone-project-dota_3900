import datetime
import json
import time

from pandas import read_sql

from cls.user import User
from lib.sql_linker import connect_sys_db, mysql


class Review:
    # Post new review
    @staticmethod
    def new_review(user_id, book_id, rating, content):
        username = User.get_username_by_id(user_id)
        conn = connect_sys_db()
        # SQL
        query = "SELECT * FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            query = "INSERT INTO review_rate VALUES(\'{book_id}\',\'{user_id}\',\'{username}\',\'{rating}\',\'{content}\',\'{time}\')".format(
                user_id=user_id,
                book_id=book_id,
                username=username,
                rating=rating,
                content=content,
                time=datetime.datetime.now()
            )
            with mysql(conn) as cursor:
                cursor.execute(query)
            return True
        else:
            return False
            # query = 'UPDATE reviews SET content = \'{content}\', time = \'{time}\ WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')'.format(

    @staticmethod
    def edit_review(user_id, book_id, rating, content):
        conn = connect_sys_db()
        # SQL
        query = "SELECT * FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
            query = 'UPDATE review_rate SET rating = \'{rating}\', review_content = \'{review_content}\', review_time = \'{review_time}\' WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')'.format(
                rating=rating,
                review_content=content,
                review_time=datetime.datetime.now(),
                user_id=user_id,
                book_id=book_id
            )
            with mysql(conn) as cursor:
                cursor.execute(query)
            return True
        else:
            return False

    @staticmethod
    def delete_review(user_id, book_id):
        review_list = Review.get_book_user_review(user_id, book_id)
        if (review_list == []):
            return False
        conn = connect_sys_db()
        # SQL
        query = 'DELETE FROM review_rate WHERE book_id = \'{book_id}\' AND user_id = \'{user_id}\'' \
            .format(
            book_id=book_id,
            user_id=user_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Get certain user's all review
    @staticmethod
    def get_user_reviews(user_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE user_id = \'{user_id}\' ORDER BY review_time DESC".format(
            user_id=user_id
        )
        # Query result -> json
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['review_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(ds[index]['review_time'] / 1000 - 28800))
            result.append(ds[index])
        return result

    # Get certain book's all review
    @staticmethod
    def get_book_review(book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE book_id = \'{book_id}\' ORDER BY review_time DESC".format(
            book_id=book_id
        )
        # Query result -> json
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['review_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(ds[index]['review_time'] / 1000 - 28800))
            result.append(ds[index])
        # print(result)
        return result

    # Get certain book's review posted by certain user
    @staticmethod
    def get_book_user_review(user_id, book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\') ORDER BY review_time DESC".format(
            user_id=user_id,
            book_id=book_id
        )
        # Query result -> result
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['review_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(ds[index]['review_time'] / 1000 - 28800))
            result.append(ds[index])
        return result

    @staticmethod
    def get_book_review_from_to(book_id, index_from, index_to):
        reviews = Review.get_book_review(book_id)
        if len(reviews) == 0:
            return []
        if len(reviews) < (index_to + 1):
            index_to = len(reviews) - 1
        result = []
        index = index_from
        while (index <= index_to):
            result.append(reviews[index])
            index = index + 1
        return result

    @staticmethod
    def get_book_average_rating(book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT rating FROM review_rate WHERE (book_id = \'{book_id}\')".format(
            book_id=book_id
        )
        # Query result -> result
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        if len(result) == 0:
            return 0
        sum = 0
        for i in result:
            sum = sum + i['rating'];
        return float(sum / len(result))

    @staticmethod
    def get_book_num_rating(book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT rating FROM review_rate WHERE (book_id = \'{book_id}\')".format(
            book_id=book_id
        )
        # Query result -> result
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return len(result)

    @staticmethod
    def get_book_review_page_num(book_id, review_each_page):
        reviews = Review.get_book_review(book_id)
        num_reviews = len(reviews)
        if num_reviews <= review_each_page:
            num_page = 1
            num_last_page = num_reviews
        else:
            num_last_page = num_reviews % review_each_page
            num_page = (num_reviews - num_last_page) / review_each_page + 1
        return num_page, num_last_page

    @staticmethod
    def get_book_review_page(book_id, review_each_page, curr_page):
        page_num, last_page_num = Review.get_book_review_page_num(book_id, review_each_page)
        reviews = Review.get_book_review(book_id)
        reviews_num = len(reviews)
        if page_num == curr_page:
            index_from = reviews_num - last_page_num + 1
            index_to = reviews_num
        else:
            index_from = 10 * (curr_page - 1) + 1
            index_to = 10 * (curr_page)
        return Review.get_book_review_from_to(book_id, index_from - 1, index_to - 1)
