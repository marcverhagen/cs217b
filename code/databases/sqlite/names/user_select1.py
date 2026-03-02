"""

Dangerous code that prompts the user for an identifier and then plugs
this identifier straight into an SQL query.

To see why this is dangerous try entering the following when prompted for an
identifier:

	0 or 1=1

This turns the entire query into

	SELECT * FROM names WHERE id=0 or 1=1

And now the entire where-clause evaluates to turn and the script will return 
all rows from the table.

This is an example of SQLI-insertion and is a danger with any code that accepts
user input. 

"""

import sqlite3

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

print('Enter your identifier\ndb> ', end='')
identifier = input()

query = f"SELECT * FROM names WHERE id={identifier}"
print(query)

cursor.execute(query)
print(cursor.fetchall())
