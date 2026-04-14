"""
tracker/routes/home.py
---------------------
This file defines the route for the homepage.

It displays a welcome page with a motivational quote.
Content may vary depending on whether the user is logged in.
"""

# render_template is used to display HTML pages.
from flask import render_template

# session is used to check if a user is logged in.
from flask import session

# Import the shared Blueprint.
from .main_blueprint import main

# Import helper function to retrieve a quote (API or fallback)
from ..quote_api import get_home_quote


# STEP 1: Home page route
@main.route("/")
def home() -> str:
    """
    Display the homepage.

    This route:
    - checks if a user is logged in
    - retrieves a motivational quote
    - passes data to the template for display

    Returns:
        str: Rendered HTML page for the homepage
    """

    # Get the user ID from the session (if the user is logged in)
    user_id = session.get("user_id")
    
    # Get a random quote (from API or fallback list)
    quote = get_home_quote()
    
    # STEP 2: Render homepage with dynamic content
    return render_template(
        "index.html",
        user_id=user_id,                 # Used to adjust content for logged-in users
        quote_text=quote["text"],        # Quote content
        quote_author=quote["author"],    # Quote author
        quote_source=quote["source"]     # Source of the quote
    )