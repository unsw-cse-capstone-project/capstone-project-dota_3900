import contextlib
import pymysql
from config import *


def connect_sys_db():
    return pymysql.connect(host=SYS_DB_HOST, user=SYS_DB_USER, password=SYS_DB_PASSWORD, database=SYS_DB_DATABASE,
                           charset=SYS_DB_CHARSET)

@contextlib.contextmanager
def mysql(conn):
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

