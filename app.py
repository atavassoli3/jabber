import sqlite3
from werkzeug.exceptions import abort

# Establishes SQL Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Returns the user from database by their 'username'
def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user = ?', (username,)).fetchone()
    conn.close()

    return user

# Verifies credentials of a login
def login(username, password):
    print(username, password)
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user = ? AND pass = ?', (username, password)).fetchone()
    conn.close()
    print(user)

    return user


# For displaying all of the registered users
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return users

# For displaying a searched user
def user(username):
    user = get_user(username)
    return user

# For creating a new user
def create(username, password):
    user = username
    pass_ = password

    # Check if it exists

    if get_user(user) != None:
        print('User already exists')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (user, pass) VALUES (?, ?)',
                        (user, pass_))
        conn.commit()
        conn.close()