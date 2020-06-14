import json

from flask_restplus import Resource, Namespace, reqparse, fields
from cls.book import Book
from lib.validation_decorator import requires_login
from config import SECRET_KEY
from flask import request, Response
import jwt
import pymysql

api = Namespace('book', description='Book api')


@api.route('/<string:content>')
class BookSearch(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Search books")
    def get(self, content):
        try:
            result = Book.book_search(content)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'list': result}, 200


@api.route('/title/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's title by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'title': info.title}, 200


@api.route('/authors/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's authors by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'authors': info.authors}, 200


@api.route('/publisher/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's publisher by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.publisher}, 200


@api.route('/published_date/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's published_date by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.published_date}, 200


@api.route('/description/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's description by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.description}, 200


@api.route('/ISBN13/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's ISBN13 by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.ISBN13}, 200


@api.route('/categories/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's categories by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.categories}, 200


@api.route('/google_rating/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's google_rating by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.google_rating}, 200


@api.route('/google_ratings_count/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's google_ratings_count by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.google_ratings_count}, 200


@api.route('/book_cover_url/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's book_cover_url by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.book_cover_url}, 200


@api.route('/language/<int:id>')
class BookTitle(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's language by ID")
    def get(self, id):
        info = Book.get_info_by_id(id)
        if info is None:
            return {'message': "Resource not found"}, 404
        else:
            return {'publisher': info.language}, 200