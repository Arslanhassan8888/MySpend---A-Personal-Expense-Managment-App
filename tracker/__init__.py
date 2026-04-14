"""
tracker/__init__.py
-------------------
This file initialises the tracker package.

It contains the Application Factory function, which:
- creates the Flask application
- applies configuration and security settings
- registers Blueprints (route groups)
- prepares the database when the app starts

Using this pattern improves:
- scalability
- maintainability
- testing
"""

# Flask is used to create the web application instance.
from flask import Flask

# CSRFProtect helps protect forms from CSRF (Cross-Site Request Forgery) attacks.
from flask_wtf import CSRFProtect

# Import database helper functions from models.py.
# These are used when the application starts to ensure the database is ready.
from .models import (
    get_db_connection,
    create_tables,
    insert_default_categories,
    insert_default_reviews
)


# STEP 1: Application Factory
def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function:
    - creates the Flask app instance
    - applies security and session settings
    - registers Blueprints (routes)
    - ensures the database and default data exist

    Returns:
        Flask: A fully configured Flask application instance
    """

    # Create a new Flask application instance.
    # __name__ helps Flask locate templates and static files.
    app = Flask(__name__)
    
    # Secret key used for session management and security features.
    app.secret_key = "ciao_bello"
    
    # STEP 2: Configure session security settings
    
    # Prevent JavaScript from accessing session cookies (reduces XSS risk)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    
    # Restrict how cookies are sent in cross-site requests (reduces CSRF risk)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    
    # Ensure cookies are only sent over HTTPS (should be True in production)
    app.config["SESSION_COOKIE_SECURE"] = False
    
    # Enable CSRF protection for all forms in the application.
    CSRFProtect(app)
    
    
    # STEP 3: Register application routes (Blueprint)
    
    # Import the main Blueprint from the routes package.
    # The dot (.) means "from the current package".
    from .routes import main
    
    # Register the Blueprint so all routes become active.
    app.register_blueprint(main)
    
    
    # STEP 4: Check database connection
    
    # Open a connection to confirm the database is accessible.
    conn = get_db_connection()
    
    # Close the connection after testing.
    conn.close()
    
    
    # STEP 5: Prepare database structure and default data
    
    # Create tables if they do not already exist.
    create_tables()
    
    # Insert default categories if they are missing.
    insert_default_categories()
    
    # Insert default reviews if the table is empty.
    insert_default_reviews()
    
    
    # Return the fully configured Flask application.
    return app