import firebase_admin
from firebase_admin import firestore, credentials
import datetime

# Application Default credentials are automatically created.
creds = credentials.Certificate({
  "type": "service_account",
  "project_id": "fbla-financial",
  "private_key_id": "31bd71c50e69120bab1eec054b8fc15cf12d3a4f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCrn5QSokzzwaEt\nO5jfGMXfNaOCTH70Px7E9U6VvPHn+yVajscxPG65AmmFG4QWdXDAOMXXXjwBZwXb\nuB5/kUdk4dz1anQLBEwWPN+YAFqESBwTm+Tig3iuoJ/Y9lI3Jj86m0A6pRm4tvBg\nDbNbKgJG2CCNjSqCNllQnScYd+UKJG0kjf21qfK6Uj7Hi6+CVy96nO4pXWI7SWf0\nlF2KE7Mpd7aoABXuTulqQEF+K+fcJWwzjXn8at2CXdOj7dU7i95kuQX98Ki8Y9rx\nt7ozYhHGtJBqTvbr/p6vp6QlV4VJqqBqK1VLAgmaFWUeRc+yZj255E599NoSI9pg\nd2FkvVbrAgMBAAECggEAEMEtdXw+wvU+ROoyjGUgvB/CbLAHHNUkrdm86EVf4GPW\nS7bwn0/lB07C+mmrRX4Fmd5xAguDFCf4nHCnGZEXRTP/nD3eQk0TGICs22v9ajiX\n9RodCDgJihLISCgT8qpbNd9+L7t6fVvur5Hm1pmNS1lCJE+JvNiNc59D99GMnKa0\nxe7yrXU6WG0e4bzISbCmKPBZLi+lkvbfDH11s5nisQQDfT6blxwp1DiOxERgwsQu\nWxEmq7AtLTBRyvc7yXaB4ecZq5ekHS12uNN3ji89lOxok5YxO3e/3OsMw326+A39\neOG2Cez+m2Rp3zqYW/3aRqfjXIiMCAWiyk1y6+LNYQKBgQDYyg22sSDZ/LxF3fA8\n49pnR5hV/7zZN2dTjSI2+sHavcLUINCs+8SotPkcq7v2++6OisTyc+lfZee9A9K2\nF2C8rrMhgsYNiudBAYmYxM9CsR8eFvPGgvaPbM7NbFnIrXjRPH0+3HPpt5UTZl8e\nN94ckue9fQOk/quPvP3Qhll0swKBgQDKqjeXG0Qz9oFGBbWdad+ecVZLjqpjTIcr\nt4fUaWeFPRqTkrR1SFYy7a4YtIrJxyD5YMfR18bW9t6kTFvU7iPLqvCz9U/o3WW3\n2yBFYImJDk1Itnn3STjm0mAYAFqMH6MkxTM2YFlyYAUHtaRJ+5qGSJcsjjClAh4m\noTl/NbVg6QKBgBYvn3Wp7PXCIrZ3vyVMIEbfkdyDPp1wSRfI4s6DnSE4uF6jORfq\n8DZfxvrDLIpbQA/AbeVuLV0A/dVfNcpC3DiTHGv6iTBLnd0OPjmvMpLds5SNvsb7\nEiadeRCW3R1ne2zWZu7u+sHZct04ZdWe3BFKi4Ld72iMU5xzN/qGNVN3AoGATofk\n4J3FMOl9MFf4BxZGe4vpZ3/R0IaP/kWw0YNChOOnj7WSTbwJAtUM2C/lc8jAo0F4\nTHzzZMrmfP3Fu93Hax1DBkixfUeFKdg0Sg3dXYl4MwvaeRMbhH3SlJpWe+OqgQ4V\nCSYOov5IFLOzBKQFPbGVOsOiX95RNqDUudFjBjkCgYA9aVVlcMSsyB9xn561juVc\nRiIPJj7JuUPFbJvKp/WQ7meiy+k6mPSaBR4Slq36LAzL0hCx56aI0gmzInWqjJdF\nYzWYUw/xLVKs3X/MavEFOS5UCr5fUxGiDXSKXiSL7G0PgaFyhJa2vilYF3vZmoT0\naUBMF8bu9UqAPqTNGpYV4A==\n-----END PRIVATE KEY-----\n",
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
