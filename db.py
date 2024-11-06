import firebase_admin
from firebase_admin import firestore, credentials

# Application Default credentials are automatically created.
creds = credentials.Certificate("fbla-financial-firebase-adminsdk-3k9zy-52ae8cf401.json")
app = firebase_admin.initialize_app(creds)
db = firestore.client()

# get user from database
def get_user(email, name=None):
    ref = db.collection("users").stream()
    for usr in ref:
        usr = usr.to_dict()
        try:
            if usr["email"] == email:
                print(usr)
                return usr # return user if exists
        except:
            new_user(email, name)

def new_user(email, name):
    ref = db.collection("users").document(email)
    data = {
        "email": email,
        "name": name,
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
