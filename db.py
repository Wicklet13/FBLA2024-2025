import firebase_admin
from firebase_admin import firestore, credentials
import datetime

# Application Default credentials are automatically created.
creds = credentials.Certificate({
  "type": "service_account",
  "project_id": "fbla-financial",
  "private_key_id": "813a54a801041a62bdf8ca0efacaffa3279a0ed7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCg+kCnxZmCgmNu\nTtrxPJTePB2aep5Begic8YRnzhMAUrJtQ98xn3z8G0/h7GDWAY6uwlzDlaNIvhL7\nB/3asQ3nGBjL9ONDY2FIvzdJhKlXi2vQ1YNaLAXi+pzyg7uh+tLdLjiuvpixHgJD\nRzeM06Cji82SXCD2eLXWrn4lMCuu0vuokC4FzMwsF01ApWE6hIkkS74y5NdspiFy\nDrotX/VjV+amV2dLBiH7ijDShhItr/m7KEWGv/J5Ir0UtycSqy9AUvKI7rgDXjJp\njL96DnZvEHubB71M+v9ijMe1jDT39iPIvuzQYMdbX4dA66UhFHlHjiyIuIthu1f5\na0bOjnPzAgMBAAECggEAAZxk1Oj5eiCzkwaEqAuwUlsCptRETNPGTfUYG0Z+J9os\nAUOVHQouC4MlylUoZkEvZtijagJPgdUDxpxUB4IPFA7IghNUyjdZNrZR0iawNSPm\n3nj3LrSoaGw+nCoCUNgm5Qy8h3nOeF3xrYUDGCHZW9mfIzBQf3bsxusJxcsqHL6U\nAhSu06hcrJNIsVZQXTvuyImB92I3LrwTz8uAk6nTUoIjwTbB+yWconHxSIs2PHFN\ny4h2UBrBILtSc5cohyeFiT/OVx96HSZBIvxAnjovOwaLLXprAPtjXvorgTeqnum/\nqXvBAU4ByONJbSCbF7W5LzOD8r3xTklhhis6t0fcQQKBgQDihzYhRqC0sDsNS4qP\n92+7jnrIerbnvRjQuYsO5pnB4Fvul8oO4sgbxv1tBWzrzLLRrdx5Wx9nMcjX6NZB\n3wdriMfuewZz9uVLcM1wf1Ivnuj7QweiUTm/g2Lrbu4N4sALGmmn2U5idf9NDQqN\nkRyYlAOuiT1REVGaZHgtNdjlQQKBgQC168zYw2RujgcVO48gSaqO0RmP8oef0KE0\nZ9na1WrufFz/I+LRxqtGhkvxm1TUBXAVtFPcFVnubmeuTBqesBMiEwKOVBw4GAnu\n4U4Rksk9TD3NO5kgfL2Il9hJKRR9Yfb2LNZIQpk5BgG07xnuY1iHaEHD1X8+IMiJ\npZIDu77IMwKBgG1qT8v82EzOPoeqcDAfnPlj1YyWMVh3rs/Kfw9gdO3/V4hECtXr\n1ioMkIYjM7wlcE31A2QejmmC03buQOcqOeRH+gIHrFNA8vngb2qiJOlZgUEz3DEb\nuJ/3b0U2nIdaedYjGNt5C/Jk+j6WSP2eFMjh3XFlWpeYnOjNFHsJ4kzBAoGAG6q7\n4a99o66n9xuyvbdWYBf+6jx5Ud3Z1m2A3V4dwB1by1W61ip/u98Kx7jW4tPc4wAk\nzNDWd4OE8yYR2lZu4ny/o8O48vL8975+MAAB6PeiYocQ17cA4DgvpZjAy/zNIU1a\nXWz7foeiVNEUQYQMX7OEZPMgQeOcfAqZNUYlUq8CgYEA3Hpb16U9l39/av+9/t00\n38SHjKio2cSo2gXOfRqMlHxpMacz3mGeN60xPPrEREBrczmSD5LtVQs5i116YJPg\nGk28KG+YCxjDd4Tlc8n7D4/Y+eGhNRMn8r93mqmI5+gWuaLs1Ux1OU/zMXys53gt\n0JrpFb9lOjUMOVjBmjpvrJM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-4x4hb@fbla-financial.iam.gserviceaccount.com",
  "client_id": "102456473024789919144",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4x4hb%40fbla-financial.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
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
