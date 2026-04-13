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
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        lockout_until TEXT,
        monthly_budget REAL DEFAULT 0
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
        amount REAL,
        month TEXT,
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
    
        # REVIEWS TABLE
    # Stores user reviews for the Reviews page
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
    
# Function to insert default reviews
def insert_default_reviews():

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if reviews already exist to avoid duplicates
    existing_reviews = cursor.execute(
        "SELECT COUNT(*) FROM reviews" 
    ).fetchone()[0] # Get the count of existing reviews

    # If there are already reviews in the database, we skip inserting defaults
    if existing_reviews > 0:
        conn.close()
        return

    # List of default UK reviews for the Reviews page
    reviews = [
        ("Emily Carter", "Manchester", 5, "MySpend has completely changed how I manage my daily expenses. The layout is simple, clear, and very easy to use."),
        ("James Walker", "London", 5, "I really like how easy it is to track spending and set a monthly budget. It feels professional without being confusing."),
        ("Sophia Green", "Birmingham", 4, "The dashboard is clean and organised. I can quickly understand where my money is going each week."),
        ("Oliver Hughes", "Liverpool", 5, "This is one of the most straightforward finance trackers I have used. It helps me stay disciplined with spending."),
        ("Amelia Turner", "Leeds", 4, "I enjoy using MySpend because it makes budgeting feel less stressful. Everything is presented in a very clear way."),
        ("George Hall", "Bristol", 5, "The visual design is excellent and the features are genuinely useful. The budget section especially helps me stay on track."),
        ("Isla Bennett", "Sheffield", 5, "I love how simple it is to add and review expenses. It saves time and helps me reflect on my spending habits."),
        ("Harry Adams", "Nottingham", 4, "Very useful app for everyday money management. The charts and summaries make a big difference."),
        ("Ava Mitchell", "Leicester", 5, "The interface feels modern and calm. I like that the app focuses on clarity instead of trying to do too much."),
        ("Noah Phillips", "Newcastle", 4, "A very strong budgeting tool for personal use. It gives me exactly what I need without unnecessary complexity."),
        ("Mia Campbell", "Oxford", 5, "This app helped me become much more aware of my monthly spending. The budget progress section is particularly helpful."),
        ("Jack Parker", "Cambridge", 4, "Easy to use, well designed, and practical. I would definitely recommend it to anyone who wants to improve money habits."),
        ("Grace Evans", "York", 5, "MySpend feels reliable and polished. It gives me confidence when I am planning my expenses each month."),
        ("Charlie Edwards", "Glasgow", 5, "The whole experience is smooth and user-friendly. I especially like how quickly I can add and review transactions."),
        ("Lily Collins", "Edinburgh", 4, "A very helpful app with a clear design and useful features. It makes expense tracking much easier than I expected.")
    ]

    # Insert default reviews
    cursor.executemany("""
        INSERT INTO reviews (user_id, reviewer_name, location, rating, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (None, name, location, rating, review_text)
        for name, location, rating, review_text in reviews
    ])

    # Save changes
    conn.commit()

    # Close connection
    conn.close()