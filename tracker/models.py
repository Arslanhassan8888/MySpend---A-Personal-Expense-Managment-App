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