"""
tracker/__init__.py
This file initializes the tracker package.

It contains the Application Factory function, which:
- Creates the Flask application
- Configures the application
- Registers Blueprints (route groups)

Using the Application Factory pattern improves:
- Scalability
- Maintainability
- Testing capability
"""

from flask import Flask

# Import the get_db_connection function from models.py.
# This allows us to test the database connection when the app starts.
# create_tables is imported to ensure that the database tables are created when the app starts.
# insert_default_categories is imported to populate the categories table with default values if they don't already exist.
from .models import get_db_connection, create_tables, insert_default_categories


# Application Factory Function
# This function creates and configures the Flask application.
# It returns a fully initialized app instance.
def create_app():
    
    # Create a new Flask application instance.
    # __name__ tells Flask where the application is located.
    app = Flask(__name__)
    
    
    # Import the Blueprint named "main" from routes.py.
    # The dot (.) indicates importing from the current package.
    from .routes import main
    
    
    # Register the Blueprint with the Flask app.
    # This connects all routes defined in routes.py.
    app.register_blueprint(main)
    
    
    # Connect to the SQLite database using the get_db_connection function.
    conn = get_db_connection()
    
    # Close the database connection after testing it.
    conn.close()
    
    create_tables()  # Ensure database tables are created when the app starts.
    
    insert_default_categories()  # Insert default categories if they don't exist.
    
    # Return the configured Flask application. 
    return app