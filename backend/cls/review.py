import datetime
import json
import time

from pandas import read_sql

from cls.book import Book
from cls.user import User
from lib.sql_linker import connect_sys_db, mysql


class Review:
    # -------------------------------------- Help Func -------------------------------------
    # Is certain review posted by certain user existed
    @staticmethod
    def is_review_exist_by_both_id(user_id, book_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\') ORDER BY review_time DESC".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True
    # -------------------------------------------------------------------------------------

    # Post new review
    @staticmethod
    def new_review(user_id, book_id, rating, content):
        user = User(user_id)
        username = user.get_username()
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        # If review does not exist
        if db_result.empty:
            query = "INSERT INTO review_rate VALUES(\'{book_id}\',\'{user_id}\',\'{username}\',\'{rating}\',\'{content}\',\'{time}\')".format(
                user_id=user_id,
                book_id=book_id,
                username=username,
                rating=rating,
                content=content,
                time=datetime.datetime.utcnow()
            )
            with mysql(conn) as cursor:
                cursor.execute(query)
            return True
        else:
            return False

    # Edit existed review
    @staticmethod
    def edit_review(user_id, book_id, rating, content):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        # If review is existed
        if not db_result.empty:
            query = 'UPDATE review_rate SET rating = \'{rating}\', review_content = \'{review_content}\', review_time = \'{review_time}\' WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')'.format(
                rating=rating,
                review_content=content,
                review_time=datetime.datetime.utcnow(),
                user_id=user_id,
                book_id=book_id
            )
            with mysql(conn) as cursor:
                cursor.execute(query)
            return True
        else:
            return False

    # Delete existed review
    @staticmethod
    def delete_review(user_id, book_id):
        # SQL
        conn = connect_sys_db()
        query = 'DELETE FROM review_rate WHERE book_id = \'{book_id}\' AND user_id = \'{user_id}\'' \
            .format(
            book_id=book_id,
            user_id=user_id
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Get certain user's all review
    @staticmethod
    def get_user_reviews(user_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE user_id = \'{user_id}\' ORDER BY review_time DESC".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            # Add book's title and cover to result list
            book = Book(ds[index]['book_id'])
            ds[index]['book_title'] = book.get_info().title
            ds[index]['book_cover_url'] = book.get_info().book_cover_url
            result.append(ds[index])
        return result

    # Get certain book's all review
    @staticmethod
    def get_book_review(book_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE book_id = \'{book_id}\' ORDER BY review_time DESC".format(
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get certain book's review posted by certain user
    @staticmethod
    def get_book_user_review(user_id, book_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT user_id, username, book_id, rating, review_content, review_time FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\') ORDER BY review_time DESC".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get reivew from index_from to index_to
    @staticmethod
    def get_book_review_from_to(book_id, index_from, index_to):
        reviews = Review.get_book_review(book_id)
        # If there is no review
        if len(reviews) == 0:
            return []
        # If index_to is over range
        if len(reviews) < (index_to + 1):
            index_to = len(reviews) - 1
        result = []
        index = index_from
        while (index <= index_to):
            result.append(reviews[index])
            index = index + 1
        return result

    # Get average rating of book
    @staticmethod
    def get_book_average_rating(book_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT rating FROM review_rate WHERE (book_id = \'{book_id}\')".format(
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        # If there is no rating
        if len(result) == 0:
            return 0
        sum = 0
        # Get average rating
        for i in result:
            sum = sum + i['rating'];
        return float(sum / len(result))

    # Get number of reviews of certain book
    @staticmethod
    def get_book_num_rating(book_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT rating FROM review_rate WHERE (book_id = \'{book_id}\')".format(
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return len(result)

    # Get total number of review page with input number of review on each page
    @staticmethod
    def get_book_review_page_num(book_id, review_each_page):
        reviews = Review.get_book_review(book_id)
        num_reviews = len(reviews)
        # If total number of review < number of review on each page
        if num_reviews <= review_each_page:
            num_page = 1
            num_last_page = num_reviews
        else:
            num_last_page = num_reviews % review_each_page
            if num_last_page != 0:
                num_page = (num_reviews - num_last_page) / review_each_page + 1
            else:
                num_page = num_reviews / review_each_page
        return num_page, num_last_page

    # Get review list on certain review page
    @staticmethod
    def get_book_review_page(book_id, review_each_page, curr_page):
        page_num, last_page_num = Review.get_book_review_page_num(book_id, review_each_page)
        reviews = Review.get_book_review(book_id)
        reviews_num = len(reviews)
        if page_num == curr_page:
            # If last page number is different with other page
            if last_page_num != 0:
                index_from = reviews_num - last_page_num + 1
                index_to = reviews_num
            else:
                index_from = reviews_num - review_each_page + 1
                index_to = reviews_num
        else:
            index_from = review_each_page * (curr_page - 1) + 1
            index_to = review_each_page * (curr_page)
        return Review.get_book_review_from_to(book_id, index_from - 1, index_to - 1)

    # Get total number of review posted by certain user
    @staticmethod
    def get_user_num_review(user_id):
        conn = connect_sys_db()
        query = "SELECT count(*) as num FROM review_rate WHERE user_id = \'{user_id}\'".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        return int(db_result.iloc[0].num)
