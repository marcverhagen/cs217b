"""

This does not have the same vulnerability as the code in user_select1.py because
what you type in as the identifier is going to be understood as just the value of 
the identifier instead of as a disjunction.

"""

import sqlite3

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

print('Enter your identifier\ndb> ', end='')
identifier = input()

query = "SELECT * FROM names WHERE id=?"
print(query)

cursor.execute(query, (identifier,))
print(cursor.fetchall())
