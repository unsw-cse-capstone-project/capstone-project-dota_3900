# -*- coding:utf-8 -*-
import datetime

import jwt
from itsdangerous import SignatureExpired, BadSignature
from time import time
from config import SECRET_KEY, EXPIRE_IN


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self._secret_key = secret_key
        self._expires_in = expires_in

    def generate_token(self, id, username, password_encrypted, admin):
        info = {
            'id': id,
            'username': username,
            'password': password_encrypted,
            'admin': admin,
            'creation_time': time()
        }
        return jwt.encode(info, self._secret_key, algorithm='HS256')

    # check whether token is expire or not
    def is_token_expired(self, info):
        if time() - info['creation_time'] > self._expires_in:
            return True
        return False

    # Validate_token, if success, return token info(decrypted)
    def validate_token(self, token):
        # Get token info by decode the given token
        try:
            info = jwt.decode(token, self._secret_key, algorithms='HS256')
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            raise BadSignature("Invalid Token.")
        # If token is expired
        if self.is_token_expired(info):
            print("expired")
            raise SignatureExpired('Token expired.')
        return info

# create AUTH
auth = AuthenticationToken(SECRET_KEY, EXPIRE_IN)
