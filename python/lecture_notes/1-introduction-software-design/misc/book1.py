class Book:

    def __init__(self, title, subtitle, author):
        self.title = title
        self.subtitle = subtitle
        self.author = author

def display_book_info(book):
    print(f'{book.title}: {book.subtitle} by {book.author}')

