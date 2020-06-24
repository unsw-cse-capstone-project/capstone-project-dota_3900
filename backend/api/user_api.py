from flask_restplus import Resource, Namespace, reqparse, fields

from cls.collection import Collection
from cls.review import Review
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
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'email': fields.String(required=True),
})


# Api: Register a new user account
@api.route('')
class UserRegister(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(500, 'Internal server error')
    @api.doc(description="Register a new user account.")
    @api.expect(user_register_model, validate=True)
    def post(self):
        # Get info from json input
        info = request.json
        username = info['username']
        password = info['password']
        email = info['email']
        # input cannot be empty string
        if username == "" or password == "" or email == "":
            return {'message': 'Register failed. Username, password or email cannot be empty'}, 201
        try:
            success, errmsg = User.register_account(username, password, 0, email)
            if not success:
                return {'message': errmsg}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Register new user account success'}, 200


# Api: Update user's password
@api.route('/password')
class UserUpdatePassword(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Change user account password ")
    @api.expect(user_password_model, validate=True)
    @requires_login
    def put(self):
        info = request.json
        new_password = info['password']
        # new password cannot be empty string
        if new_password == "":
            return {'message': 'Update failed. new password cannot be empty'}, 201
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
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Rename the account")
    @api.expect(user_username_model, validate=True)
    @requires_login
    def put(self):
        info = request.json
        new_username = info['username']
        # input cannot be empty string
        if new_username == "":
            return {'message': 'Update failed. new username cannot be empty'}, 201
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
@api.route('/<int:user_id>/detail')
class UserGetDetailByID(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's detail by ID")
    def get(self, user_id):
        info = User.get_info_by_id(user_id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'user_id': int(user_id),
                    'username': info.username,
                    'email': info.email,
                    'admin': int(info.admin),
                    }, 200

# Api: Get username by ID
@api.route('/detail')
class UserGetCurrDetailByID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get current user's detail by ID")
    @requires_login
    def get(self):
        # Get user_id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        info = User.get_info_by_id(user_id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'user_id': int(user_id),
                    'username': info.username,
                    'email': info.email,
                    'admin': int(info.admin),
                    }, 200


# Api: Get current user's ID
@api.route('/my_user_id')
class UserGetCurrID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's ID")
    @requires_login
    def get(self):
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return {'id': token_info['id']}

# Api: Get user's all review
@api.route('/<int:user_id>/reviews')
class UserGetReviewsByID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews and rating posted by user")
    def get(self, user_id):
        # Get review
        if not User.is_user_exists_by_id(user_id):
            return {'message': "Resource not found"}, 404
        result = Review.get_user_reviews(user_id)
        return {'list': result}, 200

# Api: Get user's all collections
@api.route('/<int:user_id>/collections')
class UserGetCollectionByID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's collection")
    def get(self, user_id):
        # Get review
        if not User.is_user_exists_by_id(user_id):
            return {'message': "Resource not found"}, 404
        result = Collection.get_user_collection(user_id)
        return {'list': result}, 200
