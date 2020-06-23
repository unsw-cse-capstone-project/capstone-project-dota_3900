from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY


class User:
    def __init__(self, id):
        self._id = id

    # Update account's username
    def update_username(self, new_username):
        conn = connect_sys_db()
        # SQL
        query = 'UPDATE users SET username = \'{new_username}\' WHERE id = \'{id}\''.format(
            id=self._id,
            new_username=new_username
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update account's password
    def update_password(self, new_password):
        conn = connect_sys_db()
        # SQL
        query = 'UPDATE users SET password = HEX(AES_ENCRYPT(\'{new_password}\', \'{key}\')) WHERE id = \'{id}\'' \
            .format(
            id=self._id,
            new_password=new_password,
            key=SECRET_KEY
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Register a new user or admin account
    @staticmethod
    def register_account(username, password, admin, email):
        conn = connect_sys_db()
        query = 'SELECT username FROM users WHERE username = \'{username}\''.format(
            username = username
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
            return False, 'This username has already been registered'

        query = 'SELECT email FROM users WHERE email = \'{email}\''.format(
            email=email
        )
        db_result = read_sql(sql=query, con=conn)
        if not db_result.empty:
            return False, 'This email has already been registered'

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

    @staticmethod
    def get_info_by_id(id):
        conn = connect_sys_db()
        # SQL
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

    @staticmethod
    def get_username_by_id(id):
        conn = connect_sys_db()
        # SQL
        query = "Select username FROM users WHERE id = \'{id}\'".format(
            id = id
        )
        db_result = read_sql(sql=query, con=conn)
        return db_result.iloc[0].username

    @staticmethod
    def is_user_exists_by_id(id):
        conn = connect_sys_db()
        # SQL
        query = 'SELECT id FROM users Where id = \'{id}\''.format(
            id=id
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    @staticmethod
    def is_user_exists_by_username(username):
        conn = connect_sys_db()
        # SQL
        query = 'SELECT username FROM users Where username = \'{username}\''.format(
            username=username
        )
        # with mysql(conn) as cursor:
        #     cursor.execute(query)
        #     info = cursor.fetchone()
        # return info is not None
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True
