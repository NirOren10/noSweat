import sqlite3
import json

con = sqlite3.connect('sweat.db')
cur = con.cursor()
#cur.execute("CREATE TABLE users(userid INTEGER PRIMARY KEY AUTOINCREMENT, name TINYTEXT, hash TINYTEXT, following TEXT, gym TINYTEXT)")
cur.execute("CREATE TABLE posts(postid INTEGER PRIMARY KEY AUTOINCREMENT, userid int, content TINYTEXT, details TEXT, gym TINYTEXT)")
#cur.execute("DROP TABLE posts")
#a = cur.execute('SELECT * FROM users').fetchall()
#cur.execute("INSERT INTO posts() VALUES()")
con.commit()
print("Done")
print('\n\n\n')