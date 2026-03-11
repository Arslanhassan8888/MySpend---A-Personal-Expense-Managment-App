"""
app.py
This file is the ENTRY POINT of the MySpend application.

Purpose:
- Create the Flask application using the Application Factory.
- Start the development server.
- Run the application in debug mode during development.

The app instance is created in tracker/__init__.py.
"""

# Import the factory function that builds the Flask application.
from tracker import create_app


# Create the Flask application instance.
# This calls the function defined inside tracker/__init__.py.
app = create_app()

# Run the Application
# This condition ensures the server runs only when this file
# is executed directly (not when imported as a module).
if __name__ == "__main__":
    
    # Start the Flask development server.
    # debug=True enables:
    # - Automatic reload when code changes
    # - Detailed error messages
    app.run(debug=True)