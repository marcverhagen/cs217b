"""

https://www.askpython.com/python-modules/pandas/pandas-to-sql

pip install pandas
pip install sqlalchemy

"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine


# Connection goes via sqlite, but the reading is done by pandas

conn = sqlite3.connect("flights.db")
df = pd.read_sql_query("select * from airlines limit 10;", conn)

print(df)
print(df['country'])


# And you can write to a database without knowing anything about schema

engine = create_engine('sqlite:///flights2.db')
df.to_sql('users', con=engine, if_exists='replace', index=False)


# Or from scratch from another DataFrame

df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
engine = create_engine('sqlite:///people.db')
df.to_sql('users', con=engine, if_exists='replace', index=False)

