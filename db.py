import firebase_admin
from firebase_admin import firestore, credentials
import datetime
import os




# Application Default credentials are automatically created.
creds = credentials.Certificate({
  "type": "service_account",
  "project_id": "fbla-financial",
  "private_key_id": "88d55cec5f984262028729875f070297f58bce1c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCooMtM6UKf07CM\nUVIlDz3mRtQHnZVUJr4Pct9wWhujqHxL+GsXmwx5/YuWIXvl0QM6myqbFgdmnCt/\nsmOu0EPm86MLJbo4wZooA3iVZz+AraRkHDGal+yLcSlt0CF+PK8/RmHsX9jcMRoB\nXBwEpuKSLqWjiiZhc22Y5EmiyLfod/e62/C5kdXKHIzX/N14IiVDPHeptlwEBuYr\nHIos7fn0qeYQA997BBG32VEXARHxUVyg3ggS5/w5pgpejy232chRKEgpXL1pKlZ7\nmz6z8d6XQmQWOblKdYatiE3uXBlDPGPYAHbNFBI9wc45sAqmQB/5va0n6twZMZQ1\n0J5WxvElAgMBAAECggEAFyyF0+uIjutqK1Zvqg0mrhNUxzkmUPrECt54C3ouqzaX\n4l7g5M0XkVpBSSAP5VzsiyzQ1aBY4waaScHLxjXz5vTblsgYB/2/QDl95FZcmUQD\nwAhJ3tt7FAy4q1E7kRwo31K+WVwwss4Cq2YrqY3/vCQx+kAdly3kRWs2HWtlLsq4\nvQM2fD9ksE4DswslCDnCailiSJjdpd3t80NV7eGnGkt0qOkrLTltlXrLXaYmdJpO\nDApSBX1EQ+E5xRRCWXItgLlkEL8s0104w/t64+OuI4iKPguEBMK1x1W+0KeLnPoD\n4a18Gw+NVeWOC9rciNDADSH47itLgH0yt4EysN797wKBgQDVvOlcjaoaCTv0pM54\nhLV6D7KBaQgRXEaeEqNdsU+yiajTKH0wvKgxPj195S82ZK1sGRrFPtfgFiENxYfG\nGy6XrdpZzxHMHG3+/wF2CSsvRZrPHp9ig9CutaEhVb/urWLqKwerdjs6nDAxA4J2\ny11itkkNrPOQfkJ4xBEO2LpIiwKBgQDJ+H3XgkZUe9RxdNvvNV+3uWvZLO+o37rU\nVW878Hd3cRIvs51cxaWK+oAaEj2GQZgGk9UcCP6JZWgIXu37SFkwPiWPlV1xyfha\n65MtzZfpmJwehbcS4KjWCMWdkeClay57JfKljGEGNIYIcYP9SdvZrTEdR9MxLVcE\n6aDp+lszDwKBgQCwBHId0WB7Lo2cjDio0YluKw0zO570RQy20tyMpR/gBTPuKVLn\n1wWgAAS98Aawgbq74fTE6Vr4ZOD1qW2F/Q6ixP6jpT6f2+3N6I14elaBCI5T8YEK\nrUknB9bZT/fPBCUIeUVItAZU3xlk0+IWGKYgS8PfqkWvAfuV3sm5c0v9vwKBgEZv\n6zNls7FzHjwTTUC3lJI2kG5FRa/XlwjGYuy8iG2XeYg5VAAuzfUSN+rfwaU46xQg\nKoqEeIDiZM3Gjai9Kp2wjtjsdpJgpcTPs5ydvwUwvAHJEHf88eTzWjgB0B7gqm04\nZs9ljdDkMHpxXF7Ri2L3C9HyYq0b6uVDtWLkdTnxAoGARUousIUcRf7bqDhdC+TQ\nUT92jEMIT86n+Qp6hY4JzhrnJyLbgJtgkQ/tGmaAaZlmkROo4q8XrhHJe1srNncC\nDfFJsXC9kzmmbRHzHWUuVIBYVZZf646mbIrPcED7Kw4WoS0M1zIZfuaQsQ2Z/mM9\nRBFndfU/u82/djtm5DmIiA4=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-4x4hb@fbla-financial.iam.gserviceaccount.com",
  "client_id": "102456473024789919144",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4x4hb%40fbla-financial.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
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
    new_user(email, name)

def new_user(email, name):
    ref = db.collection("users").document(email)

    data = {
        "email": email,
        "name": name,
        "incomes": [],
        "expenses": [],
        "balance": 0,
        "months": [0 for i in range(12)]
        }
    
    ref.set(data)

def update_incomes(email, incomes):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    for income in incomes:
        data[incomes[income][0]] = {
            'type': incomes[income][1],
            'amt': incomes[income][2],
            'date': incomes[income][3]
            }
    
    ref.update({"incomes": data})
    

def update_expenses(email, expenses):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    for expense in expenses:
        data[expenses[expense][0]]=  {
            'type': expenses[expense][1],
            'amt': expenses[expense][2],
            'date': expenses[expense][3]
            }
            
    ref.update({"expenses": data})
    

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
