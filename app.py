from db import *
from db import get_user
from flask import Flask, render_template, request, session, redirect
from functools import wraps
import datetime
import json

# Initialize
app = Flask(__name__)
app.secret_key = "syIyJRgEcuUQ8XI9iG-fA3slxHTBMmk"
app.permanent_session_lifetime = datetime.timedelta(days=31)

# wrapper function (checks if user is logged in)
def logged_in_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if session.get("user") is None:
            return redirect('/')
        return func(*args, **kwargs)

    return decorator

@app.route('/')
def home():
    return render_template("index.html", user=session.get("user"))

@app.route('/login', methods=["POST"])
def login():
    user = json.loads(request.form.get("creds")) # gets user login info
    session["user"] = get_user(user["email"], user["displayName"]) # stores user in browser session
    session.permanent = True
    session.modified = True
    return ""

@app.route('/account')
def account():
    return render_template("account.html", user=session.get("user"))
 
@app.route('/dashboard')
def dashboard():
    return render_template("transactions.html", user=session.get("user"))

@app.route('/analyze')
def analyze():
    return render_template("analyze.html", user=session.get("user"))

# logout link
@app.route('/logout', methods=["POST"])
def logout():
    session.clear() # clear browser session
    session.modified = True
    return ""

if __name__ == "__main__":
    app.run(debug=True)

