from flask import Flask, render_template, request, redirect, url_for, session,flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'DaXP9BxbuasMaqkS'

# MongoDB setup
client = MongoClient('mongodb+srv://no186:DaXP9BxbuasMaqkS@cluster0.zpcgbey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSweat']
users_collection = db['users']
posts_collection = db['posts']

# Check if user is logged in
def is_logged_in():
    return 'username' in session

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("AHAHAHA")
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        # Check if username already exists
        if users_collection.find_one({'name': username}):
            return 'Username already exists!'
        else:
            print("----NEW USER")
            users_collection.insert_one({'name': username, 'password': password, 'following': []})
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'name': username, 'password': password})
        if user:
            session['username'] = username
            print("LOGIN SUCCESSFUL!")
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Home route
@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    user = users_collection.find_one({'name': session['username']})
    followed_users = user["following"]
    print(followed_users)
    posts = posts_collection.find({'username': {'$in': followed_users}})
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

