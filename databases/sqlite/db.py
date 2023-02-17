import sqlite3

CREATE_TABLE = "CREATE TABLE people (name TEXT PRIMARY KEY, food TEXT)"
SELECT_WHERE = "SELECT * FROM people WHERE name=?"
SELECT = "SELECT * FROM people"
INSERT = "INSERT INTO people VALUES (?, ?)"


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)

    def create_schema(self):
        try:
            self.connection.execute(CREATE_TABLE)
        except sqlite3.OperationalError:
            print("Warning: 'people' table was already created, ignoring...")

    def get(self, name=None):
        cursor = (self.connection.execute(SELECT_WHERE, (name,))
                  if name is not None else self.connection.execute(SELECT))
        return cursor.fetchall()

    def add(self, name, food):
        try:
            self.connection.execute(INSERT, (name, food))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Warning: '%s' is already in the database, ignoring..." % name)
            self.connection.rollback()


if __name__ == '__main__':
    connection = DatabaseConnection('tmp.sqlite')
    connection.create_schema()
    connection.add('jane', 'paella')
    connection.add('john', 'wonton')
    print(connection.get())
