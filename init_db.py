import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (user, pass) VALUES (?, ?)",
            ('bryan7', 'supersecure777')
            )

cur.execute("INSERT INTO users (user, pass) VALUES (?, ?)",
            ('gosling2', 'notebook87')
            )

connection.commit()
connection.close()