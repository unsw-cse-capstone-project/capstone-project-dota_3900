from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY


class User:
    def __init__(self, id):
        self._id = id

    # Update account's username
    def update_username(self, new_username):
        # SQL
        conn = connect_sys_db()
        query = 'UPDATE users SET username = \'{new_username}\' WHERE id = \'{id}\''.format(
            id=self._id,
            new_username=new_username
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update account's password
    def update_password(self, new_password):
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

    # Get user's detail by id
    @staticmethod
    def get_info_by_id(id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT username, admin, email FROM users WHERE id = \'{id}\'".format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            # If ID not existed
            return None
        else:
            info = db_result.iloc[0]
            return info

    # Get user's username by id
    @staticmethod
    def get_username_by_id(id):
        # SQL
        conn = connect_sys_db()
        query = "Select username FROM users WHERE id = \'{id}\'".format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        return db_result.iloc[0].username

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
