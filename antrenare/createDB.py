import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
sql = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS usersTest;
CREATE TABLE users (
           id integer unique primary key autoincrement,
           name text,
           ident boolean,
           date text
);

CREATE TABLE usersTest (
           id integer unique primary key autoincrement,
           name text,
           ident boolean,
           date text
);
"""
c.executescript(sql)
conn.commit()
