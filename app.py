import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_stocks = db.execute("SELECT * FROM user_stocks WHERE user_id = ?", session['user_id'])
    user_info = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])


    return render_template("index.html", user_stocks=user_stocks, usd=usd, user_info_cash=user_info[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method =="GET":
        return render_template("buy.html")

    elif request.method == "POST":

        #Check if the symbol is typed in
        if not request.form.get("symbol"):
            return apology("please type in symbol", 400)

        #Check if the symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)

        #Check if the ammount is typed and positive
        elif not request.form.get("shares"):
            return apology("please mention a valid no of shares", 400)

        elif float(request.form.get("shares")) <= 0:
            return apology("please mention a valid no of shares", 400)

        cash_at_hand = float(db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]["cash"])
        cash_needed = float(request.form.get("shares")) * 1.0 * lookup(request.form.get("symbol"))["price"]
        #Check if the user can affort the shares
        if cash_at_hand < cash_needed:
            return apology("ya broke", 400)

        #All is okay
        time_of_purchase = datetime.datetime.now().isoformat()
        price_of_stock = lookup(request.form.get("symbol"))["price"]
        no_of_shares = float(request.form.get("shares"))
        stock_symbol = request.form.get("symbol")
        transaction_type = "buy"

        #insert the purchase
        db.execute("INSERT INTO purchases (user_id, stock_symbol, price, time, no_of_stocks, transaction_type) VALUES (?, ?, ?, ?, ?, ?)", session['user_id'], stock_symbol, price_of_stock, time_of_purchase, no_of_shares, transaction_type)

        rows = db.execute("SELECT * FROM user_stocks WHERE stock_name = ? AND user_id = ?", stock_symbol, session['user_id'])
        #Check to see if the stock has been bought before
        if len(rows) == 0:
            #new stock purchased
            db.execute("INSERT INTO user_stocks (stock_name, user_id, no_of_shares, price) VALUES (?, ?, ?, ?)", stock_symbol, session['user_id'], no_of_shares, price_of_stock)
        else:
            #The stock has been purchased before
            db.execute("UPDATE user_stocks SET no_of_shares = no_of_shares + ?, price = ? WHERE user_id = ? AND stock_name = ?", no_of_shares, price_of_stock, session['user_id'], stock_symbol)

        #update the user's cash
        new_cash_at_hand = cash_at_hand - cash_needed
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_at_hand, session['user_id'])

        #Return to homepage
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    purchases = db.execute("SELECT * FROM purchases WHERE user_id = ?", session['user_id'])
    return render_template("history.html", purchases=purchases)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
        quote_value = lookup(request.form.get("symbol"))
        stock_symbol = request.form.get("symbol")
        if not quote_value:
            return apology("invalid symbol", 400)
        else:
            return render_template("quoted.html", stock_symbol=stock_symbol, stock_price=usd(quote_value["price"]))

    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    if request.method == "GET":
        return render_template("register.html")
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    #Ensure the username doesn t already exist
    elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
        return apology("username already exists")


    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confirmation was submitted
    elif not request.form.get("confirmation"):
        return apology("must confirm password", 400)

    #ensure password matches the confirmation
    elif request.form.get("password") != request.form.get("confirmation"):
        return apology("the passwords do not match", 400)

    #all is okay
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute("SELECT * FROM user_stocks WHERE user_id = ?", session['user_id'])
        return render_template("sell.html", stocks=stocks)

    else:
        #check for input
        if not request.form.get("shares"):
            return apology("must enter no of shares", 403)

        if not request.form.get("symbol"):
            return apology("missing symbol", 403)

        #Check if the user has enough shares
        rows = db.execute("SELECT * FROM user_stocks WHERE user_id = ? AND stock_name = ?", session['user_id'], request.form.get("symbol"))
        if rows[0]["no_of_shares"] < int(request.form.get("shares")):
            return apology("not enough shares")

        #All okay
        #update the no of shares
        db.execute("UPDATE user_stocks SET no_of_shares = no_of_shares - ? WHERE user_id = ? AND stock_name = ?", request.form.get("shares"), session['user_id'], request.form.get("symbol"))

        #update the purchases db
        time_of_purchase = datetime.datetime.now().isoformat()
        price_of_stock = lookup(request.form.get("symbol"))["price"]
        no_of_shares = float(request.form.get("shares"))
        stock_symbol = request.form.get("symbol")
        transaction_type = "sell"

        db.execute("INSERT INTO purchases (user_id, stock_symbol, price, time, no_of_stocks, transaction_type) VALUES (?, ?, ?, ?, ?, ?)", session['user_id'], stock_symbol, price_of_stock, time_of_purchase, no_of_shares, transaction_type)

        #update the users cash
        cash_at_hand = float(db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]["cash"])
        cash_needed = float(request.form.get("shares")) * 1.0 * lookup(request.form.get("symbol"))["price"]
        new_cash_at_hand = cash_at_hand + cash_needed
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_at_hand, session['user_id'])

        return redirect("/")


