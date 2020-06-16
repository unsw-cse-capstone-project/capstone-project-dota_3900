from flask_restplus import Resource, Namespace
from cls.book import Book

api = Namespace('book', description='Book api')

# Api: Get search result
@api.route('/<string:content>')
class BookSearch(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Illegal user')
    @api.response(401, 'Failed login')
    @api.response(500, 'Internal server error')
    @api.doc(description="Search books")
    def get(self, content):
        result = Book.book_search(content)
        return {'list': result}, 200

# Api: Get book's title by book_id
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

# Api: Get book's author by book_id
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

# Api: Get book's publisher by book_id
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

# Api: Get book's published_date by book_id
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

# Api: Get book's description by book_id
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

# Api: Get book's ISBN13 by book_id
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
            return {'publisher': int(info.ISBN13)}, 200

# Api: Get book's categories by book_id
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

# Api: Get book's google_rating by book_id
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

# Api: Get book's google_rating_count by book_id
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

# Api: Get book's book_cover_url by book_id
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

# Api: Get book's language by book_id
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