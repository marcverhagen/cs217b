# A simple SQLite example

Assuming we have no database, create one as follows:

```bash
$ sqlite3 db-people.sqlite
SQLite version 3.6.12
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> .schema
```

This will not create a file "db-people.sqlite" yet. That will happen at the
moment we create someting in the database. Sqlite has a couple of commands that
start with a period, use ".help" to see them. The ".schema" commands shows all
tables and indexes so it does not show anything here.

Creating tables:

```sql
sqlite> CREATE TABLE people (name TEXT PRIMARY KEY, address TEXT);
sqlite> CREATE TABLE food (name TEXT, food TEXT);
sqlite> CREATE INDEX name ON food (name);
sqlite> .schema
CREATE TABLE people (name TEXT PRIMARY KEY, address TEXT);
CREATE TABLE food (name TEXT, food TEXT);
CREATE INDEX name_food ON food (name, food);
```

Inserting:

```sql
sqlite> INSERT INTO people VALUES ( "john", "here");
sqlite> INSERT INTO people VALUES ( "jane", "there");
sqlite> INSERT INTO people VALUES ( "john", "here");
SQL error: column name is not unique
```

Loading from a file:

```sql
sqlite> delete from people;
sqlite> .separator "\t"
sqlite> .import table-people.tab people
sqlite> .import table-food.tab food
```

Selecting:

```sql
sqlite> .separator "|"
sqlite> SELECT people.name, address, food FROM people, food
   ...> WHERE people.name = food.name;
john|1 Main Street, Springfield, MA|pizza
john|1 Main Street, Springfield, MA|meatloaf
jane|1 High Street, Springfield, MA|paella
jane|1 High Street, Springfield, MA|chicken
jane|1 High Street, Springfield, MA|chocolate
```