from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from flask_session import Session
from helper import login_required
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from bs4 import BeautifulSoup
import os
import sqlite3

# Configure application
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

# Configure DB
con = sqlite3.connect("sweat.db",check_same_thread=False)
db = con.cursor()

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
        return render_template("index.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    con = sqlite3.connect("sweat.db",check_same_thread=False)
    db = con.cursor()
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide password")
            return render_template("login.html")
        # Query database for username
        users = db.execute("SELECT * FROM users WHERE name = '{}'".format(request.form.get("username"))).fetchall()
        print(users)
        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(
            users[0][2], request.form.get("password")
        ):
            flash("Incorrect username or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = users[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    con = sqlite3.connect("sweat.db",check_same_thread=False)
    db = con.cursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        gym = request.form.get("gym")
        confirmation = request.form.get("confirm")

        rows = db.execute("SELECT * FROM users WHERE name = '{}'".format(username)).fetchall()
        users = db.execute("SELECT * FROM users WHERE name = '{}'".format(request.form.get("username"))).fetchall()

        # Ensure the username was submitted
        if not username:
            flash("Please provide username")
            return render_template("register.html")
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            flash("Username already exists")
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            flash("Please provide password")
            return render_template("register.html")

        # Ensure confirmation password was submitted
        elif not request.form.get("confirm"):
            flash("Please confirm password")
            return render_template("register.html")

        # Ensure passwords match
        elif not password == confirmation:
            flash("Password does not match confirmation")
            return render_template("register.html")

        else:
            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            print('preadd')
            db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)",(len(users),username,hash,'following: []',gym))
            con.commit()
            print('added')
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return redirect("/")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
