import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from cls.book import Book
from cls.review import Review
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('book', description='Book api')
review_content_model = api.model('review_content_model', {
    'book_id': fields.Integer,
    'rating': fields.Integer,
    'content': fields.String
})

# review_parser = reqparse.RequestParser()
# review_parser.add_argument('book_id', type=int, required=True)
# review_parser.add_argument('user_id', type=int, required=True)

search_parser = reqparse.RequestParser()
search_parser.add_argument('search_content', required=True)

review_parser = reqparse.RequestParser()
review_parser.add_argument('book_id', type=int)
review_parser.add_argument('user_id', type=int)


# Api: Get search result
@api.route('/search_result')
class BookSearch(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Search books")
    @api.expect(search_parser, validate=True)
    def get(self):
        args = search_parser.parse_args()
        result = Book.book_search(args.get('search_content'))
        return {'list': result}, 200

# Api: Get search result
@api.route('/<int:book_id>/detail')
class BookDetail(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's detail by id")
    def get(self, book_id):
        detail = Book.get_info_by_id(book_id)
        if detail is None:
            return {'message': 'Resource not found'}, 404
        else:
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
                    'language': detail.language
                }

@api.route('/<int:book_id>/reviews')
class BookReviews(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews of this book")
    @requires_login
    def get(self, book_id):
        # Get review
        result = Review.get_book_all_review(book_id)
        return {'reviews': result}, 200

@api.route('/<int:book_id>/avg_rating')
class BookAverageRating(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews of this book")
    @requires_login
    def get(self, book_id):
        # Get review
        result = Review.get_book_average_rating(book_id)
        return {'avg_rating': result}, 200

@api.route('/<int:book_id>/<int:user_id>/review')
class BookUserReview(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get review of certain book posted by certain user")
    @requires_login
    def get(self, book_id, user_id):
        # Get review
        result = Review.get_book_user_all_review(user_id, book_id)
        return {'Reviews': result}, 200

# @api.route('/review')
# class BookUserReview(Resource):
#     @api.response(200, 'Success')
#     @api.response(400, 'Illegal user')
#     @api.response(401, 'Failed login')
#     @api.response(500, 'Internal server error')
#     @api.doc(description="Get review of certain book posted by certain user")
#     @api.expect(review_parser, validate=True)
#     # @requires_login
#     def get(self):
#         args = review_parser.parse_args()


@api.route('/review')
class ReviewPost(Resource):
    @api.response(200, 'Success')
    @api.response(200, 'Failed, review already existed')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
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
        try:
            if Review.new_review(user_id, book_id, rating, content):
                return {'message': 'Post new review success'}, 200
            else:
                return {'message': 'Review already existed'}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Review not found')
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
        try:
            if Review.edit_review(user_id, book_id, rating, content):
                return {'message': 'Update review success'}, 200
            else:
                return {'message': 'Review not found'}, 404
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500


@api.route('/<int:book_id>/review')
class ReviewDelete(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Delete certain user account")
    @requires_login
    def delete(self, book_id):
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        try:
            if not Review.delete_review(user_id, book_id):
                return {'message': 'Delete review failed, this review does not exist'}, 402
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Delete review success'}, 200