"""
tracker/routes.py
This file defines the URL routes for the MySpend application.

Routes determine:
- What happens when a user visits a specific URL.
- Which function should execute.
- What response should be returned.

Blueprints are used to:
- Organize routes into modular components.
- Keep the project scalable and clean.
"""

# Import Blueprint from Flask.
# A Blueprint is used to group related routes.
# render_template is used to render HTML templates.
from flask import Blueprint, render_template

# "main" is the name of this Blueprint.
# __name__ helps Flask locate resources correctly.
main = Blueprint("main", __name__)

# This route handles requests to the root URL "/".
# When a user visits:
# http://127.0.0.1:5000/
# this function will execute.
@main.route("/")
def home():
    
    # Return a simple string response to the browser.
    # This will display "Welcome to MySpend!" on the homepage.
    return render_template("index.html") # Render the index.html template when the root URL is accessed.

