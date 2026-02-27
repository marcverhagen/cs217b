import sqlite3


inserts = [
	"INSERT INTO names(id, name, address) VALUES (1, 'john', 'here')",
	"INSERT INTO names(id, name, address) VALUES (2, 'john', 'there')",
	"INSERT INTO names(id, name, address) VALUES (3, 'sue', 'nowhere')",
	"INSERT INTO names(id, name, address) VALUES (4, 'liz', 'everywhere')"]

connection = sqlite3.connect('db-names.sqlite')
cursor = connection.cursor()

for insert in inserts:
	cursor.execute(insert)

connection.commit()
