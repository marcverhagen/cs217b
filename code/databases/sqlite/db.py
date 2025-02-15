import sys, sqlite3

SQL_CREATE = "CREATE TABLE people (name TEXT PRIMARY KEY, food TEXT)"
SQL_SELECT = "SELECT * FROM people"
SQL_INSERT = "INSERT INTO people VALUES (?, ?)"


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)#, check_same_thread=False)

    def create_schema(self):
        try:
            self.connection.execute(SQL_CREATE)
        except sqlite3.OperationalError:
            print("Warning: 'people' table was already created, ignoring...")

    def get(self, name=None):
        cursor = (self.connection.execute(f'{SQL_SELECT} WHERE name="{name}"')
                  if name is not None else self.connection.execute(SQL_SELECT))
        return cursor.fetchall()

    def add(self, name, food):
        try:
            self.connection.execute(SQL_INSERT, (name, food))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Warning: '%s' is already in the database, ignoring..." % name)
            self.connection.rollback()
            return False


if __name__ == '__main__':

    dbname = sys.argv[1] if len(sys.argv) > 1 else 'tmp'
    connection = DatabaseConnection(f'{dbname}.sqlite')
    connection.create_schema()
    connection.add('jane', 'paella')
    connection.add('john', 'wonton')
    print(connection.get())
