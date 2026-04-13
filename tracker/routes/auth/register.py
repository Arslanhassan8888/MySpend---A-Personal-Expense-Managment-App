"""
tracker/routes/auth/register.py

This file contains the register route for the MySpend application.
"""

# Route for the register page.
# This route handles both displaying the registration page
# and processing the registration form submission..
from flask import render_template, request

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import generate_password_hash to securely hash user passwords before storing them in the database.
from werkzeug.security import generate_password_hash

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the shared Blueprint.
from ..main_blueprint import main

@main.route("/register", methods=["GET", "POST"])
def register():

    error = None
    entered_name = ""
    entered_email = ""

    if request.method == "POST":

        entered_name = request.form.get("name", "").strip()
        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        agree_terms = request.form.get("agree_terms")

        # REQUIRED FIELDS
        if entered_name == "" or entered_email == "" or password == "" or confirm_password == "":
            error = "Please fill in all fields."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # TERMS CHECKBOX
        if not agree_terms:
            error = "You must agree to the Terms of Service and Privacy Policy."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # SIMPLE EMAIL VALIDATION
        if "@" not in entered_email or "." not in entered_email:
            error = "Please enter a valid email address."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        # CHECK IF EMAIL ALREADY EXISTS
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        if existing_user:
            conn.close()
            error = "Email already registered."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD MATCH
        if password != confirm_password:
            conn.close()
            error = "Passwords do not match."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD RULES
        has_number = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if len(password) < 12:
            conn.close()
            error = "Password must be at least 12 characters long."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_number:
            conn.close()
            error = "Password must contain at least one number."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_special:
            conn.close()
            error = "Password must contain at least one special character."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (entered_name, entered_email, password_hash)
        )

        conn.commit()
        conn.close()

        success = "Registration completed successfully. Redirecting to login page..."

        return render_template(
            "register.html",
            success=success,
            entered_name="",
            entered_email=""
        )

    return render_template(
        "register.html",
        error=error,
        entered_name=entered_name,
        entered_email=entered_email
    )
