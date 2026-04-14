"""
tracker/routes/auth/login.py

This file contains the login route for the MySpend application.
"""

# render_template is used to display HTML pages.
# request is used to read form data sent by the user.
# redirect and url_for are used to move the user to another route when needed.
from flask import render_template, request, redirect, url_for

# session is used to store login details after successful authentication.
from flask import session

# flash is used to display messages to the user.
from flask import flash

# check_password_hash is used to compare the entered password
# with the hashed password stored in the database.
from werkzeug.security import check_password_hash

# datetime and timedelta are used to handle account lock timing.
from datetime import datetime, timedelta

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


# Login route handles both:
# - displaying the login page
# - processing the submitted login form
@main.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Handle user login.

    This route:
    - shows the login page
    - validates login form input
    - checks whether the email exists
    - checks whether the account is temporarily locked
    - verifies the password
    - starts a session after successful login

    Returns:
        str: Rendered HTML page or redirect response
    """

    # Default values used when the page first loads
    error = None
    entered_email = ""

    # Process the form only when the user submits it
    if request.method == "POST":

        # Read the entered email and password from the form
        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # REQUIRED FIELDS
        # Check that both email and password were entered
        if entered_email == "" or password == "":
            error = "Please fill in all fields."
            return render_template(
                "login.html",
                error=error, # Display the error message on the login page if validation fails.
                entered_email=entered_email # Pre-fill the email field with the user's input to avoid making them re-enter it.
            )

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Search for the user by email address
        user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        # EMAIL NOT REGISTERED
        # If no matching email is found, show a generic error message
        if not user:
            conn.close()
            error = "Invalid email or password."
            return render_template(
                "login.html",
                error=error, # Display the error message on the login page if the email is not registered.
                entered_email=entered_email # Pre-fill the email field with the user's input to avoid making them re-enter it.
            )

        # CHECK LOCK FOR THIS ACCOUNT ONLY
        # If the account has a lock time stored, check whether it is still active
        if user["lockout_until"] is not None:
            lock_time = datetime.fromisoformat(user["lockout_until"]) # Convert the lockout_until string from the database into a datetime object for comparison.

            if datetime.now() < lock_time: # If the current time is still before the lockout time, the account is locked. Show an error message and prevent login.
                conn.close()
                error = "Too many failed login attempts. Please try again in 5 minutes." # Display a message indicating that the account is temporarily locked due to too many failed login attempts.
                return render_template(
                    "login.html",
                    error=error,
                    entered_email=entered_email
                )

        # CORRECT PASSWORD
        # If the password matches the stored password hash, reset failed attempts
        if check_password_hash(user["password_hash"], password):

            cursor.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE user_id = ?",
                (user["user_id"],)
            )

            conn.commit()
            conn.close()

            # Start a fresh session for the logged-in user
            session.clear()  # Clear any existing session data to ensure a clean login state.
            session["user_id"] = user["user_id"] # Store the user's ID in the session to keep them logged in across pages.
            session["name"] = user["name"] # Store the user's name in the session for personalized greetings and display.

            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))

        # WRONG PASSWORD FOR A REGISTERED EMAIL
        # Increase the failed login attempt count
        attempts = user["failed_attempts"] + 1

        # Lock the account for 5 minutes after 3 failed attempts
        if attempts >= 3:    # If the user has reached 3 or more failed login attempts, set a lockout time for 5 minutes from now and update the database with the new failed attempt count and lockout time.
            lock_time = datetime.now() + timedelta(minutes=5) # Calculate the lockout time by adding 5 minutes to the current time.

            cursor.execute(
                "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE user_id = ?",
                (attempts, lock_time.isoformat(), user["user_id"])  # Update the user's record in the database with the new failed attempt count and the lockout time in ISO format.
            )

            error = "Too many failed login attempts. Please try again in 5 minutes."

        else:
            # If attempts are below 3, update the count and show remaining tries
            cursor.execute(
                "UPDATE users SET failed_attempts = ? WHERE user_id = ?",
                (attempts, user["user_id"]) # Update the user's record in the database with the new failed attempt count.
            )

            remaining = 3 - attempts # Calculate the number of remaining login attempts before the account gets locked.
            error = f"Incorrect password. You have {remaining} attempt(s) remaining." # Display a message indicating that the password is incorrect and show how many attempts are left before the account gets locked.

        # Save failed login updates and close the connection
        conn.commit()
        conn.close()

    # Show the login page on GET request or after validation failure
    return render_template(
        "login.html",
        error=error,    #  Pass any error message to the template to be displayed to the user if validation fails.
        entered_email=entered_email # Pass the entered email back to the template to pre-fill the email field, improving user experience by not making them re-enter it after a failed login attempt.
    )