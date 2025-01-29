class Book:

    def __init__(self, title, subtitle, author):
        self.title = title
        self.subtitle = subtitle
        self.author = author

    def display_info(self):
        print(f'{self.title}: {self.subtitle} by {self.author}')
