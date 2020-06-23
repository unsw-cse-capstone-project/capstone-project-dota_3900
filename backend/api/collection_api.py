import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from cls.collection import Collection
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('collection', description='Collection api')
# collection_create_model = api.model('collection_create_model',{
#     'name': fields.String
# })

collection_name_parser = reqparse.RequestParser()
collection_name_parser.add_argument('collection_name', required=True)

collection_update_name_parser = reqparse.RequestParser()
collection_update_name_parser.add_argument('collection_id', type=int, required=True)
collection_update_name_parser.add_argument('new_name', required=True)

collection_delete_parser = reqparse.RequestParser()
collection_delete_parser.add_argument('collection_id', type=int, required=True)

collection_get_book_parser = reqparse.RequestParser()
collection_get_book_parser.add_argument('collection_id', type=int, required=True)

collection_add_book_parser = reqparse.RequestParser()
collection_add_book_parser.add_argument('collection_id', type=int, required=True)
collection_add_book_parser.add_argument('book_id', type=int, required=True)



@api.route('/')
class CollectionApi(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Create new collection")
    # @api.expect(collection_create_model, validate=True)
    @api.expect(collection_name_parser, validate=True)
    @requires_login
    def post(self):
        args = collection_name_parser.parse_args()
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get collection's name from json input
        info = request.json
        # name = info['name']
        name = args.get('collection_name')
        if name == "":
            return {'message': "Collection's name cannot be empty"}, 201
        try:
            if Collection.post_new_collection(user_id, name):
                return {'message': 'Create new collection success'}, 200
            else:
                return {'message': 'This collection already exist'}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Update collection's name")
    # @api.expect(collection_create_model, validate=True)
    @api.expect(collection_update_name_parser, validate=True)
    @requires_login
    def put(self):
        args = collection_update_name_parser.parse_args()
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        new_name = args.get('new_name')
        collection_id = args.get('collection_id')
        if new_name == "":
            return {'message': "Collection's name cannot be empty"}, 201
        try:
            flag, message = Collection.update_collection_name(user_id, collection_id, new_name)
            if not flag:
                return {'message': message}, 201
            else:
                return {'message': message}, 200
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.doc(description="Get all collections of current user")
    @requires_login
    def get(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        result = Collection.get_user_collection(user_id)
        return {'Collections': result}, 200

    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    @api.response(401, 'Authenticate Failed')
    @api.expect(collection_delete_parser, validate=True)
    @api.doc(description="Delete collection")
    @requires_login
    def delete(self):
        args = collection_delete_parser.parse_args()
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        if Collection.delete_collection(user_id, args.get('collection_id')):
            return {'message': 'Delete collection success'}, 200
        else:
            return {'message': 'Resource not found'}, 404


@api.route('/books')
class CollectionApi(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get books in collection")
    @api.expect(collection_get_book_parser, validate=True)
    # @requires_login
    def get(self):
        args = collection_get_book_parser.parse_args()
        flag, books = Collection.get_book_in_collection(args.get('collection_id'))
        if not flag:
            return {'message': 'Resource not found'}, 404
        else:
            return {'books': books}, 200

    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Add books to collection")
    @api.expect(collection_add_book_parser, validate=True)
    # @requires_login
    def post(self):
        args = collection_add_book_parser.parse_args()
        flag, message = Collection.add_book_to_collection(args.get('collection_id'), args.get('book_id'))
        return {'message': message}, flag

    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Add books to collection")
    @api.expect(collection_add_book_parser, validate=True)
    def delete(self):
        args = collection_add_book_parser.parse_args()
        if Collection.delete_book_in_collection(args.get('collection_id'), args.get('book_id')):
            return {'message': 'Delete book success'}, 200
        else:
            return {'message': 'Resource not found'}, 404

