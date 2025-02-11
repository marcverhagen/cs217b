import os, sys, sqlite3


insert_person_query = "INSERT INTO people VALUES (?, ?)"
insert_food_query = "INSERT INTO food VALUES (?, ?)"

get_person_query = "SELECT people.name, address, food " + \
                   "FROM people, food " + \
                   "WHERE people.name = ? AND people.name = food.name;"


class People(object):

    def __init__(self, dbfile, check_same_thread=True):
        self.initialized = True if os.path.exists(dbfile) else False
        self.dbfile = dbfile
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        if not self.initialized:
            self.cursor.execute("CREATE TABLE people (name TEXT PRIMARY KEY, address TEXT);")
            self.cursor.execute("CREATE TABLE food (name TEXT, food TEXT);")
            self.cursor.execute("CREATE INDEX name ON food (name);")

    def add_person(self, name=None, address=None, foods=None):
        try:
            self.cursor.execute(insert_person_query, (name, address))
        except sqlite3.IntegrityError:
            print("Warning: '%s' is already in the database, ignoring..." % name)
            return
        if foods is not None:
            for food in foods:
                self.cursor.execute(insert_food_query, (name, food))
        self.connection.commit()

    def add_food(self, name, food):
        self.cursor.execute(insert_food_query, (name, food))
        self.connection.commit()

    def get(self, name):
        self.cursor.execute(get_person_query, (name,))
        rows = self.cursor.fetchall()
        person = Person(rows)
        return person


class Person(object):

    def __init__(self, rows):
        self.name = rows[0][0]
        self.address = rows[0][1]
        self.foods = [row[2] for row in rows]

    def __str__(self):
        return "<Person>\n   name     =  %s\n   address  =  %s\n   foods    =  [%s]" % \
            (self.name, self.address, ', '.join(self.foods))



if __name__ == '__main__':

    peo = People(sys.argv[1])
    peo.add_person("john", "here", ['pizza', 'chocolate'])
    peo.add_food("john", "paella")
    john = peo.get("john")
    print(john)
