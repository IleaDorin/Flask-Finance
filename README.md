
# CS50 Flask Finance Project

### Overview

This project is a web-based stock trading simulation. Users can register, log in, look up
real-time stock prices, and manage their stock portfolios by buying and selling shares.
The application provides a simple interface for tracking holdings, viewing transaction history,
and handling cash balances.

### Features

- **User Authentication**: Users can register and log in securely using hashed passwords.
- **Stock Quote Lookup**: Fetch real-time stock prices by entering a stock symbol.
- **Buy Stocks**: Purchase shares, and the cost is deducted from the user's virtual cash balance.
- **Sell Stocks**: Sell shares from the user's portfolio, updating the holdings and cash balance.
- **Portfolio Overview**: Displays the user's current stocks, including the number of shares,
  stock symbols, and total portfolio value.
- **Transaction History**: Keeps a record of all stock purchases and sales for each user.
- **Cash Management**: Users start with $10,000 in virtual cash for stock purchases.

### Tech Stack

- **Backend**: 
  - Flask (Python web framework)
  - CS50 Library (for SQL database interactions)
- **Frontend**: 
  - HTML (for structure)
  - Jinja2 (for templating)
  - Bootstrap (for responsive design)
- **Database**: 
  - SQLite (to store user data, transactions, and portfolio information)
- **API**: 
  - Yahoo Finance (for retrieving real-time stock prices)
- **Password Hashing**: 
  - Werkzeug (used for securely hashing passwords)
- **Session Management**: 
  - Flask-Session (for managing user sessions via filesystem)
