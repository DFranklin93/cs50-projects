import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # all vars named user_*** are methods that grab the user's info such who they are, how much money they have,
    # and what stocks they've purchased
    user_id = session['user_id']
    user_info = db.execute('SELECT * FROM users WHERE id = :id', id = user_id)
    user_portfolio = db.execute('SELECT company, symbol, SUM(share_count) FROM transactions WHERE user_id = :id GROUP BY company', id = user_id)

    # create an empty array (list in python) that we will fill later
    index = []
    user_total = 0

    # runs through all transactions made that match the proper criteria given
    for i in user_portfolio:
        api_lookup = lookup(i['symbol'])
        for stake in range(len(user_portfolio)):
            if i['company'] == user_portfolio[stake]['company']:
                share_count = user_portfolio[stake]['SUM(share_count)']
                index.append({'name': i['company'], 'symbol': i['symbol'], 'share_count': share_count, 'price': api_lookup['price']})
                user_total += (share_count * api_lookup['price'])

    user_total += user_info[0]['cash']

    return render_template("index.html", user = user_info[0], stocks = index, total = user_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock == None:
            return apology("Invaild symbol")
        user = db.execute('SELECT * FROM users WHERE id = :id', id = session["user_id"])
        cash = user[0]['cash']

        # Creates transaction
        db.execute('INSERT into transactions(company, user_id, price, share_count, symbol) VALUES (:company, :user_id, :price, :share_count, :symbol)', company = stock['name'], user_id = user[0]['id'], price = stock['price'], share_count = request.form.get('shares'), symbol = stock['symbol'])

        if cash < stock['price']:
            return apology("Insufficient funds")

        # Takes money out of user's account
        cash -= (stock['price'] * int(request.form.get('shares')))
        db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash = cash, id = session["user_id"])



    return render_template("bought.html", stock = stock)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    userNames = db.execute("SELECT username FROM users")
    userName = request.args.get("username")
    search = {'username' : userName}
    if search in userNames:
        print("user name found")
        return jsonify("false")
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # all vars named user_*** are methods that grab the user's info such who they are, how much money they have,
    # and what stocks they've purchased
    user_id = session['user_id']
    user_info = db.execute('SELECT * FROM users WHERE id = :id', id = user_id)
    user_portfolio = db.execute('SELECT * FROM transactions WHERE user_id = :id', id = user_id)

    print(user_portfolio)
    return render_template("history.html", trans_history = user_portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.form.get('symbol')
        stock = lookup(symbol)
        return render_template("quoted.html", stock = stock)
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        user_name = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirmation')

        # tests to make sure that all input forms are completed and PWs match
        if not user_name:
            return 'Must provide a username'
        elif not password:
            return 'Must provide a password'
        elif not confirm:
            return 'Must retype password'
        elif password != confirm:
            return "Passwords do not match"

        # checks to make sure that username isn't already taken
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = user_name)

        if len(rows) == 1:
            return apology("Username taken. Try another.")

        # if user name is not already in use, takes input password and converts to hash
        password = generate_password_hash(password)

        # inserts new user and user password into db
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = user_name, hash = password)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # all vars named user_*** are methods that grab the user's info such who they are, how much money they have,
    # and what stocks they've purchased
    user_id = session['user_id']
    user_info = db.execute('SELECT * FROM users WHERE id = :id', id = user_id)
    user_cash = user_info[0]['cash']
    user_portfolio = db.execute('SELECT company, symbol, SUM(share_count) FROM transactions WHERE user_id = :id GROUP BY company', id = user_id)

    if request.method == "GET":

        # create an empty array (list in python) that we will fill later
        index = []

        # runs through all transactions made that match the proper criteria given
        for i in user_portfolio:
            api_lookup = lookup(i['symbol'])
            for stake in range(len(user_portfolio)):
                if i['company'] == user_portfolio[stake]['company']:
                    share_count = user_portfolio[stake]['SUM(share_count)']
                    index.append({'name': i['company'], 'symbol': i['symbol'], 'share_count': share_count, 'price': api_lookup['price']})

        return render_template("sell.html", stocks = index)

    if request.method == "POST":

        selected_value = request.form.get('symbol')
        amount_sold = int(request.form.get('shares'))
        api_lookup = lookup(selected_value)
        for i in user_portfolio:
            if i['symbol'] == selected_value:

                # makes sure that user doesn't sell more stocks than they own
                if i['SUM(share_count)'] > amount_sold:
                    db.execute('INSERT into transactions(company, user_id, price, share_count, symbol) VALUES (:company, :user_id, :price, :share_count, :symbol)', company = i['company'], user_id = user_id, price = api_lookup['price'], share_count = -abs(amount_sold), symbol = i['symbol'])
                else:
                    return apology("Can't sell what you don't have, homie")

        # update user cash amount with what has been sold
        user_cash += (api_lookup['price'] * amount_sold)
        db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash = user_cash, id = user_id)
    return redirect('history')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# def unipueStock():
#     # all vars named user_*** are methods that grab the user's info such who they are, how much money they have,
#     # and what stocks they've purchased
#     user_id = session['user_id']
#     user_info = db.execute('SELECT * FROM users WHERE id = :id', id = user_id)
#     user_portfolio = db.execute('SELECT company, symbol, SUM(share_count) FROM transactions WHERE user_id = :id GROUP BY company', id = user_id)

#     # create an empty array (list in python) that we will fill later
#     index = []

#     # runs through all transactions made that match the proper criteria given
#     for i in user_portfolio:
#         api_lookup = lookup(i['symbol'])
#         for stake in range(len(user_portfolio)):
#             if i['company'] == user_portfolio[stake]['company']:
#                 share_count = user_portfolio[stake]['SUM(share_count)']
#                 index.append({'name': i['company'], 'symbol': i['symbol'], 'share_count': share_count, 'price': api_lookup['price']})

#     return index