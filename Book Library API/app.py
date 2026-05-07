from flask import Flask, request, jsonify #imports necessary packages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #creates app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookLibrary.db" #creates database
db = SQLAlchemy(app) #links app to database


class Book(db.Model):  #creates database columns
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    genre = db.Column(db.String, nullable = False)
    available = db.Column(db.Boolean, default = True)

    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "available": self.available
        }

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Book Library API"})

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all() #gets all books from database
    return jsonify([book.to_dict() for book in books])

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id) #gets book based on id
    if book: # if it  exists
        return jsonify([book.to_dict()]) #return details in json format
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route("/books", methods=["POST"])
def add_books():
    data = request.get_json() #
    #Validating before touching database
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    if not data.get("author"):
        return jsonify({"error": "Author is required"}), 400
    if not data.get("year"):
        return jsonify({"error": "Year is required"}), 400
    if not isinstance(data.get("year"), int):
        return jsonify({"error": "Year must be a number required"}), 400
    if not data.get("genre"):
        return jsonify({"error": "Genre is required"}), 400

    new_book = Book(
        title=data["title"],
        author=data["author"],
        year=data["year"],
        genre=data["genre"]
    )

    db.session.add(new_book) #adds the new book to the database
    db.session.commit() #saves it
    return jsonify(new_book.to_dict()), 201

@app.route("/books/<int:id>", methods=["PUT"]) #Put method updates all field
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    else:
        data = request.get_json()
        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400
        if not data.get("author"):
            return jsonify({"error": "Author is required"}), 400
        if not data.get("year"):
            return jsonify({"error": "Year is required"}), 400
        if not isinstance(data.get("year"), int):
            return jsonify({"error": "Year must be a number required"}), 400
        if not data.get("genre"):
            return jsonify({"error": "Genre is required"}), 400

        book.title = data["title"]
        book.author = data["author"]
        book.year = data["year"]
        book.genre = data["genre"]

        db.session.commit()
        return jsonify(book.to_dict())

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    else:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200


@app.route("/books/<int:id>/borrow", methods=["PATCH"]) #Patch ,ethod updates one specific field
def borrow_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    else:
        book.available = False
        db.session.commit()
        return jsonify(book.to_dict())


@app.route("/books/<int:id>/return", methods=["PATCH"])
def return_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    else:
        book.available = True
        db.session.commit()
        return jsonify(book.to_dict())


if __name__ == "__main__":
    app.run(debug=True)

# 100 ==> Continue
# 200 ==> Ok
# 201 ==> Created
# 204 ==> No content
# 301 ==> Moved permanently
# 304 ==> Not modified
# 400 ==> Bad request
# 401 ==> Unauthorised
# 403 ==> Forbidden
# 404 ==> Not found
# 405 ==> Method not allowed
# 408 ==> Request timeout
# 429 ==> Too many request
# 500 ==> Internal server error
# 502 ==> Bad gateway
# 503 ==> Service unavailable
# 504 ==> Gateway timeout
