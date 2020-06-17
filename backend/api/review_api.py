import jwt
import pymysql
from flask import request
from flask_restplus import Resource, Namespace, fields
from cls.review_rating import Review_Rating
from config import SECRET_KEY
from lib.validation_decorator import requires_login

api = Namespace('review_rating', description='Review and rating api')
review_content_model = api.model('review_rating_content_model', {
    'book_id': fields.Integer,
    'rating': fields.Integer,
    'content': fields.String
})

# Api: Post a new review
@api.route('/')
class ReviewRatingPost(Resource):
    @api.response(200, 'Success')
    @api.response(200, 'Failed, review already existed')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Post new review and rating")
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
            if Review_Rating.new_review_rating(user_id, book_id, rating, content):
                return {'message': 'Post new review success'}, 200
            else:
                return {'message': 'Review already existed'}, 201
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

# Api: Edit a existed review
@api.route('/review_rating_edit')
class ReviewRatingEdit(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(404, 'Review not found')
    @api.response(500, 'Internal server error')
    @api.doc(description="Edit existed rating and review")
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
        content = info['content']
        rating = info['rating']
        try:
            if Review_Rating.edit_review_rating(user_id, book_id, rating, content):
                return {'message': 'Post new review success'}, 200
            else:
                return {'message': 'Review not found'}, 404
        except pymysql.Error as e:
            return {'message': e.args[1]}, 500

# Api: Get all review posted by current user
@api.route('/user')
class AllUserReviewRating(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews and rating posted by user")
    @requires_login
    def get(self):
        # Get user's id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get review
        result = Review_Rating.get_user_all_review_rating(user_id)
        return {'list': result}, 200

# Api: Get all review of certain book
@api.route('/book/<int:book_id>')
class AllBookReviewRating(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews and rating of certain book")
    @requires_login
    def get(self, book_id):
        result = Review_Rating.get_book_all_review_rating(book_id)
        return {'list': result}, 200

# Api: Get all review of certain book posted by current user
@api.route('/user/book/<int:book_id>')
class AllBookUserReviewRating(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Get all reviews and rating of certain book posted by user")
    @requires_login
    def get(self, book_id):
        # Get user_id from token
        token = request.headers.get('AUTH-TOKEN')
        token_info = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user_id = token_info['id']
        # Get review
        result = Review_Rating.get_book_user_all_review_rating(user_id, book_id)
        return {'list': result}, 200