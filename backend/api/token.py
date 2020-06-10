# -*- coding:utf-8 -*-

from flask import request
from flask_restplus import Resource, Namespace, fields
from cls.authenticate_token import auth
from lib.validation_decorator import requires_login

api = Namespace('token', description='Get a token by username and password')

login_model = api.model('account username-password model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('')
class Token(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Auth failed')
    @api.doc(description="Generate a authentication token with valid username and password.")
    @api.expect(login_model, validate=True)
    def post(self):
        login_info = request.json
        username = login_info['username']
        password = login_info['password']

        # validate account
        # TODO: Create account database
        if username == 'admin' and password == 'admin':
            return {'token': auth.generate_token(username, password, 'some_email@email.com', 'admin').decode()}
        else:
            return {'message': 'Authorization has been refused for those credentials'}, 401

    @api.response(200, 'Success')
    @api.response(401, 'Auth failed')
    @api.doc(description="This is for testing decorator.")
    @requires_login
    def get(self):
        return {'message': 'Test successfully'}, 200
        pass

