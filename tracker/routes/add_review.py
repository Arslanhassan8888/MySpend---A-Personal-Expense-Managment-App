"""
tracker/routes/add_review.py

This file contains the add review route for the MySpend application.
"""

# render_template is used to render HTML templates.
# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions.
from flask import render_template, request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the get_db_connection function from models.py to interact with the database.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


# Route for the add review page, which allows logged-in users to submit
# their own review about the MySpend app. Each user is allowed to submit
# only one review. If the user is not logged in, they are redirected to
# the login page. If the user has already submitted a review, they are
# redirected back to the reviews page.
@main.route("/add-review", methods=["GET", "POST"])
def add_review():

    # Only logged-in users can access this page
    if "user_id" not in session:
        flash("Please log in to leave a review.", "error")
        return redirect(url_for("main.login"))

    # Normal page load: just show the form
    if request.method == "GET":
        return render_template("add_review.html")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get submitted form values and remove extra spaces
    reviewer_name = request.form.get("reviewer_name", "").strip()
    reviewer_email = request.form.get("reviewer_email", "").strip()
    location = request.form.get("location", "").strip()
    rating = request.form.get("rating", "").strip()
    review_text = request.form.get("review_text", "").strip()

    # Validate that all fields are filled in
    if not reviewer_name or not reviewer_email or not location or not rating or not review_text:
        conn.close()
        return render_template(
            "add_review.html",
            error="All fields are required.",
            entered_name=reviewer_name,
            entered_email=reviewer_email,
            entered_location=location,
            entered_rating=rating,
            entered_review_text=review_text
        )

    # Validate email format
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

    # Validate rating value
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

    # Check whether this user has already submitted a review
    existing_review = cursor.execute(
        "SELECT review_id FROM reviews WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    # Show duplicate review error only after submit attempt
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

    # Insert the review into the database
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

    # Save changes to the database
    conn.commit()
    conn.close()

    # Flash success once, then redirect back to the same page
    flash("Thank you for sharing your feedback. Your review has been submitted successfully.", "success")
    return redirect(url_for("main.add_review"))