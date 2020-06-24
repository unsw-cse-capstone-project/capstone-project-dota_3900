import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from cls.book import Book
from cls.collection import Collection
from cls.user import User
from cls.review import Review
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('book', description='Book api')
review_content_model = api.model('review_content_model', {
    'book_id': fields.Integer,
    'rating': fields.Integer,
    'content': fields.String,
})

search_parser = reqparse.RequestParser()
search_parser.add_argument('search_content', required=True)

review_parser = reqparse.RequestParser()
review_parser.add_argument('book_id', type=int)
review_parser.add_argument('user_id', type=int)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('book_id', type=int, required=True)
delete_parser.add_argument('user_id', type=int, required=True)

review_page_parser = reqparse.RequestParser()
review_page_parser.add_argument('book_id', type=int, required=True)
review_page_parser.add_argument('page', type=int, required=True)

read_parser = reqparse.RequestParser()
read_parser.add_argument('book_id', type=int, required=True)


# Api: Get search result
@api.route('/search_result')
class BookSearch(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(500, 'Internal server error')
    @api.doc(description="Search books")
    @api.expect(search_parser, validate=True)
    def get(self):
        # Get search_content by parser
        args = search_parser.parse_args()
        result = Book.book_search(args.get('search_content'))
        return {'list': result}, 200


# Api: Get book's detail
@api.route('/<int:book_id>/detail')
class BookGetDetailByID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's detail by id")
    def get(self, book_id):
        detail = Book.get_info_by_id(book_id)
        if detail is None:
            return {'message': 'Resource not found'}, 404
        else:
            avg_rating = Review.get_book_average_rating(book_id)
            review_preview = Review.get_book_review_from_to(book_id, 0, 2)
            num_rated = Review.get_book_num_rating(book_id)
            return {'book_id': int(detail.id),
                    'title': detail.title,
                    'authors': detail.authors,
                    'publisher': detail.publisher,
                    'published_date': detail.published_date,
                    'description': detail.description,
                    'ISBN13': int(detail.ISBN13),
                    'categories': detail.categories,
                    'google_rating': float(detail.google_rating),
                    'google_ratings_count': int(detail.google_ratings_count),
                    'book_cover_url': detail.book_cover_url,
                    'language': detail.language,
                    'avg_rating': avg_rating,
                    'num_rated': num_rated,
                    'review_preview': review_preview
                    }, 200

# Api: Get info of review_page
@api.route('/review_page')
class ReviewPage(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get review page")
    @api.expect(review_page_parser, validate=True)
    def get(self):
        # Get page and book_id from parser
        args = review_page_parser.parse_args()
        page = args.get('page')
        book_id = args.get('book_id')
        page_num, last_page_num = Review.get_book_review_page_num(book_id, 10)
        # Index out of range
        if (page <= 0 or page > page_num):
            return {'message': 'Resource not found'}, 404
        result = Review.get_book_review_page(book_id, 10, page)
        return {'total_page_num': page_num,
                'current_page': page,
                'reviews': result
                }, 200

# Api: get book's review
@api.route('/review')
class ReviewApi(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get review of certain book posted by certain user")
    @api.expect(review_parser, validate=True)
    @requires_login
    def get(self):
        # Get book_id and user_id from parser
        args = review_parser.parse_args()
        book_id = args.get('book_id')
        user_id = args.get('user_id')
        # If user does not exist
        if (not User.is_user_exists_by_id(user_id)) and (user_id != None):
            return {'message': 'Resource not found'}, 404
        # if book does not exist
        if (not Book.is_book_exists_by_id(book_id)) and (book_id != None):
            return {'message': 'Resource not found'}, 404
        # show reviews posted by certain user by only input user_id
        if (book_id == None and user_id != None):
            result = Review.get_user_reviews(user_id)
            return {'reviews': result}, 200
        # show reviews of certain book by only input book_id
        elif (book_id != None and user_id == None):
            result = Review.get_book_review(book_id)
            return {'reviews': result}, 200
        # show reviews posted by certain user of certain book by input both id
        elif (book_id != None and user_id != None):
            result = Review.get_book_user_review(user_id, book_id)
            return {'reviews': result}, 200
        # book_id and user_id cannot be both empty
        elif (book_id == None and user_id == None):
            return {'message': 'book_id and user_id cannot be both empty'}, 400

    @api.response(200, 'Success')
    @api.response(201, 'Failed, review already existed')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Post new review")
    @api.expect(review_content_model, validate=True)
    @requires_login
    def post(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get book_id and content from json input
        info = request.json
        book_id = info['book_id']
        rating = info['rating']
        content = info['content']
        # input cannot be empty string
        if book_id is None or rating is None or content == "":
            return {'message': 'Rating or review content cannot be empty'}, 201
        try:
            if Review.new_review(user_id, book_id, rating, content):
                return {'message': 'Post new review success'}, 200
            else:
                return {'message': 'Review already existed'}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Edit existed rating and review")
    @api.expect(review_content_model, validate=True)
    @requires_login
    def put(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get book_id and content from json input
        info = request.json
        book_id = info['book_id']
        content = info['content']
        rating = info['rating']
        # input cannot be empty string
        if book_id is None or rating is None or content == "":
            return {'message': 'Rating or review content cannot be empty'}, 201
        try:
            if Review.edit_review(user_id, book_id, rating, content):
                return {'message': 'Update review success'}, 200
            else:
                return {'message': 'Review not found'}, 404
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Delete certain user account")
    @api.expect(delete_parser, validate=True)
    @requires_login
    def delete(self):
        # Get book_id and user_id from parser
        args = delete_parser.parse_args()
        book_id = args.get('book_id')
        user_id = args.get('user_id')
        try:
            if not Review.delete_review(user_id, book_id):
                return {'message': 'Delete review failed, this review does not exist'}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Delete review success'}, 200

# Api: Mark certain book as read
@api.route('/read')
class ReviewApi(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Mark book as read")
    @api.expect(read_parser, validate=True)
    @requires_login
    def post(self):
        # Get user_id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get book_id from parser
        args = read_parser.parse_args()
        try:
            if not Collection.mark_as_read(user_id, args.get('book_id')):
                return {'message': 'Resource not found'}, 404
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Mark success'}, 200
