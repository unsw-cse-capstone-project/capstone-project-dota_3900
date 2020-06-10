# -*- coding:utf-8 -*-

import jwt
from itsdangerous import SignatureExpired, BadSignature
from time import time
from settings import SECRET_KEY, EXPIRE_IN


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self._secret_key = secret_key
        self._expires_in = expires_in

    def generate_token(self, username, password_encrypted, email, role):
        info = {
            'username': username,
            'password': password_encrypted,
            'email': email,
            'role': role,
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
        try:
            if self.is_token_expired(info):
                raise SignatureExpired('Token expired.')

            # check whether this token has valid username and password
            # TODO: complete account database and validation function
            if info['username'] == 'admin' and info['password'] == 'admin':
                return info
            else:
                raise BadSignature("Invalid Token.")
        except KeyError:
            raise BadSignature("Invalid Token.")


# create AUTH
auth = AuthenticationToken(SECRET_KEY, EXPIRE_IN)
