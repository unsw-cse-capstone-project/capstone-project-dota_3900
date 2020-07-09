import json

from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY


class User:
    def __init__(self, id):
        self._id = id

    # Update user's username
    def update_username(self, new_username):
        # SQL
        conn = connect_sys_db()
        query = 'UPDATE users SET username = \'{new_username}\' WHERE id = \'{id}\''.format(
            id=self._id,
            new_username=new_username
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update user's username
    def update_email(self, new_email):
        # SQL
        conn = connect_sys_db()
        query = 'UPDATE users SET email = \'{new_email}\' WHERE id = \'{id}\''.format(
            id=self._id,
            new_email=new_email
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update user's password
    def update_password(self, old_password, new_password):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM users WHERE (password = HEX(AES_ENCRYPT(\'{old_password}\', \'{key}\')) AND id = \'{id}\')".format(
            old_password = old_password,
            id =self._id,
            key=SECRET_KEY
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        # SQL
        conn = connect_sys_db()
        query = 'UPDATE users SET password = HEX(AES_ENCRYPT(\'{new_password}\', \'{key}\')) WHERE id = \'{id}\'' \
            .format(
            id=self._id,
            new_password=new_password,
            key=SECRET_KEY
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Get user's detail by id
    def get_info(self):
        # SQL
        conn = connect_sys_db()
        query = "SELECT username, admin, email FROM users WHERE id = \'{id}\'".format(
            id=self._id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            # If ID not existed
            return None
        else:
            info = db_result.iloc[0]
            return info

    # Get user's username by id
    def get_username(self):
        # SQL
        conn = connect_sys_db()
        query = "Select username FROM users WHERE id = \'{id}\'".format(
            id=self._id
        )
        db_result = read_sql(sql=query, con=conn)
        return db_result.iloc[0].username

    # Register a new user
    @staticmethod
    def register_account(username, password, admin, email):
        #
        # query = 'SELECT username FROM users WHERE username = \'{username}\''.format(
        #     username = username
        # )
        # db_result = read_sql(sql=query, con=conn)
        # if not db_result.empty:
        #     return False, 'This username has already been registered'

        # If username already existed
        if User.is_user_exists_by_username(username):
            return False, 'This username has already been registered'
        # SQL
        conn = connect_sys_db()
        query = 'SELECT email FROM users WHERE email = \'{email}\''.format(
            email=email
        )
        db_result = read_sql(sql=query, con=conn)
        # If email address already been registered
        if not db_result.empty:
            return False, 'This email has already been registered'
        # SQL
        query = 'INSERT INTO users VALUES(0, \'{username}\',' \
                'HEX(AES_ENCRYPT(\'{password}\', \'{key}\')), \'{admin}\', \'{email}\')' \
            .format(
            username=username,
            password=password,
            admin=admin,
            email=email,
            key=SECRET_KEY
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True, ''



    # Is user existed by id
    @staticmethod
    def is_user_exists_by_id(id):
        # SQL
        conn = connect_sys_db()
        query = 'SELECT id FROM users Where id = \'{id}\''.format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    # Is user existed by username
    @staticmethod
    def is_user_exists_by_username(username):
        # SQL
        conn = connect_sys_db()
        query = 'SELECT username FROM users Where username = \'{username}\''.format(
            username=username
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    # Is user existed by username
    @staticmethod
    def is_user_exists_by_email(email):
        # SQL
        conn = connect_sys_db()
        query = 'SELECT email FROM users Where email = \'{email}\''.format(
            email=email
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True


    @staticmethod
    def user_search_regex(input):
        ans = ""
        for ch in input:
            if not (ch.isdigit() or ch.isalpha() or ch is "@"):
                ch = "%"
            ans += ch
        return ans

    # Search result of input content
    @staticmethod
    def user_search_length(input):
        # SQL
        conn = connect_sys_db()
        query = "SELECT count(*) as num FROM users WHERE username like \'%{input}%\' or email like \'%{input}%\'".format(
            input=input
        )
        db_result = read_sql(sql=query, con=conn)
        return db_result.iloc[0].num

    # Search result of input content
    @staticmethod
    def user_search(input):
        # SQL
        conn = connect_sys_db()
        query = "SELECT id, username, email FROM users WHERE username like \'%{input}%\' or email like \'%{input}%\'".format(
            input=input
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get total number of search result page
    @staticmethod
    def get_user_search_page_num(content, result_each_page):
        num_results = User.user_search_length(content)
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
        return num_page, num_last_page

    # Get user list on certain user page
    @staticmethod
    def get_user_search_page(content, result_each_page, curr_page):
        page_num, last_page_num = User.get_user_search_page_num(content, result_each_page)
        # reviews = Book.book_search(content)
        reviews_num = User.user_search_length(content)
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
        return User.get_user_search_from_to(content, index_from - 1, index_to - 1)

    @staticmethod
    def get_user_search_from_to(content, index_from, index_to):
        num = index_to - index_from + 1
        conn = connect_sys_db()
        query = "SELECT id, username, email FROM users WHERE username like \'%{input}%\' or email like \'%{input}%\' limit {index_from},{num}".format(
            input=content,
            index_from=index_from,
            num=num
        )
        # print(query)
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result