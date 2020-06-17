import datetime
import json
from pandas import read_sql
from lib.sql_linker import connect_sys_db, mysql


class Review:
    # Post new review
    @staticmethod
    def new_review(user_id, book_id, rating, content):
        conn = connect_sys_db()
        # SQL
        query = "SELECT * FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            query = "INSERT INTO review_rate VALUES(\'{book_id}\',\'{user_id}\',\'{rating}\',\'{content}\',\'{time}\')".format(
                user_id=user_id,
                book_id=book_id,
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
        review_list = Review.get_book_user_all_review(user_id, book_id)
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
    def get_user_all_reviews(user_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, book_id, rating, review_content, review_time FROM review_rate WHERE user_id = \'{user_id}\'".format(
            user_id=user_id
        )
        # Query result -> json
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get certain book's all review
    @staticmethod
    def get_book_all_review(book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, book_id, rating, review_content, review_time FROM review_rate WHERE book_id = \'{book_id}\'".format(
            book_id=book_id
        )
        # Query result -> json
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get certain book's review posted by certain user
    @staticmethod
    def get_book_user_all_review(user_id, book_id):
        conn = connect_sys_db()
        # SQL
        query = "SELECT user_id, book_id, rating, review_content, review_time FROM review_rate WHERE (user_id = \'{user_id}\' AND book_id = \'{book_id}\')".format(
            user_id=user_id,
            book_id=book_id
        )
        # Query result -> result
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
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
        print(result)
        sum = 0
        for i in result:
            sum = sum + i['rating'];
        return float(sum / len(result))
