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

# Import Flask class from the flask module.
from flask import Flask
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
    
    
    
    # Return the configured Flask application. 
    return app