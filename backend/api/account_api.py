import json
from flask_restplus import Resource, Namespace, reqparse, fields

from cls.admin import Admin
from cls.user import User
from lib.validation_decorator import requires_login
from config import SECRET_KEY
from flask import request
import jwt
import pymysql
from cls.account import Account

api = Namespace('account', description='Account setting')
account_password_model = api.model('account_password_model', {'password': fields.String})
account_username_model = api.model('account_username_model', {'username': fields.String})
account_register_model = api.model('account_register_model', {
    'username': fields.String,
    'password': fields.String
})


@api.route('')
class AccountRegister(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Register a new account.")
    @api.expect(account_register_model, validate=True)
    # Register a new user account
    def post(self):
        info = request.json
        username = info['username']
        password = info['password']
        admin = 0
        try:
            success, errmsg = Account.register_account(username, password, 0)
            if not success:
                return {'message': errmsg}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Register new user account success'}, 200


# API for user to change password
@api.route('/password')
class AccountPassword(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Change account password ")
    @api.expect(account_password_model, validate=True)
    @requires_login
    # AccountChangePassword
    def post(self):
        info = request.json
        new_password = info['password']

        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        tokn_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        # Get user object from username
        username = tokn_info['username']
        account = Account(username)
        try:
            account.update_password(new_password)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change password success'}, 200


# API to get user's username and rename
@api.route('/username')
class AccountUsername(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get account username")
    @requires_login
    # AccountGetUsername
    def get(self):
        # get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        username = token_info['username']
        return {'uesrname': username}, 200

    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Rename the current account")
    @api.expect(account_username_model, validate=True)
    @requires_login
    # AccountChangeUsername
    def post(self):
        info = request.json
        new_username = info['username']

        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        # Get user object from username
        username = token_info['username']
        account = Account(username)
        try:
            account.update_username(new_username)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change username success'}, 200


# API to get user's role
@api.route('/role')
class AccountRole(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get account role")
    @requires_login
    # AccountGetRole
    def get(self):
        # get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        admin = token_info['admin']
        return {'admin': admin}, 200


