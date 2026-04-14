"""
tracker/routes/about.py
----------------------
This file defines the route for the About page.

The About page provides information about the MySpend application,
its purpose, features, and the developer.
"""

# render_template is used to return an HTML page to the user.
from flask import render_template

# Import the shared Blueprint used to register routes.
from .main_blueprint import main


# STEP 1: About page route
@main.route("/about")
def about() -> str:
    """
    Display the About page.

    This route:
    - handles requests to "/about"
    - renders the about.html template

    Returns:
        str: Rendered HTML page for the About section
    """

    return render_template("about.html")