"""
tracker/routes/reviews.py

This file contains the reviews page route for the MySpend application.
"""

# render_template is used to render HTML templates.
from flask import render_template

# Import the get_db_connection function from models.py to interact with the database.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


# Route for the reviews page, which displays user reviews and testimonials
# about the MySpend app. This page is accessible from the navigation menu
# and retrieves all reviews from the database, showing the newest first.
@main.route("/reviews")
def reviews():

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all reviews from newest inserted to oldest inserted
    reviews = cursor.execute("""
        SELECT reviewer_name, location, rating, review_text
        FROM reviews
        ORDER BY review_id DESC
    """).fetchall()

    # Close the connection
    conn.close()

    # Show the Reviews page
    return render_template("reviews.html", reviews=reviews)