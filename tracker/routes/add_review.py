"""
tracker/routes/add_review.py
---------------------------
This file defines the route for adding a user review.

Logged-in users can submit one review about the MySpend application.
"""

# render_template displays HTML pages.
# request is used to access form data.
# redirect and url_for are used for navigation after actions.
from flask import render_template, request, redirect, url_for

# session is used to check if a user is logged in.
from flask import session

# flash is used to show success or error messages to the user.
from flask import flash

# Import database connection helper.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


# STEP 1: Add review route
@main.route("/add-review", methods=["GET", "POST"])
def add_review() -> str:
    """
    Handle the add review page.

    This route:
    - allows logged-in users to submit a review
    - validates user input
    - prevents duplicate reviews per user
    - saves the review to the database

    Returns:
        str: Rendered HTML page or redirect response
    """

    # Check if the user is logged in
    if "user_id" not in session:
        flash("Please log in to leave a review.", "error")
        return redirect(url_for("main.login"))

    # STEP 2: Display form on normal page load
    if request.method == "GET":
        return render_template("add_review.html")

    # STEP 3: Process form submission

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get form data and remove extra spaces
    reviewer_name = request.form.get("reviewer_name", "").strip()    # Get the reviewer's name from the form and remove leading/trailing spaces.
    reviewer_email = request.form.get("reviewer_email", "").strip()   # Get the reviewer's email from the form and remove leading/trailing spaces.
    location = request.form.get("location", "").strip()   # Get the reviewer's location from the form and remove leading/trailing spaces.
    rating = request.form.get("rating", "").strip()   # Get the reviewer's rating from the form and remove leading/trailing spaces.
    review_text = request.form.get("review_text", "").strip()   # Get the review text from the form and remove leading/trailing spaces.

    # STEP 4: Validate required fields
    if not reviewer_name or not reviewer_email or not location or not rating or not review_text: # Check if any of the required fields are empty after stripping whitespace.
        conn.close()
        return render_template( # If validation fails, re-render the form with an error message and pre-fill the fields with the user's input.
            "add_review.html",  # Render the add_review.html template
            error="All fields are required.", # Pass an error message to the template to inform the user that all fields must be filled out.
            entered_name=reviewer_name,
            entered_email=reviewer_email,
            entered_location=location,
            entered_rating=rating,
            entered_review_text=review_text
        )

    # Validate email format (basic check)
    # This is a very basic validation to check if the email contains "@" and "." characters. For a production application, consider using a more robust email validation method or library. 
    if "@" not in reviewer_email or "." not in reviewer_email:
        conn.close()
        return render_template(
            "add_review.html",
            error="Please enter a valid email address.",
            entered_name=reviewer_name,
            entered_email=reviewer_email,
            entered_location=location,
            entered_rating=rating,
            entered_review_text=review_text
        )

    # Validate rating value (must be 1–5)
    # Ensure that the rating is one of the allowed values (1, 2, 3, 4, or 5). This prevents invalid ratings from being submitted.
    if rating not in ["1", "2", "3", "4", "5"]:
        conn.close()
        return render_template(
            "add_review.html",
            error="Please choose a star rating.",
            entered_name=reviewer_name,
            entered_email=reviewer_email,
            entered_location=location,
            entered_rating=rating,
            entered_review_text=review_text
        )

    # STEP 5: Prevent duplicate reviews

    # Check if the current user already submitted a review
    existing_review = cursor.execute(
        "SELECT review_id FROM reviews WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    if existing_review:
        conn.close()
        return render_template(
            "add_review.html",
            error="You have already submitted a review.",
            entered_name=reviewer_name,
            entered_email=reviewer_email,
            entered_location=location,
            entered_rating=rating,
            entered_review_text=review_text
        )

    # STEP 6: Insert review into database
    cursor.execute("""
        INSERT INTO reviews (user_id, reviewer_name, location, rating, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        reviewer_name,
        location,
        int(rating),
        review_text
    ))

    # Save changes and close connection
    conn.commit()
    conn.close()

    # STEP 7: Show success message and reload page
    flash("Thank you for sharing your feedback. Your review has been submitted successfully.", "success")

    return redirect(url_for("main.add_review"))