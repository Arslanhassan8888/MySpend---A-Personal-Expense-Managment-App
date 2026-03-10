"""
tracker/models.py

This file contains database models and database connection logic
for the MySpend application.

While routes.py defines how users interact with the application
(the web logic), models.py defines the structure of the data that
the application will manage.
"""

# Import the sqlite3 module from Python
# This module allows Python to work with SQLite databases
import sqlite3


# Function that creates a database connection
def get_db_connection():

    # Connect to a SQLite database file called "myspend.db"
    # If the file does not exist, SQLite will automatically create it
    connection = sqlite3.connect("myspend.db")

    # This line allows us to access database columns by name instead of number
    # Example: row["email"] instead of row[0]
    connection.row_factory = sqlite3.Row

    # Return the connection so other parts of the app can use it
    return connection

# Function to create database tables
def create_tables():

    # Get a database connection
    conn = get_db_connection()

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """)

    # Create Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Create Expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        date TEXT,
        amount REAL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    """)

    # Create Income table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        date TEXT,
        source TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Create Budgets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        monthly_limit REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Create Goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target_amount REAL,
        deadline TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Create Recurring Expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recurring_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        amount REAL,
        frequency TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    """)

    # Save changes
    conn.commit()

    # Close connection
    conn.close()