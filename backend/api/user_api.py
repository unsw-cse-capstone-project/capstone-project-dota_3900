from flask_restplus import Resource, Namespace, reqparse, fields
from cls.user import User
from lib.validation_decorator import requires_login
from config import SECRET_KEY
from flask import request
import jwt
import pymysql


api = Namespace('user', description='User account setting')
user_password_model = api.model('user_password_model', {'password': fields.String})
user_username_model = api.model('user_username_model', {'username': fields.String})
user_register_model = api.model('user_register_model', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
})

# Api: Register a new user account
@api.route('')
class UserRegister(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Register a new user account.")
    @api.expect(user_register_model, validate=True)
    def post(self):
        info = request.json
        username = info['username']
        password = info['password']
        email = info['email']
        admin = 0
        try:
            success, errmsg = User.register_account(username, password, 0, email)
            if not success:
                return {'message': errmsg}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Register new user account success'}, 200


# Api: Update user's password
@api.route('/password')
class UserupdatePassword(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Change user account password ")
    @api.expect(user_password_model, validate=True)
    @requires_login
    def post(self):
        info = request.json
        new_password = info['password']

        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        tokn_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        # Get user object
        id = tokn_info['id']
        account = User(id)
        try:
            account.update_password(new_password)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change password success'}, 200


# Api: Update user's username
@api.route('/username')
class UserUpdateUsername(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Rename the account")
    @api.expect(user_username_model, validate=True)
    @requires_login
    def post(self):
        info = request.json
        new_username = info['username']

        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        # Get user object
        id = token_info['id']
        account = User(id)
        try:
            account.update_username(new_username)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change username success'}, 200

# Api: Get username by ID
@api.route('/username/<int:user_id>')
class UserGetUsername(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's username by ID")
    def get(self, user_id):
        info = User.get_info_by_id(user_id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'username': info.username}, 200


# Api: Get user's role by ID
@api.route('/role/<int:user_id>')
class UserGetRole(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's role by ID")
    def get(self, user_id):
        info = User.get_info_by_id(user_id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'admin': int(info.admin)}, 200

# Api: Get user's role by ID
@api.route('/email/<int:user_id>')
class UserGetRole(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's role by ID")
    def get(self, user_id):
        info = User.get_info_by_id(user_id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'email': info.email}, 200

# Api: Get current user's ID
@api.route('/id')
class UserGetRole(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's ID")
    @requires_login
    def get(self):
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return {'id': token_info['id']}


