"""
tracker/models.py

This file contains database models and database connection logic
for the MySpend application.

While routes.py defines how users interact with the application
(the web logic), models.py defines the structure of the data that
the application will manage.
"""

# Import sqlite3 to allow Python to work with SQLite databases
import sqlite3


# Function to create a database connection
def get_db_connection():

    # Connect to the SQLite database file
    # If the file does not exist, SQLite will create it automatically
    connection = sqlite3.connect("myspend.db")

    # Allows rows to be accessed like dictionaries
    # Example: row["email"] instead of row[0]
    connection.row_factory = sqlite3.Row
    # Enable foreign key support in SQLite
    connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support

    return connection


# Function to create database tables
def create_tables():

    # Get a database connection
    conn = get_db_connection()

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # USERS TABLE
    # Stores user account information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """)

    # CATEGORIES TABLE
    # Stores predefined spending categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # EXPENSES TABLE
    # Stores spending transactions recorded by users
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

    # INCOME TABLE
    # Stores money received by users
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

    # BUDGETS TABLE
    # Stores the monthly spending limit for a user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        monthly_limit REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # GOALS TABLE
    # Stores financial saving goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target_amount REAL,
        deadline TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # RECURRING EXPENSES TABLE
    # Stores subscriptions or repeated payments
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

    # Save changes to the database
    conn.commit()

    # Close the connection
    conn.close()


# Function to insert default categories
def insert_default_categories():

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # List of predefined categories
    categories = [
        "Food",
        "Transport",
        "Entertainment",
        "Rent",
        "Utilities",
        "Shopping",
        "Health",
        "Education",
        "Other"
    ]

    # Insert categories if they do not already exist
    for category in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,)
        )

    # Save changes
    conn.commit()

    # Close connection
    conn.close()