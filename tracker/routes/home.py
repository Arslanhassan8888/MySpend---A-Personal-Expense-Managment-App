"""
tracker/routes/home.py

This file contains the home page route for the MySpend application.
"""

# render_template is used to render HTML templates.
from flask import render_template

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import the shared Blueprint.
from .main_blueprint import main

# Import the helper function used to get the home page quote.
from ..legacy_routes import get_home_quote


# This route handles requests to the root URL "/".
# When a user visits:
# http://127.0.0.1:5000/
# this function will execute.
@main.route("/")
def home():
    
    user_id = session.get("user_id")  # Get the user_id from the session, if it exists.
    
    # Get a random motivational quote (API or fallback)
    quote = get_home_quote()
    
    # Render the index.html template when the root URL is accessed.
    # Pass the quote and user_id to the template for dynamic content rendering.
    # send quote text, author, and source to the template to display on the homepage. Also send user_id to conditionally show different content for logged-in users vs guests.
    return render_template(
        "index.html",
        user_id=user_id,  # Pass user_id to the template for conditional display.
        quote_text=quote["text"],
        quote_author=quote["author"],
        quote_source=quote["source"]
    )