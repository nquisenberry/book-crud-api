from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "book_name": self.book_name,
            "author": self.author,
            "publisher": self.publisher
        }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Book API Running!"

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict())

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)

    data = request.get_json()

    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']

    db.session.commit()

    return jsonify(book.to_dict())

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})

if __name__ == "__main__":
    app.run(debug=True)