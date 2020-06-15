from cls.user import User, is_user_exists
from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY
from pandas import read_sql
import json


class Admin(User):
    def __init__(self, id):
        User.__init__(self, id)

    # Admin adds new account (User/Admin)
    @staticmethod
    def add_new_account(username, password, admin):
        return User.register_account(username, password, admin)

    # Admin deletes user account
    @staticmethod
    def delete_user(username):
        if not is_user_exists(username):
            return False
        conn = connect_sys_db()
        # SQL
        query = 'DELETE FROM users WHERE username = \'{username}\' AND admin = \'{admin}\'' \
            .format(username=username, admin=0)
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Admin updates certain user account's password
    @staticmethod
    def update_user_password(username, new_password):
        if not is_user_exists(username):
            return False
        conn = connect_sys_db()
        # SQL
        query = 'UPDATE users SET password = HEX(AES_ENCRYPT(\'{new_password}\', \'{key}\'))' \
                ' WHERE username = \'{username}\' AND' \
                ' admin = \'{admin}\'' \
            .format(
            username=username,
            new_password=new_password,
            key=SECRET_KEY,
            admin=0
        )
        with mysql(conn) as cursor:
            cursor.execute(query)
        return True

    # Admin gets all users list
    @staticmethod
    def get_user_list():
        conn = connect_sys_db()
        sql = 'select id, username, admin from users'
        users = read_sql(con=conn, sql=sql)
        json_str = users.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return {"list": result}
