import firebase_admin
from firebase_admin import firestore, credentials

# Application Default credentials are automatically created.
creds = credentials.Certificate("firebase_creds.json")
app = firebase_admin.initialize_app(creds)
db = firestore.client()

# get user from database
def get_user(email):
    ref = db.collection("users").stream()
    for u in ref:
        u = u.to_dict()
        if u["email"] == email:
            return u # return user if exists
    new_user(email)
        
# new user in database
def new_user(email):
    ref = db.collection("users").document(email)
    data = {
        "email": email,
        "income": [],
        "expenses": [],
        "balance": None
        }
    try: # try to update data
        ref.update(data)
    except:
        #create data 
        ref.set(data)

def add_income(email, name, type, amt, date):
    ref = db.collection("users").document(email)
    data = {
        'name': name,
        'type': type,
        'amt': amt,
        'date': date
        }
    try: # try to update data
        ref.update({"income": firestore.ArrayUnion([data])})
    except:
        #create data 
        ref.set(data)
    
    update_balance(email)

def add_expenses(email, name, type, amt, date):
    ref = db.collection("users").document(email)
    data = {
        'name': name,
        'type': type,
        'amt': amt,
        'date': date
        }
    try: # try to update data
        ref.update({"expenses": firestore.ArrayUnion([data])})
    except:
        #create data 
        ref.set(data)
    
    update_balance(email)

def update_balance(email):
    ref = db.collection("users").document(email)
    usr = get_user(email)
    total_income = 0
    for i in usr["income"]:
        total_income += i["amt"]
    
    total_expense = 0
    for i in usr["expenses"]:
        total_expense -= i["amt"]

    bal = total_income + total_expense

    data = {
        "balance": bal
        }

    try: # try to update data
        ref.update(data)
    except:
        # create data 
        ref.set(data)
