import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

#Inser one user
user = (1, 'jose', 'adbf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

#Insert many users - list of tuples 
users = [
    (2, 'mateo', '1234'),
    (3, 'sadu', 'hasu1')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

#Save changes and close connection 
connection.commit()
connection.close()

