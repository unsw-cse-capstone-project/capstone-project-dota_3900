import pandas as pd
from pandas import read_sql

from cls.book import Book
from lib.sql_linker import connect_sys_db, mysql


class Recommend:

    # Create view table which will be need in below function
    @staticmethod
    def create_view_tables():
        # SQL
        conn = connect_sys_db()
        query1 = "create or replace view view4 as select books.id, count(*) as collect_time from books join collects " \
                 "on books.id = collects.book_id group by books.id "
        query2 = "create or replace view view2 as select books.id, count(*) as read_time from books join collects on " \
                 "books.id = collects.book_id join collections on collects.collection_id = collections.id where " \
                 "collections.name = 'read' group by books.id "
        query3 = "create or replace view view3 as select books.id, avg(review_rate.rating) as avg_rating from books " \
                 "join review_rate on books.id = review_rate.book_id group by books.id "
        with mysql(conn) as cursor:
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)

    # Clear up books table information and add popular grade to the table
    @staticmethod
    def get_recommend_list():
        Recommend.create_view_tables()
        conn = connect_sys_db()
        query = 'select distinct books.id, books.categories,books.authors, books.published_date, view4.collect_time, ' \
                'view2.read_time, view3.avg_rating, books.google_rating from books left join collects on books.id = ' \
                'collects.book_id left join review_rate on books.id = review_rate.book_id left join view4 on books.id ' \
                '= view4.id left join view2 on books.id = view2.id left join view3 on books.id = view3.id '
        db_result = read_sql(sql=query, con=conn)
        db_result = db_result.fillna(0)
        db_result['published_date'] = pd.to_datetime(db_result['published_date'])
        db_result['published_date'] = db_result['published_date'].dt.strftime("%Y")
        db_result.insert(6, 'popular',
                         db_result.collect_time * 0.1 + db_result.read_time * 0.2 + db_result.avg_rating * 0.3 + db_result.google_rating * 0.4)
        return db_result

    # Recommend mode: By category
    @staticmethod
    def recommend_by_category(category, number, book_id):
        df = Recommend.get_recommend_list()
        # Get total number of books with this category
        available_num = df['categories'].value_counts()
        if available_num[category] == 1: return []
        # Sort the dataframe by categories and popular grade
        df = df.sort_values(by=['categories', 'popular'], ascending=False)
        counter = 0
        result = []
        for item in df.iterrows():
            if counter == number: break
            # Do not recommend current reference book
            if item[1]['categories'] == category and item[1]['id'] != book_id:
                book = Book(item[1]['id'])
                info = book.get_info()
                # Return information which need for front-end
                temp = {'book_id': item[1]['id'], 'author': item[1]['authors'], 'categories': item[1]['categories'],
                        'popular': item[1]['popular'], 'title': info.title, 'book_cover_url': info.book_cover_url}
                result.append(temp)
                counter += 1
        return result

    # Recommend mode: By author
    @staticmethod
    def recommend_by_author(author, number, book_id):
        df = Recommend.get_recommend_list()
        # Get total number of books written by this author
        available_num = df['authors'].value_counts()
        if available_num[author] == 1: return []
        # Sort the dataframe by authors and popular grade
        df = df.sort_values(by=['authors', 'popular'], ascending=False)
        counter = 0
        result = []
        for item in df.iterrows():
            if counter == number: break
            # Do not recommend current reference book
            if item[1]['authors'] == author and item[1]['id'] != book_id:
                book = Book(item[1]['id'])
                info = book.get_info()
                # Return information which need for front-end
                temp = {'book_id': item[1]['id'], 'author': item[1]['authors'], 'categories': item[1]['categories'],
                        'popular': item[1]['popular'], 'title': info.title, 'book_cover_url': info.book_cover_url}
                result.append(temp)
                counter += 1
        return result

    # Recommend mode: Recommend by published date (in the same decade)
    @staticmethod
    def recommend_by_publishedDate(publishedDate, number, book_id):
        df = Recommend.get_recommend_list()
        # Format the published_date column in the dataframe
        df = df[df['published_date'].str.contains(publishedDate)]
        # Sort by popular grade
        df = df.sort_values(by=['popular'], ascending=False)
        counter = 0
        result = []
        for item in df.iterrows():
            if counter == number: break
            # Do not recommend the reference book
            if item[1]['id'] != book_id:
                book = Book(item[1]['id'])
                info = book.get_info()
                # Return information which need for front-end
                temp = {'book_id': item[1]['id'], 'author': item[1]['authors'], 'categories': item[1]['categories'],
                        'popular': item[1]['popular'], 'title': info.title, 'book_cover_url': info.book_cover_url}
                result.append(temp)
                counter += 1
        return result

    # Recommend mode: Combine category and author (not used)
    @staticmethod
    def recommend_by_author_category(category, author, number, book_id):
        cate_result = Recommend.recommend_by_category(category, 100, book_id)
        author_result = Recommend.recommend_by_author(author, 100, book_id)
        temp_result = [x for x in cate_result if x in author_result]
        if temp_result == []:
            return []
        result = []
        counter = 0
        for rec in temp_result:
            if counter == number: break
            result.append(rec)
        return result
