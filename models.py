import json


class Todos:
    def __init__(self):
        try:
            with open('books.json', 'r') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        return self.books[id]

    def create(self, data):
        data.pop('csrf_token')
        data['id'] = len(self.books)+1
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.books[id] = data
        self.save_all()

    def get_api(self, id):
        book = [book for book in self.all() if book['id'] == id]
        if book:
            return book[0]
        return []

    def create_api(self, data):
        self.books.append(data)
        self.save_all()

    def delete_api(self, id):
        book = self.get_api(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

    def update_api(self, id, data):
        book = self.get_api(id)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            self.save_all()
            return True
        return False


books = Todos()
