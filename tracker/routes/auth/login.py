"""
tracker/routes/auth/login.py

This file contains the login route for the MySpend application.
"""

# render_template is used to render HTML templates.
# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions.
# url_for is used to generate URLs for the specified endpoint (route function).
from flask import render_template, request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import generate_password_hash to securely hash user passwords before storing them in the database.
# werkzeug.security is a module that provides utilities for hashing passwords and checking hashed passwords.
from werkzeug.security import check_password_hash

# Import datetime and timedelta for handling date and time operations, such as calculating date ranges for expense tracking.
from datetime import datetime, timedelta

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


# Login route handles both:
# - displaying the login page
@main.route("/login", methods=["GET", "POST"])
def login():

    error = None
    entered_email = ""

    if request.method == "POST":

        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # REQUIRED FIELDS
        if entered_email == "" or password == "":
            error = "Please fill in all fields."
            return render_template(
                "login.html",
                error=error,
                entered_email=entered_email
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        # EMAIL NOT REGISTERED
        if not user:
            conn.close()
            error = "Invalid email or password."
            return render_template(
                "login.html",
                error=error,
                entered_email=entered_email
            )

        # CHECK LOCK FOR THIS ACCOUNT ONLY
        if user["lockout_until"] is not None:
            lock_time = datetime.fromisoformat(user["lockout_until"])

            if datetime.now() < lock_time:
                conn.close()
                error =  "Too many failed login attempts. Please try again in 5 minutes."
                return render_template(
                    "login.html",
                    error=error,
                    entered_email=entered_email
                )

        # CORRECT PASSWORD
        if check_password_hash(user["password_hash"], password):

            cursor.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE user_id = ?",
                (user["user_id"],)
            )

            conn.commit()
            conn.close()

            session.clear()
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))

        # WRONG PASSWORD FOR A REGISTERED EMAIL
        attempts = user["failed_attempts"] + 1

        if attempts >= 3:
            lock_time = datetime.now() + timedelta(minutes=5)

            cursor.execute(
                "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE user_id = ?",
                (attempts, lock_time.isoformat(), user["user_id"])
            )

            error = "Too many failed login attempts. Please try again in 5 minutes."

        else:
            cursor.execute(
                "UPDATE users SET failed_attempts = ? WHERE user_id = ?",
                (attempts, user["user_id"])
            )

            remaining = 3 - attempts
            error = f"Incorrect password. You have {remaining} attempt(s) remaining."

        conn.commit()
        conn.close()

    return render_template(
        "login.html",
        error=error,
        entered_email=entered_email
    )