from flask_restplus import Resource, Namespace, reqparse
from flask_restplus.inputs import boolean

from cls.book import Book
from cls.recommend import Recommend

api = Namespace('recommend', description='recommend api')
book_parser = reqparse.RequestParser()
book_parser.add_argument('book_id', type=int, required=True)

recommend_parser = reqparse.RequestParser()
recommend_parser.add_argument('book_id', type=int, required=True)
recommend_parser.add_argument('author', type=boolean, required=True)
recommend_parser.add_argument('category', type=boolean, required=True)

# Api: Recommend by category
@api.route('/recommend_by_category')
class RecommendByCategory(Resource):
    @api.expect(book_parser, validate=True)
    def get(self):
        args = book_parser.parse_args()
        book_id = args.get('book_id')
        book = Book(book_id)
        # Get reference book's category
        category = book.get_info().categories
        result = Recommend.recommend_by_category(category, 6, book_id)
        if not result:
            return {'message': 'There is no more book similar with this book, try another mode'}, 200
        return {'books': result}, 200

# Api: Recommend by author
@api.route('/recommend_by_author')
class RecommendByAuthor(Resource):
    @api.expect(book_parser, validate=True)
    def get(self):
        args = book_parser.parse_args()
        book_id = args.get('book_id')
        book = Book(book_id)
        # Get reference book's author
        author = book.get_info().authors
        result = Recommend.recommend_by_author(author, 6, book_id)
        if not result:
            return {'message': 'There is no more book similar with this book, try another mode'}, 200
        return {'books': result}, 200

# Api: Recommend by published date
@api.route('/recommend_by_publishedDate')
class RecommendByPublishedDate(Resource):
    @api.expect(book_parser, validate=True)
    def get(self):
        args = book_parser.parse_args()
        book_id = args.get('book_id')
        book = Book(book_id)
        # Get reference book's published date
        published_date = book.get_info().published_date
        result = Recommend.recommend_by_publishedDate(published_date[0:3], 6, book_id)
        if not result:
            return {'message': 'There is no more book similar with this book, try another mode'}, 200
        return {'books': result}, 200

