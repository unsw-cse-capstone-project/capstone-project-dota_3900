import json
from flask_restplus import Resource, Namespace, reqparse, fields

from lib.validation_decorator import requires_admin, requires_login
from config import SECRET_KEY
from flask import request
import jwt
import pymysql
from cls.admin import Admin

api = Namespace('admin', description='Manage user account')
admin_add_user_model = api.model('admin_add_user_model', {
    'username': fields.String,
    'password': fields.String,
    'admin': fields.Integer
})
admin_delete_user_model = api.model('admin_delete_user_model', {'username' : fields.String})
admin_update_user_model = api.model('admin_update_user_model', {
    'username': fields.String,
    'new_password': fields.String,
})

@api.route('/users')
class AdminUsersList(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all users' list")
    @requires_admin
    # Get all users list
    def get(self):
        try:
            return Admin.get_user_list(), 200
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

@api.route('/user')
class AdminUser(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Create a new user account")
    @api.expect(admin_add_user_model, validate=True)
    @requires_admin
    # Create a new user account
    def post(self):
        info = request.json
        username = info['username']
        password = info['password']
        admin = info['admin']
        try:
            success, errmsg = Admin.add_new_account(username, password, admin)
            if not success:
                return {'message': errmsg}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Create new user account success'}, 200

    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Delete certain user account")
    @api.expect(admin_delete_user_model, validate=True)
    @requires_admin
    # Delete certain user account
    def delete(self):
        info = request.json
        username = info['username']
        try:
            if not Admin.delete_user(username):
                return {'message': 'Delete user account failed, this user is not exist'}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Delete user account success'}, 200

@api.route('/user/password')
class AdminPassword(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Update certain user's password")
    @api.expect(admin_update_user_model, validate=True)
    @requires_admin
    # Update certain user's password
    def post(self):
        info = request.json
        username = info['username']
        new_password = info['new_password']
        try:
            if Admin.update_user_password(username, new_password):
                return {'message': 'Update user password success'}, 200
            else:
                return {'message': 'Cannot find this user'}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500








