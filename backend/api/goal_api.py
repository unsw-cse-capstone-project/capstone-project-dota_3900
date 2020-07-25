from datetime import datetime
import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse, inputs

from cls.goal import Goal
from cls.user import User
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('goal', description='Monthly Goal api')

goal_post_parser = reqparse.RequestParser()
goal_post_parser.add_argument('goal', type=int, required=True)

goal_get_parser = reqparse.RequestParser()
goal_get_parser.add_argument('user_id', type=int, required=True)


# Api: Goal
@api.route('')
class GoalApi(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Set new monthly goal")
    @api.expect(goal_post_parser, validate=True)
    @requires_login
    def post(self):
        # Get user's id from Token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get parameter from parser
        args = goal_post_parser.parse_args()
        goal = args.get('goal')
        year = int(datetime.now().year)
        month = int(datetime.now().month)
        print(year, month, goal, user_id)
        if goal < 0:
            return {'message': 'Invalid monthly goal'}, 401
        # Is this goal existed
        if Goal.is_goal_exists(user_id, year, month):
            if Goal.is_goal_exists_by_goal(user_id, year, month, goal):
                return {'message': 'You need to set a new monthly goal'}, 401
            try:
                Goal.update_goal(user_id, year, month, goal)
            except pymysql.Error as e:
                return {'message': e.args[1]}, 500
        else:
            try:
                Goal.set_goal(user_id, year, month, goal)
            except pymysql.Error as e:
                return {'message': e.args[1]}, 500
        return {'message': 'Monthly goal set successfully'}, 200

    @api.response(200, 'Success')
    @api.response(401, 'Failed')
    @api.response(500, 'Internal server error')
    @api.expect(goal_get_parser, validate=True)
    @api.doc(description="Get current user's monthly goal")
    def get(self):
        args = goal_get_parser.parse_args()
        user_id = args.get('user_id')
        if not User.is_user_exists_by_id(user_id):
            return {'message': 'Resource not found'}, 404
        # Get current year and month
        year = int(datetime.now().year)
        month = int(datetime.now().month)
        target, finish_book, finish_num, finish_flag = Goal.get_goal_record(user_id, year, month)
        reach_goal_num = Goal.get_goal_finish_num(user_id)
        if target != 0:
            finish_ratio = "%.2f%%" % (float(finish_num) / float(target) * 100)
        else:
            finish_ratio = 0
        return {'target': target,
                'finish_ratio': finish_ratio,
                'finish_num': finish_num,
                'reach_goal_num': reach_goal_num,
                'finish_book': finish_book}, 200
