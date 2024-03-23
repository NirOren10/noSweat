from flask import Flask, render_template, request, redirect, url_for, session,flash
import sqlite3
import json
from flask_session import Session
from tempfile import mkdtemp
# from helper import login_required

con = sqlite3.connect('sweat.db')
cur = con.cursor()

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gym = request.form['gym']
        print(username,password)
        # Check if username already exists
        userlist = cur.execute('SELECT name FROM users').fetchall()
        if username in (userlist):
            return 'Username already exists!'
        else:
            print("----NEW USER")
            cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)',(len(userlist),username,password,'',gym))
            con.commit()
            #users_collection.insert_one({'name': username, 'password': password, 'following': []})
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = cur.execute('SELECT username,password FROM users WHERE username=? AND password=?',(username,password)).fetchone()#users_collection.find_one({'name': username, 'password': password})
        if len(user)!=0:
            session['username'] = username
            print("LOGIN SUCCESSFUL!")
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# Home route
@app.route('/')
@login_required
def index():
    user = cur.execute("SELECT name FROM users WHERE ")
    # if not is_logged_in():
    #     return redirect(url_for('login'))
    # user = users_collection.find_one({'name': session['username']})
    # followed_users = user["following"]
    # print(followed_users)
    # posts = posts_collection.find({'username': {'$in': followed_users}})
    return render_template('index.html', posts=posts)

# Post route
@app.route('/post', methods=['POST'])
def post():
    if not is_logged_in():
        return redirect(url_for('login'))
    username = session['username']
    content = request.form['content']
    posts_collection.insert_one({'username': username, 'content': content})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

