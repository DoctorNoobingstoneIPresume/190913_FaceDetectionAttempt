import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
sql = """
UPDATE users
SET
    (ident, date) = (SELECT usersTest.ident, usersTest.date
                           FROM usersTest
                           WHERE usersTest.name = users.name )
WHERE
    EXISTS (
       SELECT *
       FROM usersTest
       WHERE usersTest.name = users.name
   )
"""
c.executescript(sql)
conn.commit()
