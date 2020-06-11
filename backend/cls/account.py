from pandas import read_sql

from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY

class Account:
    def __init__(self, username):
        self._username = username

    # Update account's username
    def update_username(self, new_username):
        conn = connect_sys_db()
        query = 'UPDATE users SET username = \'{new_username}\' WHERE username = \'{username}\''.format(
            username=self._username,
            new_username=new_username
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update account's password
    def update_password(self, new_password):
        conn = connect_sys_db()
        query = 'UPDATE users SET password = HEX(AES_ENCRYPT(\'{new_password}\', \'{key}\')) WHERE username = \'{username}\''\
            .format(
            username = self._username,
            new_password=new_password,
            key = SECRET_KEY
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Register a new user or admin account
    @staticmethod
    def register_account(username, password, admin):
        conn = connect_sys_db()

        # Get current user number
        query = "SELECT count(*) as users_num from users"
        db_result = read_sql(sql=query, con=conn)
        id = db_result.iloc[0].users_num

        query = 'INSERT INTO users VALUES(\'{id}\', \'{username}\','\
            'HEX(AES_ENCRYPT(\'{password}\', \'{key}\')), \'{admin}\')' \
            .format(
            id=id,
            username=username,
            password=password,
            admin=admin,
            key=SECRET_KEY
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True, ''



def is_user_exists(username):
    conn = connect_sys_db()
    query = 'SELECT username FROM users Where username = \'{username}\''.format(
        username=username
    )
    with mysql(conn) as cursor:
        cursor.execute(query)
        info = cursor.fetchone()
    return info is not None

