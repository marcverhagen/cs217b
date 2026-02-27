# Somewhat silly way of inserting into a database, but it illustrates that
# you can pipe the output of a shell script into SQLite. The target database
# does need to contain a table that can accept the inserts.
#
# Usage: 
#
# $ sh names.sh | sqlite3 db-names.sqlite

echo "INSERT INTO names(id, name, address) VALUES (1, 'john', 'here');"
echo "INSERT INTO names(id, name, address) VALUES (1, 'john', 'here');"
echo "INSERT INTO names(id, name, address) VALUES (2, 'john', 'there');"
echo "INSERT INTO names(name, address) VALUES ('john', 'there');"
