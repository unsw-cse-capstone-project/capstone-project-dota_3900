import json
from pandas import read_sql

from cls.collection import Collection
from lib.sql_linker import connect_sys_db, mysql


class Goal:

    # -------------------------------------- Help Func -------------------------------------
    # Is monthly goal already exist
    @staticmethod
    def is_goal_exists(user_id, year, month):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM monthly_goal WHERE (user_id = \'{user_id}\' AND year = \'{year}\' AND month = \'{month}\')".format(
            user_id=user_id,
            year=year,
            month=month
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True

    # Is monthly goal with certain goal number already existed
    @staticmethod
    def is_goal_exists_by_goal(user_id, year, month, goal):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM monthly_goal WHERE (user_id = \'{user_id}\' AND year = \'{year}\' AND month = \'{month}\' AND goal = \'{goal}\')".format(
            user_id=user_id,
            year=year,
            month=month,
            goal=goal
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            return False
        else:
            return True
    # -------------------------------------------------------------------------------------

    # Set monthly goal
    @staticmethod
    def set_goal(user_id, year, month, goal):
        # SQL
        conn = connect_sys_db()
        query = "INSERT INTO monthly_goal VALUES(\'{user_id}\', \'{year}\', \'{month}\', \'{goal}\')".format(
            user_id=user_id,
            year=year,
            month=month,
            goal=goal
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Update monthly goal
    @staticmethod
    def update_goal(user_id, year, month, goal):
        # SQL
        conn = connect_sys_db()
        query = "UPDATE monthly_goal SET goal = \'{goal}\' WHERE (user_id = \'{user_id}\' AND year = \'{year}\' AND month = \'{month}\')".format(
            user_id=user_id,
            year=year,
            month=month,
            goal=goal
        )
        with mysql(conn) as cursor:
            cursor.execute(query)

    # Get certain user's all monthly goal
    @staticmethod
    def get_goal(user_id):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM monthly_goal WHERE user_id = \'{user_id}\'".format(
            user_id=user_id
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Get certain user's monthly goal in certain month
    @staticmethod
    def get_goal_by_date(user_id, year, month):
        # SQL
        conn = connect_sys_db()
        query = "SELECT * FROM monthly_goal WHERE (user_id = \'{user_id}\' AND year = \'{year}\' AND month = \'{month}\')".format(
            user_id=user_id,
            year=year,
            month=month,
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        result = []
        for index in ds:
            result.append(ds[index])
        return result

    # Whether user has reached the goal of certain month
    @staticmethod
    def get_goal_record(user_id, year, month):
        # SQL
        conn = connect_sys_db()
        query = "SELECT goal FROM monthly_goal WHERE (user_id = \'{user_id}\' AND year = \'{year}\' AND month = \'{month}\')".format(
            user_id=user_id,
            year=year,
            month=month,
        )
        db_result = read_sql(sql=query, con=conn)
        if db_result.empty:
            target = 0
        else:
            target = int(db_result.iloc[0].goal)
        # Get all book read by user in that month
        finish_book = Collection.get_read_history_by_date(user_id, year, month)
        finish_num = len(finish_book)
        if finish_num >= target:
            finish_flag = True
        else:
            finish_flag = False
        return target, finish_book, finish_num, finish_flag

    # How many times that user has reached the goal
    @staticmethod
    def get_goal_finish_num(user_id):
        conn = connect_sys_db()
        query = "SELECT * FROM monthly_goal WHERE (user_id = \'{user_id}\')".format(
            user_id=user_id,
        )
        db_result = read_sql(sql=query, con=conn)
        json_str = db_result.to_json(orient='index')
        ds = json.loads(json_str)
        ans = 0
        for index in ds:
            # Get goal record from above function
            target, finish_book, finish_num, finish_flag = Goal.get_goal_record(user_id, ds[index]['year'],ds[index]['month'])
            if finish_flag:
                ans += 1
        return ans