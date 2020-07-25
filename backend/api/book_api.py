import datetime

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
search_parser.add_argument('page', type=int, required=True)
search_parser.add_argument('rating_from', type=int)
search_parser.add_argument('rating_to', type=int)
search_parser.add_argument('category')

review_parser = reqparse.RequestParser()
review_parser.add_argument('book_id', type=int)
review_parser.add_argument('user_id', type=int)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('book_id', type=int, required=True)
delete_parser.add_argument('user_id', type=int, required=True)

review_page_parser = reqparse.RequestParser()
review_page_parser.add_argument('book_id', type=int, required=True)
review_page_parser.add_argument('page', type=int, required=True)

read_id_parser = reqparse.RequestParser()
read_id_parser.add_argument('book_id', type=int, required=True)

read_parser = reqparse.RequestParser()
read_parser.add_argument('book_id', type=int, required=True)
read_parser.add_argument('year', type=int, required=True)
read_parser.add_argument('month', type=int, required=True)

# Api: Book search
@api.route('/search_page')
class SearchPage(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get search result page")
    @api.expect(search_parser, validate=True)
    def get(self):
        # Get page and book_id from parser
        args = search_parser.parse_args()
        page = args.get('page')
        rating_from = args.get('rating_from')
        rating_to = args.get('rating_to')
        category = args.get('category')

        # Default rating filter is 0 to 5
        if rating_from is None:
            rating_from = 0
        if rating_to is None:
            rating_to = 5
        if rating_to < rating_from:
            return {'message': 'Wrong rating range'}, 201

        content, category = Book.book_search_regex(args.get('search_content'), args.get('category'))
        page_num, last_page_num, total_result_num, all_result= Book.get_book_search_page_num(content, category, rating_from, rating_to, 15)
        # Index out of range
        if page <= 0 or page > page_num:
            return {'message': 'Resource not found'}, 404
        result = Book.get_book_search_page(content, 15, page, page_num, last_page_num, total_result_num, all_result)
        return {'total_page_num': page_num,
                'current_page': page,
                'total_result_num': int(total_result_num),
                'result': result
                }, 200


# Api: Get book's detail
@api.route('/<int:book_id>/detail')
class BookGetDetailByID(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get book's detail by id")
    def get(self, book_id):
        book = Book(book_id)
        detail = book.get_info()
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
        page_num, last_page_num = Review.get_book_review_page_num(book_id, 15)
        # Index out of range
        if (page <= 0 or page > page_num):
            return {'message': 'Resource not found'}, 404
        result = Review.get_book_review_page(book_id, 15, page)
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
    # @requires_login
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
    @api.response(401, 'Failed')
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
        if not Book.is_book_exists_by_id(book_id):
            return {'message': 'Resource not found'}, 404
        if not Collection.is_book_read(user_id, book_id):
            return {'message': 'You can only review and rate after you read the book'}, 401
        # input cannot be empty string
        if book_id is None or rating is None or content == "":
            return {'message': 'Rating or review content cannot be empty'}, 401
        try:
            if Review.new_review(user_id, book_id, rating, content):
                return {'message': 'Post new review successfuly'}, 200
            else:
                return {'message': 'Review already existed'}, 401
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
            return {'message': 'Rating or review content cannot be empty'}, 401
        try:
            if Review.edit_review(user_id, book_id, rating, content):
                return {'message': 'Update review successfully'}, 200
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
        if not Book.is_book_exists_by_id(book_id):
            return {'message': 'Resource not found'}, 404
        if not Review.is_review_exist_by_both_id(user_id, book_id):
            return {'message': 'Resource not found'}, 404
        try:
            Review.delete_review(user_id, book_id)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Delete review successfully'}, 200


# Api: Mark certain book as read
@api.route('/read')
class BookReadApi(Resource):
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
        book_id = args.get('book_id')

        # Get current year and month
        now_year = int(datetime.datetime.now().strftime("%Y"))
        now_month = int(datetime.datetime.now().strftime("%m"))

        if args.get('year') > now_year or args.get('year') < 1900:
            return {'message': 'Invalid year'}, 401
        if args.get('month') > 12 or args.get('month') < 1:
            return {'message': 'Invalid month'}, 401
        if args.get('year') == now_year and args.get('month') > now_month:
            return {'message': 'Invalid month'}, 401
        date = str(args.get('year')) + "-" + str(args.get('month'))
        if Collection.is_book_read(user_id, book_id):
            return {'message': 'This book is already been marked as read'}
        if not Book.is_book_exists_by_id(book_id):
            return {'message': 'Resource not found'}, 404
        try:
            Collection.mark_as_read(user_id, book_id, date)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Mark successfully'}, 200


# Api: Mark certain book as unread
@api.route('/unread')
class BookUnreadApi(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Mark book as unread")
    @api.expect(read_id_parser, validate=True)
    @requires_login
    def post(self):
        # Get user_id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']

        # Get book_id from parser
        args = read_id_parser.parse_args()
        book_id = args.get('book_id')
        if not Book.is_book_exists_by_id(book_id):
            return {'message': 'Resource not found'}, 404
        if not Collection.is_book_read(user_id, book_id):
            return {'message': 'This book is not been marked as read yet'}
        try:
            Collection.mark_as_unread(user_id, book_id)
            if Review.is_review_exist_by_both_id(user_id, book_id):
                Review.delete_review(user_id, book_id)
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500
        return {'message': 'Mark successfully'}, 200

# Api: whether user has read or review this book
@api.route("/read_review_check")
class BookReadReviewCheck(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Check wheather this book has been read or reviewed before")
    @api.expect(read_id_parser, validate=True)
    @requires_login
    def get(self):
        # Get user_id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get book_id from parser
        args = read_id_parser.parse_args()
        book_id = args.get('book_id')
        if not Book.is_book_exists_by_id(book_id):
            return {'message': 'Resource not found'}, 404
        read_flag = Collection.is_book_read(user_id, book_id)
        review_flag = Review.is_review_exist_by_both_id(user_id, book_id)
        return {'read': read_flag,
                'review': review_flag}, 200

# Api: Get most popular books
@api.route("/most_popular_book")
class BookMostPopular(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get the most popular 10 books")
    def get(self):
        return {'books': Book.get_popular_book()}, 200

# Api: Get most popular categories
@api.route("/most_popular_categories")
class BookCategoriesList(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authenticate Failed')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal server error')
    def get(self):
        return {'categories': Book.get_categories_list()}, 200