# -*- coding:utf-8 -*-

from flask import request
from flask_restplus import abort
from cls.authenticate_token import auth
from functools import wraps


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authenticate Failed')
        try:
            auth.validate_token(token)
        except Exception as e:
            print(e)
            abort(401, str(e))
        return f(*args, **kwargs)
    return decorated


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        # print(auth.validate_token(token))
        if not token:
            abort(401, 'Authenticate Failed')
        try:
            info = auth.validate_token(token)
            if info['admin'] != 1:
                abort(403, 'Requires admin account')
        except Exception as e:
            print(e)
            abort(401, str(e))
        return f(*args, **kwargs)
    return decorated



