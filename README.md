CS50 Flask Finance Project
Overview
This project is a web-based application that simulates stock trading. Users can register, log in, look up real-time stock prices, and manage their portfolio by buying and selling shares. The application provides a simple interface for users to track their stock holdings and view transaction history.

Features
User Authentication: Users can register and log in securely with hashed passwords.
Stock Quotes: Users can search for real-time stock prices by entering a stock symbol.
Buying Stocks: Users can purchase stocks and the cost is deducted from their virtual balance.
Selling Stocks: Users can sell stocks they own, updating their portfolio and balance.
Portfolio Overview: Displays the current portfolio including stock symbols, the number of shares, and the total value.
Transaction History: Keeps a record of all stock purchases and sales.
Cash Management: Each user starts with $10,000 in virtual cash for buying stocks.
Tech Stack
Backend:
Flask (Python-based web framework)
CS50 Library (SQL for database interactions)
Frontend:
HTML, Jinja2 (for templating), Bootstrap (for responsive design)
Database:
SQLite (for storing user data, stock transactions, and portfolio information)
API:
Yahoo Finance (for retrieving real-time stock data)
Session Management:
Flask-Session (for user sessions)
Authentication:
Password hashing with Werkzeug
