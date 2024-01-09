from flask import (Flask, request, render_template, redirect,
                   url_for, abort, make_response, jsonify)
from forms import TodoForm
from models import books


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xyz123'


@app.route("/")
def index():
    return redirect(url_for("todos_list"))


@app.route("/books/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("todos_list"))

    return render_template("books.html", form=form,
                           books=books.all(), error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def todos_details(book_id):
    book = books.get(book_id - 1)  # numerowanie od 1 a nie o 0
    form = TodoForm(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("todos_list"))
    return render_template("book.html", form=form, book_id=book_id)


@app.route("/api/v1/books/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(books.all())


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_todo(book_id):
    book = books.get_api(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/v1/books/", methods=["POST"])
def create_todo():
    if not request.json or 'title' not in request.json:
        abort(400)
    try:
        _id = books.all()[-1]['id'] + 1
    except IndexError:
        _id = 1
    book = {
        'id': _id,
        'title': request.json['title'],
        'author': request.json['author'],
        'year': request.json['year'],
        'number_of_pages': request.json['number_of_pages'],
        'language': request.json['language'],
        'form_of': request.json['form_of'],
        'genre': request.json['genre'],
        'done': False
    }

    books.create(book)
    return jsonify({'book': book}), 201


@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_todo(book_id):
    result = books.delete_api(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_todo(book_id):
    book = books.get_api(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'year' in data and not isinstance(data.get('year'), int),
        'number_of_pages' in data and not isinstance(data.get('number_of_pages'), int),
        'language' in data and not isinstance(data.get('language'), str),
        'form_of' in data and not isinstance(data.get('form_of'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'year': data.get('year', book['year']),
        'number_of_pages': data.get('number_of_pages', book['number_of_pages']),
        'language': data.get('language', book['language']),
        'form_of': data.get('form_of', book['form_of']),
        'genre': data.get('genre', book['genre']),
        'done': data.get('done', book['done']),
        'id': book_id,
    }
    books.update(book_id, book)
    return jsonify({'book': book}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}),
                         404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}),
                         400)


if __name__ == "__main__":
    app.run(debug=True)
