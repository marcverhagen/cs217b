import sqlite3

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

print('Enter your identifier\ndb> ', end='')
identifier = input()

query = "SELECT * FROM names WHERE id=?"
print(query)

cursor.execute(query, (identifier,))
print(cursor.fetchall())
