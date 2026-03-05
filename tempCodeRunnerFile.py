# app.py
# This file is the ENTRY POINT of the application.
# It starts the Flask server and runs the web application.

# Import the create_app function from the tracker package.
# This function is responsible for creating and configuring
# the Flask application using the Application Factory pattern.
from tracker import create_app


# Call the create_app() function to build the Flask application.
# The returned object is the actual web application.
app = create_app()


# This condition checks if this file is executed directly.
# If true, it starts the Flask development server.
if __name__ == "__main__":
    
    # debug=True enables:
    # - Automatic reload when code changes
    # - Detailed error messages during development
    app.run(debug=True)