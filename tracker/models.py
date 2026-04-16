"""
tracker/models.py
-----------------
This file handles database connection and table creation
for the MySpend application.

While routes manage user interaction (web logic),
this file defines how data is stored and structured.
"""

# sqlite3 allows Python to interact with SQLite databases.
import sqlite3


# STEP 1: Create database connection
def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    The connection:
    - opens (or creates) the database file
    - allows column access by name
    - enables foreign key constraints

    Returns:
        sqlite3.Connection: Active database connection
    """

    # Connect to the SQLite database file.
    # If it does not exist, it will be created automatically.
    connection = sqlite3.connect("myspend.db")

    # Allow rows to be accessed like dictionaries (row["email"])
    connection.row_factory = sqlite3.Row

    # Enable foreign key support (disabled by default in SQLite)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# STEP 2: Create database tables
def create_tables() -> None:
    """
    Create all required tables if they do not already exist.

    This ensures the database structure is ready before the app runs.

    Returns:
        None
    """

    # Open database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # USERS TABLE – stores user account details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        lockout_until TEXT,
        monthly_budget REAL DEFAULT 0
    )
    """)

    # CATEGORIES TABLE – predefined spending categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # EXPENSES TABLE – user spending records
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

    # # INCOME TABLE – money received by users
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS income (
    #     income_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     user_id INTEGER,
    #     amount REAL,
    #     date TEXT,
    #     source TEXT,
    #     FOREIGN KEY (user_id) REFERENCES users(user_id)
    # )
    # """)

    # BUDGETS TABLE – monthly budget limits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        month TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

  

   # RECURRING EXPENSES TABLE – subscriptions or repeated payments
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS recurring_expenses (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     user_id INTEGER NOT NULL,
    #     category_id INTEGER NOT NULL,
    #     amount REAL NOT NULL,
    #     description TEXT,
    #     frequency TEXT NOT NULL,  -- e.g. daily, weekly, monthly
    #     start_date TEXT NOT NULL,
    #     next_due_date TEXT NOT NULL,
    #     is_active INTEGER DEFAULT 1,
    #     FOREIGN KEY (user_id) REFERENCES users(user_id),
    #     FOREIGN KEY (category_id) REFERENCES categories(category_id)
    # )
    # """)

    # REVIEWS TABLE – user feedback for the Reviews page
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        reviewer_name TEXT NOT NULL,
        location TEXT NOT NULL,
        rating INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Save changes and close connection
    conn.commit()
    conn.close()


# STEP 3: Insert default categories
def insert_default_categories() -> None:
    """
    Insert predefined spending categories into the database.

    Categories are only added if they do not already exist.

    Returns:
        None
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # List of default categories
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

    # Insert categories safely (ignore duplicates)
    for category in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,)
        )

    conn.commit()
    conn.close()


# STEP 4: Insert default reviews
def insert_default_reviews() -> None:
    """
    Insert sample reviews if the reviews table is empty.

    This prevents duplicate data on repeated app launches.

    Returns:
        None
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if any reviews already exist
    existing_reviews = cursor.execute(
        "SELECT COUNT(*) FROM reviews"
    ).fetchone()[0]

    # If reviews exist, skip insertion
    if existing_reviews > 0:
        conn.close()
        return

    # Default UK-based reviews
    reviews = [
        ("Emily Carter", "Manchester", 5, "MySpend has completely changed how I manage my daily expenses. The layout is simple, clear, and very easy to use."),
        ("James Walker", "London", 5, "I really like how easy it is to track spending and set a monthly budget."),
        ("Sophia Green", "Birmingham", 4, "The dashboard is clean and organised."),
        ("Oliver Hughes", "Liverpool", 5, "A very straightforward finance tracker."),
        ("Amelia Turner", "Leeds", 4, "Makes budgeting feel less stressful.")
    ]

    # Insert reviews into database
    cursor.executemany("""
        INSERT INTO reviews (user_id, reviewer_name, location, rating, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (None, name, location, rating, review_text)
        for name, location, rating, review_text in reviews
    ])

    conn.commit()
    conn.close()