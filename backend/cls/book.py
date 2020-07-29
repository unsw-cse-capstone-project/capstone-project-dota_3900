import json
from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql


class Book:
    def __init__(self, id):
        self._id = id

    # Get book's all detail by book_id
    def get_info(self):
        # SQL
        conn = connect_sys_db()
        query = "SELECT id, title, authors, publisher, published_date, description," \
                "ISBN13, categories, google_rating, google_ratings_count, book_cover_url, " \
                "language FROM books WHERE id = \'{id}\' ".format(
            id=self._id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            # if ID not existed
            return None
        else:
            info = db_result.iloc[0]
            return info

    # -------------------------------------- Help Func -------------------------------------
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

    # Is book exist in certain collection
    @staticmethod
    def is_book_exists_in_collection(collection_id, book_id):
        # SQL
        conn = connect_sys_db()
        query = 'SELECT * FROM collects Where (book_id = \'{book_id}\' AND collection_id = \'{collection_id}\')'.format(
            book_id=book_id,
            collection_id=collection_id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True
    # -----------------------------------------------------------------------------------

    # Search result of input content
    @staticmethod
    def book_search(input):
        # SQL
        conn = connect_sys_db()
        query = "SELECT id, authors, title ,ISBN13, book_cover_url, description, publisher, published_date, categories FROM books WHERE title like \'%{input}%\' or authors like \'%{input}%\' or ISBN13 like \'%{input}%\'".format(
            input=input
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            ds[index]['average'] = Book.get_book_average_rating(ds[index]['id'])
            result.append(ds[index])
        return result

    # Length of search result of input content
    @staticmethod
    def book_search_length(input, category, rating_from, rating_to):
        # SQL
        conn = connect_sys_db()
        query = "select id, authors, title, ISBN13, book_cover_url, description, publisher, published_date, categories, average from \
                (select books.id, books.title, books.authors, books.ISBN13, books.book_cover_url, books.description, books.publisher, books.published_date, books.categories, avg(review_rate.rating) as average \
                from books left join review_rate on books.id = review_rate.book_id  \
                where books.title like \'%{input}%\' or books.authors like \'%{input}%\' or books.isbn13 like \'%{input}%\' \
                group by books.id \
                order by average desc) as subquery \
                where ((average >= \'{rating_from}\' and average <= \'{rating_to}\'))".format(
            input=input,
            rating_from=rating_from,
            rating_to=rating_to
        )
        # Reformat query if filter has no restriction of rating_from
        if rating_from == 0:
            query = query.rstrip(")")
            query += ") or average is null)"
        # Reformat query if filter has no restriction of category
        if category is not "":
            query += " and categories = \"" + category + "\""
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return len(result), result

    # Reformat the search input content
    @staticmethod
    def book_search_regex(content, category):
        content_ans = ""
        category_ans = ""
        # Change every other symbol to %
        for ch in content:
            if not (ch.isdigit() or ch.isalpha()):
                ch = "%"
            content_ans += ch
        if category is not None:
            category_ans = "['" + category + "']"
        return content_ans, category_ans

    # Get total number of search result page
    @staticmethod
    def get_book_search_page_num(content, category, rating_from, rating_to, result_each_page):
        num_results, result = Book.book_search_length(content, category, rating_from, rating_to)
        # If total number of review < number of review on each page
        if num_results <= result_each_page:
            num_page = 1
            num_last_page = num_results
        else:
            num_last_page = num_results % result_each_page
            if num_last_page != 0:
                num_page = (num_results - num_last_page) / result_each_page + 1
            else:
                num_page = num_results / result_each_page
        return num_page, num_last_page, num_results, result

    # Get book list on certain search page
    @staticmethod
    def get_book_search_page(content, result_each_page, curr_page, page_num, last_page_num, reviews_num, result):
        if (reviews_num == 0):
            return []
        if page_num == curr_page:
            if last_page_num != 0:
                index_from = reviews_num - last_page_num + 1
                index_to = reviews_num
            else:
                index_from = reviews_num - result_each_page + 1
                index_to = reviews_num
        else:
            index_from = result_each_page * (curr_page - 1) + 1
            index_to = result_each_page * (curr_page)
        return Book.get_book_search_from_to(content, index_from - 1, index_to - 1, result)

    # Get search result from index_from to index_to
    @staticmethod
    def get_book_search_from_to(content, index_from, index_to, result):
        num = index_to - index_from + 1
        conn = connect_sys_db()
        ans = []
        i = 0
        for index in result:
            if index_from <= i <= index_to:
                query = "select book_id,count(*) as num from review_rate where book_id = \'{book_id}\' group by book_id".format(
                    book_id=index['id']
                )
                db_result = read_sql(sql=query, con=conn)
                # Add book's number of review into result
                if db_result.empty:
                    index['review_num'] = 0
                else:
                    review_num = db_result.iloc[0].num
                    index['review_num'] = int(review_num)
                ans.append(index)
                i += 1
            else:
                i += 1
        return ans

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
            sum = sum + i['rating']
        return float(sum / len(result))

    # Get view table which will be need in below function
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

    # Get the most popular book
    @staticmethod
    def get_popular_book():
        Book.create_view_tables()
        # SQL
        conn = connect_sys_db()
        query = 'select distinct books.id, books.title, books.book_cover_url, view4.collect_time, view2.read_time, ' \
                'view3.avg_rating, books.google_rating from books left join collects on books.id = collects.book_id ' \
                'left join review_rate on books.id = review_rate.book_id left join view4 on books.id = view4.id left ' \
                'join view2 on books.id = view2.id left join view3 on books.id = view3.id '
        db_result = read_sql(sql=query, con=conn)
        db_result = db_result.fillna(0)
        # Popular grade formula
        db_result.insert(6, 'popular',
                         db_result.collect_time * 0.1 + db_result.read_time * 0.2 + db_result.avg_rating * 0.3 + db_result.google_rating * 0.4)
        # Sort dataframe by popular
        db_result = db_result.sort_values(by=['popular'], ascending=False)
        # Get first ten books in the list
        db_result = db_result.head(10)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(
                {'id': ds[index]['id'], 'title': ds[index]['title'], 'book_cover_url': ds[index]['book_cover_url']})
        return result

    # Get list of categories sort by number of books with this category
    @staticmethod
    def get_categories_list():
        # SQL
        conn = connect_sys_db()
        query = "select categories, count(*) as count from books group by categories order by count desc limit 12"
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            temp = ds[index]['categories'].rstrip("']")
            temp = temp.lstrip("['")
            result.append({'category': temp, 'book_num': ds[index]['count']})
        return result
