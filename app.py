"""
app.py
------
Entry point of the MySpend application.

This file:
- creates the Flask application using the factory function
- starts the development server
- enables debug mode during development

The app itself is defined in tracker/__init__.py.
"""

# Import the function that builds and configures the Flask application.
from tracker import create_app


# STEP 1: Create the Flask application instance
# This calls the factory function from tracker/__init__.py.
app = create_app()


# STEP 2: Run the application
# This block ensures the server only runs when this file is executed directly.
if __name__ == "__main__":
    
    # Start the Flask development server.
    # debug=True enables automatic reload and detailed error messages.
    app.run(debug=True)