# -*- coding:utf-8 -*-

from flask import request
from flask_restplus import Resource, Namespace, fields
from pandas import read_sql
from config import SECRET_KEY
from cls.authenticate_token import auth
from http import HTTPStatus

from lib.sql_linker import connect_sys_db

api = Namespace('token', description='Get a token by username and password')

login_model = api.model('account username-password model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'admin': fields.Integer(required=True)
})


@api.route('')
class Token(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Auth failed')
    @api.doc(description="Generate a authentication token with valid username and password.")
    @api.expect(login_model, validate=True)
    def post(self):
        conn = connect_sys_db()
        login_info = request.json
        username = login_info['username']
        password = login_info['password']
        admin = login_info['admin']

        # validate account
        query = 'SELECT id, username, password, email FROM users WHERE username = \'{username}\' AND' \
                ' password = HEX(AES_ENCRYPT(\'{password}\', \'{key}\')) AND admin = \'{admin}\'' \
            .format(
            username=username,
            password=password,
            key=SECRET_KEY,
            admin=admin,
        )
        db_result = read_sql(sql=query, con=conn)

        if db_result.shape[0]:
            password_encrypt = db_result.iloc[0].password
            account_id = int(db_result.iloc[0].id)
            email = db_result.iloc[0].email
            # return different token depends on different role
            if admin == 1:
                # Admin token
                return {'token': auth.generate_token(account_id, username, password_encrypt, 1, email).decode(),
                        'id': account_id,
                        'username': username,
                        'email': email,
                        'admin': 1,
                        }
            else:
                # User token
                return {'token': auth.generate_token(account_id, username, password_encrypt, 0, email).decode(),
                        'id': account_id,
                        'username': username,
                        'email': email,
                        'admin': 0,
                        }
        conn.close()
        return {'message': 'Uesless login info'}, 401
