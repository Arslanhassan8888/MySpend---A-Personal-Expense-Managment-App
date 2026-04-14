"""
tracker/routes/reviews.py
------------------------
This file defines the route for the Reviews page.

It displays user reviews stored in the database.
"""

# render_template is used to display HTML pages.
from flask import render_template

# Import database connection helper.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


# STEP 1: Reviews page route
@main.route("/reviews")
def reviews() -> str:
    """
    Display all user reviews.

    This route:
    - retrieves reviews from the database
    - orders them from newest to oldest
    - passes them to the template for display

    Returns:
        str: Rendered HTML page showing reviews
    """

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all reviews (newest first)
    reviews = cursor.execute("""
        SELECT reviewer_name, location, rating, review_text
        FROM reviews
        ORDER BY review_id DESC
    """).fetchall()

    # Close the connection
    conn.close()

    # Render the reviews page
    return render_template("reviews.html", reviews=reviews)