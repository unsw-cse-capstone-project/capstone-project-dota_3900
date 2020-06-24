import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from cls.collection import Collection
from cls.review import Review
from cls.user import User
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('collection', description='Collection api')

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

collection_user_id_parser = reqparse.RequestParser()
collection_user_id_parser.add_argument('user_id', type=int, required=True)


# Api: change to Collection
@api.route('/')
class CollectionApi(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Create new collection")
    @api.expect(collection_name_parser, validate=True)
    @requires_login
    def post(self):
        # Get user's id from Token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get collection_name from parser
        args = collection_name_parser.parse_args()
        name = args.get('collection_name')
        # Name input cannot be empty string
        if name == "":
            return {'message': "Collection's name cannot be empty"}, 201
        try:
            if Collection.post_new_collection(user_id, name):
                return {'message': 'Create new collection successfully'}, 200
            else:
                return {'message': 'This collection already exist'}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Update collection's name")
    @api.expect(collection_update_name_parser, validate=True)
    @requires_login
    def put(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get new_name and collection_id from parser
        args = collection_update_name_parser.parse_args()
        new_name = args.get('new_name')
        collection_id = args.get('collection_id')
        # Name input cannot be empty
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
    @api.expect(collection_user_id_parser, validate=True)
    # @requires_login
    def get(self):
        # Get user_id from parser
        args = collection_user_id_parser.parse_args()
        user_id = args.get('user_id')
        result = Collection.get_user_collection(user_id)
        collection_num = Collection.get_num_collection(user_id)
        readhistory_num = Collection.get_num_read_collection(user_id, Collection.get_readcollection_id(user_id))
        myreviews_num = Review.get_user_num_review(user_id)
        if result == None:
            return {'message': 'Resource not found'}, 404
        return {'collections_num': collection_num,
                'ReadHistory_num': readhistory_num,
                'MyReview_num': myreviews_num,
                'Collections': result
                }, 200

    @api.response(200, 'Success')
    @api.response(200, 'Failed')
    @api.response(404, 'Resource not found')
    @api.response(401, 'Authenticate Failed')
    @api.expect(collection_delete_parser, validate=True)
    @api.doc(description="Delete collection")
    @requires_login
    def delete(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get collection_id from parser
        args = collection_delete_parser.parse_args()
        collection_id = args.get('collection_id')
        read_collection_id = Collection.get_readcollection_id(user_id)
        main_collection_id = read_collection_id - 1
        if collection_id == read_collection_id or collection_id == read_collection_id:
            return {'message': 'Read History and Main collection cannot be deleted'}, 201
        if Collection.delete_collection(user_id, collection_id):
            return {'message': 'Delete collection successfully'}, 200
        else:
            return {'message': 'Resource not found'}, 404

# Api: changes to books in collection
@api.route('/books')
class CollectionBooksApi(Resource):
    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get books in collection")
    @api.expect(collection_get_book_parser, validate=True)
    # @requires_login
    def get(self):
        # Get user'id from Token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get collection_id from parser
        args = collection_get_book_parser.parse_args()
        flag, books = Collection.get_book_in_collection(args.get('collection_id'), user_id)
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
    @requires_login
    def post(self):
        # Get collection_id and book_id from parser
        args = collection_add_book_parser.parse_args()
        flag, message = Collection.add_book_to_collection(args.get('collection_id'), args.get('book_id'))
        return {'message': message}, flag

    @api.response(200, 'Success')
    @api.response(201, 'Invalid input')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Delete book in collection")
    @api.expect(collection_add_book_parser, validate=True)
    def delete(self):
        # Get collection_id and book_id from parser
        args = collection_add_book_parser.parse_args()
        if Collection.delete_book_in_collection(args.get('collection_id'), args.get('book_id')):
            return {'message': 'Delete book successfully'}, 200
        else:
            return {'message': 'Resource not found'}, 404
