from flask import Flask, render_template

app = Flask(__name__,)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/dashboard')
def search():
    return render_template("transactions.html")

@app.route('/analyze')
def analyze():
    return render_template("analyze.html")

if __name__ == "__main__":
    app.run(debug=True)