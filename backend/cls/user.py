from cls.account import Account
from cls.admin import Admin
from lib.sql_linker import connect_sys_db, mysql
from config import SECRET_KEY

class User(Account):
    def __init__(self, username):
        Account.__init__(self, username)

