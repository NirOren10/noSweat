import sqlite3

con = sqlite3.connect('sweat.db')
cur = con.cursor()
cur.execute("CREATE TABLE users(userid int, name TINYTEXT, hash TINYTEXT, following TEXT, gym TINYTEXT)")
#cur.execute("CREATE TABLE posts(postid int, userid int, content IMAGE, details TEXT, gym TINYTEXT)")
#cur.execute("DROP TABLE users")
con.commit()