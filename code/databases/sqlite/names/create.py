import sqlite3


table_definition = "CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT NOT NULL, address TEXT);"

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

cursor.execute('DROP TABLE names;')
cursor.execute(table_definition)
