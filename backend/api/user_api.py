from flask_restplus import Resource, Namespace, reqparse, fields

from cls.collection import Collection
from cls.review import Review
from cls.user import User
from lib.validation_decorator import requires_login
from config import SECRET_KEY
from flask import request
import jwt
import pymysql
import re

api = Namespace('user', description='User account setting')
user_password_model = api.model('user_password_model', {'old_password': fields.String, 'new_password': fields.String})
user_username_model = api.model('user_username_model', {'username': fields.String})
user_email_model = api.model('email', {'email': fields.String})
user_register_model = api.model('user_register_model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'email': fields.String(required=True),
})


# Api: Register a new user account
@api.route('')
class UserRegister(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Failed')
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
            return {'message': 'Register failed. Username, password or email cannot be empty'}, 401
        if len(username) < 4 or len(username) > 12:
            return {'message': 'The length of username should between 4 and 12.'},401
        if len(password) < 8 or len(password) > 32:
            return {'message': 'The length of password should between 8 and 32'}, 401
        if not (re.search('[a-z]', password) or re.search('[A-Z]', password)):
            return {'message': 'The password should contain at least one letter'}, 401
        try:
            success, errmsg = User.register_account(username, password, 0, email)
            if not success:
                return {'message': errmsg}, 401
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Register new user account successfully'}, 200


# Api: Update user's password
@api.route('/password')
class UserUpdatePassword(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Change user account password ")
    @api.expect(user_password_model, validate=True)
    @requires_login
    def put(self):
        info = request.json
        new_password = info['new_password']
        old_password = info['old_password']
        # new password cannot be empty string
        if new_password == "" or old_password == "":
            return {'message': 'Update failed. Both old password and new password cannot be empty'}, 401
        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        # Get user object
        id = token_info['id']
        user = User(id)
        try:
            if not user.update_password(old_password, new_password):
                return {'message': 'Old password is wrong'}, 401
            else:
                return {'message': 'Change password successfully'}, 200
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500


# Api: Update user's username
@api.route('/username')
class UserUpdateUsername(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Rename the account")
    @api.expect(user_username_model, validate=True)
    @requires_login
    def put(self):
        info = request.json
        new_username = info['username']
        # input cannot be empty string
        if new_username == "":
            return {'message': 'Update failed. new username cannot be empty'}, 401
        if User.is_user_exists_by_username(new_username):
            return {'message': 'This user already existed'}, 401
        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        # Get user object
        id = token_info['id']
        user = User(id)
        try:
            user.update_username(new_username)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change username successfully'}, 200

# Api: Update user's username
@api.route('/email')
class UserUpdateEmail(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Update the user's email")
    @api.expect(user_email_model, validate=True)
    @requires_login
    def put(self):
        info = request.json
        new_email = info['email']
        # input cannot be empty string
        if new_email == "":
            return {'message': 'Update failed. new username cannot be empty'}, 401
        if User.is_user_exists_by_email(new_email):
            return {'message': 'This email already been registered'}, 401
        # Get user's detail from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        # Get user object
        id = token_info['id']
        user = User(id)
        try:
            user.update_email(new_email)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Change email address successfully'}, 200


# Api: Get username by ID
@api.route('/<int:user_id>/detail')
class UserGetDetailByID(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's detail by ID")
    def get(self, user_id):
        user = User(user_id)
        info = user.get_info()
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
        user = User(user_id)
        info = user.get_info()
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


@api.route('/<int:user_id>/dashboard_tags')
class UserDashboardTag(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get user's dashboard tag")
    def get(self, user_id):
        if not User.is_user_exists_by_id(user_id):
            return {'message': 'Resource not found'}, 404
        collection_num = Collection.get_num_collection(user_id)
        readhistory_num = Collection.get_num_read_collection(user_id, Collection.get_readcollection_id(user_id))
        myreviews_num = Review.get_user_num_review(user_id)
        return {'collections_num': collection_num,
                'ReadHistory_num': readhistory_num,
                'MyReview_num': myreviews_num
                }, 200
