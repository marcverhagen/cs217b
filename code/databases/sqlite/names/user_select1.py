import sqlite3

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

print('Enter your identifier\ndb> ', end='')
identifier = input()

query = f"SELECT * FROM names WHERE id={identifier}"
print(query)

cursor.execute(query)
print(cursor.fetchall())
