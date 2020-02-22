import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_query = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)'
create_items_query = 'CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)'
cursor.execute(create_user_query)
cursor.execute(create_items_query)
cursor.execute('INSERT INTO items VALUES(NULL , ?,?)', ("test",19.12))

connection.commit()
connection.close()