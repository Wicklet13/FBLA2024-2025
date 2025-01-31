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
    session['email'] = user['email']
    session.permanent = True
    session.modified = True
    return ""

 
@app.route('/dashboard')
@logged_in_required
def dashboard():
    return render_template("transactions.html", user=session.get("user"))

@app.route('/analyze')
@logged_in_required
def analyze():
    return render_template("analyze.html", user=session.get("user"))

@app.route('/chatbot')
@logged_in_required
def chatbot():
    return render_template("chatbot.html", user=session.get("user"))

@app.route('/update_income_transactions', methods=["POST"])
def update_income_transactions():
    # get all class names, types, and numerical grades
    income_names = request.form.getlist("income_names[]")
    income_types = request.form.getlist("income_types[]")
    income_amounts = request.form.getlist("income_amounts[]")
    income_date = request.form.getlist("income_date[]")
    for i in income_amounts:
        i = float(int(i))
        if i < 0:
            return redirect("/dashboard")
        
        
        
    for i in range(len(income_date)):
        if income_date[i] == "":
            income_date[i]=datetime.datetime.today().strftime("%Y-%m-%d")

    incomes = {} # dictionary to store classes

    for i in range(len(income_names)):
        name = income_names[i]
        incomes[name] = [name, income_types[i], income_amounts[i], income_date[i]]


    update_incomes(session.get("email"), incomes)
    update_balance(session.get("email"))

    session["user"] = get_user(session.get("email"))

    return "" # tells server success

@app.route('/update_expense_transactions', methods=["POST"])
def update_expense_transactions():
    # get all class names, types, and numerical grades
    expense_names = request.form.getlist("expense_names[]")
    expense_types = request.form.getlist("expense_types[]")
    expense_amounts = request.form.getlist("expense_amounts[]")
    expense_date = request.form.getlist("expense_date[]")
    for i in expense_amounts:
        i = float(i)
        if i < 0:
            return redirect("/dashboard")
    
    for i in range(len(expense_date)):
        if expense_date[i] == "":
            expense_date[i]=datetime.datetime.today().strftime("%Y-%m-%d")

    expenses = {} # dictionary to store classes

    for i in range(len(expense_names)):
        name = expense_names[i]
        expenses[name] = [name, expense_types[i], expense_amounts[i], expense_date[i]]

    #updates session information
    update_expenses(session.get("email"), expenses)
    update_balance(session.get("email"))

    session["user"] = get_user(session.get("email"))

    return "" # tells server success

# logout link
@app.route('/logout', methods=["POST"])
@logged_in_required
def logout():
    session.clear() # clear browser session
    session.modified = True
    return ""

if __name__ == "__main__":
    app.run(debug=True)

