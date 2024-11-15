import firebase_admin
from firebase_admin import firestore, credentials
import datetime

# Application Default credentials are automatically created.
creds = credentials.Certificate({
  
})
app = firebase_admin.initialize_app(creds)
db = firestore.client()

current_year = int(datetime.datetime.today().strftime("%Y"))

# get user from database
def get_user(email, name=None):
    ref = db.collection("users").stream()
    for usr in ref:
        usr = usr.to_dict()
        try:
            if usr["email"] == email:
                return usr # return user if exists
        except Exception as e:
            pass      
    return new_user(email, name)

def new_user(email, name):
    ref = db.collection("users").document(email)

    data = {
        "email": email,
        "name": name,
        "incomes": [],
        "expenses": [],
        "balance": 0,
        "months": [0 for i in range(12)],
        "income_types": {"Cash": 0, "Check": 0, "Wire": 0},
        "expense_types": {"Cash": 0, "Check": 0, "Wire": 0}
        }

    ref.set(data)
    return data

def update_incomes(email, incomes):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    types = {"Cash": 0, "Check": 0, "Wire": 0}
    print(types)
    for income in incomes:
        data[incomes[income][0]] = {
            'type': incomes[income][1],
            'amt': incomes[income][2],
            'date': incomes[income][3]
            }
        types[incomes[income][1]] += 1

    
    ref.update({"incomes": data, "income_types": types})
    

def update_expenses(email, expenses):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    types = {"Cash": 0, "Check": 0, "Wire": 0}
    for expense in expenses:
        data[expenses[expense][0]]=  {
            'type': expenses[expense][1],
            'amt': expenses[expense][2],
            'date': expenses[expense][3]
            }
        types[expenses[expense][1]] += 1
            
    ref.update({"expenses": data, "expense_types": types})
    

def update_balance(email):
    ref = db.collection("users").document(email)
    usr = get_user(email)
    total_income = 0
    incomes = usr['incomes']

    months = [0 for i in range(12)]
    #finds total income
    for i in incomes:
        curr_amount = float(incomes[i]["amt"])
        total_income += curr_amount

        #dates incomes by month
        date = [int(d) for d in incomes[i]["date"].split("-")]
        if date[0] == current_year:
            months[date[1]-1] += curr_amount
    
        
    expenses = usr['expenses']
    total_expense = 0
    #finds total expenses
    for i in expenses:
        curr_amount = float(expenses[i]["amt"])
        total_income -= curr_amount
        
        #dates expenses by month
        date = [int(d) for d in expenses[i]["date"].split("-")]
        if date[0] == current_year:
            months[date[1]-1] -= curr_amount
    

    bal = total_expense + total_income

    data = {
        "balance": bal,
        "months": months
        }

    ref.update(data)
