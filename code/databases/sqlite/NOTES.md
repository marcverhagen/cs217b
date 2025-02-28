# Random SQLite notes

To access metadata like all table names and schema you do not have equivalent methods like the `.schema` command in the sqlite3 command in a terminal. Instead you use:

```python
>>> import sqlite3
>>> c = sqlite3.connect('test.db')
>>> c.execute('select sql from sqlite_master').fetchall()
>>> c.execute('select sql from sqlite_master where name="people";').fetchall()
```

And you can use `pandas` to dump content:

```python
>>> import pandas as pd
>>> table = pd.read_sql_query("SELECT * from people", connection)
>>> table.to_csv(table_name + '.csv', index_label='index')
```

With code like 

```html
{% for person in people %}
<tr>
	<td>{{ person[0] }}</td>
	<td>{{ person[1] }}</td>
</tr>
{% endfor %}
```

you end up with some white lines in your output, you can use `-%}` instead of `%}` to suppress that.

### Creating the example database from the slides

```python
>>> import sqlite3
>>> connection = sqlite3.connect('names.db')
```

This connection is required to send commands and receive answers. The connection is to `names.db` file, which if it did not exist will be created by the `connect()` method, but it will be empty. So first we create a table.

```python
>>> connection.execute("CREATE TABLE names (login TEXT PRIMARY KEY, first TEXT, last TEXT);")
>>> connection.execute("CREATE TABLE numbers (login TEXT, phone TEXT);")
>>> connection.execute("INSERT INTO names VALUES (?, ?, ?)", ('mark', 'Samuel', 'Clements'))
>>> connection.execute("INSERT INTO names VALUES (?, ?, ?)", ('lion', 'Lion', 'Kimbro'))
>>> connection.execute("INSERT INTO names VALUES (?, ?, ?)", ('kitty', 'Amber', 'Straub'))
>>> connection.execute("INSERT INTO numbers VALUES (?, ?)", ('mark', '555.555.5555'))
>>> connection.execute("INSERT INTO numbers VALUES (?, ?)", ('kitty', '555.666.6666'))
```


### Auto-commit
By default, SQLite operates in auto-commit mode and for each command, SQLite starts, processes, and commits the transaction automatically. If you want explicit transactions you use:

```sqlite
BEGIN TRANSACTION;
```

And then later use one of

```sqlite
COMMIT;
```
```sqlite
ROLLBACK;
```

The Python sqlite module does not use auto-commits.