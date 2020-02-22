import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user = 'CREATE TABLE users(id int, username text, password text)'
cursor.execute(create_user)

user = (1, 'bob', 'asdf')
insert_user = 'INSERT INTO users VALUES(?, ?, ?)'
cursor.execute(insert_user, user) # For 1 record insertion

users = [
    (2, 'baba', 'baba'),
    (3, 'mad', 'mad'),
]
cursor.executemany(insert_user, users)# For Multiple record insertion(s)

connection.commit()
connection.close()