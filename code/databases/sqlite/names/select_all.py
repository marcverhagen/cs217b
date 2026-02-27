import sqlite3

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

cursor.execute("SELECT * FROM names;")
print(cursor.fetchall())


# Shortcut:
#
# import sqlite3
# connection = sqlite3.connect('db-names.sqlite')
# print(connection.execute("SELECT * FROM names;").fetchall())
