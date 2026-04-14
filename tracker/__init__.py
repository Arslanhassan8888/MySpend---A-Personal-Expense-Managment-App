"""
tracker/__init__.py
-------------------
Initialises the tracker package and creates the Flask application.

This file uses the Application Factory pattern to:
- create the Flask app
- apply configuration and security settings
- register the main Blueprint
- prepare the database on startup
"""

# Flask is the main class used to create the web application instance.
from flask import Flask

# CSRFProtect adds protection against Cross-Site Request Forgery attacks
# for forms submitted within the application.
from flask_wtf import CSRFProtect

# Import database helper functions used when the application starts.
# get_db_connection checks that the database can be reached.
# create_tables ensures the required tables exist.
# insert_default_categories adds starter categories if they are missing.
# insert_default_reviews adds default review records if the table is empty.
from .models import (
    get_db_connection,
    create_tables,
    insert_default_categories,
    insert_default_reviews
)


# --> APPLICATION FACTORY
# Create and configure the Flask application, then return it.
def create_app():
    
    # Create a new Flask application instance.
    # __name__ helps Flask locate templates, static files, and package resources.
    app = Flask(__name__)
    
    # Secret key used for sessions and other security-related features.
    app.secret_key = "ciao_bello"
    
    # Cookie security settings.
    app.config["SESSION_COOKIE_HTTPONLY"] = True   # Prevent JavaScript access to session cookies.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Reduce cross-site request risks.
    app.config["SESSION_COOKIE_SECURE"] = False    # Change to True in production when using HTTPS.
    
    # Enable CSRF protection for application forms.
    CSRFProtect(app)
    
    # Import the shared Blueprint from the current package.
    from .routes import main
    
    # Register all routes linked to the Blueprint.
    app.register_blueprint(main)
    
    # Open and close a database connection to confirm the database is available.
    conn = get_db_connection()
    conn.close()
    
    # Ensure the database structure and default records are ready.
    create_tables()
    insert_default_categories()
    insert_default_reviews()
    
    # Return the fully configured application.
    return app